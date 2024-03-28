from typing import Coroutine
from textual import on
from textual.binding import Binding
from textual.app import ComposeResult
from textual.containers import Container, Horizontal, Vertical
from textual.events import Event, Key, MouseDown
from textual.screen import Screen
from textual.widgets import Header, Footer, Placeholder, TextArea, Static, Button
from textual.renderables.gradient import LinearGradient
from qplcomp import ParsingError
from textual.reactive import reactive
from textual.app import ComposeResult, RenderableType # type: ignore

from qplcomp import prepare_env

from .backends import *

from ..prover import mls

from time import time


class Editor(Screen):

    BINDINGS = [
        Binding("ctrl+l", "play_backward", "◀◀", priority=True),
        Binding("ctrl+p", "step_backward", "◀", priority=True),
        Binding("ctrl+o", "step_forward", "▶", priority=True),
        Binding("ctrl+j", "play_forward", "▶▶", priority=True),
    ]

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

        return res is not None

    def action_play_forward(self) -> None:
        while self.action_step_forward():
            pass

    def action_play_backward(self) -> None:
        while self.action_step_backward():
            pass

    def compose(self) -> ComposeResult:

        self.verified_area = TextArea(
            "",
            id='verified-area',
            show_line_numbers=True,
            read_only=True
        )
        self.code_area = TextArea(
            "// put your code here ...", 
            id='code-area',
            show_line_numbers=True)

        self.goal_area = TextArea(read_only=True)

        self.mls_info = TextArea(read_only=True)

        self.mls = mls.MLS(prepare_env())

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
                
        )

        yield Footer()

    @on(TextArea.Changed)
    def process(self, event: TextArea.Changed):
        pass


        # if event.text_area.id == 'code-area':
        #     prover = Prover(operators)
        #     cmd_stack = parse(event.text_area.text)

        #     for cmd in cmd_stack.stack:
        #         prover.execute(cmd)
        #         self.goal_area.text = str(prover)
    