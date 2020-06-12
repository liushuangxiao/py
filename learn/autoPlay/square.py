import pyautogui
import time
import random

colors = [
    {'x': 774,'y': 63},
    {'x': 797,'y': 63},
    {'x': 797,'y': 87},
    {'x': 820,'y': 63},
    {'x': 820,'y': 87},
    {'x': 843,'y': 63},
    {'x': 843,'y': 87},
    {'x': 866,'y': 63},
    {'x': 866,'y': 87},
    {'x': 889,'y': 63},
    {'x': 889,'y': 87},
    {'x': 974,'y': 63},
    {'x': 974,'y': 87}
          ]

def change_color(x, y):
    color = colors[random.randint(0,len(colors)-1)]
    pyautogui.moveTo(color['x'], color['y'], duration=0.1)
    pyautogui.click()
    pyautogui.moveTo(x, y, duration=0.1)

time.sleep(2)
pyautogui.moveTo(579, 695, duration=0.1)
time.sleep(0.3)
pyautogui.doubleClick()

# pyautogui.moveTo(971, 63, duration=0.1)
# pyautogui.click()

#
# x, y = 600,600
# pyautogui.moveTo(x, y, duration=0.1)
#
# for i in range(20):
#     ex = i * 10 + 10
#     tx = x+ex
#     ty = y+ex
#     pyautogui.moveTo(tx, ty, duration=0.1)
#
#     pyautogui.mouseDown()
#     tx = x+ex
#     ty = y-ex
#     pyautogui.moveTo(tx, ty, duration=0.1)
#     pyautogui.mouseUp()
#     change_color(tx,ty)
#     pyautogui.mouseDown()
#
#     tx = x-ex
#     ty = y-ex
#     pyautogui.moveTo(tx, ty, duration=0.1)
#     pyautogui.mouseUp()
#     change_color(tx,ty)
#     pyautogui.mouseDown()
#
#     tx = x-ex
#     ty = y+ex
#     pyautogui.moveTo(tx, ty, duration=0.1)
#     pyautogui.mouseUp()
#     change_color(tx,ty)
#     pyautogui.mouseDown()
#
#     tx = x+ex
#     ty = y+ex
#     pyautogui.moveTo(tx, ty, duration=0.1)
#     pyautogui.mouseUp()
#     change_color(tx,ty)

