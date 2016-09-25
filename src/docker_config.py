from docker import Client


class ConfigParser:
    def __init__(self):
        self._client = Client()

    def get_configuration(self):
        self._client.info()
        return []
