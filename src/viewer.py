#!/usr/bin/env python3

from core import Viewer, Shader
import ocean

def main():
    viewer = Viewer()
    print("! Shaders to implement !")
    oceanShader = Shader("ocean.vert", "ocean.frag")

    #add all the objects of the scene
    print("! Objects to implement !")
    viewer.add(ocean(oceanShader))

    #start rendering loop
    viewer.run()

if __name__ == '__main__':
    main()