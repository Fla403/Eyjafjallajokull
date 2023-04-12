#!/usr/bin/env python3

from core import Viewer, Shader
from ocean import *
import GenerateTerrain
from sphere import *
from craby import *

import sys                          # for system arguments

# External, non built-in modules
import OpenGL.GL as GL              # standard Python OpenGL wrapper
import numpy as np                  # all matrix manipulations & OpenGL args
import glfw                         # lean window system wrapper for OpenGL

from core import Shader, Mesh, Viewer, Node, load
from transform import translate, identity, rotate, scale
from craby import *
from sphere import *

class Cylinder(Node):
    """ Very simple cylinder based on provided load function """
    def __init__(self, shader):
        super().__init__()
        self.add(*load('cylinder.obj', shader))  # just load cylinder from file

def main():
    viewer = Viewer()
    # creation of the shaders
    """oceanShader = Shader("ocean.vert", "ocean.frag")
    terrainShader = Shader("terrain.vert", "terrain.frag")"""
    crabyShader = Shader("color.vert", "color.frag")
    
    # add all the objects of the scene
    light_dir = (0, -1, 0)
    """viewer.add(Ocean(oceanShader))
    viewer.add(GenerateTerrain.Terrain(terrainShader))"""

    """sphere = Sphere(crabyShader, 3, (0.2,0.2,0.2))
    node = Node(transform=scale(0.1,0.1,0.1))
    node.add(sphere)
    viewer.add(node)"""

    craby = Craby()
    viewer.add(craby)

    # start rendering loop
    viewer.run()


if __name__ == '__main__':
    main()
