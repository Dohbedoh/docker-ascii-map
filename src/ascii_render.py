from docker_config import Configuration, Container
from widget import *


def build_container_widget(container: Container) -> Widget:
    lines = []
    if container.status == 'running':
        statuschar = u"\u2713"
    else:
        statuschar = u"\u274c"
    lines.append('[' + statuschar + '] ' + container.name)
    lines.append('    ' + container.image)
    container_widget = Paragraph(lines)
    return container_widget


class Renderer:
    def __init__(self):
        pass

    def render(self, config: Configuration):
        network_widgets = []

        networks = set()

        for container in config.containers:
            for net in container.networks:
                networks.add(net)

        networks = list(networks)
        networks.sort()

        for net in networks:
            net_widgets = []

            for container in config.containers:
                if [net] == container.networks:
                    container_widget = build_container_widget(container)
                    net_widgets.append(container_widget)

            network_widgets.append(Border(VBox(net_widgets), net))

        bridge_widgets = []

        for container in config.containers:
            if len(container.networks) > 1:
                container_widget = Padding(build_container_widget(container), Size(6, 2))
                bridge_widgets.append(container_widget)

        networks_box = VBox(network_widgets)
        bridges_box = VBox(bridge_widgets)
        root_box = HBox([bridges_box, networks_box])
        return str(root_box.render())
