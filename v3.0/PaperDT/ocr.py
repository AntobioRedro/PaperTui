import cv2
import pytesseract

class TextRecognizer():
    config = None
    def __init__(self):
        # Config
        # '-l spa' Spanish language
        # '--oem 1' LSTM OCR Engine
        self.config = ('-l spa --oem 1 --psm 3')

    def transformImg(self,img):
        try:
            im = cv2.imread(img, cv2.IMREAD_COLOR)            
            im = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
            imgT = cv2.adaptiveThreshold(im,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY,11,2)

            #DEGUB ONLY
            cv2.imshow("Thresh", imgT)
            cv2.imwrite("lol.png",imgT)
            return imgT
        except Exception as e:
            print(e)
        
    def getText(self,img):
        try:
            im = self.transformImg(img)     
            text = pytesseract.image_to_string(im, config=self.config)            
            return text
        except Exception as e:
            print(e)



