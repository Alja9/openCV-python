import imutils
import dlib
import cv2
import numpy as np
from imutils import face_utils as fu

detect = dlib.get_frontal_face_detector()
predict = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')

img = cv2.imread('test1.jpg')
img = imutils.resize(img, width=500)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

rect = detect(gray, 1) # Face detections in the grayscale img

for i,rct in enumerate(rect):
    shape = predict(gray, rct)
    shape = fu.shape_to_np(shape)

    x,y,w,h = fu.rect_to_bb(rct)
    cv2.rectangle(img, (x,y), (x+w, y+h), (0,0,255),1)
    #roiColor = img[y:y +h, x:x + w]
    cv2.putText(img, "Face {}".format(i+1), (x-10, y-10), cv2.FONT_HERSHEY_COMPLEX, 0.75, (0,0,255),2)

    for x,y in shape:
        cv2.circle(img, (x,y), 1, (0,255,0), -1)

    #cv2.imshow('Crop Face', roiColor)

cv2.imshow('Show Img', img)
cv2.waitKey(0)
