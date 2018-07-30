import linecache
import sys
from urllib import parse
from urllib import request

t_dir = '/data/txt/%s.txt'
# t_dir = 'E:\\ts\%s.txt'
d_url = 'http://xiazai.xqishu.com/txt/%s.txt'
names_file = 'name.txt'


def downloading(name):
    filename = t_dir % name
    url = d_url % parse.quote(name)
    try:
        request.urlretrieve(url, filename)
        print(' success')
    except Exception as e:
        print(' fail')


if __name__ == '__main__':
    ln = 0
    if (len(sys.argv) == 1 or sys.argv[1] == ''):
        ln = 1
    elif (not str.isalnum(sys.argv[1])):
        sys.exit(9)
    else:
        ln = int(sys.argv[1])

    name = linecache.getline(names_file, ln);
    while name:
        name = name.strip()
        if (name.startswith('---')):
            print(name)
        else:
            print('dwomload %s %s' % (ln, name), end='')
            downloading(name)
        ln += 1
        name = linecache.getline(names_file, ln)
