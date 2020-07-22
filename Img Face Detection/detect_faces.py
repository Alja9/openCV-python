import numpy as np
import cv2
import time
import sys

def dot():
    loadImg = "...\n"
    for l in loadImg:
        sys.stdout.write(l)
        sys.stdout.flush()
        time.sleep(0.5)

protoTxt = 'deploy.prototxt.txt'
caffeModel = 'res10_300x300_ssd_iter_140000.caffemodel'

# Input Image name files
fileImg = str(input("Input image name files: "))
pathImg = 'img/%s' % fileImg
image = cv2.imread(pathImg)
print("[i] loading image", end=" ");dot()

# Read model files
print("[i] loading model", end=" "); dot()
readModel = cv2.dnn.readNetFromCaffe(protoTxt, caffeModel)

# Shape image to know height and width
(h, w) = image.shape[:2]
dsize = cv2.dnn.blobFromImage(cv2.resize(image, (300, 300)), 1.0, (300, 300), (104.0, 177.0, 123.0))

# detections and predictions
print("[i] computing object detections", end=" "); dot()
readModel.setInput(dsize)
detections = readModel.forward()
for i in range(0, detections.shape[2]):
    # prediction confidence
    conf = detections[0, 0, i, 2]
    if conf > 0.5:
        box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
        (startX, startY, endX, endY) = box.astype("int")

        text = "{:.2f}%".format(conf * 100)
        y = startY - 10 if startY - 10 > 10 else startY + 10
        cv2.rectangle(image, (startX, startY), (endX, endY),(0, 0, 255), 2)
        cv2.putText(image, text, (startX, y),cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 255), 1)

# Show Image input
cv2.imshow("Gambar", image)
print("[i] everything successfully")
cv2.waitKey(0)
cv2.destroyAllWindows()
