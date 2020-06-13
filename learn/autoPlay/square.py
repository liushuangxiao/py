import pyautogui
import time
import random
import math

pyautogui.PAUSE = 0

colors = [
    {'x': 774, 'y': 63},
    {'x': 797, 'y': 63},
    {'x': 797, 'y': 87},
    {'x': 820, 'y': 63},
    {'x': 820, 'y': 87},
    {'x': 843, 'y': 63},
    {'x': 843, 'y': 87},
    {'x': 866, 'y': 63},
    {'x': 866, 'y': 87},
    {'x': 889, 'y': 63},
    {'x': 889, 'y': 87},
    {'x': 974, 'y': 63},
    {'x': 974, 'y': 87}
]


def change_color(x, y):
    color = colors[random.randint(0, len(colors) - 1)]
    pyautogui.moveTo(color['x'], color['y'], duration=0.1)
    pyautogui.click()
    pyautogui.moveTo(x, y, duration=0.1)


for i in range(3, -1, -1):
    time.sleep(1)
    print(i)

x, y = pyautogui.position()
xt = 200
yt = 300

r = (yt - y) / (xt - x)
c = (x * yt - y * xt) / (x - xt)

print(r, c)

difference = xt - x

parts = [1 / 2, 1 / 3, 1 / 4]
part = parts[random.randint(0,2)]

# p1 = difference * part
# p1 = p1 if (p1 % 2) == 0 else (p1+1)
# p2 = difference - p1
# p1 = difference
#
# p1s = abs(p1 / 2)
pyautogui.mouseDown()

space = 13 * (1 if difference >= 0 else -1)
print(int(math.ceil(difference/space)))
for i in range(0, int(math.ceil(difference/space))):
    si = space * i
    xi = x + si
    yi = xi * r + c + math.sin(si/difference * 2 * math.pi) * 20 + math.sin(si/difference * 20 * math.pi) * 4
    pyautogui.moveTo(xi, yi, 0.001)

print(i)
pyautogui.mouseUp()

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
