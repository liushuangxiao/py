import cv2
from matplotlib import pyplot as plt
import numpy as np
from math import cos, sin, atan2, sqrt, pi ,radians, degrees


def center_geolocation(geolocations):
    x = 0
    y = 0
    z = 0
    lenth = len(geolocations)
    for lon, lat in geolocations:
        lon = radians(float(lon))
        lat = radians(float(lat))
        x += cos(lat) * cos(lon)
        y += cos(lat) * sin(lon)
        z += sin(lat)

    x = float(x / lenth)
    y = float(y / lenth)
    z = float(z / lenth)
    return (degrees(atan2(y, x)), degrees(atan2(z, sqrt(x * x + y * y))))

MIN_MATCH_COUNT = 10  # 设置最低特征点匹配数量为10

plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

img1 = cv2.imread('tu/5.png')
img2 = cv2.imread('tu/sly.png')

gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

akaze = cv2.AKAZE_create()

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
    if m.distance < 0.6 * n.distance:
        good.append(m)

if len(good) > MIN_MATCH_COUNT:
    # 获取关键点的坐标
    src_pts = np.float32([kp1[m.queryIdx].pt for m in good]).reshape(-1, 1, 2)
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

for index in range(len(matchesMask)):
    if matchesMask[index] == 1:
        print(kp1[good[index].queryIdx].pt)


plt.imshow(result, 'gray')
plt.show()
