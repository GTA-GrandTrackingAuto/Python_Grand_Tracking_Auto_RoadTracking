import cv2
import numpy as np
import LineManage
import time
from os import listdir
from os.path import isfile, join

cv2.namedWindow('img')
# mypath = 'images/2curve'
# onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
# images = np.empty(len(onlyfiles), dtype=object)
# for n in range(0, len(onlyfiles)):
#     images[n] = cv2.imread(join(mypath, onlyfiles[n]))

# HEIGHT, WIDTH = images[0].shape[:2]
# SPEED = 100

# print(HEIGHT, WIDTH)

# for i in images:
#     SPEED = LineManage.GetLine(i, HEIGHT, WIDTH, SPEED)

#     if cv2.waitKey(0) & 0xFF == ord('q'):
#        break

cap = cv2.VideoCapture('SaveVideo.mp4')
SPEED = 100
while cap.isOpened():
    _, frame = cap.read()
    HEIGHT, WIDTH = frame.shape[:2]
    SPEED = LineManage.GetLine(frame, HEIGHT, WIDTH, SPEED)

    if cv2.waitKey(0) & 0xFF == 27:
        break
    else:
        pass

cv2.destroyAllWindows()

