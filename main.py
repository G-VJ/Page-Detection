# -*- coding: utf-8 -*-
"""
Created on Sat May  1 11:53:26 2021

@author: gauravvijayvergiya
"""

import cv2 
import numpy as np
from matplotlib import pyplot as plt

def get_contour(img):
# convert image to gray scale 
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    
    # applying blur to image to remove noise and small unwanted pixed that we don not want to detect
    img = cv2.blur(img, (3, 3), 0)
    
    #---- apply automatic Canny edge detection using the computed median----
    
    v = np.median(img)    #get median of image pixes
    sigma = 0.33
    
    #get lower and upper filter value for canny edge detection
    lower = int(max(0, (1.0 - sigma) * (255- v)))  
    upper = int(min(255, (1.0 + sigma) *(255- v)))
    
    #canny edge detection used to detected edges of the object present in the image
    edges = cv2.Canny(img, lower, upper)
        
    # Find all the closed shape present using the edge detected earlier 
    contours, _ = cv2.findContours(edges, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
    #sort contors by area 
    contours = sorted(contours, key = cv2.contourArea, reverse = True)[:5]
    sel_contour_flag = False
    
    #select a polynomial contor with 4 edge from all contors
    for c in contours:
        peri = cv2.arcLength(c, True)
        approx = cv2 .approxPolyDP(c, 0.02 * peri, True)
    	# if our approximated contour has four points, then we
    	# can assume that we have found our screen   
        if len(approx) == 4:
            sel_contour = c
            sel_contour_flag = True

    #pick the lasrget contor if no contor detected. 
    if sel_contour_flag == False and len(contours) > 0:
        print("No Contro Detected")
        sel_contour = contours[0]  
        sel_contour_flag = True
    if sel_contour_flag == True:
        return sel_contour_flag, sel_contour
    else: 
        return sel_contour_flag, 0


if __name__ == "__main__":
    
    image_name = input('Please enter Image name')
    #Read Image and resize 
    image = cv2.imread(image_name)
    if image is None:
        print("Image is empty!!")
    else:
        flag, contour = get_contour(image)
        if flag == True:
            cv2.drawContours(image, [contour], -1, (0, 0, 255), 2)
            cv2.imwrite('output.jpg', image)
    

