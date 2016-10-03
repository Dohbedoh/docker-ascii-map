from typing import Tuple


class Raster:
    def __init__(self):
        self._cells = []

    def write(self, x: int, y: int, text):
        if type(text) is Raster:
            rastersize_x, rastersize_y = text.size()

            for ry in range(rastersize_y):
                for rx in range(rastersize_x):
                    c = text.get(rx, ry)
                    if c != ' ':
                        self.write(x + rx, y + ry, c)
        else:
            self._expand(x + len(text), y + 1)

            for i in range(len(text)):
                self._cells[y][x + i] = text[i]

    def _expand(self, x, y):
        while len(self._cells) < y:
            self._cells.append([])

        while len(self._cells[y - 1]) < x:
            self._cells[y - 1].append(' ')

    def get(self, x: int, y: int) -> str:
        if y >= 0 and y < len(self._cells) and x >= 0 and x < len(self._cells[y]):
            return self._cells[y][x]
        else:
            return ' '

    def size(self) -> Tuple[int]:
        if len(self._cells) == 0:
            return 0, 0
        else:
            return max([len(l) for l in self._cells]), len(self._cells)

    def __str__(self):
        text = ''

        for line in self._cells:
            for c in line:
                text += c

            text += '\n'

        return text
