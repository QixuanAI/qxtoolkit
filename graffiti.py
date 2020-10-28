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


class EfficientMotionDecorator(MotionDecorator):
    """Multi-thread motion decorator"""
    pass