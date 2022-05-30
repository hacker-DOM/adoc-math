from ._common import *

from . import g_output

logger = get_logger(__file__, LOGGING_LEVEL)

OptionalListOfPaths = Union[None, Iterable[Union[plib.Path, str]]]


class AdocMath(g_output.Output):
    def __init__(
        s,
        # region files
        # Not using = [] (default list) here due to
        # https://web.archive.org/web/20200221224620/http://effbot.org/zone/default-values.htm
        target_files: OptionalListOfPaths = None,
        exclude: OptionalListOfPaths = None,
        include: OptionalListOfPaths = None,
        # endregion
        # region default cell options
        default_lang: Union[Lang, str] = Lang.AMATH,
        default_scale: Union[Scale, str] = Scale(90),
        default_positioning: Union[Positioning, str] = Positioning.POSITION,
        default_vertical_align_offset: Union[
            VerticalAlignOffset, str
        ] = VerticalAlignOffset(0),
        default_alignment: Union[Alignment, str] = Alignment.CENTER,
        default_max_lines: Union[MaxLines, int] = MaxLines(6),
        # endregion
        # region other options
        filename_snippet_length: int = 4,
        filename_bytes_length: int = 4,
        images_dir: Optional[str] = None,
        output_dir: Optional[str] = None,
        # todo:
        # output_mode: Union[OutputMode, str] = OutputMode.OVERWRITE,
        # endregion
    ):
        super().__init__()

        # region initialize compound types
        s.target_files: Set[plib.Path] = set()
        s.file_contents: Dict[plib.Path, List[str]] = dict()
        s.file_contents_proposed: Dict[plib.Path, List[str]] = dict()
        s.cells = list()
        s.file_2_lines_inserted = collections.defaultdict(lambda: LinesInserted(0))
        # endregion

        # region files
        if target_files:
            for_each_apply_method(
                ps=target_files,
                method=s.target_files.add,
            )

        if exclude:
            for_each_apply_method(
                ps=exclude,
                method=s.target_files.discard,
            )

        if include:
            for_each_apply_method(
                ps=include,
                method=s.target_files.add,
            )
        # endregion

        # region default cell options
        # typecast Lang | str to Lang
        s.default_lang = Lang(default_lang.upper())
        s.default_scale = Scale(int(rshave(default_scale, "%")))
        s.default_positioning = Positioning(default_positioning.upper())
        s.default_vertical_align_offset = VerticalAlignOffset(
            float(rshave(default_vertical_align_offset, "ex"))
        )
        s.default_alignment = Alignment(default_alignment.upper())
        s.default_max_lines = MaxLines(default_max_lines)
        # endregion

        # region other options
        s.filename_snippet_length = filename_snippet_length
        s.filename_bytes_length = filename_bytes_length
        if images_dir and output_dir:
            s.images_dir = plib.Path.cwd() / images_dir
            s.output_dir = s.images_dir / output_dir
        elif images_dir and not output_dir:
            s.images_dir = plib.Path.cwd() / images_dir
            s.output_dir = s.images_dir / "adoc-math"
        elif not images_dir and output_dir:
            s.images_dir = plib.Path.cwd()
            s.output_dir = s.images_dir / output_dir
        elif not images_dir and not output_dir:
            s.images_dir = plib.Path.cwd()
            s.output_dir = s.images_dir / "imgs" / "adoc-math"
        else:
            raise AdocMathException(DEAD_CODE_MSG)
        # s.output_mode = OutputMode(output_mode.upper())
        # endregion

        # region setup
        random.seed(bytes())
        plib.Path.mkdir(s.output_dir, parents=True, exist_ok=True)
        s.lines_inserted = LinesInserted(0)
        # endregion

    def run(
        s,
    ):
        s.read()
        s.parse()
        s.process()
        s.output()
