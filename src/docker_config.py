from typing import List

from docker import Client


class Container:
    def __init__(self, name: str, status: str, networks: List[str]):
        self.name = name
        self.status = status
        self.networks = networks

    def __str__(self):
        return '%s - %s - %s' % (self.name, self.status, self.networks)


class Configuration:
    def __init__(self, containers: List[Container]):
        self.containers = containers

    def __str__(self):
        return str([str(c) for c in self.containers])


class ConfigParser:
    def __init__(self):
        self._client = Client()

    def get_configuration(self) -> Configuration:
        containers = []

        for cinfo in self._client.containers():
            name = cinfo['Names'][0]
            status = cinfo['State']
            networks = [n for n in cinfo['NetworkSettings']['Networks'].keys()]
            containers.append(Container(name, status, networks))

        return Configuration(containers)
