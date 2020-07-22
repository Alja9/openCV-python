import cv2
import time

# init face recognizer
faceCascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

# Input image
fileImg = str(input("Input image name files: "))
pathImg = 'img/%s' % fileImg
image = cv2.imread('img/presidenJokowi.jpg')
 
# converting to grayscale
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
# detect the faces in image
face = faceCascade.detectMultiScale(gray, 1.2, 5)
    
# form a rectangle on the face
for(x, y, width, height) in face:
    # Rectangle face
    cv2.rectangle(image, (x, y), (x+width, y+height), (0, 255, 0), 2)
    
cv2.imshow("IMAGE", image)
cv2.waitKey(0)
cv2.destroyAllWindows()
