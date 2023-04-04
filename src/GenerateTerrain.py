#! /usr/bin/env python3

"""
    Script for terrain generation

    idée : une grille de points. En chaque point : calcul d'une hauteur
"""
import numpy as np
import core


class Terrain(core.Mesh):
    """Class for drawing a terrain"""

    def __init__(self, shader):
        self.shader = shader
        position = np.array()
        color = np.array()
        
