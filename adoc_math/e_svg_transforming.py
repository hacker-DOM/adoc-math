from ._common import *
from . import c_parsing

logger = get_logger(__file__, LOGGING_LEVEL)


class SvgTransforming(c_parsing.Parsing):
    def transform_svg(
        s,
        cell: Cell,
        xml_str: XmlStr,
    ) -> XmlStr:
        document = xml.dom.minidom.parseString(xml_str)
        svg = document.childNodes[0]

        s.handle_vertical_align_offset(
            svg=svg,
            vertical_align_offset=cell.opts.vertical_align_offset,
        )

        s.handle_scale(
            svg=svg,
            scale=cell.opts.scale,
        )

        s.handle_positioning(
            svg=svg,
            positioning=cell.opts.positioning,
        )

        ret = s.compile_svg(svg)

        return ret

    @staticmethod
    def handle_vertical_align_offset(
        svg: Svg,
        vertical_align_offset: VerticalAlignOffset,
    ):
        if vertical_align_offset != 0:
            attrs = SvgTransforming.get_attrs(svg)
            a = svg.attributes
            vertical_align = str(attrs.vertical_align + vertical_align_offset) + "ex"
            a["style"].value = f"vertical-align: {vertical_align};"

    @staticmethod
    def handle_scale(
        svg: Svg,
        scale: Scale,
    ):
        if scale != 100:
            attrs = SvgTransforming.get_attrs(svg)

            a = svg.attributes

            vertical_align = str(attrs.vertical_align * scale / 100) + "ex"
            width = str(attrs.width * scale / 100) + "ex"
            height = str(attrs.height * scale / 100) + "ex"

            a["style"].value = f"vertical-align: {vertical_align};"
            a["width"].value = width
            a["height"].value = height

        elif scale == 100:
            pass
        else:
            raise AdocMathException(DEAD_CODE_MSG)

    @staticmethod
    def handle_positioning(
        svg: Svg,
        positioning: Positioning,
    ):
        if positioning == Positioning.POSITION:
            attrs = SvgTransforming.get_attrs(svg)
            vertical_position_perc = attrs.vertical_align / attrs.height

            viewbox_post = ViewBox(
                min_x=attrs.viewbox.min_x,
                min_y=attrs.viewbox.min_y,
                width=attrs.viewbox.width,
                height=Ex(attrs.viewbox.height * (1 + vertical_position_perc)),
            )

            a = svg.attributes
            a["viewBox"].value = str(viewbox_post)

            a["height"].value = str(attrs.height - attrs.vertical_align) + "ex"
        elif positioning == Positioning.DONT_POSITION:
            pass
        else:
            raise AdocMathException(DEAD_CODE_MSG)

    @staticmethod
    def get_attrs(
        svg: Svg,
    ) -> SvgAttributesParsed:
        attrs = svg.attributes
        raw = SvgAttributesRaw(
            style=attrs["style"].value,
            width=attrs["width"].value,
            height=attrs["height"].value,
            viewbox=attrs["viewBox"].value,
        )

        key = "vertical-align:"
        idx_of_key = raw.style.index(key)
        vertical_position: str = raw.style[idx_of_key + len(key) + 1 :]

        def parse_viewbox(vb: str) -> ViewBox:
            args = [Ex(float(el)) for el in vb.split(" ")]
            return ViewBox(*args)

        def parse_ex(ex_str: str) -> Ex:
            interm = rshave(ex_str, ";")
            interm = rshave(interm, "ex")
            return Ex(float(interm))

        return SvgAttributesParsed(
            vertical_align=parse_ex(vertical_position),
            width=parse_ex(raw.width),
            height=parse_ex(raw.height),
            viewbox=parse_viewbox(raw.viewbox),
        )

    @staticmethod
    def compile_svg(
        svg: Svg,
    ) -> XmlStr:
        ret = svg.toprettyxml(indent=" " * 4)

        # remove the weird newline issue
        ret = join_with(
            (s for s in ret.splitlines()),
            os.linesep,
        )

        return XmlStr(ret)
