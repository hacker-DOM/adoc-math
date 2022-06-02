import argparse as argp

from . import i_impl

NAME = "adoc-math"  # Cannot import from setup.py, src
DESCRIPTION = """Use MathJax (Latex or AsciiMath) in your AsciiDoc projects!"""

list_of_files = dict(
    metavar="files",
    action="store",
    nargs="*",
    default=list(),
)


def parse_args():
    p = argp.ArgumentParser(
        prog=NAME,
        description=DESCRIPTION,
    )

    p.add_argument(
        "target_files",
        help="List of files to run `adoc-math` on. Inline cells (lines such as `$x+y$ tex`) or block cells (line ranges such as [`$$ amath\n`, `x+y\n`, `$$\n`]) will be read for contents, parsed for options, passed into MathJax@3, and (optionally) the svg transformed. The svg will then be saved to the output directory, and the source file modified: the cell will be commented out and an image macro with a reference to the svg will be inserted. 🤟🚀",
        **list_of_files,
    )

    p.add_argument(
        "--exclude",
        help="List of files to be excluded; overrides `target_files`.",
        **list_of_files,
    )

    p.add_argument(
        "--include",
        help="List of files to be included; overrides `target_files` and `--exclude`.",
        **list_of_files,
    )

    p.add_argument(
        "--default-lang",
        help="Default language. Can be `TEX` (LaTeX) or `AMATH` (AsciiMath). Default: amath.",
        choices=("tex", "amath"),
    )

    p.add_argument(
        "--default-scale",
        help="Default scale. This option scales your svgs width and height (in `ex` units). Note that Asciidoctor does not provide a good API for scaling svgs - you can specify a fixed width, but cannot scale by a factor. By default, the math is a little bit too big (a little larger than surrounding text) - at least on the default Asciidoc theme. As such, the default is 90%%. Default: 90%%.",
    )

    p.add_argument(
        "--default-positioning",
        help=r'The raw svg, placed in the asciidoc document, usually gets rendered slightly above the line base (the baseline that characters which don\'t have lower parts (like "y" or "j" are above). Fortunately, Mathjax provides a "style" attribute in the svg (in the form of CSS), which is normally used by browsers to vertically align the math characters. I figured out a way to read this, process it, and achieve a similar effect in pdfs. The idea is that for simple symbols, like $x$, you usually want to position it. However, when you have a fraction ($\frac{a}{b}$), it usually looks better unpositioned. This option controls the default positioning for cells. Default: position.',
        choices=("position", "dont_position"),
    )

    p.add_argument(
        "--default-vertical-align-offset",
        help="This option allows to specify an offset to the `vertical-align` style explained above. For example, capital letter (`P`) seem to get positioned nicely, but lowercase letters (`p`) are not; I found that `vertical_align_offset = -0.4ex` works well for singleton lowercase characters. Note that this option won't have any effect if `positioning` is set to `dont_position`. Default: 0.0ex.",
    )

    p.add_argument(
        "--default-alignment",
        help="This option controls the default *horizontal* alignment of *block* cells. In particuar, it uses Asciidoc's `image:...[align=(left|center|right)]` API. Default: center.",
        choices=("left", "center", "right"),
    )

    p.add_argument(
        "--default-max-lines",
        help=r"If you forget to close a cell, it can be difficult to find the culprit. To prevent this, there is an option to set the maximum number of lines that a cell can have. This option sets the default value, but it can be overridden: as `$$max_lines=10\nx\n$$`. The `max_lines` option (set either through CLI or through a cell attribute) has no effect on inline cells, since they span just one line. Default: 6.",
    )

    p.add_argument(
        "--filename-snippet-length",
        type=int,
        help="Created files (svg) will have several parts. One of them is a snippet of the cell contents. This option controls how many characters that snippet will be. Default: 4.",
    )

    p.add_argument(
        "--filename-bytes-length",
        type=int,
        help="Another part of the svg file name is a random byte sequence. (This is necessary since the snippet only has e.g. four characters and also because not all Latex characters are allowed as filenames.) This option controls how many bytes that sequence will be. Default: 4.",
    )

    p.add_argument(
        "--images-dir",
        help="If you use `:imagesdir:` in your project, this should be the same value as that. In particular, it shouldn't be a path, but rather a string specifying the Unix-style subdirectory of `pwd`. For example, `assets/imgs`, or just `imgs.` It is used to determine the path part of the image macro (e.g. image::{path}.svg[]). In Asciidoc, `:imagesdir:` is by default `pwd`, so that is the default value here as well.",
    )

    p.add_argument(
        "--output-dir",
        help="The subdirectory of `--images-dir` that will contain the svgs. By default, it will be `imgs/adoc-math` if `--images-dir` is not defined, and `adoc-math` if it is defined.",
    )

    args = p.parse_args()
    return args


def main():
    args = parse_args()

    # The idea here is that the arguments specified in `parse_args` will have value
    # None if they are not specified by the user. If we just use something like `i_impl.AdocMath(default_positioning=args.default_positioning`
    # etc (for all other arguments), then we'll lose the default values
    # as specified in AdocMath (e.g. default_positioning = Positioning.POSITION)
    # So instead, let's just filter out those that are None
    # (more specifically those that are falsy), and pass in the rest
    kwargs = {key: val for key, val in vars(args).items() if val}
    adoc_math = i_impl.AdocMath(**kwargs)
    adoc_math.run()


if __name__ == "__main__":
    main()
