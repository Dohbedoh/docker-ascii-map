import unittest

from docker_config import *
from ascii_render import Renderer


class RenderingTests(unittest.TestCase):
    def test_renderer(self):
        config = Configuration([])
        renderer = Renderer()

        self.assertEqual('', renderer.render(config))

    def test_simple_config(self):
        config = Configuration([
            Container('n1', 'running', ['net1'], 'im'),
            Container('n2', 'running', ['net2'], 'im'),
        ])
        renderer = Renderer()

        self.assertEqual('+- net1 -+\n| [✓] n1 |\n|     im |\n+--------+\n+- net2 -+\n| [✓] n2 |\n|     im |\n+--------+\n', renderer.render(config))


if __name__ == '__main__':
    unittest.main()
