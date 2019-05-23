import cv2 
import numpy as np 
from skimage.measure import compare_ssim

class ObjectRecognizer():
    def __init__(self):
      i1 = cv2.imread("video2.png")
      i1 = cv2.cvtColor(i1, cv2.COLOR_BGR2GRAY)
      #i1 = cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY,11,2)

      i2 = cv2.imread("3.png")
      i2 = cv2.cvtColor(i2, cv2.COLOR_BGR2GRAY)
      #i2 = cv2.adaptiveThreshold(im,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY,11,2)

      height = i2.shape[0]
      width = i2.shape[1]
      dim = (width, height)

      #resize image
      resized = cv2.resize(i1, dim, interpolation = cv2.INTER_AREA)

      (score, diff) = compare_ssim(resized, i2, full=True)
      diff = (diff * 255).astype("uint8")
      print("SSIM: {}".format(score))  