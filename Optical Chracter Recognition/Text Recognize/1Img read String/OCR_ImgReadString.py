import cv2
import pytesseract

# Change this path for your own path
pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR/tesseract.exe'
tessdata_dir_config = r'--tessdata-dir "C:/Program Files/Tesseract-OCR/tessdata"'

img = cv2.imread('teksProklamasi.png')
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

# Change this language, Follow the contents of the language text in the image you made
# For example My image is in Indonesian language
print(pytesseract.image_to_string(img, lang='ind', config=tessdata_dir_config))

cv2.imshow('img', img)
cv2.waitKey(0)
