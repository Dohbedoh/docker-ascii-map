from ascii_render import Renderer
from docker_config import ConfigParser

if __name__ == '__main__':
    parser = ConfigParser()
    renderer = Renderer()

    config = parser.get_configuration()
    text = renderer.render(config)
    print(text)
