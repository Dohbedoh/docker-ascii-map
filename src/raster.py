from typing import Tuple


class Boundary:
    def __init__(self, x: int, y: int, w: int, h: int):
        self.x = x
        self.y = y
        self.w = w
        self.h = h

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __repr__(self):
        return '%d,%d %dx%d' % (self.x, self.y, self.w, self.h)


class Raster:
    def __init__(self):
        self._cells = []
        self._default = ' ', None

    def write(self, x: int, y: int, text, origin: object = None):
        if type(text) is Raster:
            rastersize_x, rastersize_y = text.size()

            for ry in range(rastersize_y):
                for rx in range(rastersize_x):
                    c, o = text.get(rx, ry)
                    self.write(x + rx, y + ry, c, o)
        else:
            self._expand(x + len(text), y + 1)

            for i in range(len(text)):
                self._cells[y][x + i] = text[i], origin

    def _expand(self, x, y):
        while len(self._cells) < y:
            self._cells.append([])

        while len(self._cells[y - 1]) < x:
            self._cells[y - 1].append(self._default)

    def get(self, x: int, y: int) -> Tuple[str, object]:
        if y >= 0 and y < len(self._cells) and x >= 0 and x < len(self._cells[y]):
            return self._cells[y][x]
        else:
            return self._default

    def size(self) -> Tuple[int]:
        if len(self._cells) == 0:
            return 0, 0
        else:
            return max([len(l) for l in self._cells]), len(self._cells)

    def origin_bounds(self, origin: object) -> Boundary:
        raster_w, raster_h = self.size()

        b_x, b_y, b_w, b_h = 0, 0, 0, 0

        for y in range(raster_h):
            for x in range(raster_w):
                cell = self.get(x, y)
                if origin == cell[1]:
                    if b_w == 0:
                        b_x, b_y, b_w, b_h = x, y, 1, 1
                    else:
                        if x >= b_x + b_w:
                            b_w = x - b_x + 1

                        if y >= b_y + b_h:
                            b_h = y - b_y + 1

        return Boundary(b_x, b_y, b_w, b_h) if b_w > 0 else None

    def __str__(self):
        text = ''

        for line in self._cells:
            for c in line:
                text += c[0]

            text += '\n'

        return text
