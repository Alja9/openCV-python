import cv2
import pytesseract
import numpy as np
from PIL import ImageGrab

pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR/tesseract.exe'
tessdata_dir_config = r'--tessdata-dir "C:/Program Files/Tesseract-OCR/tessdata"'

cap = cv2.VideoCapture(0)
cap.set(3,640)
cap.set(4,480)

def captureScreen(forBox=(200,200,640,480)):
       capScreen = np.array(ImageGrab.grab(forBox))
       capScreen = cv2.cvtColor(capScreen, cv2.COLOR_RGB2BGR)
       return capScreen

while True:
       ret, frame = cap.read()
       frame = captureScreen()

       h, w, ret = frame.shape
       boxes = pytesseract.image_to_boxes(frame, lang='ind', config=tessdata_dir_config)
       for i in boxes.splitlines():
              i=i.split()
              x,y,width,height = int(i[1]),int(i[2]),int(i[3]),int(i[4])
              cv2.rectangle(frame, (x,h-y),(w,h-height),(0,0,255),2)
              cv2.putText(frame,i[0],(x,h- y+25),cv2.FONT_HERSHEY_SIMPLEX, 0.75,(0,0,255),1)              
       cv2.imshow("frame",frame)
       if cv2.waitKey(1) & 0xFF == ord("q"):
              break
