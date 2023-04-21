#!/usr/bin/env python3

from core import Viewer, Shader, Node
#from playsound import playsound

import GenerateTerrain
from skybox import SkyboxSide
from waveMesh import WaveMesh
from craby import Craby
from rocks import Rocks
from transform import translate, scale, identity, quaternion
from keyFrames import KeyFrameControlNode
from sphere import Sphere




def main():

    # creation of the viewer
    viewer = Viewer()

    # creation of the light direction
    lightDir = (0, -1, 3)

    # creation of the shaders
    skyboxShader = Shader("skybox.vert", "skybox.frag")
    oceanShader = Shader("oceanOpti.vert", "oceanOpti.frag")  #ocean or oceanOpti can be used for two different color implementation
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

    viewer.add(GenerateTerrain.Terrain(terrainShader, lightDir))

    """sphere = Sphere(crabyShader, 6, (0.2,0.8,0.2))
    node = Node(transform=scale(10))
    node.add(sphere)
    viewer.add(node)"""

    for i in range (200):
        viewer.add(Rocks(rocksShader, lightDir))
        viewer.add(Rocks(rocksShader, lightDir, kD=(0.5, 0.1, 0.1), kA=(0.2, 0.2, 0.2), kS=(0.3, 0.1, 0.1)))

    craby = Craby()
    crabyNode = Node(transform=translate(28,8,58)@scale(5))
    crabyNode.add(craby)
    viewer.add(crabyNode)

    """translate_keys = {0: vec(0,0,0),
                        20: vec(0,5,0),
                        24: vec(0,10,0),
                        26: vec(0,15,0),
                        28: vec(0,20,0),
                        30: vec(0,25,0)}
    rotate_keys = {0: quaternion(),
                        10: quaternion()}
    scale_keys = {0: vec(1,1,1),
                        10: vec(1,1,1)}

    crabyAnimatedNode = KeyFrameControlNode(translate_keys, rotate_keys, scale_keys)
    crabyAnimatedNode.add(craby)
    viewer.add(crabyAnimatedNode)

    crabyAnimatedNode.addTranslate(40, vec(0,0,0))"""

    # start rendering loop
    viewer.run()


if __name__ == '__main__':
    #playsound("CrabRave.mp3", False)
    main()
