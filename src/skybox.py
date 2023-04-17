from OpenGL.GL import *
from OpenGL.GLU import *
from PIL import Image
import numpy as np

class Skybox:

    def __init__(self):
        cubeMapTarget = [
            GL_TEXTURE_CUBE_MAP_NEGATIVE_X,
            GL_TEXTURE_CUBE_MAP_POSITIVE_X,
            GL_TEXTURE_CUBE_MAP_NEGATIVE_Y,
            GL_TEXTURE_CUBE_MAP_POSITIVE_Y,
            GL_TEXTURE_CUBE_MAP_NEGATIVE_Z,
            GL_TEXTURE_CUBE_MAP_POSITIVE_Z,
        ]

        textureImage = [Image.open("skybox/left.bmp"), Image.open("skybox/right.bmp"), Image.open("skybox/back.bmp"),
                        Image.open("skybox/front.bmp"), Image.open("skybox/bottom.bmp"), Image.open("skybox/top.bmp")]

        self.cubeMapTextureID = glGenTextures(1)

        glBindTexture(GL_TEXTURE_CUBE_MAP, self.cubeMapTextureID)

        for i in range(6):
            textureImage[i] = textureImage[i].convert("RGB")

            width, height = textureImage[i].size

            data = textureImage[i].tobytes()

            glTexImage2D(cubeMapTarget[i], 0, GL_RGB, width, height, 0, GL_RGB, GL_UNSIGNED_BYTE, data)

        glTexParameteri(GL_TEXTURE_CUBE_MAP, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_CUBE_MAP, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_CUBE_MAP, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
        glTexParameteri(GL_TEXTURE_CUBE_MAP, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)

    def draw(self, cameraPitch, cameraYaw):

        size = 1

        glBindTexture(GL_TEXTURE_CUBE_MAP, self.cubeMapTextureID)

        # glPushMatrix()
        # glLoadIdentity()
        # glRotatef(cameraPitch, 1.0, 0.0, 0.0)
        # glRotatef(cameraYaw, 1.0, 0.0, 0.0)

        glBegin(GL_TRIANGLE_STRIP)
        glTexCoord3f(-size, -size, -size)
        glVertex3f(-size, -size, -size)
        glTexCoord3f(-size, size, -size)
        glVertex3f(-size, size, -size)
        glTexCoord3f(-size, -size, size)
        glVertex3f(-size, -size, size)
        glTexCoord3f(-size, size, size)
        glVertex3f(-size, size, size)
        glEnd()

        # glBegin(GL_TRIANGLE_STRIP)
        # glTexCoord3f(size, -size, -size)
        # glVertex3f(size, -size, -size)
        # glTexCoord3f(size, -size, size)
        # glVertex3f(size, -size, size)
        # glTexCoord3f(size, size, -size)
        # glVertex3f(size, size, -size)
        # glTexCoord3f(size, size, size)
        # glVertex3f(size, size, size)
        # glEnd()
        #
        # glBegin(GL_TRIANGLE_STRIP)
        # glTexCoord3f(-size, -size, -size)
        # glVertex3f(-size, -size, -size)
        # glTexCoord3f(-size, -size, size)
        # glVertex3f(-size, -size, size)
        # glTexCoord3f(size, -size, -size)
        # glVertex3f(size, -size, -size)
        # glTexCoord3f(size, -size, size)
        # glVertex3f(size, -size, size)
        # glEnd()
        #
        # glBegin(GL_TRIANGLE_STRIP)
        # glTexCoord3f(-size, size, -size)
        # glVertex3f(-size, size, -size)
        # glTexCoord3f(size, size, -size)
        # glVertex3f(size, size, -size)
        # glTexCoord3f(-size, size, size)
        # glVertex3f(-size, size, size)
        # glTexCoord3f(size, size, size)
        # glVertex3f(size, size, size)
        # glEnd()
        #
        # glBegin(GL_TRIANGLE_STRIP)
        # glTexCoord3f(-size, -size, -size)
        # glVertex3f(-size, -size, -size)
        # glTexCoord3f(size, -size, -size)
        # glVertex3f(size, -size, -size)
        # glTexCoord3f(-size, size, -size)
        # glVertex3f(-size, size, -size)
        # glTexCoord3f(size, size, -size)
        # glVertex3f(size, size, -size)
        # glEnd()
        #
        # glBegin(GL_TRIANGLE_STRIP)
        # glTexCoord3f(-size, -size, size)
        # glVertex3f(-size, -size, size)
        # glTexCoord3f(-size, size, size)
        # glVertex3f(-size, size, size)
        # glTexCoord3f(size, -size, size)
        # glVertex3f(size, -size, size)
        # glEnd()
        #
        # glPopMatrix()


        
