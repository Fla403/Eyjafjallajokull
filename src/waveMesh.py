import OpenGL.GL as GL
import glfw

from core import Mesh
import numpy as np


class WaveMesh(Mesh):
    def __init__(self, shader, sizeMesh, lightDir,
                 heightOffset=8.5,
                 scale=1,
                 kD=(0.0000, 0.6000, 0.6000),
                 kA=(0.0000, 0.2000, 0.2000),
                 kS=(0.8, 0.8, 0.8),
                 s=100.0000):

        # An odd number of points is more convenient for our calculation
        if sizeMesh % 2 == 0:
            sizeMesh += 1

        symSizeMesh = sizeMesh // 2

        # Position creation
        position = []
        for i in range(-symSizeMesh, symSizeMesh + 1):
            for j in range(-symSizeMesh, symSizeMesh + 1):
                position.append(np.array([i * scale, heightOffset, j * scale], dtype='f'))

        # Index creation
        index = []
        for k in range(sizeMesh - 1):
            for l in range(sizeMesh - 1):
                index.append(np.array(k * sizeMesh + l, dtype=np.uint32))
                index.append(np.array(k * sizeMesh + l + 1, dtype=np.uint32))
                index.append(np.array(k * sizeMesh + l + sizeMesh + 1, dtype=np.uint32))

                index.append(np.array(k * sizeMesh + l, dtype=np.uint32))
                index.append(np.array(k * sizeMesh + l + sizeMesh + 1, dtype=np.uint32))
                index.append(np.array(k * sizeMesh + l + sizeMesh, dtype=np.uint32))

        self.color = (.2, .2, 1)
        attributes = dict(position=position)
        super().__init__(shader, attributes=attributes, index=index, global_color=self.color, time=0.0, light=lightDir,
                         k_d=kD, k_a=kA, k_s=kS, s=s)

    def draw(self, **_args):
        GL.glEnable(GL.GL_DEPTH_TEST)
        super().draw(**_args, time=glfw.get_time())
