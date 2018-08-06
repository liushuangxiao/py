# encodeing=utf-8
import hashlib
import os

import jieba

dir = 'E:\\ts\\'


def read_file(file_path):
    file = open(file_path, 'r', encoding='utf-8')
    line = file.readline()
    while line:
        line = line.strip()
        if line != '':
            seg = jieba.cut(line, cut_all=False)
            print_num(seg)
        line = file.readline()


def print_num(seg):
    for s in seg:
        print("%s %s 1" % (name_md5, s))


if __name__ == '__main__':
    m = hashlib.new('md5')
    list = os.listdir(dir)
    for i in range(0, len(list)):
        book_name = (list[i])
        index = book_name.rfind('.')
        name_md5 = ''
        if index > -1:
            name_md5 = book_name[:index]
        else:
            name_md5 = book_name

        m.update(name_md5.encode(encoding='utf-8'))
        name_md5 = m.hexdigest()[:8]

        path = os.path.join(dir, list[i])
        if os.path.isfile(path):
            read_file(path)
