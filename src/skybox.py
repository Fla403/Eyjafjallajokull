import OpenGL.GL as GL
from itertools import cycle
import numpy as np
from core import Mesh
from texture import Texture, Textured


class SkyboxSide(Textured):
    """ Creates a side of the skybox """

    def __init__(self, shader, tex_file, position):
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

        scaled = 100000 * np.array(base_coords, np.float32)
        indices = np.array((0, 1, 2, 0, 2, 3), np.uint32)
        mesh = Mesh(shader, attributes=dict(position=scaled, tex_coord=coord_for_tex), index=indices)

        # setup & upload texture to GPU, bind it to shader name 'diffuse_map'
        texture1 = Texture(tex_file, self.wrap, *self.filter)
        super().__init__(mesh, diffuse_map=texture1)