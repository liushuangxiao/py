from random import randint
from math import ceil, sin, pi

JIAN_HUN=0x01

class move:
    # 曲线参数 y = ax + b
    __a = 1
    __b = 0

    # 生成曲线路径的 x 轴间距
    __space = 13

    __difference = None

    __curve_coe = None
    __curve_confuse_coe = None



    def __init__(self, x_start, y_start, x_target, y_target, space=None):
        a = (y_target - y_start) / (x_target - x_start)
        b = (x_start * y_target - y_start * x_target) / (x_start - x_target)
        self.x_start = x_start
        self.y_start = y_start
        self.x_target = x_target
        self.y_target = y_target
        self.__a = a
        self.__b = b
        self.__difference = x_target - x_start
        self.__space = self.__space if space is None else space
        self.__curve_coe = randint(1, 2)
        self.__curve_confuse_coe = randint(4, 10) * 2

    def path(self):
        path = []
        for i in range(0, int(ceil(self.__difference / self.__space))):
            path.append(self.move_x0y(i, self.x_start))
        path.append((self.x_target, self.y_target))

    def move_x0y(self, i, x_start):
        si = self.__space * i
        xi = x_start + si
        yi = xi * self.__a + self.__b, + sin(si / self.__difference * self.__curve_coe * pi) * 20 + sin(si / self.__difference * self.__curve_confuse_coe * pi) * 4
        return xi, yi


def speed_x(type, speed_plus):
    if type == JIAN_HUN:
        return speed_plus * 8.7 + 869.5


def speed_yt(speed_plus):
    return speed_plus * 3.028571 + 316.0


def speed_xt(speed_plus):
    return speed_plus * 2.5166666 + 261.6666666


