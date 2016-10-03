import unittest

from box_model import *


class ModelTests(unittest.TestCase):
    def test_rendering(self):
        model = Paragraph(['Hello', 'World !'])
        self.assertEqual('Hello\nWorld !\n', str(model.render()))

        model = VBox([Paragraph(['Hello', 'World !'])])
        self.assertEqual('Hello\nWorld !\n', str(model.render()))

        model = Border(Paragraph(['Hello', 'World !']))
        self.assertEqual('+---------+\n| Hello   |\n| World ! |\n+---------+\n', str(model.render()))


if __name__ == '__main__':
    unittest.main()
