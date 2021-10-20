import cv2
import numpy as np

def GetLine(frame, HEIGHT, WIDTH):
    line_check_height = int(HEIGHT / 7 * 5)
    center_point = (int(WIDTH / 2), 10)
    check_contour = [0,0]

    frame_center = (int(WIDTH / 2), line_check_height)

    m_cut = frame[line_check_height - 50:line_check_height + 50,0:WIDTH ]
    m_hsv = cv2.cvtColor(m_cut, cv2.COLOR_BGR2LAB)
    
    def mouse_event(e, x, y, flags, param):
        if e == cv2.EVENT_FLAG_LBUTTON:
            print(m_hsv[y][x])

    cv2.setMouseCallback("img", mouse_event, m_hsv)

    lower_color = (148, 120, 114)#(0, 138, 134)#(226, 175, 169)
    upper_color = (255, 142, 133)#(255, 165, 152)#(255, 255, 255)

    m_range = cv2.inRange(m_hsv, lower_color, upper_color)
    m_result = cv2.bitwise_and(m_cut, m_cut, mask=m_range)
    contours, _ = cv2.findContours(m_range, cv2.RETR_EXTERNAL, \
                                                cv2.CHAIN_APPROX_NONE)
    check_contour = [0, 0]
    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        if y == 0:
            # print('cnt :', x, y)
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

    
    # print('check_contour :',check_contour)

    for i in range(2):
        cv2.circle(m_result, (check_contour[i], 50), 3, (255, 0, 255), 10)

    got_center = int((check_contour[1] - check_contour[0]) / 2 + check_contour[0])
    cv2.circle(m_result, center_point, 3, (255, 0, 0), 10)
    cv2.circle(m_result, (got_center, 0), 3, (0, 0, 255), 5)

    # full screen mode
    cv2.circle(frame, frame_center, 3, (255, 0, 0), 10)

    # 중심제어
    if center_point[0] > got_center:
        for i in range(15):
            if center_point[0] - got_center < 30 * i:
                if i < 2:
                    cv2.putText(frame, 'on line', center_point, cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 0), 2, cv2.LINE_AA)
                    print('good line')
                    break
                cv2.putText(frame, 'go left - ' + str(i) + '%', center_point, cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 0), 2, cv2.LINE_AA)
                print('go left -', str(i) + '%')
                break
    elif center_point[0] < got_center:
        for i in range(15):
            if got_center - center_point[0] < 30 * i:
                if i < 2:
                    cv2.putText(frame, 'on line', center_point, cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 0), 2, cv2.LINE_AA)
                    print('good line')
                    break
                cv2.putText(frame, 'go right - ' + str(i) + '%', center_point, cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 0), 2, cv2.LINE_AA)
                print('go right -',str(i) + '%')
                break

    cv2.imshow('img', m_result)
    cv2.imshow('img2', m_cut)
    cv2.imshow('full screen', m_hsv)