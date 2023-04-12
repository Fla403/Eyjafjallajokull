#!/usr/bin/env python3

from core import Viewer, Shader
from ocean import *
import GenerateTerrain


def main():
    viewer = Viewer()
    # creation of the shaders
    oceanShader = Shader("ocean.vert", "ocean.frag")
    terrainShader = Shader("terrain.vert", "terrain.frag")

    # creation of the light direction
    lightDir = (0, -1, 0)

    # add all the objects of the scene
    viewer.add(Ocean(oceanShader, 251, lightDir))
    viewer.add(GenerateTerrain.Terrain(terrainShader))

    # start rendering loop
    viewer.run()


if __name__ == '__main__':
    main()
