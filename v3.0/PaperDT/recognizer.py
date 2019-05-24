import cv2 
import numpy as np 
from skimage.measure import compare_ssim

class ObjectRecognizer():
    dir ="db/"
    items = list()
    def __init__(self):
        self.getItems()

    def getItems(self):
        self.items.append("img.png")

    def compare(self,img2):
        for i in range(0,len(self.items)):

            img = cv2.imread(self.dir+self.items[i])
            i1 = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

            im = cv2.imread(img2)
            i2 = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)

            height = im.shape[0]
            width = im.shape[1]
            dim = (width, height)

            #resize image
            resized = cv2.resize(i1, dim, interpolation = cv2.INTER_AREA)

            (score, diff) = compare_ssim(resized, i2, full=True)
            diff = (diff * 255).astype("uint8")
            print("SSIM: {}".format(score))

            if (score>=0.80):
                return self.items[i].replace(".png", "")               
                break
      