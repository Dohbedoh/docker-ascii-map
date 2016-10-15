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

        net_widgets_map = {}

        for net in networks:
            net_widgets = []

            for container in config.containers:
                if [net] == container.networks:
                    container_widget = build_container_widget(container)
                    net_widgets.append(container_widget)

            net_box = Border(VBox(net_widgets), net)
            net_widgets_map[net] = net_box
            network_widgets.append(net_box)

        bridge_widgets = []
        links = []

        for container in config.containers:
            if len(container.networks) > 1:
                c = Padding(build_container_widget(container), Size(1,0))
                padded = Padding(c, Size(12, 2))
                bridge_widgets.append(padded)

                for n in container.networks:
                    net_box = net_widgets_map[n]
                    links.append((c, net_box))

        networks_box = VBox(network_widgets)
        bridges_box = VBox(bridge_widgets)
        links_box = Links(HBox([bridges_box, networks_box]), links)

        # Port mapping

        root_box = HBox([links_box])
        return str(root_box.render())
