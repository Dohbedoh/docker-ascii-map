from typing import List

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
        cmp_raster = self._component.render()
        r = Raster()
        r.write(self._amount.width, self._amount.height, cmp_raster)
        raster_size = r.size()

        # Force raster expansion
        if hints is not None and (raster_size[0] < hints.size.width or raster_size[1] < hints.size.height):
            r.write(hints.size.width - 1, hints.size.height - 1, ' ')

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
            r.write(0, y, '|')
            r.write(width + 1, y, '|')

        for x in range(width + 2):
            r.write(x, 0, '-')
            r.write(x, cmp_h + 1, '-')

        r.write(0, 0, '+')
        r.write(width + 1, 0, '+')
        r.write(0, cmp_h + 1, '+')
        r.write(width + 1, cmp_h + 1, '+')

        if len(self._title) > 0:
            r.write(2, 0, ' ' + self._title + ' ')

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
            r.write(0, r.size()[1], l)

        return r
