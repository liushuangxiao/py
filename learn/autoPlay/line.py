import pyautogui
import time
import random
import math
import math

pyautogui.PAUSE = 0.001
_space = 13
_move_pause = 0.001


def move_x0y(i, x_start, a, b, difference, curve_coe, curve_confuse_coe):
    si = _space * i
    xi = x_start + si
    yi = xi * a + b, + math.sin(si / difference * curve_coe * math.pi) * 20 + math.sin(si / difference * curve_confuse_coe * math.pi) * 4
    pyautogui.moveTo(xi, yi, _move_pause)


def move_path(x_start, a, b, difference):
    curve_coe = random.randint(1, 2)
    curve_confuse_coe = random.randint(4, 10) * 2
    for i in range(0, int(math.ceil(difference/space))):
        move_x0y(i, x_start, a, b, difference, curve_coe, curve_confuse_coe)


for i in range(3, -1, -1):
    time.sleep(1)
    print(i)

pyautogui.moveTo(300, 300, 0.001)
pyautogui.mouseDown()

space = 13
for i in range(0, 25):
    si = i * space
    c = math.sin(si / 400 * 2 * math.pi)
    xi = 300 + si
    yi = c * 50 + xi
    pyautogui.moveTo(xi, yi, 0.001)

pyautogui.mouseUp()
