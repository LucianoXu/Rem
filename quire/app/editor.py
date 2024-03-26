from textual import on
from textual.app import ComposeResult
from textual.containers import Container, Horizontal
from textual.screen import Screen
from textual.widgets import Header, Footer, Placeholder, TextArea


class Editor(Screen):

    def compose(self) -> ComposeResult:
        self.code_area = TextArea(
            "// put your code here ...", 
            id='code-area',
            show_line_numbers=True)
        self.goal_area = TextArea(read_only=True)

        yield Header()
        yield Footer()
        yield Horizontal(
            self.code_area,
            self.goal_area
        )
        
    @on(TextArea.Changed)
    def process(self, event: TextArea.Changed):
        if event.text_area.id == 'code-area':
            prover = self.app.prover # type:ignore
            prover.restart(self.app.opts)   # type: ignore
            prover(event.text_area.text)
            self.goal_area.text = str(prover)
    