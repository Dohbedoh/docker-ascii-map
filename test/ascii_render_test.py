import unittest

from docker_config import *
from ascii_render import Renderer


class RenderingTests(unittest.TestCase):
    def test_renderer(self):
        config = Configuration([])
        renderer = Renderer()

        self.assertEqual('', renderer.render(config))


if __name__ == '__main__':
    unittest.main()
