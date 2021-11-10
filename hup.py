import cv2
import numpy as np
import time
import math

def CalibrateRoad(frame):
    m_cut = frame.copy()
    m_lab = cv2.cvtColor(m_cut, cv2.COLOR_BGR2LAB)

    offset = 0
    L = np.array(cv2.split(m_lab)[0])
    print(L.mean())
    if int(L.mean()) < 120:
        offset = 13
    lower_color = (0, 150 - offset, 139 - offset)# HSV: (0, 0, 165)# Lab : (168, 113, 0)
    upper_color = (255, 163 - offset, 150)# HSV: (255, 78, 255)# Lab : (255, 142, 255)


    m_range = cv2.inRange(m_lab, lower_color, upper_color)

    contours, _ = cv2.findContours(m_range, cv2.RETR_EXTERNAL, \
                                                cv2.CHAIN_APPROX_SIMPLE)

    for cnt in contours:
        area = cv2.contourArea(cnt)
        cv2.drawContours(m_range, [cnt], 0, (255, 0, 0), 3)
        if area > 30000:
            x, y, w, h = cv2.boundingRect(cnt)
            cv2.rectangle(m_range, (x, y), (x + w, y + h), (255, 0, 0), 3)
            cv2.imshow("wr", m_range)
            return m_cut[y:y+h]
    
    return m_cut