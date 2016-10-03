from widget import VBox


class Renderer:
    def __init__(self):
        pass

    def render(self, config):
        box = VBox([])
        return str(box.render())
