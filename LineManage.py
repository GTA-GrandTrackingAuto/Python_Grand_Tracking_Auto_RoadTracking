import cv2
import numpy as np

# 변속 : 0~5
# 조향 : 0~12

# return : [변속, 조향]

def GetLine(frame):
    HEIGHT, WIDTH = frame.shape[:2]
    line_check_height = int(HEIGHT / 9 * 4)
    center_point = (int(WIDTH / 2), 30)

    center_speed = (int(WIDTH / 2), 300)

    check_contour = [0,0]

    frame_center = (int(WIDTH / 2), line_check_height)
    m_cut = frame[line_check_height - 75:line_check_height + 75]
    m_hsv = cv2.cvtColor(m_cut, cv2.COLOR_BGR2LAB)
    m_leftROI = m_hsv[:len(m_hsv), :WIDTH // 2]
    m_rightROI = m_hsv[:len(m_hsv), WIDTH // 2:]
    
    # 평균
    L, A, B = cv2.split(m_hsv)
    lightMean = L.mean()

    plus = (np.int32(A) + np.int32(B)) // 2
    L = np.where(np.logical_and(np.logical_and(140 > plus, plus > 119), L >= 120), 240, L)

    m_hsv = cv2.merge((L, A, B))
    m_cut = cv2.cvtColor(m_hsv, cv2.COLOR_LAB2BGR)

    def mouse_event(e, x, y, flags, param):
        if e == cv2.EVENT_FLAG_LBUTTON:
            _, a, b = m_hsv[y][x]
            sum = (int(a) + int(b)) // 2 
            print(m_cut[y][x], sum, int(a) - int(b))


    cv2.setMouseCallback("img", mouse_event, m_hsv)

    lower_color = (219, 230, 219)# HSV: (0, 40, 165)# Lab : (0, 120, 117)
    upper_color = (255, 255, 255)# HSV: (20, 60, 255)# Lab : (255, 140, 136)
    m_range = cv2.inRange(m_cut, lower_color, upper_color)
    m_result = cv2.bitwise_and(m_cut, m_cut, mask=m_range)

    contours, _ = cv2.findContours(m_range, cv2.RETR_EXTERNAL, \
                                                cv2.CHAIN_APPROX_SIMPLE)

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
    steering_level = 6
    
    if center_point[0] > got_center:
        for i in range(1, 15):
            if center_point[0] - got_center < WIDTH / 24 * i:
                if i > 6:
                    break
                
                if i > 1:
                    text = 'go left - level ' + str(i)
                    steering_level = 6 - i

    elif center_point[0] < got_center:
        for i in range(1, 15):
            if got_center - center_point[0] < WIDTH / 24 * i:
                if i > 6:
                    break

                if i > 1:
                    text = 'go right - level ' + str(i)
                    steering_level = i + 6

    
    cv2.putText(frame, text, center_point, cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 3, cv2.LINE_AA)

    cv2.imshow('img', m_result)
    cv2.imshow('img2', m_cut)
    cv2.imshow('img3', frame)

    return (1, steering_level)
