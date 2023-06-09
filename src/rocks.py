
"""
    Creation of a rock particle with random parameters for physic animation.
"""

import glfw
import random

from core import Mesh
from sphere import Sphere


class Rocks(Mesh):

    def __init__(self, shader, lightDir,
                 subdivisions=3,
                 kD=(0.92, 0.1, 0),
                 kA=(0.8, 0.2, 0),
                 kS=(0.95, 0.7, 0.7),
                 s=1):
        self.color = (.8, .1, .1)
        self.startTime = glfw.get_time()

        # We create some random parameters for the rock

        # Initial position
        self.posX = random.randint(-5, 5)
        self.posY = random.randint(25, 42)
        self.posZ = random.randint(-5, 5)

        # Initial speed
        self.speedX = random.randint(-5, 5)
        self.speedY = random.randint(15, 35)
        self.speedZ = random.randint(-5, 5)

        # Acceleration
        self.accelX = 0
        self.accelY = -9.81
        self.accelZ = 0

        # Size of the particle
        randomSize = random.uniform(0.05, 0.8)

        rock = Sphere(shader, subdivisions, self.color)
        attributes = dict(position=rock.vertices*randomSize)

        super().__init__(shader, attributes=attributes, index=rock.index, time=0, light=lightDir,
                         k_d=kD, k_a=kA, k_s=kS, s=s,
                         posX=self.posX, posY=self.posY, posZ=self.posZ,
                         speedX=self.speedX, speedY=self.speedY, speedZ=self.speedZ,
                         accelX=self.accelX, accelY=self.accelY, accelZ=self.accelZ)

    def draw(self, **_args):
        super().draw(**_args, time=glfw.get_time())
