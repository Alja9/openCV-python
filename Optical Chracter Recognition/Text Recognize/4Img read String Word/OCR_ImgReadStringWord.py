import cv2
import pytesseract

pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR/tesseract.exe'
tessdata_dir_config = r'--tessdata-dir "C:/Program Files/Tesseract-OCR/tessdata"'

img = cv2.imread('testBro.png')
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

# data pytesseract
# len(j)==12
# [   0          1           2           3           4          5         6       7       8        9        10       11 ]
# ['level', 'page_num', 'block_num', 'par_num', 'line_num', 'word_num', 'left', 'top', 'width', 'height', 'conf', 'text']

boxes = pytesseract.image_to_data(img, lang='ind', config=tessdata_dir_config)
for i,j in enumerate(boxes.splitlines()):
       if i != 0:
              j = j.split()
              if (len(j)==12):
                     print(j[11])
                     x,y,width,height = int(j[6]),int(j[7]),int(j[8]),int(j[9])
                     cv2.rectangle(img, (x,y), (x+width, y+height), (0,0,255), 1)
                     cv2.putText(img, j[11], (x,y-5), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0,0,255),1)
                     
cv2.imshow('img', img)
cv2.waitKey(0)
