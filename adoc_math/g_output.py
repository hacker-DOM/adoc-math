from ast import Not
from ._common import *
from . import f_processing

logger = get_logger(__file__, LOGGING_LEVEL)


class Output(f_processing.Processing):
    def output(
        s,
    ):
        # if s.output_mode == OutputMode.OVERWRITE:
        #     s.overwrite()
        # elif s.output_mode == OutputMode.DIFF:
        #     s.diff()
        # else:
        #     raise AdocMathException(DEAD_CODE_MSG)
        s.overwrite()

    def overwrite(
        s,
    ):
        for sf, content in s.file_contents_proposed.items():
            with open(sf, "w") as f:
                f.write(
                    join_with(
                        s.file_contents_proposed[sf],
                        "",
                    )
                )

    def diff(
        s,
    ):
        diff_content = s.get_diff_content()
        s.overwrite_diff_file(diff_content)

    def get_diff_content(
        s,
    ) -> DiffContent:
        raise NotImplementedError()

    def overwrite_diff_file(
        s,
        diff_content: DiffContent,
    ):
        diff_file = plib.Path("./adoc-math.diff").resolve()
        with open(diff_file, "w") as f:
            f.write(diff_content)
