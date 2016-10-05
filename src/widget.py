from raster import Raster
from typing import List


class Widget:
    def render(self) -> Raster:
        pass


class Border(Widget):
    def __init__(self, component: Widget, title: str = ''):
        self._component = component
        self._title = title

    def render(self):
        cmp_raster = self._component.render()
        cmp_w, cmp_h = cmp_raster.size()

        min_width = 2 + len(self._title)
        width = max(min_width, cmp_w)

        r = Raster()

        for y in range(cmp_h + 2):
            r.write(0, y, '|')
            r.write(width + 3, y, '|')

        for x in range(width + 4):
            r.write(x, 0, '-')
            r.write(x, cmp_h + 1, '-')

        r.write(0, 0, '+')
        r.write(width + 3, 0, '+')
        r.write(0, cmp_h + 1, '+')
        r.write(width + 3, cmp_h + 1, '+')

        r.write(2, 0, ' ' + self._title + ' ')

        r.write(2, 1, cmp_raster)

        return r


class VBox(Widget):
    def __init__(self, content: List[Widget]):
        self._content = content

    def render(self):
        r = Raster()

        for content in self._content:
            contentraster = content.render()
            r.write(0, r.size()[1], contentraster)

        return r


class Paragraph(Widget):
    def __init__(self, lines: List[str]):
        self._lines = lines

    def render(self):
        r = Raster()

        for l in self._lines:
            r.write(0, r.size()[1], l)

        return r
