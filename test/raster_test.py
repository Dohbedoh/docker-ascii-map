import unittest

from raster import Raster


class RasterTests(unittest.TestCase):
    def test_empty_raster(self):
        raster = Raster()
        self.assertEqual('', str(raster))
        self.assertEqual((0, 0), raster.size())
        self.assertEqual(' ', raster.get(5,4))

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
        r1.write(0, 0, 'Hello')
        r2 = Raster()
        r2.write(0, 0, 'World !')

        r = Raster()
        r.write(0, 0, r1)
        r.write(2, 1, r2)
        self.assertEqual('Hello\n  World !\n', str(r))
        self.assertEqual((9, 2), r.size())


if __name__ == '__main__':
    unittest.main()
