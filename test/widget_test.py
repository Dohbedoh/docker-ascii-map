import unittest

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

    def test_geometry(self):
        geom = Geometry(0,1,2, 3)
        self.assertEqual(2, geom.width)
        self.assertEqual(3, geom.height)
        self.assertEqual(0, geom.x)
        self.assertEqual(1, geom.y)


    def test_paragraph(self):
        model = Paragraph(['Hello', 'World !'])
        self.assertEqual('Hello\nWorld !\n', str(model.render()))

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
        self.assertEqual('Hello  Python rules !\nWorld !\n', str(model.render()))
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
            '\n'
            '    Hello  \n'
            '    World !\n'
            ,
            str(model.render()))

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

    def test_Links(self):
        w1 = Paragraph(['Hello', 'World !'])
        w2 = Paragraph(['Hello', 'World !'])
        model = Links(HBox([
            Padding(w1, Size(4, 1)),
            Padding(w2, Size(12, 3))
        ]), {w1: w2})

        # print(str(model.render()))

        if __name__ == '__main__':
            unittest.main()
