#! /usr/bin/env python
'''
Description : Get seriese of images from either a camera device, a video file or a folder of images.
FilePath    : /cvutils/cvutils/imgetter.py
Author      : qxsoftware@163.com
Date        : 2020-09-25 16:51:21
LastEditTime: 2020-12-25 14:14:35
Refer to    : https://github.com/QixuanAI/cvutils
'''

import cv2
import numpy as np
import os
import glob
import re
from datetime import datetime
try: # for package import
    from ._inner import *
except: # for directly running
    from _inner import *

__all__ = ["ImagesGetter"]


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
        self._adjust = []
        self.scale = scale
        if abs(scale) > 1:
            self._adjst.append(lambda img: cv2.resize(
                img, (0, 0), fx=scale, fy=scale, interpolation=cv2.INTER_CUBIC))
        elif 0 < abs(scale) < 1:
            self._adjst.append(lambda img: cv2.resize(
                img, (0, 0), fx=scale, fy=scale, interpolation=cv2.INTER_AREA))
        self.reset()

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
            for adj in self._adjust:
                img = adj(img)
            self._out_count += 1
            yield img
        if self.autorelease:
            self._release()

    def __iter__(self):
        return self

    def __next__(self):
        if self.isAvailable:
            img = self._next(self.interval)
            for adj in self._adjust:
                img = adj(img)
            self._out_count += 1
            return img
        if self.autorelease:
            self._release()
        raise StopIteration

    def get(self) -> np.ndarray:
        print("[i]Recommoned Usage: directly call this object." +
              " Example:\r\nig = ImageGetter(0)\r\nfor img in ig:\r\n\tcv2.imshow('win', img)")
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

        def _init_read(interval=0, waitSec=0.5):
            if (datetime.now()-self._init_time).seconds < waitSec:
                return self.welcome
            ret, frame = self.cap.read()
            self._next = _next
            return frame if ret else None

        self.cap = cv2.VideoCapture(int(device))
        if not self.cap.isOpened():
            report(WARNING, "Can't open camera device " + str(device))
        self.width = int(self.scale * self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.height = int(self.scale * self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.welcome = np.zeros((self.height, self.width, 3), dtype=np.uint8)
        text = "Initiling Camera..."
        font = cv2.FONT_HERSHEY_DUPLEX
        (tw, th), _ = cv2.getTextSize(text, font, 1, 1)
        org = ((self.width-tw)//2, (self.height+th)//2)
        self.welcome = cv2.putText(
            self.welcome, text, org, font, 1, (192, 168, 31), 1)

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
        self._init_time = datetime.now()
        self._next = _init_read if warmup_num > 0 else _next
        self._is_end = lambda: False
        self._release = self.cap.release

    def __setup_video__(self, file: str):
        def _next(interval=0):
            if interval > 0:
                self.crt_idx += interval
                self.cap.set(cv2.CAP_PROP_POS_FRAMES, self.crt_idx)
            ret, frame = self.cap.read()
            self.crt_idx += 1
            return frame if ret else None
        self.cap = cv2.VideoCapture(file)
        if not self.cap.isOpened():
            report(WARNING, "Can't open video file " + str(file))
        self.width = int(self.scale * self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.height = int(self.scale * self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.crt_idx = 0
        self._fps = lambda: self.cap.get(cv2.CAP_PROP_FPS)
        self.len = self.cap.get(cv2.CAP_PROP_FRAME_COUNT)
        self._init_time = datetime.now()
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
        self.width, self.height = None, None
        self.crt_idx = 0
        self.len = len(imgs)
        self._fps = lambda: -1.
        self._init_time = datetime.now()
        self._next = _next
        self._is_end = lambda: self.crt_idx >= self.len
        self._release = lambda: None


if __name__ == "__main__":
    import sys
    getter = ImagesGetter(0, cam_warmup=0)
    WIN_NAME='press q to quit'
    cv2.namedWindow(WIN_NAME, cv2.WINDOW_NORMAL)

    for i, img in enumerate(getter):
        if img is None:
            print(i, ' - None to show')
            continue
        print(i, end='\r')
        cv2.imshow(WIN_NAME, img)
        pressed = cv2.waitKey(1)
        if pressed == ord('q'):
            break
        elif pressed == ord('s'):
            path = "IMG_"+datetime.now().strftime("%Y%m%d-%H%M%S")+'.jpg'
            cv2.imwrite(path, img)
            cv2.displayStatusBar(WIN_NAME, 'Save photo to:\n'+path, 3000)
