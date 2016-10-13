from typing import List

from docker import Client


class PortMapping:
    def __init__(self, private_port, public_port):
        self.private_port = private_port
        self.public_port = public_port

    def __repr__(self):
        return '%d:%d' % (self.public_port, self.private_port)


class Container:
    def __init__(self, name: str, status: str, networks: List[str], image: str, ports: List[PortMapping]):
        self.name = name
        self.status = status
        self.networks = networks
        self.image = image
        self.ports = ports

    def __str__(self) -> str:
        return '%s - %s - %s %s' % (self.name, self.status, self.networks, self.ports)


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

        for cinfo in self._client.containers(all=True):
            name = cinfo['Names'][0]
            status = cinfo['State']
            image = cinfo['Image']
            networks = [n for n in cinfo['NetworkSettings']['Networks'].keys()]
            ports = [PortMapping(p['PrivatePort'], p['PublicPort']) for p in cinfo['Ports']]
            containers.append(Container(name, status, networks, image, ports))

        return Configuration(containers)
