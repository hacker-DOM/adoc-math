from ._common import *
from . import b_reading


class Parsing(b_reading.Reading):
    def parse(s):
        for tf in s.target_files:
            file_contents_split = s.file_contents[tf]

            skip_count = 0
            for lineno, line_raw in enumerate(file_contents_split):
                if skip_count > 0:
                    skip_count -= 1
                    continue

                linenum: Linenum = Linenum(lineno + 1)
                line: LineInFile = LineInFile(line_raw)

                # Dev: would be nice to use walrus operator here,
                # but it is only available in python 3.8
                match_block = re.match(REGEX_BLOCK_OPENING_TAG, line)
                if match_block:
                    skip_count = s.parse_block_cell(
                        tf,
                        file_contents_split,
                        Lineno(lineno),
                        match_block,
                    )
                    # Dev: A block closing tag also matches an inline cell regex,
                    # so we continue here to prevent an empty inline cell being added.
                    continue

                match_inline = re.match(REGEX_INLINE, line)
                if match_inline:
                    s.parse_inline_cell(
                        tf,
                        file_contents_split,
                        Lineno(lineno),
                        match_inline,
                    )

    def parse_block_cell(
        s,
        tf: plib.Path,
        file_contents_split: List[LineInFile],
        lineno: Lineno,  # line no (0-indexed of opening tag)
        match: re.Match,  # match object with REGEX_BLOCK_OPENING_TAG
    ):
        # parse opts
        opts_raw = match.groupdict()["opts"]
        opts_parsed: Opts = s.parse_opts(
            opts_raw=OptionsRaw(opts_raw),
            tf=tf,
            lineno=lineno,
        )

        # find closing tag
        sublineno = lineno + 1
        subline = LineInFile(file_contents_split[sublineno])
        while not re.match(REGEX_BLOCK_CLOSING_TAG, subline):
            sublineno += 1
            try:
                subline = LineInFile(file_contents_split[sublineno])
            except IndexError:
                raise AdocMathException(
                    f"Couldn't find closing tag for block cell in {tf}#L{lineno + 1}."
                )

        # check max_lines
        num_of_lines = sublineno - lineno - 1
        assert (
            num_of_lines <= opts_parsed.max_lines
        ), f"Too many lines in block cell cell between {tf}#L{lineno + 1} and L{sublineno + 1}."

        # append block cell
        s.cells.append(
            BlockCell(
                path=tf,
                closing_tag_linenum=Linenum(sublineno + 1),
                linenum=Linenum(lineno + 1),
                opts=opts_parsed,
                content=CellContent(
                    join_with(
                        file_contents_split[lineno + 1 : sublineno],
                        os.linesep,
                    )
                ),
            )
        )

        # return skip count
        ret = SkipCount(sublineno - lineno)
        return ret

    def parse_inline_cell(
        s,
        tf: plib.Path,
        file_contents_split: List[LineInFile],
        lineno: Lineno,
        match: re.Match,
    ):
        # parse contents, opts
        content, opts_raw = (
            match.groupdict()["content"],
            match.groupdict()["opts"],
        )
        opts_parsed: Opts = s.parse_opts(
            opts_raw=OptionsRaw(opts_raw),
            tf=tf,
            lineno=lineno,
        )

        # max_lines check is not performed for inline cells

        s.cells.append(
            InlineCell(
                path=tf,
                linenum=Linenum(lineno + 1),
                opts=opts_parsed,
                content=CellContent(content),
            )
        )

    def parse_opts(
        s,
        opts_raw: OptionsRaw,
        tf: plib.Path,  # for error message
        lineno: Lineno,  # for error message
    ) -> Opts:
        lang, scale, positioning, vertical_align_offset, alignment, max_lines = [
            None
        ] * 6
        for opt_raw in opts_raw.split(","):
            opt_raw = opt_raw.strip()  # handle no options
            if opt_raw == "":
                continue
            split = opt_raw.split("=")
            if len(split) == 1:
                # simple case
                try:
                    positioning = Positioning(split[0].upper())
                except ValueError:
                    try:
                        lang = Lang(split[0].upper())
                    except ValueError:
                        try:
                            alignment = Alignment(split[0].upper())
                        except ValueError:
                            raise AdocMathException(
                                f"Invalid option on {tf}#L{lineno}: {opt_raw!r}"
                            )

            elif len(split) == 2:
                # assignment case
                key, val = (
                    split[0].strip(),
                    split[1].strip(),
                )
                if key == "scale":
                    scale = Scale(int(rshave(val, "%")))
                elif key == "vertical_align_offset":
                    vertical_align_offset = VerticalAlignOffset(
                        float(rshave(val, "ex"))
                    )
                elif key == "max_lines":
                    max_lines = MaxLines(int(val))
                else:
                    raise AdocMathException(f"Invalid option: {opt_raw!r}")
            else:
                raise AdocMathException(f"Invalid option: {opt_raw!r}")
        ret = Opts(
            lang=lang or s.default_lang,
            scale=scale or s.default_scale,
            positioning=positioning or s.default_positioning,
            vertical_align_offset=vertical_align_offset
            or s.default_vertical_align_offset,
            alignment=alignment or s.default_alignment,
            max_lines=max_lines or s.default_max_lines,
        )
        return ret
