from typing import List, Mapping, Tuple

from raster import Raster


class Size:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height

    def __repr__(self):
        return 'Size{w:%d,h:%d}' % (self.width, self.height)

    def __eq__(self, other):
        return self.__dict__ == other.__dict__


class Hints:
    def __init__(self, size: Size):
        self.size = size


class Widget:
    def render(self, hints: Hints = None) -> Raster:
        pass

    def preferred_size(self) -> Size:
        pass


class Padding(Widget):
    def __init__(self, component: Widget, amount: Size):
        self._component = component
        self._amount = amount

    def preferred_size(self) -> Size:
        nested = self._component.preferred_size()
        return Size(nested.width + self._amount.width * 2, nested.height + self._amount.height * 2)

    def render(self, hints: Hints = None) -> Raster:
        r = Raster()
        nested = self._component.preferred_size()

        for y in range(nested.height + 2 * self._amount.height):
            for x in range(nested.width + 2 * self._amount.width):
                r.write(x, y, ' ', self)

        cmp_raster = self._component.render()
        r.write(self._amount.width, self._amount.height, cmp_raster)

        return r


class Border(Widget):
    def __init__(self, component: Widget, title: str = ''):
        self._component = Padding(component, Size(1, 0))
        self._title = title

    def preferred_size(self) -> Size:
        nested = self._component.preferred_size()
        return Size(nested.width + 2, nested.height + 2)

    def render(self, hints: Hints = None) -> Raster:
        cmp_raster = self._component.render()
        cmp_size = self._component.preferred_size()
        cmp_w, cmp_h = cmp_size.width, cmp_size.height

        if hints is not None:
            cmp_w, cmp_h = hints.size.width - 2, hints.size.height - 2

        min_width = 2 + len(self._title)
        width = max(min_width, cmp_w)

        r = Raster()

        for y in range(cmp_h + 2):
            r.write(0, y, '|', self)
            r.write(width + 1, y, '|', self)

        for x in range(width + 2):
            r.write(x, 0, '-', self)
            r.write(x, cmp_h + 1, '-', self)

        r.write(0, 0, '+', self)
        r.write(width + 1, 0, '+', self)
        r.write(0, cmp_h + 1, '+', self)
        r.write(width + 1, cmp_h + 1, '+', self)

        if len(self._title) > 0:
            r.write(2, 0, ' ' + self._title + ' ', self)

        r.write(1, 1, cmp_raster)

        return r


class VBox(Widget):
    def __init__(self, content: List[Widget]):
        self._content = content

    def preferred_size(self) -> Size:
        w, h = 0, 0

        for content in self._content:
            ps = content.preferred_size()
            w = max(ps.width, w)
            h += ps.height

        return Size(w, h)

    def render(self, hints: Hints = None):
        r = Raster()
        max_width = self.preferred_size().width

        for content in self._content:
            hints = Hints(Size(max_width, content.preferred_size().height))
            contentraster = content.render(hints)
            r.write(0, r.size()[1], contentraster)

        return r


class HBox(Widget):
    def __init__(self, content: List[Widget]):
        self._content = content

    def preferred_size(self) -> Size:
        w, h = 0, 0

        for content in self._content:
            ps = content.preferred_size()
            w += ps.width
            h = max(ps.height, h)

        return Size(w, h)

    def render(self, hints: Hints = None):
        r = Raster()

        for content in self._content:
            hints = Hints(content.preferred_size())
            contentraster = content.render(hints)
            r.write(r.size()[0], 0, contentraster)

        return r


class Paragraph(Widget):
    def __init__(self, lines: List[str]):
        self._lines = lines

    def preferred_size(self) -> Size:
        return Size(max([len(l) for l in self._lines]), len(self._lines))

    def render(self, hints: Hints = None):
        r = Raster()

        for l in self._lines:
            r.write(0, r.size()[1], l, self)

        return r


class Links(Widget):
    def __init__(self, root: Widget, links: List[Tuple[Widget]]):
        self._root = root
        self._links = links

    def render(self, hints: Hints = None):
        raster = self._root.render(hints)

        for w_src, w_dst in self._links:
            bounds_src = raster.origin_bounds(w_src)
            bounds_dst = raster.origin_bounds(w_dst)
            src_x = bounds_src.x + bounds_src.w
            src_y = int(bounds_src.y + bounds_src.h / 2)
            dst_x = bounds_dst.x
            dst_y = int(bounds_dst.y + bounds_dst.h / 2)
            med_x = int((src_x + dst_x) / 2)

            for x in range(src_x, dst_x):
                y = src_y if x < med_x else dst_y
                raster.write(x, y, '-')

            for y in range(min(src_y, dst_y), max(src_y, dst_y)):
                raster.write(med_x, y, '|')

            raster.write(med_x, src_y, '+')
            raster.write(med_x, dst_y, '+')

        return raster
