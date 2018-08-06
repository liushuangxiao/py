import hashlib
import linecache
import os
import sys


t_dir = '/data/txt/%s'
t_dir = 'E:\\ts\\%s'

name = t_dir % 'dirx'
name_md5 = t_dir % 'mdir'

if __name__ == '__main__':
    m = hashlib.new('md5')

    file_src = open(name, 'r', encoding='utf-8')
    file = open(name_md5, 'w', encoding='utf-8')

    line = file_src.readline()

    while line:
        line = line.strip()
        m.update(line.encode(encoding='utf-8'))
        file.writelines('%s\n' % m.hexdigest()[:7])
        line = file_src.readline()