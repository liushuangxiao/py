# encodeing=utf-8
import os

import jieba

dir = 'F:\\data\\book\\'


def read_file(filepath):
    file = open(filepath, 'r', encoding='GB18030')
    line = file.readline()
    while line:
        line = line.strip()
        if (line != ''):
            seg = jieba.cut(line, cut_all=False)
            print_num(seg)
        line = file.readline()


def print_num(seg):
    for s in seg:
        if s not in ['！', '，', '。', '“', '”', '.', '？', '(', ')']:
            print("%s 1" % s)


if __name__ == '__main__':
    list = os.listdir(dir)
    for i in range(0, len(list)):
        path = os.path.join(dir, list[i])
        if os.path.isfile(path):
            read_file(path)
