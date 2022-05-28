from ._common import *
from . import a_helpers

logger = get_logger(__file__, LOGGING_LEVEL)


class Reading(a_helpers.Helpers):
    def read(s):
        for tf in s.target_files:
            with open(tf) as f:
                try:
                    file_contents = f.read()
                    s.file_contents[tf] = file_contents.splitlines(keepends=True)  # type: ignore
                except Exception as e:
                    logger.critical(f"Couldn't read {tf}.")
                    logger.critical(e)
                    sys.exit(1)

        s.file_contents_proposed = {**s.file_contents}
