import pyautogui
import aircv as ac
import json
import cv2
import time
import numpy as np


_interval = pyautogui.PAUSE = 0.05
tmp = pyautogui.size()
width = tmp.width
height = tmp.height


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


def gauss():
    rtn = 0.0
    while rtn < 2 or rtn > 7:
        rtn = np.random.normal(loc=5, scale=1, size=1)
    return rtn / 10.0


def click(location):
    """

    :param location: 坐标 0,0 为屏幕左上角 {"x": 586,"y" : 500,"width": 120,"height": 80}
    :return:
    """
    pyautogui.moveTo(location[0], location[1], duration=0.1)
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


def mv(xt=0.0, yt=0.0):
    if xt > 0 and yt > 0:
        pyautogui.press("right")
        pyautogui.keyDown("right")
        if xt > yt:
            pyautogui.keyDown("up")
            time.sleep(yt - _interval * 3)
            pyautogui.keyUp("up")
            time.sleep(xt - yt - _interval)
            pyautogui.keyUp("right")
        else:
            pyautogui.keyDown("up")
            time.sleep(xt - _interval * 3)
            pyautogui.keyUp("right")
            time.sleep(yt - xt - _interval)
            pyautogui.keyUp("up")
    elif xt > 0 and yt == 0:
        pyautogui.press("right")
        pyautogui.keyDown("right")
        time.sleep(xt - _interval * 2)
        pyautogui.keyUp("right")
    elif xt > 0 and yt < 0:
        pyautogui.press("right")
        pyautogui.keyDown("right")
        yt = abs(yt)
        if xt > yt:
            pyautogui.keyDown("down")
            time.sleep(yt - _interval * 3)
            pyautogui.keyUp("down")
            time.sleep(xt - yt - _interval)
            pyautogui.keyUp("right")
        else:
            pyautogui.keyDown("down")
            time.sleep(xt - _interval * 3)
            pyautogui.keyUp("right")
            time.sleep(yt - xt - _interval)
            pyautogui.keyUp("down")
    elif xt == 0 and yt > 0:
        pyautogui.keyDown("up")
        time.sleep(yt - _interval)
        pyautogui.keyUp("up")

    elif xt == 0 and yt == 0:
        pass
    elif xt == 0 and yt < 0:
        pyautogui.keyDown("down")
        time.sleep(yt - _interval)
        pyautogui.keyUp("down")
    elif xt < 0 and yt > 0:
        xt = abs(xt)
        pyautogui.press("left")
        pyautogui.keyDown("left")
        if xt > yt:
            pyautogui.keyDown("up")
            time.sleep(yt - _interval * 3)
            pyautogui.keyUp("up")
            time.sleep(xt - yt - _interval)
            pyautogui.keyUp("left")
        else:
            pyautogui.keyDown("up")
            time.sleep(xt - _interval * 3)
            pyautogui.keyUp("left")
            time.sleep(yt - xt - _interval)
            pyautogui.keyUp("up")
    elif xt > 0 and yt == 0:
        xt = abs(xt)
        pyautogui.press("left")
        pyautogui.keyDown("left")
        time.sleep(xt - _interval * 2)
        pyautogui.keyUp("left")
    elif xt > 0 and yt < 0:
        xt = abs(xt)
        pyautogui.press("left")
        pyautogui.keyDown("left")
        yt = abs(yt)
        if xt > yt:
            pyautogui.keyDown("down")
            time.sleep(yt - _interval * 3)
            pyautogui.keyUp("down")
            time.sleep(xt - yt - _interval)
            pyautogui.keyUp("left")
        else:
            pyautogui.keyDown("down")
            time.sleep(xt - _interval * 3)
            pyautogui.keyUp("left")
            time.sleep(yt - xt - _interval)
            pyautogui.keyUp("down")


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


def sly_enter(picture):
    """ 赛利亚 房间的移动 """
    pyautogui.keyDown("right")
    time.sleep(1.3)
    pyautogui.keyUp("right")
    sc = pyautogui.screenshot()
    sc = np.asarray(sc)[:, :, ::-1].copy()
    location = match_img(sc, _pictures[picture])
    if location:
        click(location["result"])
        return True
    else:
        return False


def play_start(play_map):
    """

    :param play_map: 刷图 例如: [比拉谢尔, 2+2]
    :return:
    """
    pm0Str = play_map[0]
    map_tmp = _maps[play_map[0]]
    if sly_enter(map_tmp["picture"]):
        log_warning(["进入[{1}]失败", pm0Str])
        return False
    map_tmp = _maps[pm0Str]
    # 移动到 控制板
    mv(**map_tmp['move'])
    # 点击 控制板
    # click_gauss(*map_tmp['location'],doubleClick=True)


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
play_start(["比拉谢尔号", "2+2"])
