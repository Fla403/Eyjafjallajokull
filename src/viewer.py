#!/usr/bin/env python3

from core import Viewer, Shader
from ocean import *
import GenerateTerrain
from playsound import playsound
from craby import Craby
from texture import Texture, Textured
from itertools import cycle


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

    viewer.add(Ocean(oceanShader, 551, lightDir))
    viewer.add(GenerateTerrain.Terrain(terrainShader))

    """sphere = Sphere(crabyShader, 3, (0.2,0.2,0.2))
    node = Node(transform=scale(0.1,0.1,0.1))
    node.add(sphere)
    viewer.add(node)"""

    craby = Craby()
    viewer.add(craby)

    # start rendering loop
    viewer.run()


if __name__ == '__main__':
    playsound("CrabRave.mp3", False)
    main()
