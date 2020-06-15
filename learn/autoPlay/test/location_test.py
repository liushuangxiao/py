import pyautogui
import aircv as ac
import json
import cv2
import time
import numpy as np
import math
import move


import sys

sys.path.append("./")

from message_sender import press_key, release_key, type_key, left_click
from Location import Location

def print_screen(x=None, y=None, width=None, height=None):
    if x:
        im = pyautogui.screenshot(region=(x, y, width, height))
        # im = ImageGrab.grab(bbox=(x, y, x + width, y + height))
    else:
        im = pyautogui.screenshot()
        # im = ImageGrab.grab(bbox=(0, 0, _width, _height))
    return np.asarray(im)[:, :, ::-1].copy()


def gauss():
    """
    高斯分布 期望 0.5
    :return: 0.2 < return < 0.8
    """
    rtn = 0.0
    while rtn < 2 or rtn > 8:
        rtn = np.random.normal(loc=5, scale=1, size=1)
    return rtn / 10.0


def click_gauss(x, y, width, height, doubleClick=False):
    """
    0,0 为屏幕左上角 {"x": 586,"y" : 500,"width": 120,"height": 80}
    :param x: x坐标
    :param y: y坐标
    :param width: 目标宽度
    :param height: 目标高度
    :return:
    """
    # 高斯分布
    # print(x, y, width, height)
    clickX = gauss() * width + x
    clickY = gauss() * height + y
    pyautogui.moveTo(clickX, clickY, duration=0.1)
    time.sleep(2)
    left_click()
    time.sleep(0.05)
    if doubleClick:
        left_click()


sc = print_screen()
img = cv2.imread("../tu/sly_blxeh.png")
print(img.shape)
_locator = Location()
point = _locator.locate(sc, img, 0.5)
print(point)
click_gauss(*point)

