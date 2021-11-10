import cv2
import numpy as np
import hup
import LineManage
import time
from os import listdir
from os.path import isfile, join

cv2.namedWindow('img')
mypath = 'images/curve'
onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
images = np.empty(len(onlyfiles), dtype=object)
for n in range(0, len(onlyfiles)):
    images[n] = cv2.imread(join(mypath, onlyfiles[n]))

for i in images: 
    _, persent = LineManage.GetLine(i)
    if cv2.waitKey(0) & 0xFF == ord('q'):
        break
    else:
        pass

# cap = cv2.VideoCapture('SaveVideo.mp4')
# while cap.isOpened():
#     _, frame = cap.read()
#     HEIGHT, WIDTH = frame.shape[:2]
#     _, SPEED = LineManage.GetLine(frame)
#     if cv2.waitKey(0) & 0xFF == 27:
#         break
#     else:
#         pass   

cv2.destroyAllWindows()

