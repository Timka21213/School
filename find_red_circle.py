#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import cv2
import numpy as np

# создаем объект cap для захвата кадров с камеры
cap = cv2.VideoCapture(0) # /dev/video0
hsvMin = np.array((150, 142, 115), np.uint8)
hsvMax = np.array((207, 241, 189), np.uint8)


while True:
    ret, frame = cap.read() #захватываем кадр
    if ret:
        # преобразуем RGB картинку в HSV модель
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        blur = cv2.GaussianBlur(hsv, (5, 5), 2)   # размываем изображение blur

        # применяем цветовой фильтр
        thresh = cv2.inRange(blur, hsvMin, hsvMax)

        #находим контуры
        _, contours, hierarchy = cv2.findContours(thresh.copy(), cv2.RETR_TREE,
                                                  cv2.CHAIN_APPROX_SIMPLE)
        if contours:
            # берем максимальный контур по периметру
            mainContour = max(contours, key = cv2.contourArea)
            if len(mainContour) > 4: #если контур содержит больше чем 4-ре точки
                ellipse = cv2.fitEllipse(mainContour) #вписываем элипс в контур
                cv2.ellipse(frame, ellipse, (0, 255, 0), 2) #отрисовываем элипс
        '''
        # вычисляем моменты изображения
        moments = cv2.moments(thresh, 1)
        dM01 = moments['m01'] #сумма всех координат Y
        dM10 = moments['m10'] #сумма всех координат X
        dArea = moments['m00'] #количество точек

        # будем реагировать только на те моменты,
        # которые содержать больше 100 пикселей
        if dArea > 100:
            x = int(dM10 / dArea)
            y = int(dM01 / dArea)
            cv2.circle(frame, (x, y), 10, (0, 255, 0), -1)
            cv2.putText(frame, "%d-%d" % (x,y), (x+10,y-10), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    '''

        cv2.imshow('frame', frame) #отображаем кадр
        #cv2.imshow('thresh', thresh) #отображаем кадр
        
        key = cv2.waitKey(1) & 0xFF  #ждем нажатия клавиши
        if key == ord('q'): #если нажата Q тогда выходим
            break
    else:
        break

cap.release() #освобождаем cap
cv2.destroyAllWindows() #закрываем все окна
