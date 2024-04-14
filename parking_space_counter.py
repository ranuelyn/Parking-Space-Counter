# -*- coding: utf-8 -*-
"""
Created on Sat Oct 28 01:59:52 2023

@author: yusuf
"""

import cv2
import pickle
import numpy as np

def checkParkSpace(image):
    spaceCounter = 0
    for pos in posList:
        x, y = pos
        imgCrop = image[y: y + height, x: x + width]
        
        count = cv2.countNonZero(imgCrop) # count the white pixels
        
        if count < 150:
            color = (0, 255, 0)
            spaceCounter += 1
            
        else:
            color = (0, 255, 255)
        
        cv2.rectangle(img, pos, (pos[0] + width, pos[1] + height), color, 1, )
        cv2.putText(img, str(count), (x + 3, y + height - 3), cv2.FONT_HERSHEY_PLAIN, 0.6, color, 1)
     
    cv2.putText(img, f"Free: {spaceCounter} / {len(posList)} ", (5, 15) , cv2.FONT_HERSHEY_COMPLEX, 0.4, (0, 0, 0), 3)
    cv2.putText(img, f"Free: {spaceCounter} / {len(posList)} ", (5, 15) , cv2.FONT_HERSHEY_COMPLEX, 0.4, (255, 255, 255), 1)
        

cap = cv2.VideoCapture('video.mp4')

width = 27
height = 14

with open('CarParkPos', 'rb') as f:
    posList = pickle.load(f)

while True:
    success, img = cap.read()
    
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # add gaussian blur to decrease unnecessary details
    imgBlur = cv2.GaussianBlur(imgGray, (3, 3), 1)
    imgThreshold = cv2.adaptiveThreshold(imgBlur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 25, 16)
    imgMedian = cv2.medianBlur(imgThreshold, 5)
    imgDilate = cv2.dilate(imgMedian, np.ones((3, 3)), iterations = 1) 
    
    checkParkSpace(imgDilate)
    cv2.imshow('Park Space Counter', img)
    
    #cv2.imshow('imgGray', imgGray)
    #cv2.imshow('imgBlur', imgBlur)
    #cv2.imshow('imgThreshold', imgThreshold)
    #cv2.imshow('imgMedian', imgMedian)
    #cv2.imshow('imgDilate', imgDilate)


    if cv2.waitKey(200) & 0xFF == ord('q'):
        break
