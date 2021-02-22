#! /usr/bin/env python
'''
Description : A example of drawing retangle by mouse drag event
FilePath    : /qxtoolkit/selector.py
Author      : qxsoftware@163.com
Date        : 2021-02-07 08:37:04
LastEditTime: 2021-02-22 13:44:24
Refer to    : https://github.com/QixuanAI
'''

import cv2
from datetime import datetime
import qxtoolkit as qx


startpos = None
crtpos = None
drag = False
bboxes = []

WIN_NAME = "Press h for help"
HELP_MSG = """Keyboard shortcuts:
q - Quit
s - Save Picture
h - Show This Help"""


def onMouse(event, x, y, flags, *param):
    global startpos, crtpos, drag, bboxes
    crtpos = (x, y) # current mouse position
    if event == cv2.EVENT_LBUTTONDOWN:
        startpos = (x, y)
        drag = True
    if event == cv2.EVENT_LBUTTONUP:
        bbox = (startpos, crtpos)
        bboxes.append(bbox)
        drag = False
    # show event message
    msg = "event:{},x:{},y:{},flags:{}".format(event, x, y, flags)
    cv2.displayStatusBar(WIN_NAME, msg, 1000)

def setup_window():
    cv2.namedWindow(WIN_NAME, cv2.WINDOW_KEEPRATIO |
                    cv2.WINDOW_GUI_EXPANDED | cv2.WINDOW_NORMAL)
    cv2.setMouseCallback(WIN_NAME, onMouse)

def main(src):
    setup_window()
    for img in qx.ImagesGetter(src):
        if bboxes:
            for p1, p2 in bboxes:
                img = cv2.rectangle(img, p1, p2, qx.colors.Blue.value, 2)
        if drag:
            img = cv2.rectangle(img, startpos, crtpos, qx.colors.Red.value, 2)
        cv2.imshow(WIN_NAME, img)
        pressed = cv2.waitKey(1)
        if pressed == ord('\r'):
            bboxes.clear()
        elif pressed == ord('s'):
            path = datetime.now().strftime("%Y%m%d-%H%M%S")+'.jpg'
            cv2.imwrite(path, img)
            bboxes.clear()
        elif pressed == ord('q'):
            break
        elif pressed == ord('h'):
            cv2.displayOverlay(WIN_NAME, HELP_MSG, 5000)
        # Close Button Clicked
        if cv2.getWindowProperty(WIN_NAME, cv2.WND_PROP_VISIBLE) < 1:
            break

if __name__ == "__main__":
    main(src=6)