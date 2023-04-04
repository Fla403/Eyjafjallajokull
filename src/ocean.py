

import OpenGL.GL as GL

from basicModels import Triangle


class Ocean(Triangle):
    def __init__(self, shader):

        super().__init__(shader)

    def draw(self):
        super().draw()
