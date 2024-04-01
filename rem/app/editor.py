from pathlib import Path
from typing import Iterable
from textual import on
from textual.binding import Binding
from textual.app import ComposeResult
from textual.containers import Grid, Horizontal, Vertical, Container, ScrollableContainer
from textual.screen import Screen, ModalScreen
from textual.widgets import Header, Footer, TextArea, Button, Static, Switch, Label, TabbedContent, TabPane, Placeholder, Checkbox, ListView, ListItem, Input, DirectoryTree
from textual.app import ComposeResult
from textual.reactive import reactive
from textual.events import Event

from rem.mTLC.env import TermError

from ..mTLC import Env

from ..qrefine import mls, AstPres

from ..qrefine.prover.gen.gen_machine import GenMachine
import datetime


def rem_greetings() -> str:
    now = datetime.datetime.now()
    return f"Session starts at {now.strftime('%H:%M:%S')}."


class GoalBar(Static):
    def __init__(self, goal: AstPres, index: int, total: int) -> None:
        super().__init__()
        self.goal = goal
        self.index = index  # index starts from 1
        self.total = total

    def compose(self) -> ComposeResult:
        yield Label(f"Goal ({self.index}/{self.total})")
        yield TextArea(str(self.goal), read_only=True)


class EnvTabs(Static):

    env = reactive(Env)

    class EnvTabChanged(Event):
        def __init__(self, gen_env: Env) -> None:
            super().__init__()
            self.gen_env = gen_env

    def watch_env(self, env: Env) -> None:
        '''
        reload the definitions in the environment
        '''

        # stash the excluded names
        excluded_names = set()

        list_view = self.get_widget_by_id("defs_list", ListView)
        for item in list_view.children:
            assert isinstance(item, DefItem)
            if not item.selected:
                excluded_names.add(item.def_name)

        list_view = self.get_widget_by_id("defs_list", ListView)
        list_view.clear()

        for def_name, def_value in reversed(env.defs.items()):
            list_view.append(
                DefItem(
                    def_name, 
                    str(def_value.type), 
                    def_name not in excluded_names,
                )
            )

        self.post_message(self.EnvTabChanged(self.get_gen_env()))

    def compose(self) -> ComposeResult:
        yield Label("Definitions")
        yield ListView(id = "defs_list")
        
    
    def get_gen_env(self) -> Env:
        '''
        get the generation environment variables according to the selected items
        '''
        names = set()

        list_view = self.get_widget_by_id("defs_list", ListView)
        for item in list_view.children:
            assert isinstance(item, DefItem)
            if item.selected:
                names.add(item.def_name)

        return self.env.sub_env(names)
    
    @on(Switch.Changed)
    def gen_setting_change(self, event: Switch.Changed) -> None:
        '''
        update the generation environment
        '''
        self.post_message(self.EnvTabChanged(self.get_gen_env()))


class DefItem(ListItem):
    '''
    The bar for a definition.
    '''
    DEFAULT_CSS = '''
    DefItem {
        layout: horizontal;
    }
    '''
    def __init__(self, def_name: str, def_type: str, gen_selected: bool) -> None:
        super().__init__()

        self.def_name = def_name
        self.def_type = def_type
        self.gen_selected = gen_selected
        self.switch = Switch(self.gen_selected)

    def on_button_pressed(self, event: Button.Pressed) -> None:
        editor = self.app.query_one("Editor", Editor)

        if event.button.id == "show":

            cmd_code = f"Show {self.def_name}."
            editor.push_cmd(cmd_code, record = False)

            
        elif event.button.id == "eval":
            cmd_code = f"Eval {self.def_name}."
            editor.push_cmd(cmd_code, record = False)

    def compose(self) -> ComposeResult:
        yield self.switch
        yield Label(f"{self.def_name} : {self.def_type}")
        yield Button(f"SHOW", id = "show")
        yield Button(f"EVAL", id = "eval")


    @property
    def selected(self) -> bool:
        '''
        whether the def item is selected for generation
        '''
        return self.switch.value


############################################################################
# the editor
############################################################################

class RemDirectoryTree(DirectoryTree):
    def filter_paths(self, paths: Iterable[Path]) -> Iterable[Path]:
        return [path for path in paths if 
                    path.is_dir() or 
                    not path.name.startswith(".") and path.name.endswith(".rem")]


class FileScreen(ModalScreen[None|Path]):  
    """Screen with a dialog to quit."""

    def __init__(self, mode_str : str) -> None:
        super().__init__()
        self.mode_str = mode_str

        self.selected_path = Path("./")
        self.selected_is_dir = True

    @on(DirectoryTree.FileSelected)
    def on_file_selected(self, event: DirectoryTree.FileSelected) -> None:
        self.selected_path = event.path
        self.selected_is_dir = False

    @on(DirectoryTree.DirectorySelected)
    def on_directory_selected(self, event: DirectoryTree.DirectorySelected) -> None:
        self.selected_path = event.path
        self.selected_is_dir = True

    def compose(self) -> ComposeResult:
        yield Grid(
            Label(f"({self.mode_str}) Choose a file:", id="question"),
            RemDirectoryTree("./", id = "file_tree"),
            Input("", id="file_name"),
            Button("Commit", variant="primary", id="commit"),
            Button("Cancel", variant="primary", id="cancel"),
            id="dialog",
        )

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "commit":
            file_name = self.get_widget_by_id("file_name", Input).value

            if self.selected_is_dir:
                if not file_name.endswith(".rem"):
                    file_name += ".rem"
                selected_path = self.selected_path / file_name
            else:
                selected_path = self.selected_path

            self.dismiss(selected_path)
        else:
            self.dismiss(None)

class Editor(Screen):

    BINDINGS = [
        Binding("f9", "save", "💾", priority=True),
        Binding("f10", "open", "📂", priority=True),
        Binding("ctrl+j", "play_backward", "◀◀", priority=True),
        Binding("ctrl+o", "step_backward", "◀", priority=True),
        Binding("ctrl+p", "step_forward", "▶", priority=True),
        Binding("ctrl+l", "play_forward", "▶▶", priority=True),
        Binding("f1", "to_handbook", "To Handbook", priority=True),
    ]

    ############################################################
    # operation saving

    current_file = reactive("")

    def watch_current_file(self, value: str) -> None:
        if value == "":
            self.title = "Rem Editor - New File"
        else:
            self.title = f"Rem Editor - {value}"

    def action_open(self) -> None:
        def check_open(res : None|Path) -> None:
            if res is not None:
                try:
                    
                    self.action_play_backward()

                    with open(res, "r") as f:
                        self.code_area.text = f.read()

                    self.append_log(f"File {res} opened.")
                    self.current_file = res.as_posix()

                except Exception as e:
                    self.append_log(f"Error: {e}")

        self.app.push_screen(FileScreen("open"), check_open)



    def action_save(self) -> None:
        def check_save(res: None|Path) -> None:
            if res is not None:
                try:
                    with open(res, "w") as f:
                        f.write(self.verified_area.text + self.code_area.text)

                    self.append_log(f"File {res} saved.")
                    self.current_file = res.as_posix()

                except Exception as e:
                    self.append_log(f"Error: {e}")

        if self.current_file == "":
            self.app.push_screen(FileScreen("close"), check_save)

        else:
            check_save(Path(self.current_file))



    ############################################################ 
    # generation status
    # solved/working/disabled
    gen_status = reactive("disabled")


    def watch_gen_status(self, value: str) -> None:
        if value == "solved":
            self.gen_machine.terminate()
            self.apply_gen.disabled = False
            self.regen.disabled = False

        elif value == "working":
            self.apply_gen.disabled = True
            self.regen.disabled = True

        elif value == "disabled":
            self.gen_machine.initialize()
            self.apply_gen.disabled = True
            self.regen.disabled = True

            

        else:
            raise ValueError("Invalid Value.")

    ############################################################


    ############################################################
    # information from rem
    rem_log = reactive(rem_greetings())
    prover_status = reactive('')

    def append_log(self, value: str) -> None:
        self.rem_log += f"\n\n{value}"

    def watch_rem_log(self, value: str) -> None:
        self.log_area.text = value

        # set the cursor to the end
        self.log_area.select_all()
        self.log_area.move_cursor(self.log_area.cursor_location)

    def watch_prover_status(self, value: str) -> None:
        if value == '':
            self.prover_status_area.text = 'READY.'
        elif value == 'Calculating...':
            self.prover_status_area.text = value
        else:
            self.prover_status_area.text = "ERROR: " + value

    ############################################################
            

    ############################################################
    # gen-machine settings
            
    gen_worker_num = reactive(8)
    gen_max_depth = reactive(4)

    def watch_gen_worker_num(self, value: int) -> None:
        self.gen_machine.worker_num = value

    def watch_gen_max_depth(self, value: int) -> None:
        self.gen_machine.max_depth = value

    ############################################################

    def compose(self) -> ComposeResult:

        # backend components
        self.mls = mls.MLS()
        self.gen_machine = GenMachine(self.mls.selected_frame.env)

        # timer
        self.gen_update_timer = self.set_interval(1 / 10, self.update_gen, pause=False)

        # widgets

        #######################################################
        # coding area

        self.verified_area = TextArea(
            "",
            id='verified-area',
            show_line_numbers=True,
            read_only=True
        )

        self.code_area = TextArea(
            "// starting coding here", 
            id='code-area',
            show_line_numbers=True,
            tab_behavior='indent'
        )


        ##################################################
        # information area

        self.goal_list = ScrollableContainer()

        self.log_area = TextArea(read_only=True)

        self.prover_status_area = TextArea(read_only=True)


        #######################################################
        # area for variables/rule/generation

        self.env_tabs = EnvTabs()

        self.gen_area = TextArea(read_only=True)
        # the button to apply generation result
        self.apply_gen = Button("APPLY", id = "apply_gen")
        # the button to regenerate
        self.regen = Button("REGEN", id = "regen")
        # the switch to toogle generation
        self.gen_switch = Switch(True)

        self.gen_container = Vertical(
            Container(
                self.env_tabs,
            ),

            self.gen_area,
            Horizontal(
                self.apply_gen,
                self.regen
            ),
            Label("Workers:"),
            Input(str(self.gen_machine.worker_num), type = "integer", id = "gen_worker_num"),
            Label("Depth:"),
            Input(str(self.gen_machine.max_depth), type = "integer", id = "gen_max_depth"),
            Label("Auto Generation:"),
            self.gen_switch
        )
        #######################################################

        yield Header()

        yield Horizontal(
            Vertical(
                self.verified_area,
                self.code_area,
            ),
            Vertical(
                Label("Refinement Goals"),
                self.goal_list,
                Label("Info from Rem"),
                self.log_area,
                Label("Prover status"),
                self.prover_status_area
            ),
            self.gen_container,
        )

        yield Footer()
        
        # update the frame
        self.call_after_refresh(self.update_display)

    ############################################################
    # to handbook
    def action_to_handbook(self) -> None:
        self.app.switch_mode("handbook")

    @on(Input.Changed)
    def input_changed(self, event: Input.Changed) -> None:
        if event.input.id == 'gen_worker_num':
            try:
                worker_num = int(event.value)
                if worker_num < 1:
                    self.get_widget_by_id('gen_worker_num', Input).value = str(1)
                elif worker_num > 16:
                    self.get_widget_by_id('gen_worker_num', Input).value = str(16)
                else:
                    self.gen_worker_num = worker_num
            except ValueError:
                pass

        elif event.input.id == 'gen_max_depth':
            try:
                max_depth = int(event.value)
                if max_depth < 1:
                    self.get_widget_by_id('gen_max_depth', Input).value = str(1)
                elif max_depth > 8:
                    self.get_widget_by_id('gen_max_depth', Input).value = str(8)
                else:
                    self.gen_max_depth = max_depth
            except ValueError:
                pass

    @on(Switch.Changed)
    def on_switch_changed(self, event: Switch.Changed) -> None:
        if event.switch == self.gen_switch:
            if event.value:
                self.gen_update_timer.resume()
            else:
                self.gen_update_timer.pause()
                self.gen_machine.terminate()
                self.gen_status = 'disabled'
                self.update_gen()


    @on(TextArea.Changed)
    def verified_area_scroll(self, event: TextArea.Changed):
        if event.text_area == self.verified_area:
            # verified_area scroll to end
            self.verified_area.scroll_end(animate = False)

            # set the cursor to the end
            self.verified_area.select_all()
            self.verified_area.move_cursor(self.verified_area.cursor_location)


    def push_cmd(self, cmd_code: str, record: bool) -> None:
        '''
        push one command to the system (don't affect the code area)
        record : whether to record this command in the verified code
        '''
        
        # set the status
        self.prover_status = 'Calculating...'

        res = self.mls.step_forward(cmd_code)

        # add the logging
        if res is not None:
            if res[1] is not None:
                self.append_log(res[1])

        self.prover_status = self.mls.error

        if record:
            self.verified_area.text = self.mls.verified_code

    def on_button_pressed(self, event: Button.Pressed) -> None:

        # apply the generation result
        if event.button.id == 'apply_gen':

            cmd_code = f"\n\nStep {self.gen_machine.sol}."

            self.push_cmd(cmd_code, record = True)

        # regenerate
        elif event.button.id == 'regen':
            self.gen_machine.initialize()


    def action_step_forward(self) -> bool:
        # set the status
        self.prover_status = 'Calculating...'

        res = self.mls.step_forward(self.code_area.text)

        if res is not None:
            self.code_area.text = res[0]

            # check whether to log the output.
            if res[1] is not None:
                self.append_log(res[1])

        self.prover_status = self.mls.error

        self.verified_area.text = self.mls.verified_code

        return res is not None


    def action_step_backward(self) -> bool:
        # set the status
        self.prover_status = 'Calculating...'

        res = self.mls.step_backward()

        if res is not None:
            self.code_area.text = res + self.code_area.text

        self.prover_status = self.mls.error

        self.verified_area.text = self.mls.verified_code

        # push the code_area cursor backwards
        if res is not None:
            row_offset = res.count('\n')
            col_offset = len(res.split('\n')[-1])
            self.code_area.move_cursor_relative(row_offset, col_offset)

        return res is not None

    def action_play_forward(self) -> None:
        # turn off the auto-gen temporarily
        auto_gen = self.gen_switch.value
        self.gen_switch.value = False

        while self.action_step_forward():
            pass

        self.gen_switch.value = auto_gen

        # clean the error
        self.prover_status = ''

    def action_play_backward(self) -> None:
        # turn off the auto-gen temporarily
        auto_gen = self.gen_switch.value
        self.gen_switch.value = False

        while self.action_step_backward():
            pass
        
        self.gen_switch.value = auto_gen

        # clean the error
        self.prover_status = ''

    @on(EnvTabs.EnvTabChanged)
    def env_tabs_change_detected(self, event: EnvTabs.EnvTabChanged) -> None:
        '''
        update the generation environment
        '''

        # check before assigning to avoid redundant updates
        if event.gen_env != self.gen_machine.gen_env:
            self.gen_machine.gen_env = event.gen_env

    def update_gen(self) -> None:
        '''
        Update the generation information and checks the state of gen_machine.
        '''
        if self.gen_switch.value:
            machine_str = str(self.gen_machine)
        else:
            machine_str = "Generation is disabled."

        if machine_str != self.gen_area.text:
            self.gen_area.text = machine_str
        
        if self.gen_switch.value:

            selected_goal = self.mls.selected_goal
            
            if not self.mls.latest_selected or selected_goal is None:
                self.gen_status = "disabled"

            # conditions to trigger the generation
            # 1. the latest frame is selected
            # 2. there is a current goal
            # 3. the current goal is different from the last generated goal
            elif selected_goal != self.gen_machine.goal:

                self.gen_machine.gen(
                    goal = selected_goal,
                )       

                self.gen_status = "working"

            # terminate the generation if the solution found
            if self.gen_machine.sol is not None:
                self.gen_status = "solved"

        else:
            self.gen_status = "disabled"

    def update_display(self) -> None:

            ############################################
            # Update the goal list according to the mls
                
            goals: list[AstPres] = self.mls.selected_frame.current_goals

            # remove all childs
            children = self.goal_list.query(None)
            for child in children:
                child.remove()

            if len(goals) == 0:
                if self.mls.selected_frame.refinement_mode:
                    self.goal_list.mount(
                        Label("Goal Clear.")
                    )
                else:
                    self.goal_list.mount(
                        Label("Not in refinement mode.")
                    )
            else:
                for i, goal in enumerate(goals, start=1):
                    self.goal_list.mount(
                        GoalBar(goal, i, len(goals))
                    )

            ############################################
            # Update the defs tab (only on the latest frame)
            if self.mls.latest_selected:
                self.env_tabs.env = self.mls.selected_frame.env


    @on(TextArea.SelectionChanged)
    def selection_changed(self, event: TextArea.SelectionChanged) -> None:
        '''
        Select the code in verified-area and show the corresponding frame.
        '''
        if event.text_area.id == 'verified-area':
            
            # avoid the empty selection
            if self.verified_area.text == "":
                return
            

            # avoid unexpected exceptions
            try:
                # calculate the pos of the cursor 
                pos = len(self.verified_area.get_text_range((0,0), event.selection.end)) + 1
                
                self.mls.set_cursor(pos)

            except Exception:
                pass
            
            self.update_display()