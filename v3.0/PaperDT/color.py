import cv2
import numpy as np


cap = cv2.VideoCapture(1)

while True:
    _, frame = cap.read()
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    # Green color
    low_green = np.array([25, 52, 72])
    high_green = np.array([102, 255, 255])
    green_mask = cv2.inRange(hsv_frame, low_green, high_green)
    green = cv2.bitwise_and(frame, frame, mask=green_mask)

    image, contours, hier = cv2.findContours(green_mask, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)

    for contour in contours:
        rect = cv2.minAreaRect(contour)
        box = cv2.boxPoints(rect)
        box = np.int0(box)
        W = rect[1][0] 
        H = rect[1][1] 

        if (W>50) and (H>50) and (W<500) and (H<300):
            epsilon = 0.1*cv2.arcLength(contour,True)
            approx = cv2.approxPolyDP(contour,epsilon,True)
            cv2.drawContours(frame, approx, -1, (0, 255, 255), 3)

    cv2.imshow("Green", green_mask)
    cv2.imshow("w", frame)

    key = cv2.waitKey(1)
    if key == 27:
        break