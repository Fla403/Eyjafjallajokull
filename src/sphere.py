#! /usr/bin/env python3

import OpenGL.GL as GL
import glfw    
import numpy as np
from core import *
import math


def midPoint(p1, p2):
    return ((p1[0]+p2[0])/2, (p1[1]+p2[1])/2, (p1[2]+p2[2])/2)

def putOnSphere(p):
    d = math.sqrt(p[0]**2 + p[1]**2 + p[2]**2)
    return (p[0]/d, p[1]/d, p[2]/d)

def deform(x, y, z, flattening):
    y_diff = math.sqrt(1-x**2)
    y_diff *= 0.6
    return (x, y+y_diff, z)

class Sphere(Mesh):

    def precize(self):

        nb_sommets = np.shape(self.triangles)[0]

        first_round = True

        i = 0
        while i < nb_sommets:

            newS1 = putOnSphere(midPoint(self.triangles[i], self.triangles[i+1]))
            newS2 = putOnSphere(midPoint(self.triangles[i+1], self.triangles[i+2]))
            newS3 = putOnSphere(midPoint(self.triangles[i+2], self.triangles[i]))

            if first_round :
                newTriangles = np.array((self.triangles[i], newS1, newS3, self.triangles[i+2], newS3, newS2, newS3, newS1, newS2, self.triangles[i+1], newS2, newS1), 'f')
                first_round = False
            else :
                newTriangles = np.concatenate((newTriangles, np.array((self.triangles[i], newS1, newS3, self.triangles[i+2], newS3, newS2, newS3, newS1, newS2, self.triangles[i+1], newS2, newS1))))

            i += 3
        
        self.triangles = newTriangles

    def __init__(self, shader, recursion_level, color):

        self.color = color
        self.shader = shader
        
        a = 1/math.sqrt(2)

        s1 = (0,1,0)
        s2 = (a,0,a)
        s3 = (-a,0,a)
        s4 = (-a,0,-a)
        s5 = (a,0,-a)
        s6 = (0,-1,0)

        t1 = np.array((s1, s3, s2), 'f')
        t2 = np.array((s1, s4, s3), 'f')
        t3 = np.array((s1, s5, s4), 'f')
        t4 = np.array((s1, s2, s5), 'f')
        t5 = np.array((s6, s5, s2), 'f')
        t6 = np.array((s6, s4, s5), 'f')
        t7 = np.array((s6, s3, s4), 'f')
        t8 = np.array((s6, s2, s3), 'f')

        self.triangles = np.concatenate((t1, t2, t3, t4, t5, t6, t7, t8))

        for i in range(recursion_level):
            self.precize()

        super().__init__(shader, attributes=dict(position= self.triangles), global_color=self.color)

    def draw(self, **_args):
        super().draw(**_args)

    def change(attributes):
        self.vertex_array.execute(GL.GL_TRIANGLES, attributes)

    def transformByMatrix(self, matrix):

        nb_sommets = np.shape(self.triangles)[0]

        i = 0
        while i < nb_sommets:

            self.triangles[i] = tuple(np.array((self.triangles[i][0], self.triangles[i][1], self.triangles[i][2], 0), 'f') @ matrix)[:3]

            i += 1 
        
        super().__init__(self.shader, attributes=dict(position= self.triangles), global_color=self.color)

    def transformByFunction(self, f):

        nb_sommets = np.shape(self.triangles)[0]

        i = 0
        while i < nb_sommets:

            self.triangles[i] = f(self.triangles[i][0], self.triangles[i][1], self.triangles[i][2])

            i += 1 
        
        super().__init__(self.shader, attributes=dict(position= self.triangles), global_color=self.color)

    def modelling(self, flattening=0, mitigation_pos=0.9, mitigation_neg=0.9, inflation_pos=0, inflation_neg=0, xMax=1, yMax=1, zMax=1):

        nb_sommets = np.shape(self.triangles)[0]

        i = 0
        while i < nb_sommets:

            x = self.triangles[i][0]
            y = self.triangles[i][1]
            z = self.triangles[i][2]

            if y >= 0:
                y += (yMax - y) * (inflation_pos if x >= 0 else inflation_neg) * abs(y)/yMax
            else :
                y -= (yMax + y) * (inflation_pos if x >= 0 else inflation_neg) * abs(y)/yMax
            if z >= 0:
                z += (zMax - z) * (inflation_pos if x >= 0 else inflation_neg) * abs(z)/zMax
            else:
                z -= (zMax + z) * (inflation_pos if x >= 0 else inflation_neg) * abs(z)/zMax
            
            x_temp = x*mitigation_pos if x >= 0 else x*mitigation_neg

            y_diff = math.sqrt(1-x_temp**2) * flattening

            self.triangles[i] = (x, y+y_diff, z)

            i += 1 
        
        super().__init__(self.shader, attributes=dict(position= self.triangles), global_color=self.color)

    
    def stretch(self, xMax, yMax, zMax):

        nb_sommets = np.shape(self.triangles)[0]

        i = 0
        while i < nb_sommets:

            x = self.triangles[i][0]
            y = self.triangles[i][1]
            z = self.triangles[i][2]

            xDiff = (yMax - abs(y)) * abs(x) / xMax
            zDiff = (yMax - abs(y)) * abs(z) / zMax

            x += xDiff if x >= 0 else -xDiff
            z += zDiff/4 if z >= 0 else -zDiff

            self.triangles[i] = (x/(1+yMax), y/(1+yMax), z/(1+yMax))

            i += 1 
        
        super().__init__(self.shader, attributes=dict(position= self.triangles), global_color=self.color)

        