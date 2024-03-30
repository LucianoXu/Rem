from textual import on
from textual.binding import Binding
from textual.app import ComposeResult
from textual.containers import Horizontal, Vertical, Container, ScrollableContainer
from textual.screen import Screen
from textual.widgets import Header, Footer, TextArea, Button, Static, Switch, Label, TabbedContent, TabPane, Placeholder, Checkbox, ListView, ListItem
from textual.app import ComposeResult
from textual.reactive import reactive

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
    def reload_defs(self, env: Env):
        '''
        reload the definitions in the environment
        '''
        list_view = self.get_widget_by_id("defs_list", ListView)
        list_view.clear()

        for def_name, def_value in env.defs.items():
            list_view.append(DefItem(def_name, str(def_value.type), False))

    def compose(self) -> ComposeResult:
        with TabbedContent():
            with TabPane("Defs"):
                yield ListView(id = "defs_list")
            with TabPane("Rules"):
                yield ListView(id = "rules_list")


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

    def on_button_pressed(self, event: Button.Pressed) -> None:
        editor = self.app.query_one("Editor", Editor)

        if event.button.id == "show":

            cmd_code = f"Show {self.def_name}."
            editor.push_cmd(cmd_code, record = False)

            
        elif event.button.id == "eval":
            cmd_code = f"Eval {self.def_name}."
            editor.push_cmd(cmd_code, record = False)

    def compose(self) -> ComposeResult:
            yield Switch(self.gen_selected)
            yield Label(f"{self.def_name} : {self.def_type}")
            yield Button(f"SHOW", id = "show")
            yield Button(f"EVAL", id = "eval")




class Editor(Screen):

    BINDINGS = [
        Binding("ctrl+j", "play_backward", "◀◀", priority=True),
        Binding("ctrl+o", "step_backward", "◀", priority=True),
        Binding("ctrl+p", "step_forward", "▶", priority=True),
        Binding("ctrl+l", "play_forward", "▶▶", priority=True),
    ]

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
            self.error_area.text = 'READY.'
        elif value == 'Calculating...':
            self.error_area.text = value
        else:
            self.error_area.text = "ERROR: " + value

    ############################################################

    def compose(self) -> ComposeResult:

        # backend components
        self.mls = mls.MLS()
        self.gen_machine = GenMachine()

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

        self.error_area = TextArea(read_only=True)


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
            Label("Auto Generation:", id='gen_switch_label'),
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
                self.error_area
            ),
            self.gen_container,
        )

        yield Footer()
        
        # update the frame
        self.call_later(self.update_display)


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



    def update_gen(self) -> None:
        '''
        Update the generation information and checks the state of gen_machine.
        '''
        machine_str = str(self.gen_machine)
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

                self.gen_machine.terminate()

                self.gen_machine.gen(
                    goal = selected_goal,
                    worker_num = 8,
                    gen_env = self.mls.selected_frame.env,
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
                self.env_tabs.reload_defs(self.mls.selected_frame.env)


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