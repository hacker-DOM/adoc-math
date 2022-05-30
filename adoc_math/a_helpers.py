from ._common import *


class Helpers:
    # region files
    target_files: Set[plib.Path]
    file_contents: Dict[plib.Path, List[LineInFile]]
    file_contents_proposed: Dict[plib.Path, List[LineInFile]]
    # endregion

    # region default cell options
    default_lang: Lang
    default_scale: Scale
    default_positioning: Positioning
    default_vertical_align_offset: VerticalAlignOffset
    default_alignment: Alignment
    default_max_lines: MaxLines
    # endregion

    # region other options
    filename_snippet_length: int
    filename_bytes_length: int
    images_dir: plib.Path
    output_dir: plib.Path
    # output_mode: OutputMode
    # endregion

    # region algorithm substate
    cells: List[Cell]
    file_2_lines_inserted: Dict[plib.Path, LinesInserted]
    # endregion
