import unittest
from unittest.mock import patch

from docker import Client

from docker_ascii_map.docker_config import ConfigParser, PortMapping


class ConfigTests(unittest.TestCase):
    def test_portmapping(self):
        self.assertEqual('80:8080', str(PortMapping(private_port=8080, public_port=80)))

    def test_empty_config(self):
        with patch.object(Client, 'containers', return_value=[]) as mock_method:
            configuration_parser = ConfigParser()
            self.assertEqual([], configuration_parser.get_configuration().containers)

    def test_single_container(self):
        with patch.object(Client, 'containers', return_value=[
            {'Names': ['/im1'], 'State': 'running', 'Image': 'ubuntu:latest',
             'NetworkSettings': {'Networks': {}}, 'Ports': []}]) as mock_method:
            configuration_parser = ConfigParser()
            self.assertEqual('[\'im1 - running - [] []\']', str(configuration_parser.get_configuration()))

        mock_method.assert_called_once_with(all=True)
