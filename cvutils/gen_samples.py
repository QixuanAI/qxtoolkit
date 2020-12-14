#! /usr/bin/env python
'''
Description: 
FilePath: \cvutils\cvutils\gen_samples.py
Author: qxsoftware@163.com
Date: 2020-10-30 14:16:55
LastEditTime: 2020-12-14 22:46:33
Refer to: https://github.com/QixuanAI
'''
from matplotlib import pyplot as plt
import os
import cv2
import argparse
import numpy as np
from pathlib import Path
from warnings import warn
from datetime import datetime
from ._inner import FOURCC_CODEC

__all__ = ["gen_gray_level_calib_imgs", "gen_rgb_level_calib_imgs"]


def _get_param(bits, channel):
    maxval = 1 << bits
    shape = (maxval, maxval, channel)
    if bits == 8:
        dtype = np.uint8
    elif bits == 16:
        dtype = np.uint16
    return maxval, shape, dtype


def gen_gray_level_calib_imgs(bits=8):
    maxval, shape, dtype = _get_param(bits, 1)
    for i in range(maxval):
        img = np.full(shape, i, dtype=dtype)
        yield img
    img = np.zeros(shape, dtype=dtype)
    for i in range(maxval):
        yield img
        img[:, -i:, :] += 1
    img = np.zeros(shape, dtype=dtype)
    for i in range(maxval):
        yield img
        img[-i:, :, :] += 1
    img = np.zeros(shape, dtype=dtype)
    for i in range(maxval):
        yield img
        img[-i:, -i:, :] += 1
    img = np.zeros(shape, dtype=dtype)
    for i in range(maxval//2):
        yield img
        img[:, maxval-i*2-1, :] = maxval-1
    img = np.zeros(shape, dtype=dtype)
    for i in range(maxval//2):
        yield img
        img[maxval-i*2-1, :, :] = maxval-1
    img = np.zeros(shape, dtype=dtype)
    for i in range(maxval//2):
        yield img
        img[:, maxval-i*2-1, :] = maxval-1
        img[maxval-i*2-1, :, :] = maxval-1


def gen_rgb_level_calib_imgs(bits=8):
    maxval, shape, dtype = _get_param(bits, 3)
    for c in (0, 1, 2):
        img = np.zeros(shape, dtype=dtype)
        for i in range(maxval):
            yield img
            img[:, :, c] += 1
    for c in (0, 1, 2):
        img = np.zeros(shape, dtype=dtype)
        for i in range(maxval):
            yield img
            img[:, -i:, c] += 1
    for c in (0, 1, 2):
        img = np.zeros(shape, dtype=dtype)
        for i in range(maxval):
            yield img
            img[-i:, :, c] += 1
    for c in (0, 1, 2):
        img = np.zeros(shape, dtype=dtype)
        for i in range(maxval):
            yield img
            img[-i:, -i:, c] += 1
    for c in (0, 1, 2):
        img = np.zeros(shape, dtype=dtype)
        for i in range(maxval//2):
            yield img
            img[:, maxval-i*2-1, c] = maxval-1
    for c in (0, 1, 2):
        img = np.zeros(shape, dtype=dtype)
        for i in range(maxval//2):
            yield img
            img[maxval-i*2-1, :, c] = maxval-1
    for c in (0, 1, 2):
        img = np.zeros(shape, dtype=dtype)
        for i in range(maxval//2):
            yield img
            img[:, maxval-i*2-1, c] = maxval-1
            img[maxval-i*2-1, :, c] = maxval-1


def gen_rgb_spiral_curve_imgs(bits=8):
    # todo
    # 绘制等角螺线
    maxval, shape, dtype = _get_param(bits, 3)
    center = (shape[0]//2, shape[1]//2)  # 中心坐标
    angle = np.radians(85)  # 螺线固定角度，大于90度为顺时针，小于为逆时针
    # circle_num=8 # 圈数
    # phase = 0
    for i in range(10000):  # 初始相位
        circle_num = min(1+i/100, 10)
        phase = i/500
        # 极坐标
        theta = np.linspace(0, circle_num*2*np.pi, 5000)+phase*2*np.pi  # 角度
        r = angle*np.exp(theta/np.tan(angle))  # 距离
        # 极坐标转直角坐标
        x = r*np.cos(theta)+center[0]
        y = r*np.sin(theta)-center[1]
        img = np.zeros(shape, dtype=dtype)
        # plt.plot(x,y)
        # plt.show()
        scale = (maxval+10)/(x.max()-x.min())
        x -= x.min()
        y -= y.min()
        x *= scale
        y *= scale
        h, s, v = 128*np.sin(phase)+128, 255, 255
        pts = np.stack((x.astype(np.int), y.astype(np.int)), -1)
        img = cv2.polylines(img, [pts], False, (h, s, v), thickness=2)
        img = cv2.cvtColor(img, cv2.COLOR_HSV2BGR)
        yield img


if __name__ == "__main__":
    import sys
    getter = gen_rgb_spiral_curve_imgs
    delay = 1
    save = False
    if save:
        path = "sample.mp4"
        fourcc = cv2.VideoWriter_fourcc(*FOURCC_CODEC["small"][0])
        out = cv2.VideoWriter(path, fourcc, 25, (256, 256))
    cv2.namedWindow('press q to quit', cv2.WINDOW_NORMAL)
    for i, img in enumerate(getter(bits=8)):
        if img is None:
            print(i, ' - None to show')
            continue
        print(i, end='\r')
        cv2.imshow('press q to quit', img)
        if save:
            out.write(img)
        if cv2.waitKey(delay) == ord('q'):
            break
    if save:
        out.release()
