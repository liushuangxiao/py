import cv2
import pyautogui
from matplotlib import pyplot as plt
from PIL import ImageGrab
import numpy as np
from math import cos, sin, atan2, sqrt, pi ,radians, degrees


def center_geolocation(geolocations):
    x = 0
    y = 0
    lenth = len(geolocations)
    for index in geolocations:
        lon = index[0][0]
        lat = index[0][1]
        x += lon
        y += lat
    x = float(x / lenth)
    y = float(y / lenth)
    return x,y

MIN_MATCH_COUNT = 10  # 设置最低特征点匹配数量为10

plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

# img2 = cv2.imread('tu/sly_blxeh.png')
img2 = cv2.imread('tu/tkdxs.png')

# img1 = pyautogui.screenshot()
img1 = ImageGrab.grab()
img1 = np.asarray(img1)[:,:,::-1].copy()
# cv2.imshow("opencv",img2)


gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
# img2 = cv2.imread('tu/blxeh_board.png')
# gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

# akaze = cv2.AKAZE_create()
akaze = cv2.BRISK_create()
# akaze = cv2.ORB_create()


kp1, des1 = akaze.detectAndCompute(gray1, None)
kp2, des2 = akaze.detectAndCompute(gray2, None)

flann_params = dict(algorithm=cv2.NORM_HAMMING)  # 2

fbm = cv2.FlannBasedMatcher(flann_params)

matches = fbm.knnMatch(des1, trainDescriptors=des2, k=2)  # typo fixed

# Apply ratio test
good = []
for ma in matches:
    if len(ma) < 2:
        continue
    m = ma[0]
    n = ma[1]
    if m.distance < 0.4 * n.distance:
        good.append(m)

if len(good) > MIN_MATCH_COUNT:
    # 获取关键点的坐标
    src_pts = np.float32([kp1[m.queryIdx].pt for m in good]).reshape(-1, 1, 2)
    print(center_geolocation(src_pts))
    dst_pts = np.float32([kp2[m.trainIdx].pt for m in good]).reshape(-1, 1, 2)
    # 计算变换矩阵和MASK
    M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)
    matchesMask = mask.ravel().tolist()
    h, w = gray1.shape
    # 使用得到的变换矩阵对原图像的四个角进行变换，获得在目标图像上对应的坐标
    pts = np.float32([[0, 0], [0, h - 1], [w - 1, h - 1], [w - 1, 0]]).reshape(-1, 1, 2)
    dst = cv2.perspectiveTransform(pts, M)
    cv2.polylines(gray2, [np.int32(dst)], True, 0, 2, cv2.LINE_AA)
else:
    print("Not enough matches are found - %d/%d" % (len(good), MIN_MATCH_COUNT))
    matchesMask = None

draw_params = dict(matchColor=(0, 255, 0),
                   singlePointColor=(0, 0, 255),
                   matchesMask=matchesMask,
                   flags=0)
result = cv2.drawMatches(gray1, kp1, gray2, kp2, good, None, **draw_params)

plt.imshow(result, 'gray')
plt.show()
