from ._common import *
from . import e_svg_transforming

logger = get_logger(__file__, LOGGING_LEVEL)


class Processing(e_svg_transforming.SvgTransforming):
    def process(s):
        for cell in s.cells:
            stdout = s.call_mathjax_wrapper(cell)
            xml_str = s.transform_svg(cell, XmlStr(stdout))
            file_name = s.get_file_name(cell)
            file_path = s.write_svg_file(file_name, xml_str)
            s.handle_source_file(cell, file_path)

    def handle_source_file(
        s,
        cell: Cell,
        file_path: plib.Path,
    ):
        # region comment out cell math
        closing_tag_linenum = None
        if isinstance(cell, BlockCell):
            closing_tag_linenum = cell.closing_tag_linenum
        elif isinstance(cell, InlineCell):
            closing_tag_linenum = cell.linenum
        else:
            raise AdocMathException(DEAD_CODE_MSG)
        lines_inserted = s.file_2_lines_inserted[cell.path]
        s.comment_out(
            file_contents=s.file_contents_proposed[cell.path],
            linenums=range(
                cell.linenum - 1 + lines_inserted,  # These will be 0-indexed
                closing_tag_linenum - 1 + lines_inserted + 1,
            ),  # type: ignore
        )
        # endregion

        # region macro name part
        if isinstance(cell, BlockCell):
            macro_name = "image::"
        else:
            macro_name = "image:"
        # endregion

        # region import part
        import_part = plib.PosixPath(os.path.relpath(file_path, start=s.images_dir))
        # endregion

        # region image options
        if isinstance(cell, BlockCell):
            image_options = f"align={cell.opts.alignment.lower()}"
        else:
            image_options = ""

        # region insert image macro
        macro = f"{macro_name}{import_part}[{image_options}]{os.linesep}"

        # last line might not have os.linesep...
        file_contents = s.file_contents_proposed[cell.path]
        if file_contents[-1][-1] != os.linesep:
            file_contents[-1] = LineInFile(file_contents[-1] + os.linesep)
        file_contents.insert(
            closing_tag_linenum + lines_inserted,
            LineInFile(macro),
        )
        s.file_2_lines_inserted[cell.path] = LinesInserted(lines_inserted + 1)
        # endregion

    def get_file_name(
        s,
        cell: Cell,
    ) -> FileName:
        # region prefix
        block_or_inline_part = None
        if isinstance(cell, BlockCell):
            block_or_inline_part = "b_block"
        elif isinstance(cell, InlineCell):
            block_or_inline_part = "a_inline"
        else:
            raise AdocMathException(DEAD_CODE_MSG)
        # endregion

        # region lang part
        lang_part = cell.opts.lang.lower()
        # endregion

        # region snippet part
        snippet_part = s.get_snippet_part(cell, s.filename_snippet_length)
        # endregion

        # region random part
        bytes_len = s.filename_bytes_length
        random_part = (
            random.getrandbits(bytes_len * 8).to_bytes(bytes_len, byteorder="big").hex()
        )
        # endregion

        base = join_with(
            (
                block_or_inline_part,
                lang_part,
                snippet_part,
                random_part,
            ),
            "_",
        )
        full = base + ".svg"
        return FileName(full)

    def write_svg_file(
        s,
        file_name: FileName,
        xml_str: XmlStr,
    ) -> plib.Path:
        file_path = s.output_dir / file_name
        with open(file_path, "w") as f:
            f.write(xml_str)
        return file_path

    @staticmethod
    def get_snippet_part(
        cell: Cell,
        filename_snippet_length: int,
    ) -> SnippetPart:
        ret = join_with(
            (
                char
                for char in cell.content
                if char.isalnum() or char in {"+", "-", "=", "_", "(", ")"}
            ),
            "",
        )[:filename_snippet_length]
        return SnippetPart(ret)

    @staticmethod
    def call_mathjax_wrapper(
        cell: Cell,
    ) -> StdOut:
        pgm = "node"
        script_path_str = str(plib.Path(__file__).parent / "d_mathjax_wrapper.js")
        lang = cell.opts.lang.lower()
        block_or_inline = None
        if isinstance(cell, BlockCell):
            block_or_inline = "block"
        elif isinstance(cell, InlineCell):
            block_or_inline = "inline"
        else:
            raise AdocMathException(DEAD_CODE_MSG)
        cmd_args = [
            pgm,
            script_path_str,
            lang,
            block_or_inline,
        ]
        try:
            stdout, _ = run_cmd(
                Command(join_with(cmd_args, " ")),
                stdin=cell.content.encode(),
                raise_on_error=True,
            )
            return stdout
        except AdocMathException as e:
            logger.critical(
                f"Math cell in file {cell.path} starting on line {cell.linenum} failed in Mathjax. Here are the cell contents:\n{cell.content}"
            )
            logger.critical(e)
            sys.exit(1)

    @staticmethod
    def comment_out(
        file_contents: MutableSequence[LineInFile],
        linenums: Iterable[Linenum],
    ):
        for linenum in linenums:
            # Asciidoc comments have to *start with* "//"
            if not file_contents[linenum].startswith("//"):
                file_contents[linenum] = LineInFile(f"// {file_contents[linenum]}")
