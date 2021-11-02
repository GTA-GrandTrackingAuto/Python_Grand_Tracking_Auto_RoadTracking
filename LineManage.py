import cv2
import numpy as np
import time
import math

def GetLine(frame, HEIGHT, WIDTH, SPEED):

    line_check_height = int(HEIGHT / 9 * 4)
    center_point = (int(WIDTH / 2), 30)

    center_speed = (int(WIDTH / 2), 300)

    check_contour = [0,0]

    frame_center = (int(WIDTH / 2), line_check_height)
    print("Height", line_check_height)
    m_cut = frame[line_check_height - 50:line_check_height + 50,0:WIDTH ]
    m_hsv = cv2.cvtColor(m_cut, cv2.COLOR_BGR2HSV)
    # 평균
    b, a, l = cv2.split(m_hsv)
    b = np.where(b > 10, 10, b)
    a = np.where(a < 50, 50, a)
    m_hsv = cv2.merge((b, a, l))
    m_cut = cv2.cvtColor(m_hsv, cv2.COLOR_HSV2BGR)
    # m_cut = cv2.cvtColor(m_cut, cv2.COLOR_BGR2GRAY)
    
    def mouse_event(e, x, y, flags, param):
        if e == cv2.EVENT_FLAG_LBUTTON:
            print(m_hsv[y][x])

    cv2.setMouseCallback("img", mouse_event, m_hsv)
    # HSV: (102, 28, 145)# Lab : (148, 120, 114)
    # HSV: (170, 41, 255)# Lab : (255, 142, 133)

    lower_color = (0, 40, 165)# HSV: (0, 0, 165)# Lab : (168, 113, 0)
    upper_color = (20, 60, 255)# HSV: (255, 78, 255)# Lab : (255, 142, 255)

    m_range = cv2.inRange(m_hsv, lower_color, upper_color)
    m_result = cv2.bitwise_and(m_cut, m_cut, mask=m_range)

    m_result_gray = cv2.cvtColor(m_result, cv2.COLOR_BGR2GRAY)
    m_result_canny = cv2.Canny(m_result_gray, 50, 200)
    lines = cv2.HoughLinesP(m_result_canny, 0.8, np.pi / 180, 90, minLineLength=10, maxLineGap=100)

    for i in lines:
        line_width, line_height =  abs(i[0][2] - i[0][0]), abs(i[0][1] - i[0][3])
        if line_height > 10:
            line_top = int(math.sqrt((line_width ** 2) + (line_height ** 2)))
            angle = math.cos(line_width / line_top) * 180 / np.pi
            if line_height > 90:
                cv2.line(m_result, (i[0][0], i[0][1]), (i[0][2], i[0][3]), (0, 0, 255), 2)

    contours, _ = cv2.findContours(m_range, cv2.RETR_EXTERNAL, \
                                                cv2.CHAIN_APPROX_NONE)
    check_contour = [0, 0]
    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        
        if w > 10 and h > 10 and y == 0:
            cv2.rectangle(m_result, (x, y), (x + w, y + h), (255, 0, 0), 3)
            if (x > WIDTH / 2):
                if check_contour[1] == 0:
                    check_contour[1] = x
                elif check_contour[1] > x:
                    check_contour[1] = x
                    
            else:
                if check_contour[0] == 0:
                    check_contour[0] = x + w
                elif check_contour[0] < x:
                    check_contour[0] = x + w

    for i in range(2):
        cv2.circle(m_result, (check_contour[i], 50), 3, (255, 0, 255), 10)

    got_center = int((check_contour[1] - check_contour[0]) / 2 + check_contour[0])
    cv2.circle(m_result, center_point, 3, (255, 0, 0), 10)
    cv2.circle(m_result, (got_center, 0), 3, (0, 0, 255), 5)

    # full screen mode
    cv2.circle(frame, frame_center, 3, (255, 0, 0), 10)


    # 중심제어
    text = 'on line'
    speed = 'speed up'
    return_speed = SPEED
    tf = False
    if center_point[0] > got_center:
        for i in range(15):
            if center_point[0] - got_center < 30 * i:
                if i > 1:
                    text = 'go left - ' + str(i) + '%'
                    speed = 'speed down ' + str(i) + 'km/s'
                    if SPEED > 100 - i * 5:
                        return_speed -= i * 5
                        tf = True

                    # print('go left -', str(i) + '%')
                    break
    elif center_point[0] < got_center:
        for i in range(15):
            if got_center - center_point[0] < 30 * i:
                if i > 1:
                    text = 'go right - ' + str(i) + '%'
                    speed = 'speed down ' + str(i) + 'km/s'
                    if SPEED > 100 - i * 5:
                        return_speed -= i * 5
                        tf = True
                    # print('go right -',str(i) + '%')
                    break
    
    # cv2.putText(frame, text, center_point, cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 3, cv2.LINE_AA)
    if tf != True:
        speed = 'good speed'
    # cv2.putText(frame, speed, center_speed, cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 3, cv2.LINE_AA)
    cv2.imshow('img', m_result)
    cv2.imshow('img2', m_hsv)
    cv2.imshow('full screen', m_result_canny)

    return return_speed
