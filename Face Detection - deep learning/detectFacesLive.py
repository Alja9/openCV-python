from imutils.video import VideoStream
import numpy as np
import imutils
import time
import cv2
import sys

def dot():
    loadImg = "...\n"
    for l in loadImg:
        sys.stdout.write(l)
        sys.stdout.flush()
        time.sleep(0.5)

protoTxt = 'deploy.prototxt.txt'
caffeModel = 'res10_300x300_ssd_iter_140000.caffemodel'

# Read model files
print("[i] loading model", end=" "); dot()
readModel = cv2.dnn.readNetFromCaffe(protoTxt, caffeModel)

# Init camera
print("[i] starting video stream", end=" "); dot()
vs = VideoStream(src=0).start()
time.sleep(2.0)

# Frame of video stream
while True:
        frame = vs.read()
        frame = imutils.resize(frame, width=720) # 720p
	# Shape frame video to know height and width
        (h, w) = frame.shape[:2]
        dsize = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)), 1.0, (300, 300), (104.0, 177.0, 123.0))

        readModel.setInput(dsize)
        detections = readModel.forward()

	# loop over the detections
        for i in range(0, detections.shape[2]):
		# prediction confidence
                conf = detections[0, 0, i, 2]
                if conf < 0.5:
                        continue

                box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                (startX, startY, endX, endY) = box.astype("int")
 
                text = "{:.2f}%".format(conf * 100)
                y = startY - 10 if startY - 10 > 10 else startY + 10
                cv2.rectangle(frame, (startX, startY), (endX, endY),(0, 255, 0), 2)
                cv2.rectangle(frame, (startX, y+20), (endX, y-5),(0, 255, 0), cv2.FILLED)
                cv2.putText(frame, text, (startX+2, y+14),cv2.FONT_HERSHEY_SIMPLEX, 0.45, (255, 255, 255), 1)

	# Show the output frame video
        cv2.imshow("Frame", frame)
        if cv2.waitKey(1) & 0xFF == ord("q"): # Press q to quit
                break

cv2.destroyAllWindows()
vs.stop()
