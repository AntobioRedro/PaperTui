import cv2
import numpy as np
import os
import ocr as tr
import database as db

class ObjectTracker():
    frame = None
    containers = None
    idx = None
    maxidx = None
    mult = 1.01
    tmp_dir ="temp/"
    database = None

    def start(self,camera):
        print("Starting database")
        self.database = db.Database()
       
        print("Starting computer vision system")
        #Camera settings
        self.cap = cv2.VideoCapture(camera)
        
        #General settings
        self.idx = 0
        self.maxidx = 0

        #Green Range
        self.low_green = np.array([25, 52, 72])
        self.high_green = np.array([102, 255, 255])

        #White Range
        self.low_white = np.array([0, 0, 240])
        self.high_white = np.array([255, 15, 255])

        self.ret, self.frame = self.cap.read()
    
    def stop(self):
        try:
            print("Stopping camera")
            self.cap.release()
            cv2.destroyAllWindows()
            print("Stopped")
        except Exception as e:
            print(e)

    def normalizar(self,W,H,x1,x2,y1,y2,angle,center):       
        rotated = False 
                
        if angle < -45: 
            angle+=90 
            rotated = True
             
        
        size = (int(self.mult*(x2-x1)),int(self.mult*(y2-y1))) 
        M = cv2.getRotationMatrix2D((size[0]/2, size[1]/2), angle, 1.0) 

        try:
            cropped = cv2.getRectSubPix(self.frame, size, center)  
            cropped = cv2.warpAffine(cropped, M, size)
             
            croppedW = W if not rotated else H 
            croppedH = H if not rotated else W 

            croppedRotated = cv2.getRectSubPix(cropped, (int(croppedW*self.mult), int(croppedH*self.mult)), (size[0]/2, size[1]/2)) 

            if croppedW>10 and croppedH>10:                    
                cv2.imwrite(self.tmp_dir+str(self.idx) + '.png', croppedRotated)  
                print(self.idx," Foto tomada \n")    
                self.idx += 1          
                if (self.idx > self.maxidx):
                    self.maxidx = self.idx  

        except Exception as e:
            print(e)
    
    #checar funcion
    def deleteExtraPics(self):
        if (self.maxidx > self.idx):
            rm = self.maxidx - self.idx
            for x in range(0, rm):
                try:
                    if os.path.exists(self.tmp_dir+str(self.idx+x)+".png"):
                        print("Deleting ", self.tmp_dir+str(self.idx+x)+".png" )
                        self.items.pop(self.idx+x)
                        os.remove(self.tmp_dir+str(self.idx+x)+".png")
                except Exception as e:
                    print(e)


    def saveItem(self,con):
        xrange = False
        yrange = False
        saved = False
        rect = cv2.minAreaRect(con)
        box = cv2.boxPoints(rect)
        # convert all coordinates floating point values to int
        box = np.int0(box)
        
        #Get coordinates
        W = rect[1][0] 
        H = rect[1][1] 
        Xs = [i[0] for i in box] 
        Ys = [i[1] for i in box] 
        x1 = min(Xs) 
        x2 = max(Xs) 
        y1 = min(Ys) 
        y2 = max(Ys) 
        angle = rect[2] 
        center = (int((x1+x2)/2), int((y1+y2)/2)) 

        print("ITEM: ",self.idx)
        titem = self.database.getItem(self.idx)
        
        if (titem==None):
            self.database.insertItem(self.idx,x1,x2,y1,y2,"","","")
            saved = True                 
        else:
            print(titem)
            if ((x1 > titem[1] - 5) and (x1 < titem[3]+5)):
                xrange = True

            if ((y1 > titem[3] -5 ) and (y1 < titem[3]+5)):
                yrange = True

            if (xrange == False) and (yrange==False):
                self.database.updateItem(self.idx,x1,x2,y1,y2,"","","")
                saved = True                  
            else:
                print("NO cambios: ",self.idx, "\n")
                self.idx += 1          
                if (self.idx > self.maxidx):
                    self.maxidx = self.idx 
                saved = False

        return W,H,x1,x2,y1,y2,angle,center,saved
            

    def trackContainers(self):
        print("Tracking Tokens")
        while True:        
            self.idx = 0
            _, self.frame = self.cap.read()
            #Paper detection
            hsv_frame = cv2.cvtColor(self.frame, cv2.COLOR_BGR2HSV)

            #Green
            green_mask = cv2.inRange(hsv_frame, self.low_green, self.high_green)
            green = cv2.bitwise_and(self.frame, self.frame, mask=green_mask)
            image, contours, hier = cv2.findContours(green_mask, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
            for contour in contours:
                rect = cv2.minAreaRect(contour)
                box = cv2.boxPoints(rect)
                box = np.int0(box)
                W = rect[1][0] 
                H = rect[1][1] 

                if (W>50) and (H>50):
                    #Contour Approximation
                    epsilon = 0.1*cv2.arcLength(contour,True)
                    approx = cv2.approxPolyDP(contour,epsilon,True)
                    #Draw contours
                    cv2.drawContours(self.frame, approx, -1, (0, 255, 255), 3)
                    #Save coords
                    

            #White 
            white_mask = cv2.inRange(hsv_frame, self.low_white, self.high_white)
            white = cv2.bitwise_and(self.frame, self.frame, mask=white_mask)
            image, contours, hier = cv2.findContours(white_mask, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
            for contour in contours:
                rect = cv2.minAreaRect(contour)
                box = cv2.boxPoints(rect)
                box = np.int0(box)
                W = rect[1][0] 
                H = rect[1][1] 

                if (W>10) and (H>10):
                    #Contour Approximation
                    epsilon = 0.1*cv2.arcLength(contour,True)
                    approx = cv2.approxPolyDP(contour,epsilon,True)
                    #Draw contours
                    cv2.drawContours(self.frame, approx, -1, (255, 255, 0), 3)
                    W,H,x1,x2,y1,y2,angle,center,saved = self.saveItem(contour)
                    if (saved):
                        self.normalizar(W,H,x1,x2,y1,y2,angle,center)
                    #Save coords
                    
    
            #self.deleteExtraPics()
            #debug only
            cv2.imshow("Green", green_mask)
            cv2.imshow("White", white_mask)
            cv2.imshow("Color", self.frame)

            #Terminate capture
            key = cv2.waitKey(1)
            if key == 27:
               self.stop()
               break

            os.system("PAUSE")

        

        

        
