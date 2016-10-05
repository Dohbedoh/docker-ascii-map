from widget import *
from docker_config import Configuration


class Renderer:
    def __init__(self):
        pass

    def render(self, config: Configuration):
        root_widgets = []

        networks = set()

        for container in config.containers:
            for net in container.networks:
                networks.add(net)

        for net in networks:
            net_widgets = []

            for container in config.containers:
                lines = []

                if container.status == 'running':
                    statuschar = u"\u2713"
                else:
                    statuschar = u"\u274c"

                lines.append('[' + statuschar + '] ' + container.name)
                lines.append('    ' + container.image)
                net_widgets.append(Paragraph(lines))

            root_widgets.append(Border(VBox(net_widgets), net))

        root_box = VBox(root_widgets)
        return str(root_box.render())
