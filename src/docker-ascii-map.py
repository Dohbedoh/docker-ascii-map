#!/usr/bin/env python3
import sys

from ascii_render import Renderer
from docker_config import ConfigParser

if __name__ == '__main__':
    parser = ConfigParser()
    renderer = Renderer()

    config = parser.get_configuration()
    # print(config)
    text = renderer.render(config, sys.stdout.encoding)
    print(text)
