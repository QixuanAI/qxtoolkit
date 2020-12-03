#! /usr/bin/env python
'''
Description: A simple video recorder, support Windows and Linux.
Requirments: opencv-python>=4.2.0.34, numpy
Author: qxsoftware@163.com
Date: 2020-10-14 08:29:17
LastEditTime: 2020-12-03 09:57:00
Refer to: https://github.com/QixuanAI
'''

import os
import sys
import cv2
import argparse
import numpy as np
from pathlib import Path
from warnings import warn
from datetime import datetime

__all__=["cam_record","parse_args","VERSION"]


VERSION = "1.0.0"

CODEC = {
    "small": ["mp4v", '.mp4'],
    "normal": ["DIVX", '.avi'],
    "lossless": ["HFYU", '.avi'],
}

WIN_NAME = "Press h for help"


def get_media_folder():
    """Return system default picture and video folder"""
    pic, video = "Pictures", "Videos"
    if sys.platform == 'linux':
        with open(Path.home()/'.config/user-dirs.dirs') as f:
            for i in f.readlines():
                i = i.strip()
                if i.startswith('XDG_PICTURES_DIR'):
                    pic = i.split('=')[-1].strip("\"'").replace('$HOME', '~')
                elif i.startswith('XDG_VIDEOS_DIR'):
                    video = i.split('=')[-1].strip("\"'").replace('$HOME', '~')
    elif sys.platform == 'win32':
        import re
        import winreg
        keys = winreg.OpenKey(
            winreg.HKEY_CURRENT_USER, r'Software\Microsoft\Windows\CurrentVersion\Explorer\User Shell Folders')
        pic = winreg.QueryValueEx(keys, 'My Pictures')[0]
        video = winreg.QueryValueEx(keys, 'My Video')[0]
        for name in re.findall('%([^%]+)%', pic):
            pic = pic.replace("%"+name+"%", os.environ[name])
        for name in re.findall('%([^%]+)%', video):
            video = video.replace("%"+name+"%", os.environ[name])
    pic = Path(pic).expanduser().resolve()
    video = Path(video).expanduser().resolve()
    return pic, video


PICTURE, VIDEO = get_media_folder()


class VideoCapture:
    def __init__(self, cam_id):
        if not self.__setup__(cam_id):
            warn("[!]Can't open camera device " + str(cam_id))

    def isOpened(self):
        return self.cam.isOpened()

    def read(self):
        return self.cam.read()

    @property
    def shape(self):
        return self.width, self.height

    def __setup__(self, cam_id):
        try:
            cam = cv2.VideoCapture(cam_id)
            if cam.isOpened():
                self.cam = cam
                self.ID = cam_id
                self.FPS = cam.get(cv2.CAP_PROP_FPS)
                self.width = int(cam.get(cv2.CAP_PROP_FRAME_WIDTH))
                self.height = int(cam.get(cv2.CAP_PROP_FRAME_HEIGHT))
                return True
            else:
                raise RuntimeError("Can't open camera device " + str(cam_id))
        except:
            return False

    def changeCamera(self, cam_id):
        if cam_id == self.ID:
            return True
        if not self.__setup__(cam_id):
            warn("[!]Failed to change camera, can't open device " + str(cam_id))
            return False
        return True


class FakeWriter:
    def __init__(self, *args):
        pass

    def write(self, frame):
        pass

    def release(self):
        pass


class VideoWriter:
    writer = None

    def __init__(self, path, fourcc: str, fps, size):
        self.path = str(path)
        os.makedirs(os.path.dirname(self.path), exist_ok=True)
        fourcc = cv2.VideoWriter_fourcc(*fourcc)
        self.fps = fps
        self.size = size
        self.writer = cv2.VideoWriter(self.path, fourcc, self.fps, self.size)
        assert self.writer, "Can't initialize VideoWriter."

    def write(self, frame):
        self.writer.write(frame)

    def release(self):
        self.writer.release()

    def __del__(self):
        if self.writer:
            self.writer.release()


def get_camera_ids(candidate_ids=[]):
    """find availabel cameras on this platform"""
    available_ids = []
    if candidate_ids is None or len(candidate_ids) == 0:
        if sys.platform == 'linux':
            candidate_ids = [int(x.name[5:])
                             for x in Path("/dev").glob("video*")]
        elif sys.platform == 'win32':
            candidate_ids = list(range(20))
    for d in candidate_ids:
        try:
            cam = cv2.VideoCapture(d)
            if cam.isOpened():
                available_ids.append(d)
        finally:
            cam.release()
    return available_ids


def get_proper_size(cam_w, cam_h):
    try:
        import tkinter as tk
        win = tk.Tk()
        win.withdraw()
        screen_w = win.winfo_screenwidth()
        screen_h = win.winfo_screenheight()
        win.destroy()
        if cam_w <= screen_w and cam_h <= screen_h:
            pro_w, pro_h = cam_w, cam_h
        else:
            ratio = cam_w / cam_h
            # If Screen W-H ratio is bigger than camera W-H ratio
            if screen_w / screen_h > ratio:
                # then the proper height is 2/3 of screen
                pro_h = int(2 * screen_h / 3)
                # and the proper width can get from ratio.
                pro_w = int(pro_h * ratio)
            else:
                # otherwise, the proper width is 2/3 of screen
                pro_w = int(2 * screen_w / 3)
                # and the proper height can get from ratio.
                pro_h = int(pro_w / ratio)
    except:
        pro_w, pro_h = 0, 0
    return pro_w, pro_h


def init_window(fixed: bool, size, cam: VideoCapture, cam_ids, cam_idx, text="Initialing Camera..."):
    def changeCamera(cam_idx):
        if cam.changeCamera(cam_ids[cam_idx]):
            title = "Cam {} | {}".format(cam.ID, WIN_NAME)
            cv2.setWindowTitle(WIN_NAME, title)

    width, height = size
    welcom = np.zeros((height, width, 3), dtype=np.uint8)
    font = cv2.FONT_HERSHEY_DUPLEX
    (tw, th), _ = cv2.getTextSize(text, font, 1, 1)
    org = ((width-tw)//2, (height+th)//2)
    welcom = cv2.putText(welcom, text, org, font, 1, (192, 168, 31), 1)
    win_flag = cv2.WINDOW_KEEPRATIO | cv2.WINDOW_GUI_EXPANDED
    win_flag |= cv2.WINDOW_AUTOSIZE if fixed else cv2.WINDOW_NORMAL
    cv2.namedWindow(WIN_NAME, win_flag)
    title = "Cam {} | {}".format(cam.ID, WIN_NAME)
    cv2.setWindowTitle(WIN_NAME, title)
    cv2.resizeWindow(WIN_NAME, *size)
    cv2.createTrackbar("Change Camera:", WIN_NAME, cam_idx,
                       len(cam_ids)-1, changeCamera)
    cv2.imshow(WIN_NAME, welcom)
    cv2.waitKey(1000)
    return True


def cam_record(args):
    cam_ids = get_camera_ids(args.cam_ids)
    if not cam_ids:
        raise RuntimeError("Can't find any available cameras.")
    cam_id = cam_ids[0]
    itval = int(args.interval)
    HELP_MSG = "Keyboard shortcuts:\nq - quit\ns - save picture" + \
        "\n0~{} - Change camera device\n\n".format(min(9, len(cam_ids))) +\
        "h - Show this help"
    cam = VideoCapture(cam_id)
    if not cam.isOpened():
        raise RuntimeError("Can't open camera, device id: %d" % cam_id)
    fps = cam.FPS if itval == 0 else 1000/itval
    cam_w, cam_h = cam.shape

    if args.record:
        saveto = Path(args.saveto)
        fourcc, suffix = CODEC[args.quality]
        if not saveto.suffix:  # Suppose to be a dictionary
            saveto = saveto / "VID_cam{}_{}{}".format(
                cam.ID, datetime.now().strftime("%Y%m%d-%H%M%S"), suffix)
        elif saveto.suffix != suffix:
            warn("Fourcc codec '" + fourcc + "' does't match suffix " + path.suffix +
                 ", change save path to" + path.with_suffix(suffix))
            path = path.with_suffix(fourcc)
        out = VideoWriter(saveto, fourcc, fps, (cam_w, cam_h))
        print("Save to", out.path)
        itval = 1
    else:
        out = FakeWriter()
        itval = int(1000/fps if itval == 0 else itval)
    try:
        init_window(args.fixedsize, get_proper_size(
            cam_w, cam_h), cam, cam_ids, 0)
        while cam.isOpened():
            ret, frame = cam.read()
            if ret and frame.shape > (0, 0):
                if args.flip:
                    frame = cv2.flip(frame, 1)
                cv2.imshow(WIN_NAME, frame)
            else:
                warn("[!]No responding from camera " + str(cam.ID))
                continue
            out.write(frame)
            pressed = cv2.waitKey(itval)
            # Close Button Clicked
            if cv2.getWindowProperty(WIN_NAME, cv2.WND_PROP_VISIBLE) < 1:
                break
            if pressed == ord('q'):
                break
            elif 0 <= pressed-ord('0') < min(10, len(cam_ids)):
                new_id = cam_ids[pressed-ord('0')]
                if new_id == cam.ID:
                    cv2.displayOverlay(
                        WIN_NAME, "Already camra "+str(new_id), 2000)
                elif cam.changeCamera(new_id):
                    # cv2.destroyWindow(WIN_NAME)
                    new_title = "Cam {} | {}".format(cam.ID, WIN_NAME)
                    cv2.setWindowTitle(WIN_NAME, new_title)
                    # init_window(WIN_NAME, args.fixedsize, get_proper_size(
                    #     cam_w, cam_h), cam, cam_ids, pressed-ord('0'))
                    cv2.setTrackbarPos(
                        "Change Camera:", WIN_NAME, pressed-ord('0'))
                    cv2.displayOverlay(
                        WIN_NAME, "Change to camera " + str(cam.ID), 2000)
                else:
                    cv2.displayOverlay(
                        WIN_NAME, "Fail to change camera " + str(new_id), 2000)

            elif pressed == ord('h'):
                cv2.displayOverlay(WIN_NAME, HELP_MSG, 5000)
            elif pressed == ord('s'):
                path = os.path.join(
                    PICTURE, "IMG_cam"+str(cam_id) + datetime.now().strftime("%Y%m%d-%H%M%S")+'.jpg')
                cv2.imwrite(path, frame)
                cv2.displayStatusBar(WIN_NAME, 'Save photo to:\n'+path, 3000)

    finally:
        out.release()
        cv2.destroyAllWindows()


def parse_args():
    DEFAULT_SAVE_TO = VIDEO
    parser = argparse.ArgumentParser(
        description='A Simple Video VideoWriter with Camera, support Windows and Linux.')
    parser.add_argument('-n', '--cam_ids', nargs="*", type=int,
                        help="The camera's device IDs, can be either a nuber or serveral numbers separated by space.")
    parser.add_argument('-r', '--record', action='store_true',
                        help='Whether to record video to a file or not.')
    parser.add_argument('-t', '--saveto', default=DEFAULT_SAVE_TO,
                        help='Where to save the result.')
    parser.add_argument('-q', '--quality', default='normal', choices=CODEC.keys(),
                        help="The quality of saved video file, default is lossless.")
    parser.add_argument('-i', '--interval', default=0,
                        help='Interval milliseconds between two frames.')
    parser.add_argument('-f', '--flip', action='store_true',
                        help='Flip video around vertical axes.')
    parser.add_argument('-s', '--fixedsize', action='store_true',
                        help='Fixed preview windows in original size rather than fit the screen.')
    parser.add_argument('-V', '--version',
                        action='store_true', help="Show version.")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    if args.version:
        print(VERSION)
        exit()
    cam_record(args)
