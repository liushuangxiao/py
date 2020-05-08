import pyautogui
import math
import time

pyautogui.FAILSAFE = True
time.sleep(2)

width, height = pyautogui.size()
r = 20 # 圆的半径
# 圆心
o_x = width/2
o_y = height/2
pi = 3.1415926
begin = True
for i in range(3):  # 转10圈
    for angle in range(0, 360, 5): # 利用圆的参数方程
        X = o_x + r * math.sin(angle*pi/180)
        Y = o_y + r * math.cos(angle*pi/180)
        if begin :
            pyautogui.moveTo(X, Y, duration=0.05)
            pyautogui.mouseDown()
        else:
            pyautogui.dragTo(X, Y, duration=0.05)
        r = r + 0.7
        print(r)

pyautogui.mouseUp()