import os
import cv2
import IPython
path = os.path.dirname(os.path.abspath("den_mau.jpg"))

image1=cv2.imread(path,cv2.IMREAD_UNCHANGED)
scale_percent = 10 # percent of original size
width = int(image1.shape[1] * scale_percent / 100)
height = int(image1.shape[0] * scale_percent / 100)
dim = (width, height)
image1=cv2.resize(image1,dim, interpolation = cv2.INTER_AREA)
cv2.imshow('image',image1)
cv2.waitKey(0)
cv2.destroyWindow()
