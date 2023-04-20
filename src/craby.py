#! /usr/bin/env python3

import OpenGL.GL as GL
import glfw    
import numpy as np
from core import *
import math
from transform import translate, identity, rotate, scale, quaternion_from_axis_angle, quaternion
from sphere import Sphere
from keyFrames import KeyFrameControlNode


class Leg(KeyFrameControlNode):
    def __init__(self):
        super().__init__()
        crabyShader = Shader("color.vert", "color.frag")

        sphere1 = Sphere(crabyShader, 3, (0.85, 0.45, 0))
        sphere1.transformByMatrix(scale(1,0.2,0.2))
        sphere1.modelling(flattening=0.3, mitigation_pos=0.6, mitigation_neg=1, inflation_pos=0, inflation_neg=0, xMax=1, yMax=0.2, zMax=0.2)

        legP1Node = Node(transform= rotate((0,0,1), 45) @ translate(-0.85,-0.25,0))
        legP1Node.add(sphere1)

        self.joint1 = KeyFrameControlNode()
        self.joint1.add(legP1Node)

        
        sphere2 = Sphere(crabyShader, 3, (0.90, 0.5, 0))
        sphere2.transformByMatrix(scale(1,0.15,0.15))
        sphere2.modelling(flattening=0.3, mitigation_pos=0.7, mitigation_neg=0.7, inflation_pos=1, inflation_neg=1, xMax=1, yMax=0.2, zMax=0.2)
        
        legP2Node = Node(transform=rotate((0,0,1), 0) @ translate(0.85,-0.23,0))
        legP2Node.add(sphere2)

        link1 = Node(transform=rotate((0,0,1), 30)@translate(-1.7,0,0))
        link1.add(self.joint1)
        link1.add(legP2Node)

        self.joint2 = KeyFrameControlNode()
        self.joint2.add(link1)


        sphere3 = Sphere(crabyShader, 3, (0.95, 0.55, 0))
        sphere3.transformByMatrix(scale(1,0.3,0.3))
        sphere3.modelling(flattening=0.2, mitigation_pos=1, mitigation_neg=1, inflation_pos=0.8, inflation_neg=0.8, xMax=1, yMax=0.2, zMax=0.2)
        
        legP3Node = Node(transform=rotate((0,0,1), 0) @ translate(0.85,-0.1,0))
        legP3Node.add(sphere3)

        link2 = Node(transform=translate(-1.7,0,0))
        link2.add(self.joint2)
        link2.add(legP3Node)
        
        self.joint3 = KeyFrameControlNode()
        self.joint3.add(link2)

        self.add(self.joint3)

class Body(KeyFrameControlNode):
    def __init__(self):
        super().__init__()
        crabyShader = Shader("color.vert", "color.frag")

        sphere = Sphere(crabyShader, 3, (.9, 0.5, 0, 1))
        sphere.transformByMatrix(scale(1,0.5,1))
        sphere.stretch(1, 0.5, 1)

        self.add(sphere)

class Eye(KeyFrameControlNode):

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

class Claw(KeyFrameControlNode):
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


class Craby(KeyFrameControlNode):
    def __init__(self):
        super().__init__()


        self.isMoving = False
        self.endMove = 0
        self.elevation = 2
        self.jumpDuration = 0.8
        self.rotation = 0
        self.rotationDiff = 15
        self.rotateDuration = 0.2
        self.isHappy = False
        self.isClawTight = False


        self.body = Body()

        self.eye1 = Eye()
        self.eye2 = Eye()

        eyeNode1 = Node(transform=translate(-0.2,0.1,0.73) @ scale(0.1))
        eyeNode1.add(self.eye1)

        eyeNode2 = Node(transform=translate(0.2,0.1,0.73) @ scale(0.1))
        eyeNode2.add(self.eye2)

        self.mouth = Mouth()

        mouthNode = Node(transform=translate(0,-0.1,0.70) @ scale(0.08) @ rotate((1,0,0), 30))
        mouthNode.add(self.mouth)

        face = Node()
        face.add(eyeNode1)
        face.add(eyeNode2)
        face.add(mouthNode)

        self.legL1 = Leg()
        legL1Node = Node(transform=translate(0.6,-0.1,0.15) @ scale(0.25) @ rotate((0,0,1), -20) @ rotate((0,1,0), 180))
        legL1Node.add(self.legL1)

        self.legL2 = Leg()
        legL2Node = Node(transform=translate(0.65,-0.1,-0.1) @ scale(0.25) @ rotate((0,0,1), -20) @ rotate((0,1,0), 180))
        legL2Node.add(self.legL2)

        self.legL3 = Leg()
        legL3Node = Node(transform=translate(0.58,-0.1,-0.35) @ scale(0.25) @ rotate((0,0,1), -20) @ rotate((0,1,0), 180))
        legL3Node.add(self.legL3)

        self.legL4 = Leg()
        legL4Node = Node(transform=translate(0.5,-0.1,-0.6) @ scale(0.25) @ rotate((0,0,1), -20) @ rotate((0,1,0), 180))
        legL4Node.add(self.legL4)

        self.legR1 = Leg()
        legR1Node = Node(transform=translate(-0.6,-0.1,0.15) @ scale(0.25) @ rotate((0,0,1), 20))
        legR1Node.add(self.legR1)

        self.legR2 = Leg()
        legR2Node = Node(transform=translate(-0.65,-0.1,-0.1) @ scale(0.25) @ rotate((0,0,1), 20))
        legR2Node.add(self.legR2)

        self.legR3 = Leg()
        legR3Node = Node(transform=translate(-0.58,-0.1,-0.35) @ scale(0.25) @ rotate((0,0,1), 20))
        legR3Node.add(self.legR3)

        self.legR4 = Leg()
        legR4Node = Node(transform=translate(-0.5,-0.1,-0.6) @ scale(0.25) @ rotate((0,0,1), 20))
        legR4Node.add(self.legR4)

        legs = Node()
        legs.add(legL1Node)
        legs.add(legL2Node)
        legs.add(legL3Node)
        legs.add(legL4Node)
        legs.add(legR1Node)
        legs.add(legR2Node)
        legs.add(legR3Node)
        legs.add(legR4Node)

        self.clawL = Claw()
        clawLNode = Node(transform=translate(-0.6,-0.1,0.4)  @ rotate((0,1,0), 20) @ scale(0.25) @ rotate((0,0,1), 45) @ rotate((1,0,0), 310))
        clawLNode.add(self.clawL)

        self.clawR = Claw()
        clawRNode = Node(transform=translate(0.6,-0.1,0.4) @ rotate((0,1,0), -20) @ scale(0.25) @ rotate((0,0,1), -45) @ rotate((1,0,0), 310) @ rotate((0,1,0), 180))
        clawRNode.add(self.clawR)

        claws = Node()
        claws.add(clawLNode)
        claws.add(clawRNode)

        self.add(self.body)
        self.add(face)
        self.add(legs)
        self.add(claws)

    def key_handler(self, key):
        time = glfw.get_time()

        if (self.isMoving == True and time >= self.endMove):
            self.isMoving = False

        if (not self.isMoving):

            if (key == glfw.KEY_UP):
                self.isMoving = True
                self.endMove = time+self.jumpDuration
                self.addTranslate(time, vec(0,0,0))
                self.addTranslate(time+self.jumpDuration/3, vec(0,-0.25,0))
                self.addTranslate(time+self.jumpDuration*2/3, vec(0,self.elevation,0))
                self.addTranslate(time+self.jumpDuration, vec(0,0,0))
                for leg in [self.legL1, self.legL2, self.legL3, self.legL4, self.legR1, self.legR2, self.legR3, self.legR4]:
                    leg.joint1.addRotate(time, quaternion())
                    leg.joint2.addRotate(time, quaternion())
                    leg.joint3.addRotate(time, quaternion())
                    leg.joint1.addRotate(time+self.jumpDuration/3, quaternion_from_axis_angle((0,0,1), 0))
                    leg.joint2.addRotate(time+self.jumpDuration/3, quaternion_from_axis_angle((0,0,1), 30))
                    leg.joint3.addRotate(time+self.jumpDuration/3, quaternion_from_axis_angle((0,0,1), -30))
                    leg.joint1.addRotate(time+self.jumpDuration*4/9, quaternion_from_axis_angle((0,0,1), -40))
                    leg.joint2.addRotate(time+self.jumpDuration*4/9, quaternion_from_axis_angle((0,0,1), -10))
                    leg.joint3.addRotate(time+self.jumpDuration*4/9, quaternion_from_axis_angle((0,0,1), 50))
                    leg.joint1.addRotate(time+self.jumpDuration*8/9, quaternion_from_axis_angle((0,0,1), -40))
                    leg.joint2.addRotate(time+self.jumpDuration*8/9, quaternion_from_axis_angle((0,0,1), -10))
                    leg.joint3.addRotate(time+self.jumpDuration*8/9, quaternion_from_axis_angle((0,0,1), 50))
                    leg.joint1.addRotate(time+self.jumpDuration, quaternion_from_axis_angle((0,0,1), 0))
                    leg.joint2.addRotate(time+self.jumpDuration, quaternion_from_axis_angle((0,0,1), 0))
                    leg.joint3.addRotate(time+self.jumpDuration, quaternion_from_axis_angle((0,0,1), 0))

            
            if (key == glfw.KEY_DOWN):

                if (self.isHappy):
                    self.mouth.transform = identity()
                else:
                    self.mouth.transform = rotate((1,0,0), 180) @ translate(0,-1,0)
                self.isHappy = not self.isHappy

            if (key == glfw.KEY_LEFT or key == glfw.KEY_RIGHT):
                self.isMoving = True
                self.endMove = time+self.rotateDuration
                self.addRotate(time, quaternion_from_axis_angle((0,1,0), self.rotation))
                self.rotation = self.rotation + (self.rotationDiff if key == glfw.KEY_LEFT else -self.rotationDiff)
                self.addRotate(time+self.rotateDuration, quaternion_from_axis_angle((0,1,0), self.rotation))
                for leg in [self.legL1, self.legL3, self.legR2, self.legR4]:
                    leg.joint1.addRotate(time, quaternion())
                    leg.joint2.addRotate(time, quaternion())
                    leg.joint3.addRotate(time, quaternion())
                    leg.joint1.addRotate(time+self.rotateDuration*1/3, quaternion_from_axis_angle((0,0,1), 20))
                    leg.joint2.addRotate(time+self.rotateDuration*1/3, quaternion_from_axis_angle((0,0,1), -10))
                    leg.joint3.addRotate(time+self.rotateDuration*1/3, quaternion_from_axis_angle((0,0,1), -10))
                    leg.joint1.addRotate(time+self.rotateDuration*2/3, quaternion())
                    leg.joint2.addRotate(time+self.rotateDuration*2/3, quaternion())
                    leg.joint3.addRotate(time+self.rotateDuration*2/3, quaternion())

                for leg in [self.legL2,self.legL4, self.legR1, self.legR3]:
                    leg.joint1.addRotate(time+self.rotateDuration/3, quaternion())
                    leg.joint2.addRotate(time+self.rotateDuration/3, quaternion())
                    leg.joint3.addRotate(time+self.rotateDuration/3, quaternion())
                    leg.joint1.addRotate(time+self.rotateDuration*2/3, quaternion_from_axis_angle((0,0,1), 20))
                    leg.joint2.addRotate(time+self.rotateDuration*2/3, quaternion_from_axis_angle((0,0,1), -10))
                    leg.joint3.addRotate(time+self.rotateDuration*2/3, quaternion_from_axis_angle((0,0,1), -10))
                    leg.joint1.addRotate(time+self.rotateDuration, quaternion())
                    leg.joint2.addRotate(time+self.rotateDuration, quaternion())
                    leg.joint3.addRotate(time+self.rotateDuration, quaternion())

            """if (key == glfw.KEY_C):
                for claw in [self.clawL, self.clawR]:
                    if (self.isClawTight):"""
                        

        """self.elevation += 1 * int(key == glfw.KEY_UP)
        self.elevation -= 1 * int(key == glfw.KEY_DOWN)
        self.transform = translate(0, self.elevation, 0)"""
        super().key_handler(key)



