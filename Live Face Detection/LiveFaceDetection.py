import cv2
import time

# open camera
camera = cv2.VideoCapture(0)

# init face recognizer
faceCascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
eyeCascade = cv2.CascadeClassifier('haarcascade_eye.xml')

# Size GUIDesktop Camera
widthGC = int(camera.get(cv2.CAP_PROP_FRAME_WIDTH))
heighGC = int(camera.get(cv2.CAP_PROP_FRAME_HEIGHT))
frameSize = (widthGC,heighGC)
print("Size: ", widthGC, ",", heighGC)

timePrev = 0
while True:
    # read the vision from the camera
    ret, vision = camera.read()
    
    # converting to grayscale
    gray = cv2.cvtColor(vision, cv2.COLOR_BGR2GRAY)

    # Get time frame
    timeCurt = time.time()
    sec = timeCurt - timePrev
    timePrev = timeCurt

    fps = 1/(sec)
    str = "FPS: %d" % fps

    # Put text FPS
    cv2.putText(vision, str, (5,50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)
    
    # detect the faces from vision in the camera
    face = faceCascade.detectMultiScale(gray, 1.3, 5)
    
    # form a rectangle on the face
    for(x, y, width, height) in face:
        # Rectangle face
        cv2.rectangle(vision, (x, y), (x+width, y+height), (0, 255, 0), 2)

        # Rectangle for bg text
        cv2.rectangle(vision, (x, y+20), (x+width, y-5),(0, 255, 0), cv2.FILLED)

        # Custom text face
        cv2.putText(vision, "FACE", (x, y+15), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,255,255), 2)
    cv2.imshow("CAMERA", vision)
    if cv2.waitKey(1) == ord("q"): ## press Q in keyboard for exit
        break
    
camera.release()
cv2.destroyAllWindows()
