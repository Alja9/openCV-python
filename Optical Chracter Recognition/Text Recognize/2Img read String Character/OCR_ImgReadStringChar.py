import cv2
import pytesseract

# Change this path for your own path
pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR/tesseract.exe'
tessdata_dir_config = r'--tessdata-dir "C:/Program Files/Tesseract-OCR/tessdata"'

img = cv2.imread('teksTest.png')
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

# Change this language, Follow the contents of the language text in the image you made
# For example My image is in Indonesian language
# print(pytesseract.image_to_string(img, lang='ind', config=tessdata_dir_config))

# Put the text character into image
h, w, rd = img.shape
boxes = pytesseract.image_to_boxes(img, lang='ind', config=tessdata_dir_config)
for i in boxes.splitlines():
       i = i.split(' ')
       print(i)
       x, y, width, height = int(i[1]), int(i[2]), int(i[3]), int(i[4])
       cv2.rectangle(img, (x,h-y), (width,h-height), (0,0,255),1)
       cv2.putText(img, i[0], (x,h- y+25), cv2.FONT_HERSHEY_SIMPLEX, 0.75,(0,0,255), 2)

cv2.imshow('img', img)
cv2.waitKey(0)
