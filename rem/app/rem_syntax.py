from pathlib import Path
from tree_sitter import Language, Parser

from rich.style import Style
from textual._text_area_theme import TextAreaTheme

Language.build_library(
  # Store the library in the `build` directory
  'build/rem.so',

  # Include one or more languages
  [
    'rem/tree-sitter-rem'
  ]
)

PY_REM = Language('build/rem.so', "rem")

# this is registed at the editor
rem_highlight_query = (Path(__file__).parent / "rem_highlights.scm").read_text()



REM_THEME = TextAreaTheme(
    name="subaru",
    syntax_styles={
        "comment": Style(color="green", italic=True),
        "prog_keyword": Style(color="black", bold=True),
        "keyword": Style(color="blue"),
        "variable": Style(color="#F92672", bold=True),
        "type": Style(color="green"),
        "operator": Style(color="purple"),
    },
)


REM_THEME_VERIFIED = TextAreaTheme(
    name="subaru-verified",
    # base_style=Style(bgcolor="#98fb98"),  # the pale green
    syntax_styles={
        "comment": Style(color="green", italic=True),
        "prog_keyword": Style(color="black", bold=True),
        "keyword": Style(color="blue"),
        "variable": Style(color="#F92672", bold=True),
        "type": Style(color="green"),
        "operator": Style(color="purple"),
    },
)