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
        "target_files", help="List of files to run `adoc-math` on.", **list_of_files
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

    # p.add_argument("--default-alignment", help="Default alignment")

    p.add_argument(
        "--default-lang",
        help="Default language. Can be TEX (LaTeX) or AMATH (AsciiMath).",
    )

    p.add_argument(
        "--default-max-lines",
        help="To ensure that you don't forget to close a cell, there is an option to set the maximum number of lines that a cell can have. This option sets the default value, but it can be overridden: as `$$max_lines=10\nx\n$$`. Max lines option (either through CLI or through a cell attribute) has no effect on inline cells, since they span just one line. Default: 6.",
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
    # None if they are not specified by the user. If we just use something like `i_impl.AdocMath(default_alignment=args.default_alignment`
    # etc (for all other arguments), then we'll lose the default values
    # as specified in AdocMath (e.g. default_alignment = Alignment.ALIGN)
    # So instead, let's just filter out those that are None
    # (more specifically those that are falsy), and pass in the rest
    kwargs = {key: val for key, val in vars(args).items() if val}
    adoc_math = i_impl.AdocMath(**kwargs)
    adoc_math.run()


if __name__ == "__main__":
    main()
