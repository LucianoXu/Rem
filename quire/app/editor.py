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

from .backends import *

from ..prover import mls

from time import time


class Editor(Screen):

    BINDINGS = [
        Binding("ctrl+o", "step_forward", "Step Forward", priority=True),
        Binding("ctrl+p", "step_backward", "Step Backward", priority=True),
    ]

    def action_step_forward(self) -> None:
        res = self.mls.step_forward(self.code_area.text)
        if res is not None:
            self.code_area.text = res
        self.goal_area.text = self.mls.info
        self.verified_area.text = self.mls.verified_code


    def action_step_backward(self) -> None:
        res = self.mls.step_backward()
        if res is not None:
            self.code_area.text = res + self.code_area.text
        self.goal_area.text = self.mls.info
        self.verified_area.text = self.mls.verified_code

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

        self.mls = mls.MLS()

        yield Header()

        yield Horizontal(
            Vertical(
                self.verified_area,
                self.code_area,
            ),
            self.goal_area,
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
    