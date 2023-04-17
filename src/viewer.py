#!/usr/bin/env python3

from core import Viewer, Shader, Node
from ocean import *
import GenerateTerrain
from playsound import playsound
from craby import Craby
from transform import translate


def main():

    viewer = Viewer()
    # creation of the shaders
    oceanShader = Shader("ocean.vert", "ocean.frag")
    terrainShader = Shader("terrain.vert", "terrain.frag")
    # skyboxShader = Shader("skybox.vert", "skybox.frag")
    crabyShader = Shader("color.vert", "color.frag")

    # creation of the light direction
    lightDir = (0, -1, 0)

    # add all the objects of the scene
    """viewer.add(Ocean(oceanShader, 251, lightDir))
    viewer.add(GenerateTerrain.Terrain(terrainShader))"""

    """sphere = Sphere(crabyShader, 3, (0.2,0.2,0.2))
    node = Node(transform=scale(0.1,0.1,0.1))
    node.add(sphere)
    viewer.add(node)"""

    craby = Craby()
    crabyNode = Node(transform=translate(40,5,50))
    crabyNode.add(craby)
    viewer.add(craby)

    # start rendering loop
    viewer.run()


if __name__ == '__main__':
    #playsound("CrabRave.mp3", False)
    main()
