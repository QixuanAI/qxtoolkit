import cv2
import os
import glob
import re
from warnings import warn

VIDEO_EXT = ('.mp4', '.avi', '.mpg', '.mpeg', '.mov')
IMG_EXT = ('.jpg', '.jpeg', '.jpe', '.png', '.bmp', '.dib', '.tif', '.tiff')


class ImagesGetter(object):
    """
    Quickly get seriese of images from anyone of a camera, a video or a directory of pictures.
    """

    def __init__(self, src, interval=0, scale=1, img_ext='.jpg'):
        """
        Args:
            src: can be a int (for a camera device number),
                           a path to a video file,
                           or a path to a directory with seriese of images.
            interval: the interval of frame skip.
            scale: a scale factor for output images.
            img_ext: a filter to determin what kinds of images can be loaded.
                        default is '.jpg'. It can alse be a tuple like ('.jpg', '.bmp').
        """
        self.src = src
        self.interval = interval
        self.img_ext = img_ext
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
    def FPS(self):
        fps = self._fps()
        return fps / (self.interval+1) if fps >= 0 else -1

    @property
    def FrameCount(self):
        return self.len / (self.interval+1) if self.len >= 0 else -1

    def __call__(self):
        while self.isAvailable:
            img = self._next(self.interval)
            img = self._scale(img)
            yield img
        self._release()

    def get(self):
        print('Recommoned Usage: directly call this object with brackets ending." + \
            " Like this:\r\nfor img in ImageGetter(0)():\r\n\tcv2.imshow("win", img)')
        return self()

    def reset(self):
        # camera
        if type(self.src) == int or re.match("[0-9]+$", self.src) is not None:
            self.__setup_cam__(self.src)
        elif os.path.isfile(self.src):  # video
            self.__setup_video__(self.src)
        elif os.path.isdir(self.src):  # images
            self.__setup_images__(self.src, self.img_ext)

    def __setup_cam__(self, device: int):
        def _next(interval=0):
            ret, frame = self.cap.read()
            for _ in range(interval):
                ret, frame = self.cap.read()
            return frame if ret else None
        self.cap = cv2.VideoCapture(int(device))
        if not self.cap.isOpened():
            warn("Can't open camera device " + str(device))
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
            warn("Can't open video file " + str(file))
        self.crt_idx = 0
        self._fps = lambda: cap.get(cv2.CAP_PROP_FPS)
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
            warn("Can't find any images in " + str(dir))
        self.crt_idx = 0
        self.len = len(imgs)
        self._next = _next
        self._is_end = lambda: self.crt_idx >= self.len
        self._release = lambda: None


if __name__ == "__main__":
    import sys
    getter = ImagesGetter(0)
    cv2.namedWindow('press q to quit', cv2.WINDOW_NORMAL)
    for i, img in enumerate(getter.get()):
        if img is None:
            print(i, ' - None to show')
            continue
        print(i, end='\r')
        cv2.imshow('press q to quit', img)
        if cv2.waitKey(10) == ord('q'):
            break
