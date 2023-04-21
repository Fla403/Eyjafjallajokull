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


class Sphere(Mesh):

    calculated_sphere = {}

    def nb_vertices_on_level(self, level):

        if ((level == 1) or (level == self.nb_levels-1)):
            return 1
        if (level <= self.middle_level):
            return level*4
        return (self.nb_levels-1 - level)*4

    def precize(self):

        self.nb_levels = 2*self.nb_levels - 1
        self.middle_level = (self.nb_levels-1)//2

        new_vertices = [self.vertices[0], 
                putOnSphere(midPoint(self.vertices[0], self.vertices[1])),
                putOnSphere(midPoint(self.vertices[0], self.vertices[2])),
                putOnSphere(midPoint(self.vertices[0], self.vertices[3])),
                putOnSphere(midPoint(self.vertices[0], self.vertices[4]))]

        level = 2
        first_index = 1

        while (level <= self.middle_level):
            
            if (level%2 == 0):
                for i in range(2*level - 1):
                    new_vertices.append(self.vertices[first_index+i])
                    new_vertices.append(putOnSphere(midPoint(self.vertices[first_index+i], self.vertices[first_index+i+1])))
                new_vertices.append(self.vertices[first_index+2*level-1])
                new_vertices.append(putOnSphere(midPoint(self.vertices[first_index+2*level-1], self.vertices[first_index])))
            else:
                for i in range(4):
                    for j in range((level-1)//2):
                        new_vertices.append(putOnSphere(midPoint(self.vertices[first_index+i*(level-1)//2+j], self.vertices[first_index+4*(level-1)//2+i*(level+1)//2+j])))
                        new_vertices.append(putOnSphere(midPoint(self.vertices[first_index+i*(level-1)//2+j], self.vertices[first_index+4*(level-1)//2+i*(level+1)//2+j+1])))
                    if (i < 3):
                        new_vertices.append(putOnSphere(midPoint(self.vertices[first_index+i*(level-1)//2+(level-1)//2], self.vertices[first_index+4*(level-1)//2+i*(level+1)//2+(level-1)//2])))
                    else:
                        new_vertices.append(putOnSphere(midPoint(self.vertices[first_index], self.vertices[first_index+4*(level-1)//2+i*(level+1)//2+(level-1)//2])))
                first_index += 2*(level-1)

            level += 1

        first_index += self.nb_vertices_on_level(self.middle_level)//2

        while (level < self.nb_levels-2):
            
            if (level%2 == 0):
                nb_vert_prev = self.nb_vertices_on_level(level)//2
                for i in range(nb_vert_prev - 1):
                    new_vertices.append(self.vertices[first_index+i])
                    new_vertices.append(putOnSphere(midPoint(self.vertices[first_index+i], self.vertices[first_index+i+1])))
                new_vertices.append(self.vertices[first_index+nb_vert_prev-1])
                new_vertices.append(putOnSphere(midPoint(self.vertices[first_index+nb_vert_prev-1], self.vertices[first_index])))

                first_index += self.nb_vertices_on_level(level)//2
            else:

                for i in range(4):
                    nb_vert_prev_by_side_up = self.nb_vertices_on_level(level-1)//(2*4)
                    nb_vert_prev_by_side_down = self.nb_vertices_on_level(level+1)//(2*4)
                    for j in range(nb_vert_prev_by_side_down):
                        new_vertices.append(putOnSphere(midPoint(self.vertices[first_index+i*nb_vert_prev_by_side_down+j], self.vertices[first_index + (i-4)*nb_vert_prev_by_side_up + j])))
                        new_vertices.append(putOnSphere(midPoint(self.vertices[first_index+i*nb_vert_prev_by_side_down+j], self.vertices[first_index + (i-4)*nb_vert_prev_by_side_up + j+1])))
                    if (i < 3):
                        new_vertices.append(putOnSphere(midPoint(self.vertices[first_index+(i+1)*nb_vert_prev_by_side_down], self.vertices[first_index + (i-4)*nb_vert_prev_by_side_up + nb_vert_prev_by_side_down])))
                    else:
                        new_vertices.append(putOnSphere(midPoint(self.vertices[first_index], self.vertices[first_index + (i-4)*nb_vert_prev_by_side_up + nb_vert_prev_by_side_down])))

            level += 1

        new_vertices += [
                putOnSphere(midPoint(self.vertices[-1], self.vertices[-5])),
                putOnSphere(midPoint(self.vertices[-1], self.vertices[-4])),
                putOnSphere(midPoint(self.vertices[-1], self.vertices[-3])),
                putOnSphere(midPoint(self.vertices[-1], self.vertices[-2])),
                self.vertices[-1]]

        self.vertices = np.array(new_vertices)
    

        # Ancien code
        """nb_vertices = np.shape(self.sommets)[0]
        nb_triangle = np.shape(self.indices)[0]/3

        first_round = True

        i = 0
        while i < nb_vertices:

            newS1 = putOnSphere(midPoint(self.vertices[i], self.vertices[i+1]))
            newS2 = putOnSphere(midPoint(self.vertices[i+1], self.vertices[i+2]))
            newS3 = putOnSphere(midPoint(self.vertices[i+2], self.vertices[i]))

            if first_round :
                newTriangles = np.array((self.vertices[i], newS1, newS3, self.vertices[i+2], newS3, newS2, newS3, newS1, newS2, self.vertices[i+1], newS2, newS1), 'f')
                first_round = False
            else :
                newTriangles = np.concatenate((newTriangles, np.array((self.vertices[i], newS1, newS3, self.vertices[i+2], newS3, newS2, newS3, newS1, newS2, self.vertices[i+1], newS2, newS1))))

            i += 3
        
        self.vertices = newTriangles"""

    def index_triangles(self):

        first_index = 1

        new_index = [0,1,2, 0,2,3, 0,3,4, 0,4,1]
        level = 1
        while (level < self.middle_level):
            for i in range(4):
                new_index += [first_index+i*level, first_index+(4+i)*level+i, first_index+(4+i)*level+i+1]
                for j in range(level):
                    if ((i < 3) or (j < level-1)):
                        new_index += [first_index+i*level+j, first_index+(4+i)*level+j+i+1, first_index+i*level+j+1] + [first_index+i*level+j+1, first_index+(4+i)*level+j+i+1, first_index+(4+i)*level+j+i+2]
                    else:
                        new_index += [first_index+i*level+j, first_index+(4+i)*level+j+i+1, first_index] + [first_index, first_index+(4+i)*level+j+i+1, first_index+4*level]

            first_index += level*4
            level += 1
        
        first_index += self.nb_vertices_on_level(self.middle_level)

        while (level < self.nb_levels-2):
            nb_vert_by_side_up = self.nb_vertices_on_level(level)//4
            nb_vert_by_side = self.nb_vertices_on_level(level+1)//4
            for i in range(4):
                new_index += [first_index+i*nb_vert_by_side, first_index + (i-4)*nb_vert_by_side_up + 1, first_index + (i-4)*nb_vert_by_side_up]
                for j in range(nb_vert_by_side):
                    if (not ((i == 3) and (j == nb_vert_by_side-1))):
                        new_index += [first_index+i*nb_vert_by_side+j, first_index+i*nb_vert_by_side+j+1, first_index + (i-4)*nb_vert_by_side_up + j+1] + [first_index+i*nb_vert_by_side+j+1, first_index + (i-4)*nb_vert_by_side_up + j+2, first_index + (i-4)*nb_vert_by_side_up + j+1]
                    else:
                        new_index += [first_index+i*nb_vert_by_side+j, first_index, first_index + (i-4)*nb_vert_by_side_up + j+1] + [first_index, first_index - 4*nb_vert_by_side_up, first_index + (i-4)*nb_vert_by_side_up + j+1]

            first_index += nb_vert_by_side*4
            level += 1


        nb_vert = np.shape(self.vertices)[0]
        new_index += [nb_vert-1,nb_vert-4,nb_vert-5, nb_vert-1,nb_vert-3,nb_vert-4, nb_vert-1,nb_vert-2,nb_vert-3, nb_vert-1,nb_vert-5,nb_vert-2]

        self.index = np.array(new_index)


    def __init__(self, shader, recursion_level, color):

        self.color = color
        self.shader = shader

        if (recursion_level in Sphere.calculated_sphere):

            self.vertices = np.copy(Sphere.calculated_sphere[recursion_level][0])
            self.index = Sphere.calculated_sphere[recursion_level][1]
            self.nb_levels = Sphere.calculated_sphere[recursion_level][2]
            self.middle_level = Sphere.calculated_sphere[recursion_level][3]

        else:
        
            a = 1/math.sqrt(2)

            s1 = (0,1,0)
            s2 = (-a,0,a)
            s3 = (a,0,a)
            s4 = (a,0,-a)
            s5 = (-a,0,-a)
            s6 = (0,-1,0)

            self.vertices = np.array((s1, s2, s3, s4, s5, s6), np.float32)

            t1 = np.array((0, 1, 2), np.uint32)
            t2 = np.array((0, 2, 3), np.uint32)
            t3 = np.array((0, 3, 4), np.uint32)
            t4 = np.array((0, 4, 1), np.uint32)
            t5 = np.array((5, 1, 4), np.uint32)
            t6 = np.array((5, 4, 3), np.uint32)
            t7 = np.array((5, 3, 2), np.uint32)
            t8 = np.array((5, 2, 1), np.uint32)

            self.index = np.concatenate((t1, t2, t3, t4, t5, t6, t7, t8))

            self.nb_levels = 3
            self.middle_level = 1

            for i in range(recursion_level):
                self.precize()

            self.index_triangles()

            Sphere.calculated_sphere[recursion_level] = [np.copy(self.vertices), self.index, self.nb_levels, self.middle_level]


        super().__init__(shader, attributes=dict(position= self.vertices), index=self.index, global_color=self.color)


    def transformByMatrix(self, matrix):

        nb_vertices = np.shape(self.vertices)[0]

        i = 0
        while i < nb_vertices:

            self.vertices[i] = tuple(np.array((self.vertices[i][0], self.vertices[i][1], self.vertices[i][2], 0), 'f') @ matrix)[:3]

            i += 1 
        
        super().__init__(self.shader, attributes=dict(position= self.vertices), index=self.index, global_color=self.color)

    def transformByFunction(self, f):

        nb_vertices = np.shape(self.vertices)[0]

        i = 0
        while i < nb_vertices:

            self.vertices[i] = f(self.vertices[i][0], self.vertices[i][1], self.vertices[i][2])

            i += 1 
        
        super().__init__(self.shader, attributes=dict(position= self.vertices), index=self.index, global_color=self.color)

    def modelling(self, flattening=0, mitigation_pos=0.9, mitigation_neg=0.9, inflation_pos=0, inflation_neg=0, xMax=1, yMax=1, zMax=1):

        nb_vertices = np.shape(self.vertices)[0]

        i = 0
        while i < nb_vertices:

            x = self.vertices[i][0]
            y = self.vertices[i][1]
            z = self.vertices[i][2]

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

            self.vertices[i] = (x, y+y_diff, z)

            i += 1 
        
        super().__init__(self.shader, attributes=dict(position= self.vertices), index=self.index, global_color=self.color)

    
    def stretch(self, xMax, yMax, zMax):

        nb_vertices = np.shape(self.vertices)[0]

        i = 0
        while i < nb_vertices:

            x = self.vertices[i][0]
            y = self.vertices[i][1]
            z = self.vertices[i][2]

            xDiff = (yMax - abs(y)) * abs(x) / xMax
            zDiff = (yMax - abs(y)) * abs(z) / zMax

            x += xDiff if x >= 0 else -xDiff
            z += zDiff/4 if z >= 0 else -zDiff

            self.vertices[i] = (x/(1+yMax), y/(1+yMax), z/(1+yMax))

            i += 1 
        
        super().__init__(self.shader, attributes=dict(position= self.vertices), index=self.index, global_color=self.color)

        