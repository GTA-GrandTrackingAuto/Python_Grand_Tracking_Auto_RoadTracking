import cv2
import numpy as np

# 변속 : 0~5
# 조향 : 0~12

# return : [변속, 조향]

def GetLine(frame):
    HEIGHT, WIDTH = frame.shape[:2]
    line_check_height = int(HEIGHT / 2)
    center_point = (int(WIDTH / 2), 30)

    center_speed = (int(WIDTH / 2), 300)

    check_contour = [0,0]

    frame_center = (int(WIDTH / 2), line_check_height)
    m_cut = frame[line_check_height - 50:line_check_height + 50]
    # leftROIV = np.array(cv2.split(m_cut[:len(m_cut), :len(m_cut) // 2])[2])
    # rightROIV = np.array(cv2.split(m_cut[:len(m_cut), len(m_cut) // 2:])[2])
    # print("left: ", leftROIV.mean(), "right: ", rightROIV.mean())
    m_hsv = cv2.cvtColor(m_cut, cv2.COLOR_BGR2LAB)
    # 평균
    L, A, B = cv2.split(m_hsv)
    
    A = np.where(L < 190, A + 10, A)
    B = np.where(L < 190, B + 10, B)
    # a = np.where(a < 50, 50, a)
    m_hsv = cv2.merge((L, A, B))
    m_cut = cv2.cvtColor(m_hsv, cv2.COLOR_LAB2BGR)

    def mouse_event(e, x, y, flags, param):
        if e == cv2.EVENT_FLAG_LBUTTON:
            print(m_result_gray[y][x])

    cv2.setMouseCallback("img", mouse_event, m_hsv)
    # HSV: (102, 28, 145)# Lab : (148, 120, 114)
    # HSV: (170, 41, 255)# Lab : (255, 142, 133)

    lower_color = (0, 117, 117)# HSV: (0, 40, 165)# Lab : (0, 120, 117)
    upper_color = (255, 143, 139)# HSV: (20, 60, 255)# Lab : (255, 140, 136)

    m_range = cv2.inRange(m_hsv, lower_color, upper_color)
    m_result = cv2.bitwise_and(m_cut, m_cut, mask=m_range)
    check_contour = [0, 0]
    # 외곽선 검출 -------------------------
    m_result_gray = cv2.cvtColor(m_result, cv2.COLOR_BGR2GRAY)
    m_result_canny = cv2.Canny(m_result_gray, 200, 255)
    m_leftROI = m_result_canny[:len(m_result_canny), :WIDTH // 2]
    m_rightROI = m_result_canny[:len(m_result_canny), WIDTH // 2:]
    leftLines = cv2.HoughLinesP(m_leftROI, 0.8, np.pi / 180, 90, minLineLength=50, maxLineGap=50)
    rightLines = cv2.HoughLinesP(m_rightROI, 0.8, np.pi / 180, 90, minLineLength=50, maxLineGap=50)
    
    if type(leftLines) == np.ndarray: 
        leftLines = sorted(leftLines, key=lambda x: x[0][2] + abs(x[0][1] - x[0][3]))
        rightLines = sorted(rightLines, key=lambda x: x[0][0] + abs(x[0][1] - x[0][3]), reverse=True)

        leftIMG = leftLines.pop()
        rightIMG = rightLines.pop()
        # 왼쪽 점 (leftIMG[0][2], 50)
        # 오른쪽 점 (WIDTH // 2 + rightIMG[0][0], 50)
        check_contour[0] = leftIMG[0][2]
        check_contour[1] = WIDTH // 2 + rightIMG[0][0]

        cv2.circle(m_cut, (leftIMG[0][2], 50), 3, (255, 0, 0), 10)
        cv2.circle(m_cut, (WIDTH // 2 + rightIMG[0][0], 50), 3, (255, 0, 0), 10)
        cv2.line(m_cut, (leftIMG[0][0], leftIMG[0][1]), (leftIMG[0][2], leftIMG[0][3]), (0, 0, 255), 5)
        cv2.line(m_cut, (WIDTH // 2 + rightIMG[0][0], rightIMG[0][1]), (WIDTH // 2 + rightIMG[0][2], rightIMG[0][3]), (0, 0, 255), 5)
    # 외곽선 검출 --------------------------

    got_center = int((check_contour[1] - check_contour[0]) / 2 + check_contour[0])
    cv2.circle(m_result, center_point, 3, (255, 0, 0), 10)
    cv2.circle(m_result, (got_center, 0), 3, (0, 0, 255), 5)

    # # full screen mode
    cv2.circle(frame, frame_center, 3, (255, 0, 0), 10)

    # 중심제어
    text = 'on line'
    speed = 'speed up'
    tf = False
    movementPersent = 0
    if check_contour[1] > 0 and check_contour[0] > 0:
        movementPersent = round(abs(center_point[0] - got_center) / abs(check_contour[1] - check_contour[0]) * 12)
        if movementPersent >= 6:
            text = "left"
        elif movementPersent < 6:
            text = "right"

    cv2.putText(frame, text, center_point, cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 3, cv2.LINE_AA)
    if tf != True:
        speed = 'good speed'
    cv2.putText(frame, speed, center_speed, cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 3, cv2.LINE_AA)


    cv2.imshow('img', m_result)
    cv2.imshow('img2', frame)
    cv2.imshow('img3', m_cut)

    return (1, movementPersent)