import unittest

from ascii_render import Renderer
from docker_config import *


class RenderingTests(unittest.TestCase):
    def test_renderer(self):
        config = Configuration([])
        renderer = Renderer()

        self.assertEqual('', renderer.render(config))

    def test_simple_config(self):
        config = Configuration([
            Container('n1', 'running', ['net1'], 'group1/image-long-name', []),
            Container('n2', 'stopped', ['net2'], 'group2/image-short', []),
        ])
        renderer = Renderer()

        self.assertEqual(
            '+- net1 ---------------------+\n'
            '| [✓] n1                     |\n'
            '|     group1/image-long-name |\n'
            '+----------------------------+\n'
            '+- net2 ---------------------+\n'
            '| [❌] n2                     |\n'
            '|     group2/image-short     |\n'
            '+----------------------------+\n',
            renderer.render(config))

    def test_dual_net_config(self):
        self.maxDiff = None
        config = Configuration([
            Container('n1', 'running', ['net1'], 'im', []),
            Container('n2', 'running', ['net2'], 'im', []),
            Container('n-front', 'running', ['net1', 'net2'], 'httpd:2.4', []),
        ])
        renderer = Renderer()

        text = renderer.render(config)
        # print(text)

        self.assertEqual(
            '                                       +- net1 -+\n'
            '                                       | [✓] n1 |\n'
            '             [✓] n-front         +-----|     im |\n'
            '                 httpd:2.4 ------+     +--------+\n'
            '                                 |     +- net2 -+\n'
            '                                 |     | [✓] n2 |\n'
            '                                 +-----|     im |\n'
            '                                       +--------+\n'
            , text)

    def test_port_map(self):
        self.maxDiff = None
        config = Configuration([
            Container('n1', 'running', ['net1'], 'im', []),
            Container('n2', 'running', ['net2'], 'im', [PortMapping(private_port=8080, public_port=80)]),
        ])
        renderer = Renderer()

        text = renderer.render(config)
        print(text)

        # self.assertEqual(
        #     '                                       +- net1 -+\n'
        #     '                                       | [✓] n1 |\n'
        #     '             [✓] n-front         +-----|     im |\n'
        #     '                 httpd:2.4 ------+     +--------+\n'
        #     '                                 |     +- net2 -+\n'
        #     '                                 |     | [✓] n2 |\n'
        #     '                                 +-----|     im |\n'
        #     '                                       +--------+\n'
        #     , text)


if __name__ == '__main__':
    unittest.main()
