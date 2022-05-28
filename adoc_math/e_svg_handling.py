from ._common import *
from . import c_parsing

logger = get_logger(__file__, LOGGING_LEVEL)


class SvgHandling(c_parsing.Parsing):
    def handle_svg(
        s,
        xml_str: XmlStr,
    ) -> XmlStr:
        # todo:
        # This will contain any svg handling and manipulation code. Currently, it is the identity function
        return xml_str
