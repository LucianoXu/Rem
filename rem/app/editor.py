from textual import on
from textual.binding import Binding
from textual.app import ComposeResult
from textual.containers import Horizontal, Vertical, Container
from textual.screen import Screen
from textual.widgets import Header, Footer, TextArea
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

    #############################################################
    # auto-gen switch
    # controls whether the generation is carried out and updated automatically
    auto_gen = reactive(True)

    def watch_auto_gen(self, value: bool) -> None:
        if value:
            self.gen_update_timer.resume()
        else:
            self.gen_update_timer.pause()
            self.gen_machine.terminate()
    ############################################################


    def compose(self) -> ComposeResult:

        self.gen_update_timer = self.set_interval(1 / 60, self.update_gen, pause=True)

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

        self.mls = mls.MLS()

        self.gen_area = TextArea(read_only=True)

        self.gen_machine = GenMachine()

        # the switch that controls whether auto generation is on
        self.auto_gen = True


        yield Header()

        yield Horizontal(
            Vertical(
                self.verified_area,
                self.code_area,
            ),
            Vertical(
                self.goal_area,

                Horizontal(
                    self.mls_info,
                    self.gen_area,
                )
            ),
                
        )

        yield Footer()



    def action_step_forward(self) -> bool:
        res = self.mls.step_forward(self.code_area.text)

        if res is not None:
            self.code_area.text = res

        self.mls_info.text = self.mls.info
        self.goal_area.text = self.mls.prover_info
        self.verified_area.text = self.mls.verified_code

        # verified_area scroll to end
        self.verified_area.scroll_end(animate = False)

        # set the cursor to the end
        self.verified_area.select_all()
        self.verified_area.move_cursor(self.verified_area.cursor_location)

        return res is not None


    def action_step_backward(self) -> bool:
        res = self.mls.step_backward()

        if res is not None:
            self.code_area.text = res + self.code_area.text


        self.mls_info.text = self.mls.info
        self.goal_area.text = self.mls.prover_info
        self.verified_area.text = self.mls.verified_code

        # verified_area scroll to end
        self.verified_area.scroll_end(animate = False)

        # set the verified_area cursor to the end
        self.verified_area.select_all()
        self.verified_area.move_cursor(self.verified_area.cursor_location)

        # push the code_area cursor backwards
        if res is not None:
            row_offset = res.count('\n')
            col_offset = len(res.split('\n')[-1])
            self.code_area.move_cursor_relative(row_offset, col_offset)

        return res is not None

    def action_play_forward(self) -> None:
        # turn off the auto-gen temporarily
        auto_gen = self.auto_gen
        self.auto_gen = False

        while self.action_step_forward():
            pass

        self.auto_gen = auto_gen

    def action_play_backward(self) -> None:
        # turn off the auto-gen temporarily
        auto_gen = self.auto_gen
        self.auto_gen = False

        while self.action_step_backward():
            pass
        
        self.auto_gen = auto_gen


    def update_gen(self) -> None:
        '''
        Update the generation area.
        '''
        self.gen_area.text = str(self.gen_machine)

        if self.auto_gen:
            current_goal = self.mls.current_goal
            
            # conditions to trigger the generation
            # 1. the latest frame is selected
            # 2. there is a current goal
            # 3. the current goal is different from the last generated goal
            if self.mls.latest_selected and \
                current_goal is not None and \
                current_goal != self.gen_machine.goal:

                self.gen_machine.terminate()

                self.gen_machine.gen(
                    goal = current_goal,
                    worker_num = 1,
                    gen_env = self.mls.current_frame.env,
                )

            # terminate the generation if the solution found
            if self.gen_machine.sol is not None and self.gen_machine.working:

                self.gen_machine.terminate()


    @on(TextArea.SelectionChanged)
    def show_frame(self, event: TextArea.SelectionChanged) -> None:
        '''
        Select the code in verified-area and show the corresponding frame.
        '''
        if event.text_area.id == 'verified-area':
            
            # avoid the empty selection
            if self.verified_area.text == "":
                return
            
            # calculate the pos of the cursor 
            pos = len(self.verified_area.get_text_range((0,0), event.selection.end)) + 1
            
            self.mls.set_cursor(pos)

            self.mls_info.text = self.mls.info
            self.goal_area.text = self.mls.prover_info
            
    