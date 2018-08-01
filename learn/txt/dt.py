import linecache
import os
import sys
from urllib import parse
from urllib import request

# nohup python3 -u dt.py 3183 > g.log 2>&1 &

# t_dir = '/data/txt/%s.txt'
t_dir = 'E:\\ts\%s.txt'
d_url = 'http://xiazai.xqishu.com/txt/%s.txt'
d_url2 = 'http://down.xqishu.com/txt/%s.txt'
names_file = 'name.txt'


def downloading(filename):
    file_path = t_dir % filename
    if os.path.exists(file_path):
        print(' exists')
        return
    url = d_url % parse.quote(filename)
    try:
        request.urlretrieve(url, file_path)
        print(' success')
    except Exception as e:
        url = d_url2 % parse.quote(filename)
        try:
            request.urlretrieve(url, file_path)
            print(' success')
        except Exception as e:
            print(' fail')


if __name__ == '__main__':
    ln = 0
    if len(sys.argv) == 1 or sys.argv[1] == '':
        ln = 573
    elif not str.isdigit(sys.argv[1]):
        print('%s not a number' % sys.argv[1])
        sys.exit(9)
    else:
        ln = int(sys.argv[1])

    if len(sys.argv) < 3:
        names_file = 'xuanhuan'
    else:
        names_file = sys.argv[2]
        t_dir = '/data/txt/' + names_file + '/%s.txt'

    if not os.path.exists(names_file):
        print('file %s not exists' % sys.argv[2])
        sys.exit(8)

    name = linecache.getline(names_file, ln)
    while name:
        name = name.strip()
        if name.startswith('---'):
            print(name)
        else:
            print('dwomload %s %s' % (ln, name), end='')
            downloading(name)
        ln += 1
        name = linecache.getline(names_file, ln)

# 00332
