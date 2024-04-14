# -*- coding: utf-8 -*-
"""
Created on Sat Oct 28 02:00:12 2023

@author: yusuf
"""

import cv2
import pickle

width = 27
height = 14

try:
    with open('CarParkPos', 'rb') as f:
        posList = pickle.load(f)
except:
    posList = []

def mouseClick(events, x, y, flags, parameters):
    
    if events == cv2.EVENT_LBUTTONDOWN:
        posList.append((x, y))
        
    if events == cv2.EVENT_RBUTTONDOWN:
        for i, pos in enumerate(posList):
            x1, y1 = pos
            if x1 < x < x1 + width and y1 < y < y1 + height: # click rb to delete the one we click
                posList.pop(i)
                
    with open('CarParkPos', 'wb') as f:
        pickle.dump(posList, f)
        
        

while True:
    img = cv2.imread('first_frame.png')
   
    # visualize the clicks
    for pos in posList:
        cv2.rectangle(img, pos, (pos[0] + width, pos[1] + height), (255, 0, 0), 2)
        
   
    # print('posList -> ', posList)
    
    cv2.imshow('ParkingSpaceCounter', img)
    cv2.setMouseCallback('ParkingSpaceCounter', mouseClick)
    cv2.waitKey(1)