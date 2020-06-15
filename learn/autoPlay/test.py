import aircv as ac
import pyautogui
import numpy as np
import math

# https://www.jb51.net/article/165409.htm 找不同

def matchImg(imgsrc,imgobj,confidencevalue=0.5):#imgsrc=原始图像，imgobj=待查找的图片

    imsrc = pyautogui.screenshot()
    imsrc = np.asarray(imsrc)[:, :, ::-1].copy()
    imobj = ac.imread(imgobj)

    match_result = ac.find_template(imsrc,imobj,confidencevalue)  # {'confidence': 0.5435812473297119, 'rectangle': ((394, 384), (394, 416), (450, 384), (450, 416)), 'result': (422.0, 400.0)}
    if match_result is not None:
        match_result['shape']=(imsrc.shape[1],imsrc.shape[0])#0为高，1为宽

    return match_result


c = matchImg("./tu/3.png", "tu/sly_blxeh.png", 0.5)
print(c)
#
#
# if c == 1:
#     pass
# elif 1 == c:
#     print("ssssssssssss")

# ma = 0
# mi = 5
# for i in range(1000000):
#     n = np.random.normal(loc=5, scale=1, size=1)
#     ma = max(n, ma)
#     mi = min(n, mi)
#
# print(ma, mi)

for i in range(1,2):
    print(i)

# rtn = 1
# while rtn > 0.5 or rtn < -0.5:
#     rtn = np.random.normal(loc=0, scale=1, size=1)
#     print(rtn)
#
# print(rtn)