import cv2
from matplotlib import pyplot as plt
import numpy as np


class Location:
    img_source = None
    img_target = None
    coefficient = 0.5
    min_match_count = 10  # 设置最低特征点匹配数量为10

    def __init__(self, algorithm='BRISK'):
        if 'ORB' == algorithm:
            self.alg = cv2.ORB_create()
        elif 'AKAZE' == algorithm:
            self.alg = cv2.AKAZE_create()
        else:
            self.alg = cv2.BRISK_create()

    def change_coefficient(self, coefficient=0.5):
        self.coefficient = coefficient

    def change_min_match_count(self, min_match_count=10):
        self.min_match_count = min_match_count

    @staticmethod
    def __center_x0y(x0y):
        """

        :param x0y:
        :return: x y width height
        """
        x = 0
        y = 0
        l = len(x0y)
        max_x = 0
        min_x = 5000
        max_y = 0
        min_y = 5000
        for index in x0y:
            lon = index[0][0]
            max_x = max(max_x, lon)
            min_x = min(min_x, lon)
            lat = index[0][1]
            max_y = max(max_y, lat)
            min_y = min(min_y, lat)
            x += lon
            y += lat
        x = float(x / l)
        y = float(y / l)
        return x, y, max_x - min_x, max_y - min_y

    def locate(self, img_source, img_target):
        min_match_count = self.min_match_count
        plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
        plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

        # img_source = cv2.imread('tu/3.png')
        gray1 = cv2.cvtColor(img_source, cv2.COLOR_BGR2GRAY)
        # img_target = cv2.imread('tu/sly_blxeh.png')
        gray2 = cv2.cvtColor(img_target, cv2.COLOR_BGR2GRAY)

        algorithm = self.alg

        kp1, des1 = algorithm.detectAndCompute(gray1, None)
        kp2, des2 = algorithm.detectAndCompute(gray2, None)

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
            if m.distance < 0.5 * n.distance:
                good.append(m)

        # 获取关键点的坐标
        src_pts = np.float32([kp1[m.queryIdx].pt for m in good]).reshape(-1, 1, 2)
        dst_pts = np.float32([kp2[m.trainIdx].pt for m in good]).reshape(-1, 1, 2)

        return self.__center_x0y(src_pts)
