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

_interval = 0.05
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
        type_key(_key, interval=0.03)


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
    rtn = 1
    while rtn > 0.5 or rtn < -0.5:
        rtn = np.random.normal(loc=0, scale=1, size=1)
    return rtn[0] + 0.5


def click(x, y):
    """
    0,0 为屏幕左上角 {"x": 586,"y" : 500}
    :param x: 坐标
    :param y: 坐标 0,0
    :return:
    """
    pyautogui.moveTo(x, y, duration=0.1)
    pyautogui.click()


def click_gauss(x, y, width, height, doubleClick=False, gap=0.05, type=None):
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
    clickX = gauss0to1() * width + x
    clickY = gauss0to1() * height + y
    pyautogui.moveTo(clickX, clickY, duration=0.1)
    time.sleep(gap)
    left_click()
    time.sleep(0.05)
    if doubleClick:
        left_click()


def click_circle_gauss(x, y, radius, doubleClick=False, gap=0, type=None):
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
    time.sleep(gap)
    left_click()
    if doubleClick:
        left_click()


def mv(xt=0.0, yt=0.0):
    interval = _interval
    x_time = abs(xt)
    y_time = abs(yt)
    x_key = "right" if xt > 0 else "left"
    y_key = "up" if yt > 0 else "down"
    if yt == 0:
        press_key(x_key)
        time.sleep(x_time)
        release_key(x_key)
        return
    if xt == 0:
        press_key(y_key)
        time.sleep(y_time)
        release_key(y_key)
        return
    if x_time > y_time:
        press_key(x_key)
        time.sleep(interval)
        press_key(y_key)
        time.sleep(y_time - interval)
        release_key(y_key)
        time.sleep(x_time - y_time)
        release_key(x_key)
    else:
        press_key(x_key)
        time.sleep(interval)
        press_key(y_key)
        time.sleep(x_time - interval)
        release_key(x_key)
        time.sleep(y_time - x_time)
        release_key(y_key)


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


def click_pictures(img_str):
    img = _pictures[img_str]
    x0y = location_pictures(img)
    print(x0y)
    if x0y[0] != 0:
        click_gauss(*x0y)
        return True
    else:
        return False


def location_pictures(img):
    sc = print_screen()
    return _locator.locate(sc, img)


def exist_pictures(img):
    sc = print_screen()
    return _locator.exist(sc, img, mmc=7)


def sly_enter(picture, character):
    """ 赛利亚 房间的移动 """
    mv(500 / character["townSpeedX"], -100 / character["townSpeedY"])
    return click_pictures(picture)


def choose_difficulty(diff):
    for i in range(1,diff):
        type_key("right", 0.1)


def play_map(map):
    location = map["location"]
    t = location["type"]
    if t == "rectangle":
        click_gauss(**location)
        choose_difficulty(map["difficulty"])
        type_key("space", 0.05)


def play_blxeh(play_map, character):
    """
    该方法只支持比拉谢尔号地图
    :param play_map: 刷图 例如: [比拉谢尔, 2+2]
    :return:
    """
    pm0Str = play_map[0]
    map0_tmp = _maps[pm0Str]
    if not sly_enter(map0_tmp["picture"], character):
        log_warning(["进入[{1}]失败", pm0Str])
        return False
    dis = map0_tmp['board']["dis"]
    xtown = character["townSpeedX"]
    ytown = character["townSpeedY"]
    # 移动到 控制板
    mv(dis / xtown, 0)
    # 打开 面板
    click_pictures(map0_tmp['board']["picture"])
    # 选着地图
    pm1Str = play_map[1]
    map1_tmp = map0_tmp["maps"][pm1Str]
    local = map1_tmp['location']
    click_circle_gauss(**local)


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
character = {'moveSpeed': 1336, "townSpeedY": move.speed_yt(140), "townSpeedX": move.speed_xt(140)}

# for i in range(3, -1, -1):
#     time.sleep(1)
#     print(i)
pms = ["比拉谢尔号", "2+2"]
# play_blxeh(["比拉谢尔号", "2+2"],character)

pm0Str = pms[0]
map0_tmp = _maps[pm0Str]
pm1Str = pms[1]
map1_tmp = map0_tmp["maps"][pm1Str]
ssm = map1_tmp["maps"][0]
# play_map(ssm)
enter_img = ssm["enter_img"]
print(enter_img)
ex = exist_pictures(_pictures[enter_img])
print(ex)