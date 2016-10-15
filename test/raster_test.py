import unittest

from raster import Raster, Boundary


class RasterTests(unittest.TestCase):
    def test_empty_raster(self):
        raster = Raster()
        self.assertEqual('', str(raster))
        self.assertEqual((0, 0), raster.size())
        self.assertEqual((' ', None), raster.get(5, 4))

    def test_expansion(self):
        raster = Raster()
        raster.write(8, 0, ' ')
        raster.write(0, 4, ' ')
        self.assertEqual(
            '         \n'
            '\n'
            '\n'
            '\n'
            ' \n'
            , str(raster)
        )

    def test_basic_raster(self):
        raster = Raster()
        raster.write(0, 0, 'a')
        self.assertEqual('a\n', str(raster))
        self.assertEqual((1, 1), raster.size())

    def test_multiline(self):
        raster = Raster()
        raster.write(2, 1, 'a')
        self.assertEqual('\n  a\n', str(raster))
        self.assertEqual((3, 2), raster.size())

    def test_string(self):
        raster = Raster()
        raster.write(2, 1, 'abc')
        raster.write(3, 1, 'abc')
        raster.write(4, 1, 'abc')
        self.assertEqual('\n  aaabc\n', str(raster))

    def test_write_raster(self):
        r1 = Raster()
        r1.write(0, 0, 'Hello', r1)
        r2 = Raster()
        r2.write(0, 0, 'World !', r2)

        r = Raster()
        r.write(0, 0, r1)
        r.write(2, 1, r2)
        self.assertEqual('Hello\n  World !\n', str(r))
        self.assertEqual((9, 2), r.size())

    def test_boundaries(self):
        r = Raster()
        r.write(4, 2, 'Hello', 'Origin1')
        r.write(4, 3, 'Hello', 'Origin1')
        r.write(4, 4, 'World', 'Origin2')

        self.assertEqual('4,2 5x2', str(r.origin_bounds('Origin1')))
        self.assertEqual('4,4 5x1', str(r.origin_bounds('Origin2')))
        self.assertEqual(None, r.origin_bounds('Origin3'))

    def test_boundary(self):
        self.assertEqual('4,2 5x2', str(Boundary(4, 2, 5, 2)))
        self.assertEqual(Boundary(4, 2, 5, 2), Boundary(4, 2, 5, 2))


if __name__ == '__main__':
    unittest.main()
