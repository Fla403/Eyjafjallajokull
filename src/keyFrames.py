#! /usr/bin/env python3

from bisect import bisect_left

import OpenGL.GL as GL
import glfw
import numpy as np

from core import Node, vec
from transform import (lerp, quaternion_slerp, quaternion_matrix, translate, rotate,
                       scale, identity, quaternion)


# -------------- Keyframing Utilities TP6 ------------------------------------
class KeyFrames:
    """ Stores keyframe pairs for any value type with interpolation_function"""
    def __init__(self, time_value_pairs, interpolation_function=lerp):
        if isinstance(time_value_pairs, dict):
            time_value_pairs = time_value_pairs.items()
        self.keyframes = sorted(((key[0], key[1]) for key in time_value_pairs))
        self.times, self.values = zip(*self.keyframes)
        self.interpolate = interpolation_function

    def value(self, time):
        """ Computes interpolated value from keyframes, for a given time """

        if time <= self.times[0]:
            return self.values[0]
        if time >= self.times[-1]:
            return self.values[-1]

        t_i = bisect_left(self.times, time) - 1

        f = (time - self.times[t_i]) / (self.times[t_i + 1] - self.times[t_i])
        return self.interpolate(self.values[t_i], self.values[t_i + 1], f)

    def add(self, time, value):
        self.keyframes.append((time, value))
        self.times, self.values = zip(*self.keyframes)


class TransformKeyFrames:
    """ KeyFrames-like object dedicated to 3D transforms """
    def __init__(self, translate_keys, rotate_keys, scale_keys):
        """ stores 3 keyframe sets for translation, rotation, scale """
        self.translate_keyFrames = KeyFrames(translate_keys)
        self.rotate_keyFrames = KeyFrames(rotate_keys)
        self.scale_keyFrames = KeyFrames(scale_keys)


    def value(self, time):
        """ Compute each component's interpolation and compose TRS matrix """
        translate_mat = translate(self.translate_keyFrames.value(time))
        rotate_mat = quaternion_matrix(self.rotate_keyFrames.value(time))
        scale_mat = scale(self.scale_keyFrames.value(time))

        return translate_mat @ rotate_mat @ scale_mat

    def addTranslate(self, time, translation):
        self.translate_keyFrames.add(time, translation)
    
    def addRotate(self, time, rotation):
        self.rotate_keyFrames.add(time, rotation)



class KeyFrameControlNode(Node):
    """ Place node with transform keys above a controlled subtree """
    def __init__(self, trans_keys={0: vec(0,0,0), 10: vec(0,0,0)}, rot_keys={0: quaternion(), 10: quaternion()}, scale_keys={0: vec(1,1,1),10: vec(1,1,1)}, transform=identity()):
        super().__init__(transform=transform)
        self.keyframes = TransformKeyFrames(trans_keys, rot_keys, scale_keys)

    def draw(self, primitives=GL.GL_TRIANGLES, **uniforms):
        """ When redraw requested, interpolate our node transform from keys """
        self.transform = self.keyframes.value(glfw.get_time())
        super().draw(primitives=primitives, **uniforms)
    
    def addTranslate(self, time, translation):
        self.keyframes.addTranslate(time, translation)

    def addRotate(self, time, rotation):
        self.keyframes.addRotate(time, rotation)