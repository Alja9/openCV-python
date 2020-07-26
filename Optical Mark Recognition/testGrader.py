import numpy as np
import cv2
import imutils
from imutils.perspective import four_point_transform as fpt
from imutils import contours

# {number: answer}
correctAnswer = {0: 0, 1: 1, 2: 1, 3: 2, 4: 3, 5: 4, 6: 0, 7: 1, 8: 1, 9: 2}

path = 'images/test1.png'
img = cv2.imread(path)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
blur = cv2.GaussianBlur(gray, (5,5), 0)
edge = cv2.Canny(blur, 75, 200)

contour = cv2.findContours(edge.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
contour = imutils.grab_contours(contour)
documentContour = None

if len(contour)>0:
       contour = sorted(contour, key=cv2.contourArea, reverse=True)
       for i in contour:
              eps = cv2.arcLength(i, True)
              approxi = cv2.approxPolyDP(i, 0.02 * eps, True)

              if len(approxi) == 4:
                     documentContour = approxi
                     break

paper = fpt(img, documentContour.reshape(4,2))
wrped = fpt(gray, documentContour.reshape(4,2))


thresh = cv2.threshold(wrped, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
contour = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
contour = imutils.grab_contours(contour)
questionContour = []

for i in contour:
       (x, y, w, h) = cv2.boundingRect(i)
       aspectRatio = w/float(h)

       if (w>=20 and h>=20 and (aspectRatio >=0.9 and aspectRatio<=1.1)):
              questionContour.append(i)

questionContour = contours.sort_contours(questionContour, method="top-to-bottom")[0]
correct = 0

for(a, b) in enumerate(np.arange(0, len(questionContour), 5)):
       contour = contours.sort_contours(questionContour[b:b+5])[0]
       bubbled = None
       for(c,d) in enumerate(contour):
              mask = np.zeros(thresh.shape, dtype="uint8")
              cv2.drawContours(mask, [d], -1, 255, -1)
              mask = cv2.bitwise_and(thresh, thresh, mask=mask)
              total = cv2.countNonZero(mask)
              if bubbled is None or total > bubbled[0]:
                     bubbled = (total, c)

       color = (0,0,255)
       keyy = correctAnswer[a]
       if keyy==bubbled[1]:
              color=(0,255,0)
              correct+=1
       cv2.drawContours(paper, [contour[keyy]], -1, color, 3)

score = (correct/5.0)*100
print("[i] score: {:.2f}%".format(score))
cv2.putText(paper, "{:.2f}%".format(score), (10,30),cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0,0,255),2)
cv2.imshow("Ori", img)
cv2.imshow("Exam", paper)
cv2.waitKey(0)
cv2.destroyAllWindows()
