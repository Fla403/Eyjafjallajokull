#!/usr/bin/env python3

from core import Viewer, Shader
from ocean import *


def main():
    viewer = Viewer()
    # creation of the shaders
    oceanShader = Shader("ocean.vert", "ocean.frag")

    # add all the objects of the scene
    viewer.add(Ocean(oceanShader))

    # start rendering loop
    viewer.run()


if __name__ == '__main__':
    main()
