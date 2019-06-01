import cv2
import pytesseract

class TextRecognizer():
    config = None
    def __init__(self):
        # Config
        # '-l spa' Spanish language
        # '--oem 1' LSTM OCR Engine
        self.config = ('-l spa --oem 1 --psm 3')
        
    def getText(self,img):
        try:    
            text = pytesseract.image_to_string(img, config=self.config)            
            return text
        except Exception as e:
            print(e)



