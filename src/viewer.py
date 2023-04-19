#!/usr/bin/env python3

from core import Viewer, Shader
from playsound import playsound

import GenerateTerrain
from skybox import SkyboxSide
from waveMesh import WaveMesh
from craby import Craby
from rocks import Rocks


def main():

    # creation of the viewer
    viewer = Viewer()

    # creation of the light direction
    lightDir = (0, -1, 3)

    # creation of the shaders
    skyboxShader = Shader("skybox.vert", "skybox.frag")
    oceanShader = Shader("ocean.vert", "ocean.frag")
    lavaShader = Shader("lava.vert", "lava.frag")
    terrainShader = Shader("terrain.vert", "terrain.frag")
    crabyShader = Shader("color.vert", "color.frag")
    rocksShader = Shader("rocks.vert", "rocks.frag")

    # add all the objects of the scene
    viewer.add(SkyboxSide(skyboxShader, "skyboxSunset/front.png", 1))
    viewer.add(SkyboxSide(skyboxShader, "skyboxSunset/back.png", 2))
    viewer.add(SkyboxSide(skyboxShader, "skyboxSunset/left.png", 3))
    viewer.add(SkyboxSide(skyboxShader, "skyboxSunset/right.png", 4))
    viewer.add(SkyboxSide(skyboxShader, "skyboxSunset/bottom.png", 5))
    viewer.add(SkyboxSide(skyboxShader, "skyboxSunset/top.png", 6))

    viewer.add(WaveMesh(oceanShader, 1551, lightDir))

    viewer.add(WaveMesh(lavaShader, 67, lightDir, heightOffset=44, scale=0.2, kD=(0.92, 0.26, 0), kA=(0.7, 0.3, 0), kS=(0.9, 0.35, 0.35), s=1.5))

    viewer.add(GenerateTerrain.Terrain(terrainShader))

    viewer.add(Craby())
    """sphere = Sphere(crabyShader, 3, (0.2,0.2,0.2))
    node = Node(transform=scale(0.1,0.1,0.1))
    node.add(sphere)
    viewer.add(node)"""

    for i in range (100):
        viewer.add(Rocks(rocksShader, lightDir))
        viewer.add(Rocks(rocksShader, lightDir, kD=(0.5, 0.1, 0.1), kA=(0.2, 0.2, 0.2), kS=(0.3, 0.1, 0.1)))

    # start rendering loop
    viewer.run()


if __name__ == '__main__':
    playsound("CrabRave.mp3", False)
    main()
