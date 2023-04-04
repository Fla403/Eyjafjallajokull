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
        self.shader = shader
        position = np.array(((0, 0, 0), (0, 0, 1), (1, 0, 0), (1, 0, 1)), 'f')
        color = np.array(((0, 1, 0), (0, 1, 0), (0, 0, 1), (0, 0, 1)), 'f')
        self.index = np.array((0, 1, 2, 2, 1, 3), np.uint32)

        attributes = dict(position=position, color=color)
        super().__init__(shader, attributes=attributes)

        self.glid = GL.glGenVertexArrays(1)  # create OpenGL vertex array id
        GL.glBindVertexArray(self.glid)      # activate to receive state below
        self.buffers = GL.glGenBuffers(3)    # create buffer for position attrib

        # create position attribute, send to GPU, declare type & per-vertex size
        loc = GL.glGetAttribLocation(shader.glid, 'position')
        GL.glEnableVertexAttribArray(loc)    # assign to position attribute
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, self.buffers[0])
        GL.glBufferData(GL.GL_ARRAY_BUFFER, position, GL.GL_STATIC_DRAW)
        GL.glVertexAttribPointer(loc, 3, GL.GL_FLOAT, False, 0, None)

        # create color attribute, send to GPU, declare type & per-vertex size
        loc = GL.glGetAttribLocation(shader.glid, 'color')
        GL.glEnableVertexAttribArray(loc)    # assign to color
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, self.buffers[1])
        GL.glBufferData(GL.GL_ARRAY_BUFFER, color, GL.GL_STATIC_DRAW)
        GL.glVertexAttribPointer(loc, 3, GL.GL_FLOAT, False, 0, None)

        # create a dedicated index buffer, copy python array to GPU
        GL.glBindBuffer(GL.GL_ELEMENT_ARRAY_BUFFER, self.buffers[2])
        GL.glBufferData(GL.GL_ELEMENT_ARRAY_BUFFER, self.index,
                        GL.GL_STATIC_DRAW)
        
    def draw(self, projection, view, **_args):
        GL.glUseProgram(self.shader.glid)

        loc = GL.glGetUniformLocation(self.shader.glid, 'view')
        GL.glUniformMatrix4fv(loc, 1, True, view)

        loc = GL.glGetUniformLocation(self.shader.glid, 'projection')
        GL.glUniformMatrix4fv(loc, 1, True, projection)

        # draw triangle as GL_TRIANGLE indexed mode array, pass array size
        GL.glBindVertexArray(self.glid)
        GL.glDrawElements(GL.GL_TRIANGLES, self.index.size,
                          GL.GL_UNSIGNED_INT, None)

    # def __del__(self):
    #     GL.glDeleteVertexArrays(1, [self.glid])
    #     GL.glDeleteBuffers(3, self.buffers)
        
