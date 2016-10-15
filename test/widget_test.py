import unittest

from raster import Boundary
from widget import *


class ModelTests(unittest.TestCase):
    @staticmethod
    def test_abstracts():
        w = Widget()
        w.render()
        w.preferred_size()

    def test_size(self):
        size = Size(2, 3)
        self.assertEqual(2, size.width)
        self.assertEqual(3, size.height)
        self.assertEqual('Size{w:2,h:3}', repr(size))
        self.assertEqual('Size{w:2,h:3}', str(size))

    def test_paragraph(self):
        model = Paragraph(['Hello', 'World !'])
        raster = model.render()
        self.assertEqual(
            'Hello\n'
            'World !\n',
            str(raster))
        self.assertEqual('0,0 7x2', str(raster.origin_bounds(model)))

    def test_VBox(self):
        model = VBox([Paragraph(['Hello', 'World !']), Paragraph(['Python rules !'])])
        self.assertEqual(
            'Hello  \n'
            'World !\n'
            'Python rules !\n',
            str(model.render()))

    def test_VBox_Borders(self):
        model = VBox([Border(Paragraph(['Hello', 'World !'])), Border(Paragraph(['Python rules !']))])
        self.assertEqual(
            '+----------------+\n'
            '| Hello          |\n'
            '| World !        |\n'
            '+----------------+\n'
            '+----------------+\n'
            '| Python rules ! |\n'
            '+----------------+\n',
            str(model.render()))

    def test_HBox(self):
        model = HBox([Paragraph(['Hello', 'World !']), Paragraph(['Python rules !'])])
        self.assertEqual(
            'Hello  Python rules !\n'
            'World !\n',
            str(model.render()))
        self.assertEqual(Size(21, 2), model.preferred_size())

    def test_Border_WithoutTitle(self):
        model = Border(Paragraph(['Hello', 'World !']))
        self.assertEqual('+---------+\n| Hello   |\n| World ! |\n+---------+\n', str(model.render()))

    def test_Border_WithTitle(self):
        model = Border(Paragraph(['Hello', 'World !']), 'Tt')
        self.assertEqual('+- Tt ----+\n| Hello   |\n| World ! |\n+---------+\n', str(model.render()))

    def test_Border_Filler(self):
        self.maxDiff = None
        model = Border(Paragraph(['Hello', 'World !']))
        self.assertEqual(
            '+----------------+\n'
            '| Hello          |\n'
            '| World !        |\n'
            '|                |\n'
            '+----------------+\n'
            ,
            str(model.render(Hints(Size(18, 5)))))

    def test_Padding(self):
        self.maxDiff = None
        model = Padding(Paragraph(['Hello', 'World !']), Size(4, 1))
        self.assertEqual(
            '               \n'
            '    Hello      \n'
            '    World !    \n'
            '               \n'
            ,
            str(model.render()))

    def test_Padding_4(self):
        self.maxDiff = None
        model = Padding(Paragraph(['Hello', 'World !']), Size(4, 1), Size(1, 2))
        self.assertEqual(
            '            \n'
            '    Hello   \n'
            '    World ! \n'
            '            \n'
            '            \n'
            ,
            str(model.render()))

    def test_Padding_Origin(self):
        self.maxDiff = None
        paragraph = Paragraph(['Hello', 'World !'])
        padding = Padding(paragraph, Size(4, 1))
        raster = padding.render()
        self.assertEqual(Boundary(4, 1, 7, 2), raster.origin_bounds(paragraph))
        self.assertEqual(Boundary(0, 0, 15, 4), raster.origin_bounds(padding))

    def test_PaddingStacked(self):
        self.maxDiff = None
        model = VBox([
            Padding(Paragraph(['Hello', 'World !']), Size(4, 1)),
            Padding(Paragraph(['Hello', 'World !']), Size(4, 1))
        ])

        self.assertEqual(
            '               \n'
            '    Hello      \n'
            '    World !    \n'
            '               \n'
            '               \n'
            '    Hello      \n'
            '    World !    \n'
            '               \n'
            ,
            str(model.render()))

    def test_Links_Down(self):
        self.maxDiff = None
        w1 = Paragraph(['Hello', 'World !'])
        w2 = Paragraph(['Hello', 'World !'])
        model = Links(HBox([
            Padding(w1, Size(4, 1)),
            Padding(w2, Size(12, 3))
        ]), [(w1, w2)])

        self.assertEqual(
            '                                              \n'
            '    Hello  --------+                          \n'
            '    World !        |                          \n'
            '                   +-------Hello              \n'
            '                           World !            \n'
            '                                              \n'
            '                                              \n'
            '                                              \n'
            , str(model.render()))

    def test_Links_Up(self):
        w1 = Paragraph(['Hello', 'World !'])
        w2 = Paragraph(['Hello', 'World !'])
        model = Links(HBox([
            Padding(w1, Size(4, 4)),
            Padding(w2, Size(12, 1))
        ]), [(w1, w2)])

        self.assertEqual(
            '                                              \n'
            '                   +-------Hello              \n'
            '                   |       World !            \n'
            '                   |                          \n'
            '    Hello  --------+\n'
            '    World !    \n'
            '               \n'
            '               \n'
            '               \n'
            '               \n'
            , str(model.render()))

    def test_Links_Straight(self):
        w1 = Paragraph(['Hello', 'World !'])
        w2 = Paragraph(['Hello', 'World !'])
        model = Links(HBox([
            Padding(w1, Size(4, 2)),
            Padding(w2, Size(12, 1))
        ]), [(w1, w2)])

        self.assertEqual(
            '                                              \n'
            '                           Hello              \n'
            '    Hello  ----------------World !            \n'
            '    World !                                   \n'
            '               \n'
            '               \n'
            , str(model.render()))

    def test_Annotation(self):
        self.maxDiff = None
        w1 = Paragraph(['Hello', 'World !'])
        w2 = Paragraph(['Hello', 'World !'])
        model = Annotations(VBox([
            Padding(w1, Size(4, 4)),
            Padding(w2, Size(12, 1))
        ]), [(w2, '8080'), (w2, '  22')])

        self.assertEqual(Size(38, 14), model.preferred_size())

        self.assertEqual(
            '                                      \n'
            '                                      \n'
            '                                      \n'
            '                                      \n'
            '           Hello                      \n'
            '           World !                    \n'
            '                                      \n'
            '                                      \n'
            '                                      \n'
            '                                      \n'
            '                                      \n'
            '8080 ]------------ Hello              \n'
            '  22 ]------------ World !            \n'
            '                                      \n'
            , str(model.render())
        )


if __name__ == '__main__':
    unittest.main()
