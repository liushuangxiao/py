import cv2
from matplotlib import pyplot as plt
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

img = cv2.imread('tu/sly.png',0)

akaze = cv2.AKAZE_create()
kp, des = akaze.detectAndCompute(img,None)
img2=cv2.drawKeypoints(img,kp,None,(255,0,0),4)


plt.figure(figsize=(10,10))
plt.title('akaze检测特征点',fontsize=20)
plt.axis('off')
plt.imshow(img2)
plt.show()


cv2.waitKey(0)
cv2.destroyAllWindows()