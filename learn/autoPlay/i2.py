#
'''
基于FLANN的匹配器(FLANN based Matcher)
1.FLANN代表近似最近邻居的快速库。它代表一组经过优化的算法，用于大数据集中的快速最近邻搜索以及高维特征。
2.对于大型数据集，它的工作速度比BFMatcher快。
3.需要传递两个字典来指定要使用的算法及其相关参数等
对于SIFT或SURF等算法，可以用以下方法：
index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)
对于ORB，可以使用以下参数：
index_params= dict(algorithm = FLANN_INDEX_LSH,
                   table_number = 6, # 12   这个参数是searchParam,指定了索引中的树应该递归遍历的次数。值越高精度越高
                   key_size = 12,     # 20
                   multi_probe_level = 1) #2
'''
import cv2
from matplotlib import pyplot as plt


im1 = cv2.imread("tu/2.png")
im2 = cv2.imread("tu/sly.png")

detector = cv2.AKAZE_create()#创建sift检测器

(kps1, descs1) = detector.detectAndCompute(im1, None)
(kps2, descs2) = detector.detectAndCompute(im2, None)

descs1 = descs1.astype("float32")
descs2 = descs2.astype("float32")

bf = cv2.BFMatcher(cv2.NORM_L1)
matches = bf.knnMatch(descs1,descs2, k=2)    # typo fixed

print(matches)

# Apply ratio test
good = []
for m,n in matches:
    if m.distance < 0.9*n.distance:
        good.append([m])

# cv2.drawMatchesKnn expects list of lists as matches.
im3 = cv2.drawMatchesKnn(im1, kps1, im2, kps2, good[1:20], None, flags=2)
cv2.imshow("AKAZE matching", im3)
cv2.waitKey(0)
