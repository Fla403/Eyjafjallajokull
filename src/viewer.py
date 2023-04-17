#!/usr/bin/env python3

from core import Viewer, Shader, Node
from ocean import *
import GenerateTerrain
from playsound import playsound
from craby import Craby
from transform import translate, scale, identity, quaternion
from texture import Texture, Textured
from itertools import cycle
from keyFrames import KeyFrameControlNode



class TexturedPlane(Textured):
    """ Simple first textured object """

    def __init__(self, shader, tex_file, position):
        # prepare texture modes cycling variables for interactive toggling
        self.wraps = cycle([GL.GL_REPEAT, GL.GL_MIRRORED_REPEAT,
                            GL.GL_CLAMP_TO_BORDER, GL.GL_CLAMP_TO_EDGE])
        self.filters = cycle([(GL.GL_NEAREST, GL.GL_NEAREST),
                              (GL.GL_LINEAR, GL.GL_LINEAR),
                              (GL.GL_LINEAR, GL.GL_LINEAR_MIPMAP_LINEAR)])
        self.wrap, self.filter = next(self.wraps), next(self.filters)
        self.file = tex_file

        # setup plane mesh to be textured
        if position == 1:
            base_coords = ((-1, -1, -1), (1, -1, -1), (1, 1, -1), (-1, 1, -1))  # Front
        elif position == 2:
            base_coords = ((1, -1, 1), (-1, -1, 1), (-1, 1, 1), (1, 1, 1))  # Back
        elif position == 3:
            base_coords = ((-1, 1, -1), (-1, 1, 1), (-1, -1, 1), (-1, -1, -1))  # Left
        elif position == 4:
            base_coords = ((1, -1, -1), (1, -1, 1), (1, 1, 1), (1, 1, -1))  # Right
        elif position == 5:
            base_coords = ((-1, -1, 1), (1, -1, 1), (1, -1, -1), (-1, -1, -1))  # Bottom
        else:
            base_coords = ((-1, 1, -1), (1, 1, -1), (1, 1, 1), (-1, 1, 1))  # Top

        coord_for_tex = ((0, 0), (0, 1), (1, 1), (1, 0))

        scaled = 1000 * np.array(base_coords, np.float32)
        indices = np.array((0, 1, 2, 0, 2, 3), np.uint32)
        mesh = Mesh(shader, attributes=dict(position=scaled, tex_coord=coord_for_tex), index=indices)

        # setup & upload texture to GPU, bind it to shader name 'diffuse_map'
        texture1 = Texture(tex_file, self.wrap, *self.filter)
        super().__init__(mesh, diffuse_map=texture1)


def vec(*iterable):
    """ shortcut to make numpy vector of any iterable(tuple...) or vector """
    return np.asarray(iterable if len(iterable) > 1 else iterable[0], 'f')

def main():
    viewer = Viewer()
    # creation of the shaders
    oceanShader = Shader("ocean.vert", "ocean.frag")
    terrainShader = Shader("terrain.vert", "terrain.frag")
    crabyShader = Shader("color.vert", "color.frag")

    skyboxShader = Shader("skybox.vert", "skybox.frag")

    # creation of the light direction
    lightDir = (-1, -1, 2)
    # add all the objects of the scene
    viewer.add(TexturedPlane(skyboxShader, "skybox/front.jpg", 1))
    viewer.add(TexturedPlane(skyboxShader, "skybox/back.png", 2))
    viewer.add(TexturedPlane(skyboxShader, "skybox/left.png", 3))
    viewer.add(TexturedPlane(skyboxShader, "skybox/right.png", 4))
    viewer.add(TexturedPlane(skyboxShader, "skybox/bottom.png", 5))
    viewer.add(TexturedPlane(skyboxShader, "skybox/top.png", 6))

    #viewer.add(Ocean(oceanShader, 551, lightDir))
    #viewer.add(GenerateTerrain.Terrain(terrainShader))

    """sphere = Sphere(crabyShader, 3, (0.2,0.2,0.2))
    node = Node(transform=scale(0.1,0.1,0.1))
    node.add(sphere)
    viewer.add(node)"""

    craby = Craby()
    #crabyNode = Node(transform=translate(40,10,50) @ scale(5))
    #crabyNode.add(craby)
    #viewer.add(crabyNode)

    translate_keys = {0: vec(0,0,0),
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

    # start rendering loop
    viewer.run()


if __name__ == '__main__':
    #playsound("CrabRave.mp3", False)
    main()
