#! /usr/bin/env python3

"""
    Script for terrain generation

    idée : une grille de points. En chaque point : calcul d'une hauteur
"""
import OpenGL.GL as GL
import numpy as np
from core import Mesh


def rand(x, z):
    return (0.5 * np.sin(np.dot((x, z), (12.9898, 78.233))*500) * 43758.5453) % 1


def terrainPoint(x, z):
    height =(np.exp(-(x*x + z*z)/500)*40
           + np.exp(-(x*x + z*z)/4500)*10
           - np.exp(-(x*x + z*z)/10)*50
           + np.exp(-((x+20)*(x+35) + (z+20)*(z+35))/100)*5
           + np.exp(-((x-25)*(x-25) + (z+25)*(z+25))/50)*10
           + np.exp(-((x-40)*(x-40) + (z+15)*(z+15))/100)*10
           + np.exp(-((x-45)*(x-45) + (z+30)*(z+30))/20)*10
           + np.exp(-((x+45)*(x+45) + (z-30)*(z-30))/20)*10
           + np.exp(-((x+40)*(x+40) + (z-35)*(z-35))/100)*5
           + np.exp(-((x+40)*(x+40) + (z)*(z))/100)*10
           + np.exp(-((x+38)*(x+38) + (z-20)*(z-20))/100)*10
           + np.exp(-((x+5)*(x+5) + (z-40)*(z-40))/150)*15
           + np.exp(-((x+25)*(x+25) + (z-35)*(z-35))/50)*12
           + np.exp(-((x+22)*(x+22) + (z-45)*(z-45))/10)*8
           + np.exp(-((x-22)*(x-22) + (z+45)*(z+45))/1000)*3
           + 0.2*rand(x, z)
           - 2)
    # if(x*x + z*z >= 12000):
    #     # height += rand(x, z)
    #     height -= 15
    if(height >= 18):
        height += 0.8*rand(x, z)

    return height


def normalize(x, y, z):
    norm = np.sqrt(x * x + y * y + z * z)
    return np.array((x / norm, y / norm, z / norm))


class Terrain(Mesh):
    """Class for drawing a terrain"""

    def __init__(self, shader, lightDir):
        sizeMesh = 271
        scale = .75
        
        # We need only an odd amount of points on a side
        if sizeMesh % 2 == 0:
            sizeMesh += 1

        symSizeMesh = sizeMesh // 2


        # Position creation
        position = []
        for i in range(-symSizeMesh, symSizeMesh + 1):
            for j in range(-symSizeMesh, symSizeMesh + 1):
                position.append(np.array([i * scale, terrainPoint(i * scale, j * scale), j * scale], dtype='f'))
        # print(position)

        normal = []
        for i in range(len(position) - sizeMesh - 1):
            v1 = position[i + 1] - position[i]
            v2 = position[i + 1 + sizeMesh] - position[i]
            norm = -np.cross(v1, v2)
            norm = normalize(norm[0], norm[1], norm[2])
            normal.append(np.array(norm, dtype='f'))

            # v3 = position[i+sizeMesh] - position[i+1+sizeMesh]
            # v4 = position[i+1] - position[i+1+sizeMesh]
            # norm2 = -np.cross(v3, v4)
            # norm2 = normalize(norm2[0], norm2[1], norm[2])
            # normal.append(np.array(norm2, 'f'))

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

        # self.color = (.3, .3, .3)

        color = []
        for i in range(-symSizeMesh, symSizeMesh + 1):
            for j in range(-symSizeMesh, symSizeMesh + 1):
                color.append(np.array([.3, .3, .3], dtype='f'))
        
        attributes = dict(position=position, color=color, normal=normal)

        uniforms = dict(
            k_d=('COLOR_DIFFUSE', (1, 1, 1)),
            k_s=('COLOR_SPECULAR', (1, 1, 1)),
            k_a=('COLOR_AMBIENT', (0.5, .5, .5)),
            s=('SHININESS', 16.),
        )
        super().__init__(shader, attributes=attributes, index=index, uniforms=uniforms, light=lightDir)

    def draw(self, **_args):
        GL.glEnable(GL.GL_DEPTH_TEST)
        super().draw(**_args)
