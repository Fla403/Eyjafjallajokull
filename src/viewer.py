#!/usr/bin/env python3

from core import Viewer, Shader
import ocean
import GenerateTerrain

def main():
    viewer = Viewer()
    print("! Shaders to implement !")
    oceanShader = Shader("ocean.vert", "ocean.frag")
    terrainShader = Shader("terrain.vert", "terrain.frag")

    #add all the objects of the scene
    print("! Objects to implement !")
    # viewer.add(ocean(oceanShader))
    viewer.add(GenerateTerrain.Terrain(terrainShader))

    #start rendering loop
    viewer.run()

if __name__ == '__main__':
    main()