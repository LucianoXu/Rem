from textual import on
from textual.binding import Binding
from textual.app import ComposeResult
from textual.containers import Horizontal, Vertical, Container, ScrollableContainer
from textual.screen import Screen
from textual.widgets import Header, Footer, TextArea, Button, Static, Switch, Label
from textual.app import ComposeResult # type: ignore
from textual.reactive import reactive

from ..qrefine import mls, AstPres

from ..qrefine.prover.gen.gen_machine import GenMachine


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


    def compose(self) -> ComposeResult:

        # backend components
        self.mls = mls.MLS()
        self.gen_machine = GenMachine()

        # timer
        self.gen_update_timer = self.set_interval(1 / 10, self.update_gen, pause=False)

        # widgets
        self.verified_area = TextArea(
            "",
            id='verified-area',
            show_line_numbers=True,
            read_only=True
        )
        self.code_area = TextArea(
            "// put your code here ...", 
            id='code-area',
            show_line_numbers=True,
            tab_behavior='indent'
        )

        self.goal_area = TextArea(read_only=True)

        self.mls_info = TextArea(read_only=True)


        #######################################################
        # area for variables/rule/generation

        self.gen_area = TextArea(read_only=True)
        # the button to apply generation result
        self.apply_gen = Button("APPLY", id = "apply_gen")
        # the button to regenerate
        self.regen = Button("REGEN", id = "regen")
        # the switch to toogle generation
        self.gen_switch = Switch(True)

        self.gen_container = Container(
            self.gen_area,
            Horizontal(
                self.apply_gen,
                self.regen
            ),

            Label("Toogle Generation: "),
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
                self.goal_area,
                self.mls_info,
            ),
            self.gen_container,
        )

        yield Footer()


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



    def on_button_pressed(self, event: Button.Pressed) -> None:

        # apply the generation result
        if event.button.id == 'apply_gen':
            cmd = f"\n\nStep {self.gen_machine.sol}."
            res = self.mls.step_forward(cmd)

            self.mls_info.text = self.mls.info
            self.goal_area.text = self.mls.prover_info
            self.verified_area.text = self.mls.verified_code

        # regenerate
        elif event.button.id == 'regen':
            self.gen_machine.initialize()


    def action_step_forward(self) -> bool:
        res = self.mls.step_forward(self.code_area.text)

        if res is not None:
            self.code_area.text = res

        self.mls_info.text = self.mls.info
        self.goal_area.text = self.mls.prover_info
        self.verified_area.text = self.mls.verified_code

        return res is not None


    def action_step_backward(self) -> bool:
        res = self.mls.step_backward()

        if res is not None:
            self.code_area.text = res + self.code_area.text

        self.mls_info.text = self.mls.info
        self.goal_area.text = self.mls.prover_info
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

    def action_play_backward(self) -> None:
        # turn off the auto-gen temporarily
        auto_gen = self.gen_switch.value
        self.gen_switch.value = False

        while self.action_step_backward():
            pass
        
        self.gen_switch.value = auto_gen

        Vertical().remove


    def update_gen(self) -> None:
        '''
        Update the generation information and checks the state of gen_machine.
        '''
        self.gen_area.text = str(self.gen_machine)
        
        if self.gen_switch.value:

            current_goal = self.mls.current_goal
            
            if not self.mls.latest_selected or current_goal is None:
                self.gen_status = "disabled"

            # conditions to trigger the generation
            # 1. the latest frame is selected
            # 2. there is a current goal
            # 3. the current goal is different from the last generated goal
            elif current_goal != self.gen_machine.goal:

                self.gen_machine.terminate()

                self.gen_machine.gen(
                    goal = current_goal,
                    worker_num = 8,
                    gen_env = self.mls.current_frame.env,
                )

                self.gen_status = "working"

            # terminate the generation if the solution found
            if self.gen_machine.sol is not None:
                self.gen_status = "solved"

        else:
            self.gen_status = "disabled"

    @on(TextArea.SelectionChanged)
    def show_frame(self, event: TextArea.SelectionChanged) -> None:
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

                self.mls_info.text = self.mls.info
                self.goal_area.text = self.mls.prover_info

            except Exception:
                pass
            
    