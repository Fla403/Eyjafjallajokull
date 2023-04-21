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
        crabyShader = Shader("craby.vert", "craby.frag")

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
        crabyShader = Shader("craby.vert", "craby.frag")

        sphere = Sphere(crabyShader, 3, (.9, 0.5, 0, 1))
        sphere.transformByMatrix(scale(1,0.5,1))
        sphere.stretch(1, 0.5, 1)

        self.add(sphere)

class Eye(KeyFrameControlNode):

    def __init__(self):
        super().__init__()
        crabyShader = Shader("craby.vert", "craby.frag")


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

        crabyShader = Shader("craby.vert", "craby.frag")

        sphere = Sphere(crabyShader, 3, (0.05,0.05,0.05))
        sphere.transformByMatrix(scale(1,0.15,0.15))
        sphere.modelling(flattening=0.8, mitigation_pos=1, mitigation_neg=1, inflation_pos=0.9, inflation_neg=0.9, xMax=1, yMax=0.2, zMax=0.2)

        self.add(sphere)

class Claw(KeyFrameControlNode):
    def __init__(self):
        super().__init__()
        crabyShader = Shader("craby.vert", "craby.frag")

        sphere1 = Sphere(crabyShader, 3, (0.85, 0.45, 0))
        sphere1.transformByMatrix(scale(1,0.3,0.3))
        sphere1.modelling(flattening=0.8, mitigation_pos=0.95, mitigation_neg=0.5, inflation_pos=0.5, inflation_neg=0.5, xMax=1, yMax=0.3, zMax=0.3)

        clawNode1 = Node(transform= rotate((0,0,1), 60) @ scale(0.8) @ translate(0.8,-0.7,0))
        clawNode1.add(sphere1)

        self.joint1 = KeyFrameControlNode()
        self.joint1.add(clawNode1)

        sphere2 = Sphere(crabyShader, 4, (0.8, 0.4, 0))
        sphere2.transformByMatrix(scale(1,0.3,0.5))
        sphere2.modelling(flattening=-0.8, mitigation_pos=0.98, mitigation_neg=0.5, inflation_pos=0.5, inflation_neg=0.5, xMax=1, yMax=0.3, zMax=0.5)

        clawNode2 = Node(transform=translate(0.8,0.7,0))
        clawNode2.add(sphere2)
        
        link1 = Node(transform= scale(0.9) @ rotate((0,0,1), 180))
        link1.add(self.joint1)
        link1.add(clawNode2)

        sphere3 = Sphere(crabyShader, 3, (0.90, 0.5, 0))
        sphere3.transformByMatrix(scale(1,0.15,0.15))
        sphere3.modelling(flattening=0.6, mitigation_pos=0.8, mitigation_neg=0.8, inflation_pos=1, inflation_neg=1, xMax=1, yMax=0.15, zMax=0.15)

        clawNode3 = Node(transform=translate(0.8,-0.45,0))
        clawNode3.add(sphere3)

        link2 = Node(transform=rotate((0,0,1), 90) @ translate(-1.6,0,0))
        link2.add(link1)
        link2.add(clawNode3)

        sphere4 = Sphere(crabyShader, 3, (0.95, 0.55, 0))
        sphere4.transformByMatrix(scale(1,0.2,0.2))
        sphere4.modelling(flattening=0.2, mitigation_pos=1, mitigation_neg=1, inflation_pos=0.8, inflation_neg=0.8, xMax=1, yMax=0.2, zMax=0.2)

        clawNode4 = Node(transform=scale(1.1) @ translate(0.8,-0.1,0))
        clawNode4.add(sphere4)

        link3 = Node(transform=translate(-1.8,0.02,0))
        link3.add(link2)
        link3.add(clawNode4)

        self.joint2 = KeyFrameControlNode()
        self.joint2.add(link3)

        self.add(self.joint2)


class Craby(KeyFrameControlNode):
    def __init__(self):
        super().__init__()


        self.elevation = 2
        self.walkDistance = 1
        self.rotationDiff = 15
        self.clawRotationMin = -40
        self.clawRotationMax = 130
        self.clawRotationDiff = 10
        
        self.jumpDuration = 0.8
        self.walkDuration = 0.2
        self.rotateDuration = 0.2
        self.clawDuration = 0.1
        self.clawMoveDuration = 0.1

        self.isMoving = False
        self.isLeftClawMoving = False
        self.isLeftClawOpen = True
        self.isRightClawMoving = False
        self.isRightClawOpen = True
        
        self.endMove = 0
        self.endLeftClawMove = 0
        self.endRightClawMove = 0

        self.position = vec(0,0,0)
        self.rotation = 0
        self.clawLeftRotation = 0
        self.clawRightRotation = 0
        self.isHappy = False


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
        clawLNode = Node(transform=translate(0.6,-0.1,0.4) @ rotate((0,1,0), -20) @ scale(0.25) @ rotate((0,0,1), -45) @ rotate((1,0,0), 310) @ rotate((0,1,0), 180))
        clawLNode.add(self.clawL)

        self.clawR = Claw()
        clawRNode = Node(transform=translate(-0.6,-0.1,0.4)  @ rotate((0,1,0), 20) @ scale(0.25) @ rotate((0,0,1), 45) @ rotate((1,0,0), 310))
        clawRNode.add(self.clawR)

        claws = Node()
        claws.add(clawLNode)
        claws.add(clawRNode)

        self.add(self.body)
        self.add(face)
        self.add(legs)
        self.add(claws)

    def legs_move_animation(self, time, duration):

        for leg in [self.legL1, self.legL3, self.legR2, self.legR4]:
            leg.joint1.addRotate(time, quaternion())
            leg.joint2.addRotate(time, quaternion())
            leg.joint3.addRotate(time, quaternion())
            leg.joint1.addRotate(time+duration*1/3, quaternion_from_axis_angle((0,0,1), 20))
            leg.joint2.addRotate(time+duration*1/3, quaternion_from_axis_angle((0,0,1), -10))
            leg.joint3.addRotate(time+duration*1/3, quaternion_from_axis_angle((0,0,1), -10))
            leg.joint1.addRotate(time+duration*2/3, quaternion())
            leg.joint2.addRotate(time+duration*2/3, quaternion())
            leg.joint3.addRotate(time+duration*2/3, quaternion())

        for leg in [self.legL2,self.legL4, self.legR1, self.legR3]:
            leg.joint1.addRotate(time+duration/3, quaternion())
            leg.joint2.addRotate(time+duration/3, quaternion())
            leg.joint3.addRotate(time+duration/3, quaternion())
            leg.joint1.addRotate(time+duration*2/3, quaternion_from_axis_angle((0,0,1), 20))
            leg.joint2.addRotate(time+duration*2/3, quaternion_from_axis_angle((0,0,1), -10))
            leg.joint3.addRotate(time+duration*2/3, quaternion_from_axis_angle((0,0,1), -10))
            leg.joint1.addRotate(time+duration, quaternion())
            leg.joint2.addRotate(time+duration, quaternion())
            leg.joint3.addRotate(time+duration, quaternion())


    def key_handler(self, key):

        # COMMANDES POUR FAIRE BOUGER CRABY :

        # w : avancer
        # x : reculer
        # q : se deplacer sur la gauche
        # d : se deplacer sur la droite
        # fleche gauche : se tourner sur la gauche
        # fleche droite : sse tourner sur la droite
        # fleche haut : sauter
        # fleche bas : changer le sourire
        # 1 (pave numerique) : baisser la pince gauche
        # 7 (pave numerique) : lever la pince gauche
        # 4 (pave numerique) : fermer/ouvrir la pince gauche
        # 3 (pave numerique) : baisser la pince droite
        # 9 (pave numerique) : lever la pince droite
        # 6 (pave numerique) : fermer/ouvrir la pince droite

        time = glfw.get_time()

        if (self.isMoving == True and time >= self.endMove):
            self.isMoving = False
        if (self.isLeftClawMoving == True and time >= self.endLeftClawMove):
            self.isLeftClawMoving = False
        if (self.isRightClawMoving == True and time >= self.endRightClawMove):
            self.isRightClawMoving = False

        if (not self.isMoving):

            if (key == glfw.KEY_UP): 
                self.isMoving = True
                self.endMove = time+self.jumpDuration
                self.addTranslate(time, self.position)
                self.addTranslate(time+self.jumpDuration/3, vec(self.position[0],self.position[1]-0.25,self.position[2]))
                self.addTranslate(time+self.jumpDuration*2/3, vec(self.position[0],self.position[1]+self.elevation,self.position[2]))
                self.addTranslate(time+self.jumpDuration, self.position)
                for leg in [self.legL1, self.legL2, self.legL3, self.legL4, self.legR1, self.legR2, self.legR3, self.legR4]:
                    leg.joint1.addRotate(time, quaternion())
                    leg.joint2.addRotate(time, quaternion())
                    leg.joint3.addRotate(time, quaternion())
                    leg.joint1.addRotate(time+self.jumpDuration/3, quaternion_from_axis_angle((0,0,1), 0))
                    leg.joint2.addRotate(time+self.jumpDuration/3, quaternion_from_axis_angle((0,0,1), 40))
                    leg.joint3.addRotate(time+self.jumpDuration/3, quaternion_from_axis_angle((0,0,1), -40))
                    leg.joint1.addRotate(time+self.jumpDuration*4/9, quaternion_from_axis_angle((0,0,1), -50))
                    leg.joint2.addRotate(time+self.jumpDuration*4/9, quaternion_from_axis_angle((0,0,1), -20))
                    leg.joint3.addRotate(time+self.jumpDuration*4/9, quaternion_from_axis_angle((0,0,1), 60))
                    leg.joint1.addRotate(time+self.jumpDuration*8/9, quaternion_from_axis_angle((0,0,1), -50))
                    leg.joint2.addRotate(time+self.jumpDuration*8/9, quaternion_from_axis_angle((0,0,1), -20))
                    leg.joint3.addRotate(time+self.jumpDuration*8/9, quaternion_from_axis_angle((0,0,1), 60))
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
                self.legs_move_animation(time, self.rotateDuration)
                
            if (key == glfw.KEY_Z or key == glfw.KEY_X or key == glfw.KEY_A or key == glfw.KEY_D):
                self.isMoving = True
                self.endMove = time+self.walkDuration
                self.addTranslate(time, self.position)
                if (key == glfw.KEY_Z):
                    self.position = vec(self.position[0] + self.walkDistance*math.sin(math.radians(self.rotation)), self.position[1], self.position[2] + self.walkDistance*math.cos(math.radians(self.rotation)))
                elif (key == glfw.KEY_X):
                    self.position = vec(self.position[0] - self.walkDistance*math.sin(math.radians(self.rotation)), self.position[1], self.position[2] - self.walkDistance*math.cos(math.radians(self.rotation)))
                elif (key == glfw.KEY_A):
                    self.position = vec(self.position[0] + self.walkDistance*math.cos(math.radians(self.rotation)), self.position[1], self.position[2] - self.walkDistance*math.sin(math.radians(self.rotation)))
                elif (key == glfw.KEY_D):
                    self.position = vec(self.position[0] - self.walkDistance*math.cos(math.radians(self.rotation)), self.position[1], self.position[2] + self.walkDistance*math.sin(math.radians(self.rotation)))
                
                self.addTranslate(time + self.walkDuration, self.position)
                self.legs_move_animation(time, self.walkDuration)

        if (not self.isLeftClawMoving):

            if (key == glfw.KEY_KP_4):
                self.isLeftClawMoving = True
                self.endLeftClawMove = time+self.clawDuration
                if (self.isLeftClawOpen):
                    self.clawL.joint1.addRotate(time, quaternion())
                    self.clawL.joint1.addRotate(time+self.clawDuration, quaternion_from_axis_angle((0,0,1), -33))
                else:
                    self.clawL.joint1.addRotate(time, quaternion_from_axis_angle((0,0,1), -33))
                    self.clawL.joint1.addRotate(time+self.clawDuration, quaternion())
                self.isLeftClawOpen = not self.isLeftClawOpen

            if (key == glfw.KEY_KP_1 and self.clawLeftRotation > self.clawRotationMin):
                self.isLeftClawMoving = True
                self.endLeftClawMove = time+self.clawMoveDuration
                self.clawL.addRotate(time, quaternion_from_axis_angle((1,-0.8,0), self.clawLeftRotation))
                self.clawLeftRotation -= self.clawRotationDiff
                self.clawL.addRotate(time+self.clawMoveDuration, quaternion_from_axis_angle((1,-0.8,0), self.clawLeftRotation))

            if (key == glfw.KEY_KP_7 and self.clawLeftRotation < self.clawRotationMax):
                self.isLeftClawMoving = True
                self.endLeftClawMove = time+self.clawMoveDuration
                self.clawL.addRotate(time, quaternion_from_axis_angle((1,-0.8,0), self.clawLeftRotation))
                self.clawLeftRotation += self.clawRotationDiff
                self.clawL.addRotate(time+self.clawMoveDuration, quaternion_from_axis_angle((1,-0.8,0), self.clawLeftRotation))

        if (not self.isRightClawMoving):

            if (key == glfw.KEY_KP_6):
                self.isRightClawMoving = True
                self.endRightClawMove = time+self.clawDuration
                if (self.isRightClawOpen):
                    self.clawR.joint1.addRotate(time, quaternion())
                    self.clawR.joint1.addRotate(time+self.clawDuration, quaternion_from_axis_angle((0,0,1), -33))
                else:
                    self.clawR.joint1.addRotate(time, quaternion_from_axis_angle((0,0,1), -33))
                    self.clawR.joint1.addRotate(time+self.clawDuration, quaternion())
                self.isRightClawOpen = not self.isRightClawOpen

            if (key == glfw.KEY_KP_3 and self.clawRightRotation < -self.clawRotationMin):
                self.isRightClawMoving = True
                self.endRightClawMove = time+self.clawMoveDuration
                self.clawR.addRotate(time, quaternion_from_axis_angle((1,-0.8,0), self.clawRightRotation))
                self.clawRightRotation += self.clawRotationDiff
                self.clawR.addRotate(time+self.clawMoveDuration, quaternion_from_axis_angle((1,-0.8,0), self.clawRightRotation))

            if (key == glfw.KEY_KP_9 and self.clawRightRotation > -self.clawRotationMax):
                self.isRightClawMoving = True
                self.endRightClawMove = time+self.clawMoveDuration
                self.clawR.addRotate(time, quaternion_from_axis_angle((1,-0.8,0), self.clawRightRotation))
                self.clawRightRotation -= self.clawRotationDiff
                self.clawR.addRotate(time+self.clawMoveDuration, quaternion_from_axis_angle((1,-0.8,0), self.clawRightRotation))

        super().key_handler(key)



