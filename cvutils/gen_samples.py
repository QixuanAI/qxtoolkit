#! /usr/bin/env python
'''
Description: 
FilePath: /cvutils/cvutils/gen_samples.py
Author: qxsoftware@163.com
Date: 2020-10-30 14:16:55
LastEditTime: 2020-12-03 09:41:17
Refer to: https://github.com/QixuanAI
'''
import os
import cv2
import argparse
import numpy as np
from pathlib import Path
from warnings import warn
from datetime import datetime
from matplotlib import pyplot as plt

__all__=["gen_gray_level_calib_imgs","gen_rgb_level_calib_imgs"]


def gen_gray_level_calib_imgs(bits=8):
    maxval = 1 << bits
    shape = (maxval, maxval, 1)
    if bits == 8:
        dtype = np.uint8
    elif bits == 16:
        dtype = np.uint16
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
    maxval = 1 << bits
    shape = (maxval, maxval, 3)
    if bits == 8:
        dtype = np.uint8
    elif bits == 16:
        dtype = np.uint16
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


if __name__ == "__main__":
    import sys
    getter = gen_gray_level_calib_imgs
    cv2.namedWindow('press q to quit', cv2.WINDOW_NORMAL)
    for i, img in enumerate(getter(bits=8)):
        if img is None:
            print(i, ' - None to show')
            continue
        print(i, end='\r')
        cv2.imshow('press q to quit', img)
        if cv2.waitKey(100) == ord('q'):
            break
