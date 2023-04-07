import OpenGL.GL as GL
from core import Mesh
import numpy as np


class Ocean(Mesh):
    def __init__(self, shader):
        sizeMesh = 121
        #We need only an odd amount of points on a side
        if sizeMesh%2 == 0:
            sizeMesh+=1

        symSizeMesh = sizeMesh//2

        scale = 1

        # Position creation
        position = []
        for i in range(-symSizeMesh, symSizeMesh+1):
            for j in range(-symSizeMesh, symSizeMesh+1):
                position.append(np.array([i*scale, 0, j*scale], dtype='f'))
        print(position)


        # Index creation
        index = []
        for k in range(sizeMesh-1):
            for l in range(sizeMesh - 1):
                index.append(np.array(k*sizeMesh+l, dtype=np.uint32))
                index.append(np.array(k*sizeMesh+l+1, dtype=np.uint32))
                index.append(np.array(k*sizeMesh+l+sizeMesh+1, dtype=np.uint32))

                index.append(np.array(k*sizeMesh+l, dtype=np.uint32))
                index.append(np.array(k*sizeMesh+l+sizeMesh+1, dtype=np.uint32))
                index.append(np.array(k*sizeMesh+l+sizeMesh, dtype=np.uint32))

        #index = np.array((0, 1, 4, 0, 4, 3, 1, 2, 5, 1, 5, 4, 3, 4, 7, 3, 7, 6, 4, 5, 8, 4, 8, 7), np.uint32)

        self.color = (.2, .2, 1)
        attributes = dict(position=position)
        super().__init__(shader, attributes=attributes, index=index, global_color=self.color)

    def draw(self, **_args):
        super().draw(**_args)
