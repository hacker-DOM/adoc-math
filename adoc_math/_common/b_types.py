from .a_imports import *

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
Scale = NewType("Scale", int)
VerticalAlignOffset = NewType("VerticalAlignOffset", float)
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
SvgDocument = NewType("SvgDocument", xml.dom.minidom.Document)
Svg = NewType("Svg", xml.dom.minidom.Element)
Ex = NewType("Ex", float)


class OutputMode(str, enum.Enum):
    OVERWRITE = "OVERWRITE"
    DIFF = "DIFF"


class Lang(str, enum.Enum):
    AMATH = "AMATH"
    TEX = "TEX"


class Positioning(str, enum.Enum):
    POSITION = "POSITION"
    DONT_POSITION = "DONT_POSITION"


class Alignment(str, enum.Enum):
    LEFT = "LEFT"
    CENTER = "CENTER"
    RIGHT = "RIGHT"


class Opts(NamedTuple):
    lang: Lang
    scale: Scale
    positioning: Positioning
    vertical_align_offset: VerticalAlignOffset
    alignment: Alignment
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


class SvgAttributesRaw(NamedTuple):
    style: str
    width: str
    height: str
    viewbox: str


class ViewBox(NamedTuple):
    # https://developer.mozilla.org/en-US/docs/Web/SVG/Attribute/viewBox
    min_x: Ex
    min_y: Ex
    width: Ex
    height: Ex

    def __str__(s):
        els = []
        for el in s:
            if el.is_integer():
                els.append(int(el))
            else:
                els.append(el)
        a, b, c, d = els
        return f"{a} {b} {c} {d}"


class SvgAttributesParsed(NamedTuple):
    vertical_align: Ex
    width: Ex
    height: Ex
    viewbox: ViewBox
