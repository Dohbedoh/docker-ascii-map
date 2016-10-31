import unittest
from argparse import ArgumentParser
from unittest.mock import patch

import docker_ascii_map.argument_parser


class Args:
    def __init__(self, mono=None, color=None):
        self.mono = mono
        self.color = color


class ParametersTests(unittest.TestCase):
    def test_monoterm(self):
        with patch('os.getenv', return_value='vt100') as mock_getenv:
            with patch.object(ArgumentParser, 'parse_args', return_value=Args()) as mock_parse:
                r = docker_ascii_map.argument_parser.get_input_parameters()
                self.assertEqual(False, r[0])

    def test_colorterm(self):
        with patch('os.getenv', return_value='xterm-256color') as mock_getenv:
            with patch.object(ArgumentParser, 'parse_args', return_value=Args()) as mock_parse:
                r = docker_ascii_map.argument_parser.get_input_parameters()
                self.assertEqual(True, r[0])


if __name__ == '__main__':
    unittest.main()
