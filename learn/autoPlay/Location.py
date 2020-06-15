import cv2
from matplotlib import pyplot as plt
import numpy as np
from math import ceil


def avg(args, max_dis):
    # print(args, max_dis)
    l = len(args)
    middle = args[int(ceil(l / 2))]
    ma = middle
    mi = middle
    su = 0
    num = 0
    half_dis = max_dis / 2
    for it in args:
        mat = max(ma, it)
        mit = min(mi, it)
        if mat - mit < half_dis:
            su += it
            num += 1
            ma = mat
            mi = mit
    return su / num, ma - mi


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
    def __center_x0y(x0y, width, height):
        """

        :param x0y:
        :return: x y width height
        """
        # print(x0y)
        l = len(x0y)
        if l == 0:
            return 0, 0, 0, 0
        ya = [xy[0][1] for xy in x0y]
        ya.sort()
        xa = [xy[0][0] for xy in x0y]
        xa.sort()

        x, x_dis = avg(xa, width)
        y, y_dis = avg(ya, height)

        return x, y, x_dis, y_dis

    def locate(self, img_source, img_target, cf=None):
        # 获取关键点的坐标
        src_pts, dst_pts = self.__c(img_source, img_target, cf=cf)
        sp = img_target.shape
        width = sp[1]
        height = sp[0]
        return self.__center_x0y(src_pts, width, height)

    def exist(self, img_source, img_target, cf=None , mmc=None):
        if mmc is None:
            mmc = self.min_match_count
        # 获取关键点的坐标
        src_pts, dst_pts = self.__c(img_source, img_target, cf=cf)
        return len(src_pts) > mmc

    def __c(self, img_source, img_target, cf=None):
        if cf is None:
            cf = self.coefficient

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
            if m.distance < cf * n.distance:
                good.append(m)

        # 获取关键点的坐标
        src_pts = np.float32([kp1[m.queryIdx].pt for m in good]).reshape(-1, 1, 2)
        dst_pts = np.float32([kp2[m.trainIdx].pt for m in good]).reshape(-1, 1, 2)

        return src_pts, dst_pts
