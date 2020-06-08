import time
import numpy as np
import pyautogui
from PIL import ImageGrab

from matplotlib import pyplot as plt

def screen():
    im = pyautogui.screenshot()       #实现截屏功能
    im.show()

# 每抓取一次屏幕需要的时间约为1s,如果图像尺寸小一些效率就会高一些
beg = time.time()

screen()

end = time.time()
print(end - beg)

