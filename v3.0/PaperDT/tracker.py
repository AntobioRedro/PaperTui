import cv2
import numpy as np

class ObjectTracker():

    frame = None
    containers = None
    def start(self):
        print("Starting")
        #Camera settings
        self.cap = cv2.VideoCapture(1)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

        #General settings
        escala = 1.21
        maxidx = 0
        idx = 0
        itemlist = []

        #Let's go
        self.ret, self.frame = self.cap.read()
    
    def stop(self):
        print("Stopping")
        self.cap.release()
        cv2.destroyAllWindows()
        print("Stopped")

    def trackContainers(self):
        print("Tracking Containers")
        while True:
            _, self.frame = self.cap.read()
            #Containers
            hsv_frame = cv2.cvtColor(self.frame, cv2.COLOR_BGR2HSV)
            low_green = np.array([25, 52, 72])
            high_green = np.array([102, 255, 255])
            green_mask = cv2.inRange(hsv_frame, low_green, high_green)
            green = cv2.bitwise_and(self.frame, self.frame, mask=green_mask)

            image, contours, hier = cv2.findContours(green_mask, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)

            for contour in contours:
                rect = cv2.minAreaRect(contour)
                box = cv2.boxPoints(rect)
                box = np.int0(box)
                W = rect[1][0] 
                H = rect[1][1] 

                if (W>50) and (H>50) and (W<500) and (H<300):
                    #Contour Approximation
                    epsilon = 0.1*cv2.arcLength(contour,True)
                    approx = cv2.approxPolyDP(contour,epsilon,True)
                    #Draw contours
                    cv2.drawContours(self.frame, approx, -1, (0, 255, 255), 3)
                    
            #debug only
            cv2.imshow("Green", green_mask)
            cv2.imshow("w", self.frame)

            #Terminate capture
            key = cv2.waitKey(1)
            if key == 27:
               self.stop()
               break

    def trackTokens():
        print("Tracking Objects")

