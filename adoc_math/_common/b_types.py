from .c_constants import *

OptionsRaw = NewType("OptionsRaw", str)
OptionRaw = NewType("OptionRaw", str)
AssignmentOpt = NewType("AssignmentOpt", str)
SkipCount = NewType("SkipCount", int)
Lineno = NewType("Lineno", int)
Linenum = NewType("Linenum", int)
"""Line number

We're using the following terminology:
* lineno  is line number 0-indexed
  * this follows e.g. python ast's lineno
* linenum is line number 1-indexed
  * this follows e.g. editors (e.g. vs code)"""
MaxLines = NewType("MaxLines", int)
LineInFile = NewType("LineIFile", str)
Command = NewType("Command", str)
StdOut = NewType("StdOut", str)
StdErr = NewType("StdErr", str)
XmlStr = NewType("XmlStr", str)
CellContent = NewType("CellContent", str)
FileName = NewType("FileName", str)
SnippetPart = NewType("SnippetPart", str)
DiffContent = NewType("DiffContent", str)
LinesInserted = NewType("LinesInserted", int)


class OutputMode(str, enum.Enum):
    OVERWRITE = "OVERWRITE"
    DIFF = "DIFF"


class Lang(str, enum.Enum):
    AMATH = "AMATH"
    TEX = "TEX"


# class Alignment(str, enum.Enum):
#     ALIGN = "ALIGN"
#     DONT_ALIGN = "DONT_ALIGN"


class Opts(NamedTuple):
    lang: Lang
    # alignment: Alignment
    max_lines: MaxLines


class BlockCell(NamedTuple):
    path: plib.Path
    linenum: Linenum  # 1-indexed line num of opening tag
    closing_tag_linenum: Linenum
    opts: Opts
    content: CellContent


class InlineCell(NamedTuple):
    path: plib.Path
    linenum: Linenum
    opts: Opts
    content: CellContent


Cell = Union[InlineCell, BlockCell]
