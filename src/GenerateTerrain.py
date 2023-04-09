#! /usr/bin/env python3

"""
    Script for terrain generation

    idée : une grille de points. En chaque point : calcul d'une hauteur
"""
import OpenGL.GL as GL
import glfw    
import numpy as np
import core


class Terrain(core.Mesh):
    """Class for drawing a terrain"""

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
        # print(position)


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

        self.color = (.3, .3, .3)
        attributes = dict(position=position)

        uniforms = dict(
            k_d=('COLOR_DIFFUSE', (1, 1, 1)),
            k_s=('COLOR_SPECULAR', (1, 1, 1)),
            k_a=('COLOR_AMBIENT', (0, 0, 0)),
            s=('SHININESS', 16.),
        )
        super().__init__(shader, attributes=attributes, index=index, global_color=self.color, uniforms=uniforms)

    def draw(self, **_args):
        super().draw(**_args)
        
