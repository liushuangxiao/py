import pyautogui
import math
import time
from pynput.keyboard import Key, Controller



pyautogui.PAUSE=0.05
pyautogui.FAILSAFE = True
time.sleep(2)

# pyautogui.typewrite('bu neng shu zhong wen ')
#
# pyautogui.typewrite('\n')
#
# pyautogui.typewrite('zhe ')
# pyautogui.typewrite('yang ')
# pyautogui.typewrite('jiu ')
# pyautogui.typewrite('ke ')
# pyautogui.typewrite('yi ')
# pyautogui.typewrite('le ')

# beg = time.time()
#
# pyautogui.keyDown("left")
# time.sleep(3)
# pyautogui.keyUp("left")
#
# end = time.time()
# print(end - beg)

pyautogui.keyDown("left")
tm = 1.3
for i in range(math.ceil(tm/pyautogui.PAUSE)):
        print(i)
        pyautogui.press("left")
pyautogui.keyUp("left")

print(math.ceil(tm))