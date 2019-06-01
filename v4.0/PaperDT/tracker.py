import cv2
import numpy as np
import os
import time
import ocr as tr
import database as db
import recognizer as obr
import modelgen as mgen
from threading import Thread

class ObjectTracker():
    frame = None
    outputframe = None
    containers = None
    idx = None
    maxidx = None
    conid = None
    conmaxid = None
    mult = 1.01
    tmp_dir ="temp/"
    database = None
    ocr = None
    recognizer = None
    mgenerator = None
    debug = False    

    def start(self,camera):
        print(">>> Starting PaperType <<<")
        print("Connecting to database")
        self.database = db.Database()
       
        print("Starting computer vision system")
        #Camera settings
        self.cap = cv2.VideoCapture(camera)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

        print("Starting optical character recognition")
        self.ocr = tr.TextRecognizer()

        print("Starting Object recognition")
        self.recognizer = obr.ObjectRecognizer()
        
        print("Starting Model generator")
        self.mgenerator = mgen.ModelGenerator(self.database)

        #General settings
        self.idx = 0
        self.maxidx = 0
        self.conid = 0
        self.conmaxid = 0

        #Green Range
        self.low_green = np.array([25, 52, 72])
        self.high_green = np.array([102, 255, 255])

        #White Range
        self.low_white = np.array([0, 0, 230])
        #self.high_white = np.array([255, 15, 255])
        self.high_white = np.array([255,20, 255])

        self.ret, self.frame = self.cap.read()
        
    def stop(self):
        try:
            print("Shuting down all systems")
            self.cap.release()
            cv2.destroyAllWindows()
            print(">>> PaperType stopped <<<")
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
                im = cv2.imread(self.tmp_dir+str(self.idx) + '.png', cv2.IMREAD_COLOR)            
                ret,imgT = cv2.threshold(im,127,255,cv2.THRESH_BINARY)
                cv2.imwrite(self.tmp_dir+str(self.idx) + '.png',imgT)
                #print(self.idx," Foto tomada \n")

                #get Text
                text = self.ocr.getText(self.tmp_dir+str(self.idx) + '.png')
                self.database.updateText(self.idx,text)
                
                if (text==""):
                    #get Type
                    type = self.recognizer.compare(self.tmp_dir+str(self.idx) + '.png')
                    self.database.updateType(self.idx,type)
                    cv2.putText(self.outputframe, type, center, cv2.FONT_HERSHEY_SIMPLEX,0.5, (0, 0, 255), 2)
                else:
                    cv2.putText(self.outputframe, text, center, cv2.FONT_HERSHEY_SIMPLEX,0.5, (255, 0, 255), 2)
                self.idx += 1 
                if (self.idx > self.maxidx):
                    self.maxidx = self.idx                                           

        except Exception as e:
            print(e)
    
    
    def deleteExtraItems(self):
        #print("DELETING?", self.maxidx," - ",self.idx)
        if (self.maxidx > self.idx):
            rm = self.maxidx - self.idx

            for x in range(0, rm):
                try:
                    if os.path.exists(self.tmp_dir+str(self.idx+x)+".png"):                        
                        os.remove(self.tmp_dir+str(self.idx+x)+".png")                        
                        #print("Deleting ", self.tmp_dir+str(self.idx+x)+".png" )
                except Exception as e:
                    print(e)
            self.database.removeExtras(self.idx-1)
            self.maxidx = self.idx

    def deleteExtraContainers(self):
        #print("DELETING C?", self.conmaxid," - ",self.conid)
        if (self.conmaxid > self.conid):
            self.database.removeExtrasContainers(self.conid-1)
            self.conmaxid = self.conid

    def saveItem(self,con):
        xrange = False
        yrange = False
        saved = False
        rect = cv2.minAreaRect(con)
        box = cv2.boxPoints(rect)
        box = np.int0(box)

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

        #print("ITEM: ",self.idx)                 
        titem = self.database.getItem(self.idx)

        if (titem==None):
            self.database.insertItem(self.idx,x1,x2,y1,y2,"","","")
            saved = True                 
        else:
            #print(titem)
            if(titem[7]=="None"):
                self.database.updateItem(self.idx,x1,x2,y1,y2,"","","")
                saved = True 
            else:
                if ((x1 > titem[1] - 5) and (x1 < titem[3]+5)):
                    xrange = True

                if ((y1 > titem[3] -5 ) and (y1 < titem[3]+5)):
                    yrange = True

                if (xrange == False) and (yrange==False):
                    self.database.updateItem(self.idx,x1,x2,y1,y2,"","","")
                    saved = True                  
                else:
                    #print("NO cambios: ",self.idx, "\n")
                    if (titem[6]!=""):
                        cv2.putText(self.outputframe, titem[6], center, cv2.FONT_HERSHEY_SIMPLEX,0.5, (255, 0, 255), 2)
                    else:
                        cv2.putText(self.outputframe, titem[7], center, cv2.FONT_HERSHEY_SIMPLEX,0.5, (0, 0, 255), 2)

                    self.idx += 1          
                    if (self.idx > self.maxidx):
                        self.maxidx = self.idx 
                    saved = False


        return W,H,x1,x2,y1,y2,angle,center,saved
            
    def saveContainer(self,con):
        xrange = False
        yrange = False
        rect = cv2.minAreaRect(con)
        box = cv2.boxPoints(rect)
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

        titem = self.database.getContainer(self.conid)

        if (titem==None):
            self.database.insertContainer(self.conid,x1,x2,y1,y2,"div") 
            self.conid += 1
        else:
            #print(titem)            
            if ((x1 > titem[1] - 5) and (x1 < titem[3]+5)):
                xrange = True
            if ((y1 > titem[3] -5 ) and (y1 < titem[3]+5)):
                yrange = True
            if (xrange == False) and (yrange==False):
                self.database.updateContainer(self.conid,x1,x2,y1,y2,"div")
                self.conid += 1
            else:
                #print("NO cambios: ",self.conid, "\n")   
                self.conid += 1
                
        if (self.conid > self.conmaxid):
            self.conmaxid = self.conid            
    
    def video(self):
        _, self.frame = self.cap.read()
        _, self.outputframe = self.cap.read()

    def trackContainers(self):
        print("Tracking Tokens")               
        start = time.time()
        
        while True:                    
            self.idx = 0
            self.conid = 0     
            Thread(target=self.video, args=()).start()
            #_, self.frame = self.cap.read()
            #_, self.outputframe = self.cap.read()

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
                    cv2.drawContours(self.outputframe, approx, -1, (0, 255, 255), 3)
                    self.saveContainer(contour)
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

                if (W>15) and (H>15):
                    #Contour Approximation
                    epsilon = 0.1*cv2.arcLength(contour,True)
                    approx = cv2.approxPolyDP(contour,epsilon,True)
                    #Draw contours
                    cv2.drawContours(self.outputframe, approx, -1, (255, 255, 0), 3)
                    W,H,x1,x2,y1,y2,angle,center,saved = self.saveItem(contour)
                    if (saved):
                        self.normalizar(W,H,x1,x2,y1,y2,angle,center)
                        
                    #Save coords
                    #print("Max: ",self.maxidx)
                    
            #Delete extra tokens
            self.deleteExtraItems()
            self.deleteExtraContainers()
            
            #Generate model            
            self.mgenerator.updateModel()

            #debug only
            if (self.debug):
                cv2.imshow("Green", green_mask)
                cv2.imshow("White", white_mask)
                cv2.imshow("Color", self.frame)
           
            cv2.imshow("PaperType", self.outputframe)
            
            #Terminate capture
            key = cv2.waitKey(1)
            if key == 27:
               self.stop()
               break

            finish = time.time()
            idtime = finish - start

            #print("Identification time: ", idtime)     

            if (self.debug):
                os.system("PAUSE")

        

        

        
