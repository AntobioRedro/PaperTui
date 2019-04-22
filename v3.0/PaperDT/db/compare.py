from skimage.measure import compare_ssim
import numpy as np
import cv2

img = cv2.imread("video.png")
img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
i1 = cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY,11,2)
cv2.imwrite('video_t.png', i1)

