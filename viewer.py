#!/usr/bin/env python3

import OpenGL.GL as GL
import numpy as np
import glfw
import core, texture, transform

def main():
    viewer = Viewer()
    shader = Shader()

    #add all the objects of the scene
    viewer.add()

    #start rendering loop
    viewer.run()

if __name__ == '__main__':
    main()