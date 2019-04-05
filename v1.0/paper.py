import os
import time 
import numpy as np
import cv2
import pytesseract
from skimage.measure import compare_ssim


def identify(path):
  img = cv2.imread("db/video.png")
  img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
  i1 = cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY,11,2)

  im = cv2.imread(path)
  im = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
  i2 = cv2.adaptiveThreshold(im,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY,11,2)

  height = im.shape[0]
  width = im.shape[1]
  dim = (width, height)

  #resize image
  resized = cv2.resize(i1, dim, interpolation = cv2.INTER_AREA)

  (score, diff) = compare_ssim(resized, i2, full=True)
  diff = (diff * 255).astype("uint8")
  #print("SSIM: {}".format(score))

  if (score> 0.60):
      return ("Video")

  img = cv2.imread("db/img.png")
  img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
  i1 = cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY,11,2)

  im = cv2.imread(path)
  im = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
  i2 = cv2.adaptiveThreshold(im,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY,11,2)

  height = im.shape[0]
  width = im.shape[1]
  dim = (width, height)

  #resize image
  resized = cv2.resize(i1, dim, interpolation = cv2.INTER_AREA)

  (score, diff) = compare_ssim(resized, i2, full=True)
  diff = (diff * 255).astype("uint8")
  #print("SSIM: {}".format(score))

  if (score> 0.60):
      return ("img")

  img = cv2.imread("db/map.png")
  img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
  i1 = cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY,11,2)

  im = cv2.imread(path)
  im = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
  i2 = cv2.adaptiveThreshold(im,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY,11,2)

  height = im.shape[0]
  width = im.shape[1]
  dim = (width, height)

  #resize image
  resized = cv2.resize(i1, dim, interpolation = cv2.INTER_AREA)

  (score, diff) = compare_ssim(resized, i2, full=True)
  diff = (diff * 255).astype("uint8")
  #print("SSIM: {}".format(score))

  if (score> 0.60):
      return ("map")
  
cap = cv2.VideoCapture(1)
#cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
#cap.set(cv2.CAP_PROP_BRIGHTNESS , 100)
#cap.set(cv2.CAP_PROP_CONTRAST  , 100)
maxidx = 0

while(True):
  # Capture frame-by-frame
   ret, frame = cap.read()

   # Our operations on the frame come here
   gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
   ret, thresh_gray = cv2.threshold(cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY),200, 255, cv2.THRESH_BINARY)
   image, contours, hier = cv2.findContours(thresh_gray, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)

   mult = 1 # I wanted to show an area slightly larger than my min rectangle set this to one if you don't 
   idx = 0
   for con in contours:
        rect = cv2.minAreaRect(con)
        box = cv2.boxPoints(rect)
        # convert all coordinates floating point values to int
        box = np.int0(box)

        #CROP PICS
        W = rect[1][0] 
        H = rect[1][1] 

        Xs = [i[0] for i in box] 
        Ys = [i[1] for i in box] 
        x1 = min(Xs) 
        x2 = max(Xs) 
        y1 = min(Ys) 
        y2 = max(Ys) 

        rotated = False 
        angle = rect[2] 

        if angle < -45: 
           angle+=90 
           rotated = True
           
        center = (int((x1+x2)/2), int((y1+y2)/2)) 
        size = (int(mult*(x2-x1)),int(mult*(y2-y1))) 

        M = cv2.getRotationMatrix2D((size[0]/2, size[1]/2), angle, 1.0) 

        try:
           cropped = cv2.getRectSubPix(gray, size, center)  
           cropped = cv2.warpAffine(cropped, M, size)
           
           croppedW = W if not rotated else H 
           croppedH = H if not rotated else W 

           croppedRotated = cv2.getRectSubPix(cropped, (int(croppedW*mult), int(croppedH*mult)), (size[0]/2, size[1]/2)) 

           if croppedW>50 and croppedH>20:
              idx+=1
              cv2.imwrite(str(idx) + '.png', croppedRotated)
              if (idx > maxidx):
                maxidx = idx
        except Exception as e:
           pass
        
        #DELETE EXTRA PICS
        if (maxidx > idx):
          rm = maxidx - idx
          for x in range(1, rm+1):
            n = idx+1
            try:
              if os.path.exists(str(n)+".png"):
                os.remove(str(n)+".png") 
            except Exception as e:
                print("Cannot delete")

        #GET TEXT
        text = ""
        try:
          config = ('-l spa --oem 1 --psm 3')
          im = cv2.imread(str(idx) + '.png', cv2.IMREAD_COLOR)
          text = pytesseract.image_to_string(im, config=config)
        except Exception as e:
          print("no text")

        if text:
          cv2.putText(frame, text, (int((x1+x2)/2), int((y1+y2)/2)), cv2.FONT_HERSHEY_SIMPLEX,0.5, (0, 255, 255), 2)
          text = ""

        #COMPARE PICS
        try:
          item = identify(str(idx) + '.png')
          if item:
            cv2.putText(frame, item, (int((x1+x2)/2), int((y1+y2)/2)), cv2.FONT_HERSHEY_SIMPLEX,0.5, (255, 0, 255), 2)
        except Exception as e:
          print("No img")
        
        cv2.drawContours(frame, [box], 0, (0, 255, 0),1)

   # Display the resulting frame
   #cv2.imshow('frame',thresh_gray)
   cv2.imshow('color',frame)
   #cv2.imshow('threshold',thresh_gray)
   if cv2.waitKey(1) & 0xFF == ord('q'):
        break
   #time.sleep(0.5)
# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()

