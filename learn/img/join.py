from os import listdir

from PIL import Image


def join(path):
    imgs = [Image.open(path + '/' + fn) for fn in listdir(path) if fn.lower().endswith('.jpg')]

    width, height = imgs[0].size
    result = Image.new(imgs[0].mode, (width, height * len(imgs)))

    for i, im in enumerate(imgs):
        result.paste(im, box=(0, i * height))

    result.save(path + '-he.jpg')

home = 'E:/hczj/kehu/'
for dir in listdir(home):

    if dir.lower().endswith('.zip'):
        continue

    join(home + '/' + dir + '/施工图')
    join(home + '/' + dir + '/物料清单')