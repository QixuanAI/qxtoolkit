#! /usr/bin/env python
# Get seriese of images from either a camera device, a video file or a folder of images.
# author:liuqixuan
# date:2020/9/25
# email:qxsoftware@163.com
# url:https://github.com/QixuanAI/cvutils

import cv2
import os
import glob
import re
from _inner import *
from static_decorator import StaticDecorator


class ImagesGetter(object):
    """
    Quickly get seriese of images from either of a camera, a video or a directory of pictures.
    """

    def __init__(self, src, interval=0, scale=1, img_ext='.jpg', cam_warmup=-1, autorelease=True):
        """
        Args:
            @src: can be a int (for a camera device number),
                           a path to a video file,
                           or a path to a directory with seriese of images.
            @interval: the interval of frame skip.
            @scale: a scale factor for output images.
            @img_ext: a filter to determin what kinds of images can be loaded.
                        default is '.jpg'. It can alse be a tuple like ('.jpg', '.bmp').
            @cam_warmup: Since some cameras require a warm-up time, we can spend this time
                        by taking some useless photos. This parameter decides how many photos
                        we should take. 0 means None, negative number like -1 means autofit.
                        A proper value is 3 to 5 for most cameras.
            @autorelease: Release device or files after get all images.
            @errlevel: (Todo)Difined the action when meeting problems. Refer to global.py.
        """
        self.src = src
        self.interval = interval
        self.img_ext = img_ext
        self.cam_warmup = cam_warmup
        self.autorelease = autorelease
        self._is_end = lambda: True
        self.reset()
        if abs(scale) > 1:
            self._scale = lambda img: cv2.resize(
                img, (0, 0), fx=scale, fy=scale, interpolation=cv2.INTER_CUBIC)
        elif 0 < abs(scale) < 1:
            self._scale = lambda img: cv2.resize(
                img, (0, 0), fx=scale, fy=scale, interpolation=cv2.INTER_AREA)
        else:
            self._scale = lambda img: img

    @property
    def isAvailable(self):
        return not self._is_end()

    @property
    def FPS_interval(self):
        fps = self._fps()
        return fps / (self.interval+1) if fps >= 0 else -1

    @property
    def FPS_src(self):
        return self._fps()

    @property
    def FrameCount_interval(self):
        return int(self.len / (self.interval+1) if self.len >= 0 else -1)

    @property
    def FrameCount_src(self):
        return int(self.len)

    def __call__(self):
        while self.isAvailable:
            img = self._next(self.interval)
            img = self._scale(img)
            yield img
        if self.autorelease:
            self._release()

    def get(self):
        print("[i]Recommoned Usage: directly call this object with brackets ending." +
              " Example:\r\nfor img in ImageGetter(0)():\r\n\tcv2.imshow('win', img)")
        return self()

    def reset(self):
        # camera
        if isinstance(self.src, int) or re.match("[0-9]+$", self.src) is not None:
            self.__setup_cam__(self.src, self.cam_warmup)
        elif os.path.isfile(self.src):  # video
            self.__setup_video__(self.src)
        elif os.path.isdir(self.src):  # images
            self.__setup_images__(self.src, self.img_ext)

    def __setup_cam__(self, device: int, warmup_num: int):
        def _next(interval=0):
            ret, frame = self.cap.read()
            for _ in range(interval):
                ret, frame = self.cap.read()
            return frame if ret else None
        self.cap = cv2.VideoCapture(int(device))
        if not self.cap.isOpened():
            report(WARNING, "Can't open camera device " + str(device))
        warmup_num = 1000 if warmup_num < 0 else warmup_num
        for i in range(warmup_num):
            ret, frame = self.cap.read()
            if ret and frame is not None:
                if frame.any():
                    break
                else:
                    print(i)
            else:
                print(i)
        self.len = -1
        self._fps = lambda: self.cap.get(cv2.CAP_PROP_FPS)
        self._next = _next
        self._is_end = lambda: False
        self._release = self.cap.release

    def __setup_video__(self, file: str):
        def _next(interval=0):
            if interval > 0:
                self.crt_idx += interval
                self.cap.set(cv2.CAP_PROP_POS_FRAMES, self.crt_idx)
            ret, frame = self.cap.read()
            return frame if ret else None
        self.cap = cv2.VideoCapture(file)
        if not self.cap.isOpened():
            report(WARNING, "Can't open video file " + str(file))
        self.crt_idx = 0
        self._fps = lambda: self.cap.get(cv2.CAP_PROP_FPS)
        self.len = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
        self._next = _next
        self._is_end = lambda: self.crt_idx >= self.len
        self._release = lambda: self.cap.release

    def __setup_images__(self, dir: str, img_ext):
        def _next(interval=0):
            if interval > 0:
                self.crt_idx += interval
            img = cv2.imread(imgs[self.crt_idx])
            self.crt_idx += 1
            return img
        imgs = []
        if isinstance(img_ext, str):
            imgs = glob.glob(os.path.join(dir, '*'+img_ext))
        elif type(img_ext) in [tuple, list]:
            for ext in img_ext:
                imgs.extend(glob.glob(os.path.join(dir, '*'+ext)))
        if len(imgs) == 0:
            errreport()
            report(WARNING, "Can't find any images in " + str(dir))
        self.crt_idx = 0
        self.len = len(imgs)
        self._next = _next
        self._is_end = lambda: self.crt_idx >= self.len
        self._release = lambda: None


if __name__ == "__main__":
    import sys
    getter = ImagesGetter(0, cam_warmup=-1)
    cv2.namedWindow('press q to quit', cv2.WINDOW_NORMAL)

    def printf():
        print('\ntake a pic\n')
    cv2.createButton('cap', printf, 'userdata', cv2.QT_PUSH_BUTTON)
    for i, img in enumerate(getter.get()):
        if img is None:
            print(i, ' - None to show')
            continue
        print(i, end='\r')
        cv2.imshow('press q to quit', img)
        if cv2.waitKey(10) == ord('q'):
            break
