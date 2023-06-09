#!/usr/bin/env python3

from core import Viewer, Shader, Node
# from playsound import playsound

import generateTerrain
from skybox import SkyboxSide
from waveMesh import WaveMesh
from craby import Craby
from rocks import Rocks
from transform import translate, scale


def main():
    # creation of the viewer
    viewer = Viewer()

    # creation of the light direction
    lightDir = (0, -1, 3)

    # creation of the shaders
    skyboxShader = Shader("skybox.vert", "skybox.frag")
    oceanShader = Shader("oceanOpti.vert", "oceanOpti.frag")  # ocean or oceanOpti can be used for two different color implementation
    lavaShader = Shader("lava.vert", "lava.frag")
    terrainShader = Shader("terrain.vert", "terrain.frag")
    rocksShader = Shader("rocks.vert", "rocks.frag")

    # add all the objects of the scene
    viewer.add(SkyboxSide(skyboxShader, "skyboxSunset/front.png", 1))
    viewer.add(SkyboxSide(skyboxShader, "skyboxSunset/back.png", 2))
    viewer.add(SkyboxSide(skyboxShader, "skyboxSunset/left.png", 3))
    viewer.add(SkyboxSide(skyboxShader, "skyboxSunset/right.png", 4))
    viewer.add(SkyboxSide(skyboxShader, "skyboxSunset/bottom.png", 5))
    viewer.add(SkyboxSide(skyboxShader, "skyboxSunset/top.png", 6))

    viewer.add(WaveMesh(oceanShader, 551, lightDir))

    viewer.add(WaveMesh(lavaShader, 67, lightDir, heightOffset=44, scale=0.2, kD=(0.92, 0.26, 0), kA=(0.7, 0.3, 0), kS=(0.9, 0.35, 0.35), s=1.5))

    viewer.add(generateTerrain.Terrain(terrainShader, lightDir))

    for i in range(100):
        viewer.add(Rocks(rocksShader, lightDir, subdivisions=1))
        viewer.add(Rocks(rocksShader, lightDir, kD=(0.5, 0.1, 0.1), kA=(0.2, 0.2, 0.2), kS=(0.3, 0.1, 0.1)))

    craby = Craby()
    crabyNode = Node(transform=translate(28, 8, 58) @ scale(5))
    crabyNode.add(craby)
    viewer.add(crabyNode)

    # Keyboard control for Craby
    print("\nKeyboard control for Craby :")
    print("\nw : forward")
    print("x : move backwards")
    print("q : move to the left")
    print("d : move to the right")
    print("left arrow : turn to the left")
    print("right arrow : turn to the right")
    print("up arrow : jump")
    print("arrow down : change the face")
    print("1 (numeric keypad) : lower the left claw")
    print("7 (numeric keypad) : raise left claw")
    print("4 (numeric keypad) : close/open the left claw")
    print("3 (numeric keypad) : lower the right claw")
    print("9 (numeric keypad) : raise right claw")
    print("6 (numeric keypad) : close/open the right claw")

    # start rendering loop
    viewer.run()


if __name__ == '__main__':
    # playsound("CrabRave.mp3", False)
    main()
