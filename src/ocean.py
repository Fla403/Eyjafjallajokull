import OpenGL.GL as GL
import glfw

from core import Mesh
import numpy as np


class Ocean(Mesh):
    def __init__(self, shader, sizeMesh, lightDir):

        # Parameters of the ocean
        scale = 1
        heightOffset = 1


        # We need only an odd amount of points on a side
        if sizeMesh % 2 == 0:
            sizeMesh += 1

        symSizeMesh = sizeMesh // 2


        # Position creation
        position = []
        for i in range(-symSizeMesh, symSizeMesh + 1):
            for j in range(-symSizeMesh, symSizeMesh + 1):
                position.append(np.array([i * scale, heightOffset, j * scale], dtype='f'))
        print(position)

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
        print(attributes)
        super().__init__(shader, attributes=attributes, index=index, global_color=self.color, time=0.0, light=lightDir, k_d=(0.0000, 0.6000, 0.6000), k_a=(0.0000, 0.2000, 0.2000), k_s=(0.8, 0.8, 0.8), s=100.0000)

    def draw(self, **_args):
        super().draw(**_args, time=glfw.get_time())
