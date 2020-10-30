#! /usr/bin/env python
# Get seriese of images from either a camera device, a video file or a folder of images.
# author:liuqixuan
# date:2020/9/25
# email:qxsoftware@163.com
# url:https://github.com/QixuanAI/cvutils

import cv2
import numpy as np
import os
import glob
import re
from time import sleep
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
                        A proper value is 10 for most cameras.
            @autorelease: Release device or files after get all images.
            @errlevel: (Todo)Difined the action when meeting problems. Refer to global.py.
        """
        self.src = src
        self.interval = interval
        self.img_ext = img_ext
        self.cam_warmup = cam_warmup
        self.autorelease = autorelease
        self._out_count = 0
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
    def isAvailable(self) -> bool:
        return not self._is_end()

    @property
    def frameDelay(self) -> int:
        """Return a proper delay of two frames.
        It's useful in cv2.waitKey(delay=imggetter.frameDelay)."""
        return int(1000/self.FPS_interval) if self.FPS_interval > 0 else 33

    @property
    def FPS_interval(self) -> float:
        """Get FPS after caculating intervals.
        If the source is images, this returns -1."""
        fps = self._fps()
        return fps / self.interval if self.interval > 0 else fps

    @property
    def FPS_src(self) -> float:
        """Get FPS of the source.
        If the source is images, this returns -1."""
        return self._fps()

    @property
    def frameCount_interval(self) -> float:
        """Get count of total frames after caculating intervals.
        If the source is camera, this returns float('inf')"""
        return self.len / self.interval if self.interval > 0 else self.len

    @property
    def frameCount_src(self) -> float:
        """Get count of total frames of the source.
        If the source is camera, this returns float('inf')"""
        return self.len

    def __call__(self) -> np.ndarray:
        while self.isAvailable:
            img = self._next(self.interval)
            img = self._scale(img)
            self._out_count += 1
            yield img
        if self.autorelease:
            self._release()

    def get(self) -> np.ndarray:
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

        def _init_read(waitSec=2):
            if self._out_count < 1:
                ret, frame = self.cap.read()
                return frame if ret else None
            sleep(waitSec)
            ret, frame = self.cap.read()
            self._next = _next
            return frame if ret else None

        self.cap = cv2.VideoCapture(int(device))
        if not self.cap.isOpened():
            report(WARNING, "Can't open camera device " + str(device))
        # If warm_up is set to -1, we will try 1000 times to get a stable stream from camera.
        # If we can cap 5 pictures consecutively, the stream can be regarded as stable.
        warmup_num = 1000 if warmup_num < 0 else warmup_num
        test_pics = []
        for i in range(warmup_num):
            ret, frame = self.cap.read()
            if ret and frame is not None:
                test_pics.append(frame.any())
                if len(test_pics) > 5:
                    if all(test_pics):
                        break
                    test_pics.pop(0)
        del test_pics
        self.len = float('inf')
        self._fps = lambda: self.cap.get(cv2.CAP_PROP_FPS)
        self._next = _init_read if warmup_num > 0 else _next
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
        self.len = self.cap.get(cv2.CAP_PROP_FRAME_COUNT)
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
            report(WARNING, "Can't find any images in " + str(dir))
        self.crt_idx = 0
        self.len = len(imgs)
        self._fps = lambda: -1.
        self._next = _next
        self._is_end = lambda: self.crt_idx >= self.len
        self._release = lambda: None


if __name__ == "__main__":
    import sys
    getter = ImagesGetter('cal.mp4', cam_warmup=-1)
    cv2.namedWindow('press q to quit', cv2.WINDOW_NORMAL)

    def printf(state, *args):
        print(state, '\ntake a pic\n')
    # cv2.createButton('cap', printf, 'userdata', cv2.QT_PUSH_BUTTON)
    for i, img in enumerate(getter()):
        if img is None:
            print(i, ' - None to show')
            continue
        print(i, end='\r')
        cv2.imshow('press q to quit', img)
        if cv2.waitKey(getter.frameDelay-10) == ord('q'):
            break
