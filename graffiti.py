#! /usr/bin/env python
'''
Description: 
FilePath: /calibratecameras/cvutils/graffiti.py
Author: qxsoftware@163.com
Date: 2020-10-26 15:13:20
LastEditTime: 2020-10-30 18:54:36
Refer to: https://github.com/QixuanAI
'''
import cv2
from ._inner import *


class Graffiti:

    def __init__(self, canvas=None, motiontime=None, colortype=None):
        self.canvas = canvas
        self.motiontime = motiontime
        self.colortype = colortype

    @property
    def canvas(self):
        return self._canvas

    @canvas.setter
    def canvas(self, value):
        self._canvas = value

    @property
    def elapsedtime(self):
        return self._elapsed

    @property
    def motiontime(self):
        return self._time

    @motiontime.setter
    def motiontime(self, value):
        self._time=value

    @property
    def colortype(self):
        return self._colortype

    @colortype.setter
    def colortype(self,value):
        self._colortype=value

    def caption(self, text, img, elapsed, time):
        pass

    def subimage(self, subimg, img, elapsed, time):
        pass


    def putText(img, text, org, fontFace=cv2.FONT_HERSHEY_DUPLEX,fontScale=1.,color=[0,0,255],):
        img = cv2.putText(img, text, org, fontFace, fontScale, color, thickness=1, lineType=8, bottomLeftOrigin=False)
        return img

class EfficientMotionDecorator(MotionDecorator):
    """Multi-thread motion decorator"""
    pass