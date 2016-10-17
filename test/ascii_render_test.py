import unittest

from docker_ascii_map.docker_config import *

from docker_ascii_map.ascii_render import Renderer


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

    def test_ascii_fallback(self):
        config = Configuration([
            Container('n1', 'running', ['net1'], 'group1/image-long-name', []),
            Container('n2', 'stopped', ['net2'], 'group2/image-short', []),
        ])
        renderer = Renderer()

        self.assertEqual(
            '+- net1 ---------------------+\n'
            '| [V] n1                     |\n'
            '|     group1/image-long-name |\n'
            '+----------------------------+\n'
            '+- net2 ---------------------+\n'
            '| [x] n2                     |\n'
            '|     group2/image-short     |\n'
            '+----------------------------+\n',
            renderer.render(config, 'ascii'))

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
            '             [✓] n-front   ------+-----|     im |\n'
            '                 httpd:2.4       |     +--------+\n'
            '                                 |     +- net2 -+\n'
            '                                 +-----| [✓] n2 |\n'
            '                                       |     im |\n'
            '                                       +--------+\n'
            , text)

    def test_dual_net_sort(self):
        self.maxDiff = None
        config = Configuration([
            Container('n1', 'running', ['net1'], 'im', []),
            Container('n2', 'running', ['net2'], 'im', []),
            Container('n3', 'running', ['net3'], 'im', []),
            Container('n-front', 'running', ['net1', 'net3'], 'httpd:2.4', []),
        ])
        renderer = Renderer()

        text = renderer.render(config)
        # print(text)

        self.assertEqual(
            '                                       +- net1 -+\n'
            '                                       | [✓] n1 |\n'
            '             [✓] n-front   ------+-----|     im |\n'
            '                 httpd:2.4       |     +--------+\n'
            '                                 |     +- net3 -+\n'
            '                                 +-----| [✓] n3 |\n'
            '                                       |     im |\n'
            '                                       +--------+\n'
            '                                       +- net2 -+\n'
            '                                       | [✓] n2 |\n'
            '                                       |     im |\n'
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
        # print(text)

        self.assertEqual(
            '     +- net1 -+\n'
            '     | [✓] n1 |\n'
            '     |     im |\n'
            '     +--------+\n'
            '     +- net2 -+\n'
            '80 ]-+ [✓] n2 |\n'
            '     |     im |\n'
            '     +--------+\n'
            , text)

    def test_port_map_multiple(self):
        self.maxDiff = None
        config = Configuration([
            Container('n1', 'running', ['net1'], 'im',
                      [PortMapping(private_port=22, public_port=99)]),
            Container('n2', 'running', ['net2'], 'im',
                      [
                          PortMapping(private_port=8080, public_port=80),
                          PortMapping(private_port=22, public_port=22),
                          PortMapping(private_port=25, public_port=25),
                      ]),
        ])
        renderer = Renderer()

        text = renderer.render(config)
        # print(text)

        self.assertEqual(
            '     +- net1 -+\n'
            '99 ]-+ [✓] n1 |\n'
            '     |     im |\n'
            '     +--------+\n'
            '     +- net2 -+\n'
            '80 ]-+ [✓] n2 |\n'
            '22 ]-+     im |\n'
            '25 ]-+--------+\n'
            , text)


if __name__ == '__main__':
    unittest.main()
