from .b_types import *

LOGGING_LEVEL = logging.DEBUG

# Note: whitespace before $$ is not allowed
REGEX_BLOCK_OPENING_TAG_SRC = r"^\$\$(?P<opts>.*?)\s*$"
REGEX_BLOCK_OPENING_TAG = re.compile(REGEX_BLOCK_OPENING_TAG_SRC)

# Note: whitespace before $$ is not allowed
REGEX_BLOCK_CLOSING_TAG_SRC = r"^\$\$\s*$"
REGEX_BLOCK_CLOSING_TAG = re.compile(REGEX_BLOCK_CLOSING_TAG_SRC)

REGEX_INLINE_SRC = r"^\$(?P<content>.+?)\$(?P<opts>.*?)\s*$"
REGEX_INLINE = re.compile(REGEX_INLINE_SRC)

REPO = "https://github.com/hacker-dom/asciidoc-mathjax"

DEAD_CODE_MSG = (
    f"""This case should not happen. Please create an issue at {REPO}/issues/new."""
)
