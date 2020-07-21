import cv2
import math

# File image
path = 'test.png'
gambar = cv2.imread(path)

# point list
daftarTitik = []

# mouse point
def cursor(event, x, y, flags, params):
    if event == cv2.EVENT_LBUTTONDOWN:
        # size of point list
        ukuran = len(daftarTitik)
        if ukuran != 0 and ukuran % 3 != 0:
            cv2.line(gambar, tuple(daftarTitik[::3][-1]), (x, y), (0,255,0), 2)
        # draw point line
        cv2.circle(gambar, (x, y), 3, (0, 0, 255), cv2.FILLED)
        daftarTitik.append([x, y])

# position point
# gradient
def gradient(pt1, pt2):
    return (pt2[1]-pt1[1])/(pt2[0]-pt1[0])

# get angle with list point
def getSudut(daftarTitik):
    pt1, pt2, pt3 = daftarTitik[-3:]
    m1 = gradient(pt1, pt2)
    m2 = gradient(pt1, pt3)
    sudutR = abs(math.atan((m2 - m1)/(1+(m2*m1))))
    sudutD = round(math.degrees(sudutR))
    cv2.putText(gambar, str(sudutD), (pt1[0]-40, pt1[1]-20), cv2.FONT_HERSHEY_COMPLEX, 0.7, (0,255,0))

while True:
    if len(daftarTitik) % 3 == 0 and len(daftarTitik) != 0:
        getSudut(daftarTitik)

    cv2.imshow('Gambar', gambar)
    cv2.setMouseCallback('Gambar', cursor)
    if cv2.waitKey(1) & 0xFF == ord('r'): #refresh
        daftarTitik = []
        gambar = cv2.imread(path)
    elif cv2.waitKey(1) & 0xFF == ord('q'): #quit
        break

cv2.destroyAllWindows()
