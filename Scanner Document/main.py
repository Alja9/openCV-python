from pyimagesearch.transform import four_point_transform
from skimage.filters import threshold_local

import numpy as np
import cv2
import imutils

#pathImg = str(input("Input file name img: "))
img = cv2.imread('img.jpg')
ratio = img.shape[0]/500.0
ori = img.copy()
img = imutils.resize(img, height=500)

# EDGE DETECTION
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
gray = cv2.GaussianBlur(gray, (5,5), 0)
forEdge = cv2.Canny(gray, 75, 200)

print("[i] Edge Detection")
cv2.imshow('Edge',forEdge)
cv2.waitKey(0)

# FINDING CONTOURS
contours = cv2.findContours(forEdge.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
contours = imutils.grab_contours(contours)
contours = sorted(contours, key=cv2.contourArea, reverse = True)[:5]

for i in contours:
       peri = cv2.arcLength(i, True)
       approximate = cv2.approxPolyDP(i, 0.02*peri, True)

       if len(approximate)==4:
              screenContours = approximate
              break

print("[i] Find Contours of Object box")
cv2.drawContours(img, [screenContours], -1, (0,255,0), 2)
cv2.imshow("Outline", img)
cv2.waitKey(0)
cv2.destroyAllWindows()

# APPLY A PERSPECTIVE TRANSFORM & THRESHOLD
warp = four_point_transform(ori, screenContours.reshape(4,2)*ratio)
warp = cv2.cvtColor(warp, cv2.COLOR_BGR2GRAY)
thresHold = threshold_local(warp, 11, offset=10, method="gaussian")
warp = (warp>thresHold).astype("uint8")*255

print("[i] Apply a Perspective Transform & Threshold")
cv2.imshow("Original", imutils.resize(ori, height = 650))
cv2.imshow("Scanned", imutils.resize(warp, height = 650))
cv2.waitKey(0)
