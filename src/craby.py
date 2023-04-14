#! /usr/bin/env python3

import OpenGL.GL as GL
import glfw    
import numpy as np
from core import *
import math
from transform import translate, identity, rotate, scale
from sphere import Sphere, deform


class Leg(Node):
    def __init__(self):
        super().__init__()
        crabyShader = Shader("color.vert", "color.frag")

        

        sphere1 = Sphere(crabyShader, 3, (0.85, 0.45, 0))
        sphere1.transformByMatrix(scale(1,0.2,0.2))
        sphere1.modelling(flattening=0.3, mitigation_pos=0.6, mitigation_neg=1, inflation_pos=0, inflation_neg=0, xMax=1, yMax=0.2, zMax=0.2)

        legP1Node = Node(transform= rotate((0,0,1), 45) @ translate(-0.85,-0.25,0))
        legP1Node.add(sphere1)

        
        sphere2 = Sphere(crabyShader, 3, (0.90, 0.5, 0))
        sphere2.transformByMatrix(scale(1,0.15,0.15))
        sphere2.modelling(flattening=0.3, mitigation_pos=0.7, mitigation_neg=0.7, inflation_pos=1, inflation_neg=1, xMax=1, yMax=0.2, zMax=0.2)
        
        legP2Node = Node(transform=rotate((0,0,1), 0) @ translate(0.85,-0.23,0))
        legP2Node.add(sphere2)


        joint1 = Node(transform=rotate((0,0,1), 30) @translate(-1.7,0,0))
        joint1.add(legP1Node)
        joint1.add(legP2Node)


        sphere3 = Sphere(crabyShader, 3, (0.95, 0.55, 0))
        sphere3.transformByMatrix(scale(1,0.3,0.3))
        sphere3.modelling(flattening=0.2, mitigation_pos=1, mitigation_neg=1, inflation_pos=0.8, inflation_neg=0.8, xMax=1, yMax=0.2, zMax=0.2)
        
        legP3Node = Node(transform=rotate((0,0,1), 0) @ translate(0.85,-0.1,0))
        legP3Node.add(sphere3)

        
        joint2 = Node(transform=translate(-1.7,0,0))
        joint2.add(joint1)
        joint2.add(legP3Node)


        self.add(joint2)
        

    """def add(self, *drawables):
        super().add(*drawables)

    def draw(self, model=identity(), **other_uniforms):
        self.world_transform = model @ self.transform
        for child in self.children:
            child.draw(model=self.world_transform, **other_uniforms)

    def key_handler(self, key):
        super().key_handler(key)"""

class Body(Node):
    def __init__(self):
        super().__init__()
        crabyShader = Shader("color.vert", "color.frag")

        sphere = Sphere(crabyShader, 4, (.9, 0.5, 0))
        sphere.transformByMatrix(scale(1,0.5,1))
        sphere.stretch(1, 0.5, 1)

        self.add(sphere)

class Eye(Node):

    def __init__(self):
        super().__init__()
        crabyShader = Shader("color.vert", "color.frag")


        sphere1 = Sphere(crabyShader, 3, (0.05,0.05,0.05))
        sphere1.transformByMatrix(scale(0.5,1,0.2))

        sphere2 = Sphere(crabyShader, 3, (1,1,1))
        sphere2.transformByMatrix(scale(1,1,0.2))
        blanc1 = Node(transform=rotate((1,-0.45,0), -3) @ translate(0.1,0.25,0.2) @ scale(0.3))
        blanc1.add(sphere2)

        sphere3 = Sphere(crabyShader, 3, (1,1,1))
        sphere3.transformByMatrix(scale(1,1,0.2))
        blanc2 = Node(transform=rotate((1,0.45,0), 6) @ translate(-0.2,-0.4,0.20) @ scale(0.15))
        blanc2.add(sphere3)

        eye = Node()
        eye.add(sphere1)
        eye.add(blanc1)
        eye.add(blanc2)

        self.add(eye)

class Mouth(Node):

    def __init__(self):
        super().__init__()
        crabyShader = Shader("color.vert", "color.frag")

        sphere = Sphere(crabyShader, 3, (0.05,0.05,0.05))
        sphere.transformByMatrix(scale(1,0.15,0.15))
        sphere.modelling(flattening=0.8, mitigation_pos=1, mitigation_neg=1, inflation_pos=0.9, inflation_neg=0.9, xMax=1, yMax=0.2, zMax=0.2)

        self.add(sphere)

class Claw(Node):
    def __init__(self):
        super().__init__()
        crabyShader = Shader("color.vert", "color.frag")

        sphere1 = Sphere(crabyShader, 3, (0.85, 0.45, 0))
        sphere1.transformByMatrix(scale(1,0.3,0.3))
        sphere1.modelling(flattening=0.8, mitigation_pos=0.95, mitigation_neg=0.5, inflation_pos=0.5, inflation_neg=0.5, xMax=1, yMax=0.3, zMax=0.3)

        clawNode1 = Node(transform= rotate((0,0,1), 50) @ scale(0.8) @ translate(0.8,-0.7,0))
        clawNode1.add(sphere1)

        sphere2 = Sphere(crabyShader, 4, (0.8, 0.4, 0))
        sphere2.transformByMatrix(scale(1,0.3,0.5))
        sphere2.modelling(flattening=-0.8, mitigation_pos=0.98, mitigation_neg=0.5, inflation_pos=0.5, inflation_neg=0.5, xMax=1, yMax=0.3, zMax=0.5)

        clawNode2 = Node(transform=translate(0.8,0.7,0))
        clawNode2.add(sphere2)
        
        joint1 = Node(transform= scale(0.9) @ rotate((0,0,1), 180))
        joint1.add(clawNode1)
        joint1.add(clawNode2)

        sphere3 = Sphere(crabyShader, 3, (0.90, 0.5, 0))
        sphere3.transformByMatrix(scale(1,0.15,0.15))
        sphere3.modelling(flattening=0.6, mitigation_pos=0.8, mitigation_neg=0.8, inflation_pos=1, inflation_neg=1, xMax=1, yMax=0.15, zMax=0.15)

        clawNode3 = Node(transform=translate(0.8,-0.45,0))
        clawNode3.add(sphere3)

        joint2 = Node(transform=rotate((0,0,1), 90) @ translate(-1.6,0,0))
        joint2.add(joint1)
        joint2.add(clawNode3)

        sphere4 = Sphere(crabyShader, 3, (0.95, 0.55, 0))
        sphere4.transformByMatrix(scale(1,0.2,0.2))
        sphere4.modelling(flattening=0.2, mitigation_pos=1, mitigation_neg=1, inflation_pos=0.8, inflation_neg=0.8, xMax=1, yMax=0.2, zMax=0.2)

        clawNode4 = Node(transform=scale(1.1) @ translate(0.8,-0.1,0))
        clawNode4.add(sphere4)

        joint3 = Node(transform=translate(-1.8,0.02,0))
        joint3.add(joint2)
        joint3.add(clawNode4)

        self.add(joint3)


class Craby(Node):
    def __init__(self):
        super().__init__()

        body = Body()

        eye1 = Eye()
        eye2 = Eye()

        eyeNode1 = Node(transform=translate(-0.2,0.1,0.73) @ scale(0.1))
        eyeNode1.add(eye1)

        eyeNode2 = Node(transform=translate(0.2,0.1,0.73) @ scale(0.1))
        eyeNode2.add(eye2)

        mouth = Mouth()

        mouthNode = Node(transform=translate(0,-0.1,0.70) @ scale(0.08) @ rotate((1,0,0), 30))
        mouthNode.add(mouth)

        face = Node()
        face.add(body)
        face.add(eyeNode1)
        face.add(eyeNode2)
        face.add(mouthNode)

        legL1 = Leg()
        legL1Node = Node(transform=translate(-0.6,-0.1,0.15) @ scale(0.25) @ rotate((0,0,1), 20))
        legL1Node.add(legL1)

        legL2 = Leg()
        legL2Node = Node(transform=translate(-0.65,-0.1,-0.1) @ scale(0.25) @ rotate((0,0,1), 20))
        legL2Node.add(legL2)

        legL3 = Leg()
        legL3Node = Node(transform=translate(-0.58,-0.1,-0.35) @ scale(0.25) @ rotate((0,0,1), 20))
        legL3Node.add(legL3)

        legL4 = Leg()
        legL4Node = Node(transform=translate(-0.5,-0.1,-0.6) @ scale(0.25) @ rotate((0,0,1), 20))
        legL4Node.add(legL4)

        legR1 = Leg()
        legR1Node = Node(transform=translate(0.6,-0.1,0.15) @ scale(0.25) @ rotate((0,0,1), -20) @ rotate((0,1,0), 180))
        legR1Node.add(legR1)

        legR2 = Leg()
        legR2Node = Node(transform=translate(0.65,-0.1,-0.1) @ scale(0.25) @ rotate((0,0,1), -20) @ rotate((0,1,0), 180))
        legR2Node.add(legR2)

        legR3 = Leg()
        legR3Node = Node(transform=translate(0.58,-0.1,-0.35) @ scale(0.25) @ rotate((0,0,1), -20) @ rotate((0,1,0), 180))
        legR3Node.add(legR3)

        legR4 = Leg()
        legR4Node = Node(transform=translate(0.5,-0.1,-0.6) @ scale(0.25) @ rotate((0,0,1), -20) @ rotate((0,1,0), 180))
        legR4Node.add(legR4)

        legs = Node()
        legs.add(face)
        legs.add(legL1Node)
        legs.add(legL2Node)
        legs.add(legL3Node)
        legs.add(legL4Node)
        legs.add(legR1Node)
        legs.add(legR2Node)
        legs.add(legR3Node)
        legs.add(legR4Node)

        clawL = Claw()
        clawLNode = Node(transform=translate(-0.6,-0.1,0.4)  @ rotate((0,1,0), 20) @ scale(0.25) @ rotate((0,0,1), 45) @ rotate((1,0,0), 310))
        clawLNode.add(clawL)

        clawR = Claw()
        clawRNode = Node(transform=translate(0.6,-0.1,0.4) @ rotate((0,1,0), -20) @ scale(0.25) @ rotate((0,0,1), -45) @ rotate((1,0,0), 310) @ rotate((0,1,0), 180))
        clawRNode.add(clawL)

        claws = Node()
        claws.add(legs)
        claws.add(clawLNode)
        claws.add(clawRNode)








        self.add(claws)



