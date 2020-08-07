import imutils
import dlib
import cv2
import numpy as np
from imutils import face_utils as fu
from scipy.spatial import distance as dist

cap = cv2.VideoCapture('blinkDetectionDemo.mp4')
'''
EAR Concept:
	eye[1]   eye[2]
eye[0] - - - - + - - - eye[3]
	eye[5]   eye[4]

	Formula --> EAR = (||eye[1] - eye[5]|| + ||eye[2] - eye[4]||) / (2*||eye[0] - eye[3]||)
'''
def eyeAspectRatio(eye):
    a = dist.euclidean(eye[1], eye[5])
    b = dist.euclidean(eye[2], eye[4])
    c = dist.euclidean(eye[0], eye[3])
    return (a + b) / (2.0 * c)

count = 0
total = 0
detect = dlib.get_frontal_face_detector()
predict = dlib.shape_predictor('Facial Landmark/shape_predictor_68_face_landmarks.dat')

(lStart, lEnd) = fu.FACIAL_LANDMARKS_IDXS["left_eye"]
(rStart, rEnd) = fu.FACIAL_LANDMARKS_IDXS["right_eye"]
while True:
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    rects = detect(gray, 0)

    for rect in rects:
        shape = predict(gray, rect)
        shape = fu.shape_to_np(shape)

        leftEye = shape[lStart:lEnd]
        rightEye = shape[rStart:rEnd]
        leftEAR = eyeAspectRatio(leftEye)
        rightEAR = eyeAspectRatio(rightEye)
        ear = (leftEAR + rightEAR) / 2.0

        leftEyeHull = cv2.convexHull(leftEye)
        rightEyeHull = cv2.convexHull(rightEye)
        cv2.drawContours(frame, [leftEyeHull], -1, (0, 255, 0), 1)
        cv2.drawContours(frame, [rightEyeHull], -1, (0, 255, 0), 1)

        if ear < 0.3:
            count += 1
        else:
            if count >= 3:
                total += 1
            count = 0

        cv2.putText(frame, "Blinks: {}".format(total), (20, 30), cv2.FONT_HERSHEY_COMPLEX, 0.75, (0, 0, 255), 2)
        cv2.putText(frame, "EAR: {:.2f}".format(ear), (300, 30), cv2.FONT_HERSHEY_COMPLEX, 0.75, (0, 0, 255), 2)

    reSize = cv2.resize(frame, (500,400), interpolation=cv2.INTER_LINEAR)
    cv2.imshow("Frame", reSize)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
