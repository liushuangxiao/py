# encoding=utf-8
# ^([\d\.]+).*(/public/sms/code)
filename='ips'

file = open(filename, 'r', encoding='UTF-8')
ips = dict()
try:
    while True:
        line = file.readline()
        if line:
            line = line.replace('\n', '')
            if line in ips:
                count = ips[line] + 1
                ips[line] = count
            else:
                ips[line] = 1
        else:
            break
finally:
    file.close()

lower_5 = 0
for key in ips:
    if ips[key] < 20:
        lower_5 += 1
    else:
        print('deny %s;' % key)

print(lower_5)