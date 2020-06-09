import pyautogui
import aircv as ac
import json
import cv2
import time
import numpy as np
import math

import sys

sys.path.append("./")

import Location

_interval = pyautogui.PAUSE = 0.05
_pi = 3.1415926
tmp = pyautogui.size()
_width = tmp.width
_height = tmp.height
_locator = Location()


def print_screen(x=None, y=None, width=None, height=None):
    if x:
        im = pyautogui.screenshot(region=(x, y, width, height))
        # im = ImageGrab.grab(bbox=(x, y, x + width, y + height))
    else:
        im = pyautogui.screenshot()
        # im = ImageGrab.grab(bbox=(0, 0, _width, _height))
    return np.asarray(im)[:, :, ::-1].copy()


def load_map_img(pictures):
    _pictureMap = {}
    for key in pictures:
        _pictureMap[key] = cv2.imread(key)
        # if os.path.exists(key):
        #     _pictureMap[key] = cv2.imdecode(np.fromfile(key, dtype=np.uint8), -1)
        # else:
        #     _pictureMap[key] = None
    return _pictureMap


def load_maps():
    with open("maps.json", encoding="utf-8") as f:
        data = json.load(f)
    return data


def press_skill(key_array):
    for _key in key_array:
        pyautogui.press(_key, interval=0.03)


def key_down(key, tm):
    pyautogui.keyDown(key)
    for i in range(math.ceil(tm / _interval)):
        print(i)
        pyautogui.press(key)
    pyautogui.keyUp(key)


def gauss():
    """
    高斯分布 期望 0.5
    :return: 0.2 < return < 0.8
    """
    rtn = 0.0
    while rtn < 2 or rtn > 8:
        rtn = np.random.normal(loc=5, scale=1, size=1)
    return rtn / 10.0


def gauss2():
    """
    高斯分布 期望 0
    :return: -0.8 < return < 0.8
    """
    rtn = 0.0
    while rtn < 0.8 or rtn > -0.8:
        rtn = np.random.normal(loc=0, scale=1, size=1)
    return rtn


def gauss0to1():
    """
    高斯分布 期望 0.5
    :return: 0 < return < 1
    """
    rtn = 0.0
    while rtn < 0.5 or rtn > -0.5:
        rtn = np.random.normal(loc=0, scale=1, size=1)
    return rtn + 0.5


def click(x, y):
    """
    0,0 为屏幕左上角 {"x": 586,"y" : 500}
    :param x: 坐标
    :param y: 坐标 0,0
    :return:
    """
    pyautogui.moveTo(x, y, duration=0.1)
    pyautogui.click()


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
    clickX = gauss() * width + x
    clickY = gauss() * height + y
    pyautogui.moveTo(clickX, clickY, duration=0.1)
    pyautogui.click()
    if doubleClick:
        pyautogui.click()


def click_circle_gauss(x, y, radius, doubleClick=False):
    """
    高斯分布 期望值为圆心
    :param x: 圆心
    :param y: 圆心
    :param radius: 半径
    :return:
    """
    angle = gauss0to1() * 360
    clickX = x + radius * math.sin(angle * _pi / 180)
    clickY = y + radius * math.cos(angle * _pi / 180)
    pyautogui.moveTo(clickX, clickY, duration=0.1)
    pyautogui.click()
    if doubleClick:
        pyautogui.click()


def mv(xt=0.0, yt=0.0):
    x_time = math.ceil(abs(xt) / _interval)
    y_time = math.ceil(abs(yt) / _interval)
    x_key = "right" if xt > 0 else "left"
    y_key = "up" if yt > 0 else "down"

    pyautogui.keyDown(x_key)
    pyautogui.keyDown(y_key)
    for count in range(max(x_time, y_time) + 1):
        if count < x_time:
            pyautogui.press(x_key, interval=0.03)
        else:
            pyautogui.keyUp(x_key)
        if count < y_time:
            pyautogui.press(y_key, interval=0.03)
        else:
            pyautogui.keyUp(y_key)


def log_info(s):
    print(s)


def log_warning(s):
    print(*s)


def match_img(img_src, im_obj, confidence=0.5):
    """

    :param img_src: 原始图像
    :param im_obj: 待查找的图片
    :param confidence:
    :return:
    """
    match_result = ac.find_template(img_src, im_obj, confidence)
    if match_result is not None:
        match_result['shape'] = (img_src.shape[1], img_src.shape[0])  # 0为高，1为宽
    return match_result


def location(img):
    sc = print_screen()
    return _locator.locate(sc, img)


def sly_enter(picture):
    """ 赛利亚 房间的移动 """
    key_down("right", 1.3)
    x0y = location(_pictures[picture])
    if location:
        click(*x0y)
        return True
    else:
        return False


def play_blxeh(play_map):
    """
    该方法只支持比拉谢尔号地图
    :param play_map: 刷图 例如: [比拉谢尔, 2+2]
    :return:
    """
    pm0Str = play_map[0]
    map0_tmp = _maps[play_map[0]]
    if not sly_enter(map0_tmp["picture"]):
        log_warning(["进入[{1}]失败", pm0Str])
        return False
    map0_tmp = _maps[pm0Str]
    # 移动到 控制板
    mv(**map0_tmp['move'])
    # 点击 控制板
    click_gauss(*map0_tmp['location'], doubleClick=True)
    # 选着地图
    pm1Str = play_map[1]
    map1_tmp = map0_tmp["maps"][pm1Str]
    click_circle_gauss(**map1_tmp['location'], doubleClick=True)


# 范围 boundary True 大, False 小
# 可柔化技能 follow
# 打全伤害中断点 breakPoint
skill = [
    {'name': "破空拔刀斩", 'key': ['shiftleft'], 'coolingTime': 40, 'duration': 1, 'boundary': True, 'follow': [],
     'breakPoint': 0.7, 'last': 0},
    {'name': "名字", 'key': ['altleft'], 'coolingTime': 40, 'duration': 1, 'boundary': True, 'follow': [],
     'breakPoint': 0.7, 'last': 0},
    {'name': "剑舞", 'key': ['b'], 'coolingTime': 20, 'duration': 2, 'boundary': False, 'follow': [], 'breakPoint': 0.7,
     'last': 0}
]

skill_low = [
    {'name': "拔刀斩", 'key': ['a'], 'coolingTime': 10, 'duration': 1, 'boundary': False, 'follow': [], 'breakPoint': 0.7,
     'last': 0}
]

play = ["痛", "魂"]
_maps = load_maps()
_pictures = load_map_img(_maps['pictures'])

time.sleep(2)
play_blxeh(["比拉谢尔号", "2+2"])
