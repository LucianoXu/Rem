from pathlib import Path
from sys import argv


from textual.app import App, ComposeResult
from textual.reactive import var
from textual.screen import Screen
from textual.widgets import Header, Footer, MarkdownViewer, Label


class Handbook(Screen):
    BINDINGS = [
        ("t", "toggle_table_of_contents", "Table of Contents"),
        ("f1", "to_editor", "To Editor"),
    ]

    path = var("README.md")

    def action_to_editor(self) -> None:
        self.app.switch_mode("editor")

    @property
    def markdown_viewer(self) -> MarkdownViewer:
        """Get the Markdown widget."""
        return self.query_one(MarkdownViewer)

    def compose(self) -> ComposeResult:
        self.title = "QRefine Handbook"
        yield Header()
        yield Footer()
        yield MarkdownViewer()

    async def on_mount(self) -> None:
        self.markdown_viewer.focus()
        try:
            await self.markdown_viewer.go(self.path)
        except FileNotFoundError:
            pass

    def action_toggle_table_of_contents(self) -> None:
        try:
            self.markdown_viewer.show_table_of_contents = (
                not self.markdown_viewer.show_table_of_contents
            )
        except:
            pass