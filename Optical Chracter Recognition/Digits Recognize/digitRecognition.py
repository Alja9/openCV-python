import cv2
import imutils
from imutils import contours
from imutils.perspective import four_point_transform as fpt

imgPath = '1Test.jpg'

digitNumber = {
        (1,1,1,0,1,1,1): 0,
        (0,1,0,0,1,0,0): 1,
        (1,0,1,1,1,0,1): 2,
        (1,0,1,1,0,1,1): 3,
        (0,1,1,1,0,1,0): 4,
        (1,1,0,1,0,1,1): 5,
        (1,1,0,1,1,1,1): 6,
        (1,1,1,0,0,1,0): 7,
        (1,1,1,1,1,1,1): 8,
        (1,1,1,1,0,1,1): 9,
        }

img = cv2.imread(imgPath)
img = imutils.resize(img, height=500)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
blur = cv2.GaussianBlur(gray, (5,5), 0)
edge = cv2.Canny(blur, 50, 200, 255)

cnt = cv2.findContours(edge.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnt = imutils.grab_contours(cnt)
cnt = sorted(cnt, key=cv2.contourArea, reverse=True)
displayCnt = None

for i in cnt:
        peri = cv2.arcLength(i, True)
        approximate = cv2.approxPolyDP(i, 0.02*peri, True)
        if (len(approximate) == 4):
                displayCnt = approximate
                break

warp = fpt(gray, displayCnt.reshape(4,2))
output = fpt(img, displayCnt.reshape(4,2))

thresh = cv2.threshold(warp, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
kernel  = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (1,5))
thresh = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)

cnt = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnt = imutils.grab_contours(cnt)
digitCnt = []

for i in cnt:
        (x,y,w,h) = cv2.boundingRect(i)
        if w>= 15 and (h>=30 and h<=40):
                digitCnt.append(i)

digitCnt = contours.sort_contours(digitCnt, method="left-to-right")[0]
digitz = []

for i in digitCnt:
        (x,y,w,h) = cv2.boundingRect(i)
        # region of interest
        roi = thresh[y:y+h, x:x+w]

        (roiHeight, roiWidth) = roi.shape
        (dWidth, dHeight) = (int(roiWidth*0.25), int(roiHeight*0.15))
        dHC = int(roiHeight*0.05)

        segemnts = [
                ((0, 0), (w, dHeight)), # top
		((0, 0), (dWidth, h // 2)), # top-left
		((w - dWidth, 0), (w, h // 2)), # top-right
		((0, (h // 2) - dHC) , (w, (h // 2) + dHC)), # center
		((0, h // 2), (dWidth, h)),	# bottom-left
		((w - dWidth, h // 2), (w, h)), # bottom-right
		((0, h - dHeight), (w, h)) # bottom
                ]

        on = [0]*len(segemnts)

        for (j, ((x1,y1), (x2,y2))) in enumerate(segemnts):
                ROIseg = roi[y1:y2, x1:x2]
                total = cv2.countNonZero(ROIseg)
                area = (x2 - x1)*(y2 - y1)
                if total / int(area) > 0.5:
                        on[j]=1
                        
        digits = digitNumber[tuple(on)]
        digitz.append(digits)
        cv2.rectangle(output, (x,y), (x+w, y+h), (0, 255, 0),1)
        cv2.putText(output, str(digits), (x-10, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.65, (0,255,0),2)
        
print("{}{}.{} \u00b0C".format(*digitz))
cv2.imshow("output", output)
cv2.waitKey(0)
