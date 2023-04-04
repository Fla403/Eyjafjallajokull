#!/usr/bin/env python3

import OpenGL.GL as GL
import numpy as np
import glfw
from core import Viewer, Shader
import texture, transform

def main():
    viewer = Viewer()
    print("! Shaders to implement !")
#    shader = Shader()

    #add all the objects of the scene
    print("! Objects to implement !")
#    viewer.add()

    #start rendering loop
    viewer.run()

if __name__ == '__main__':
    main()