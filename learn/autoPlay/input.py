import pyautogui
import math
import time

pyautogui.PAUSE=0.05
pyautogui.FAILSAFE = True
time.sleep(2)

pyautogui.typewrite('bu neng shu zhong wen ')

pyautogui.typewrite('\n')

pyautogui.typewrite('zhe ')
pyautogui.typewrite('yang ')
pyautogui.typewrite('jiu ')
pyautogui.typewrite('ke ')
pyautogui.typewrite('yi ')
pyautogui.typewrite('le ')

beg = time.time()

pyautogui.keyDown("left")
time.sleep(0.2)
pyautogui.keyUp("left")

end = time.time()
print(end - beg)