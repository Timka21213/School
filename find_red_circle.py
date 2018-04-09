#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import cv2
import numpy as np

# создаем объект cap для захвата кадров с камеры
cap = cv2.VideoCapture(0) # /dev/video0
hsvMin = np.array((53, 0, 0), np.uint8)
hsvMax = np.array((83, 255, 255), np.uint8)


while True:
    ret, frame = cap.read() #захватываем кадр
    if ret:
        # преобразуем RGB картинку в HSV модель
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # применяем цветовой фильтр
        thresh = cv2.inRange(hsv, hsvMin, hsvMax)

        
        cv2.imshow('frame', thresh) #отображаем кадр

        key = cv2.waitKey(1) & 0xFF  #ждем нажатия клавиши
        if key == ord('q'): #если нажата Q тогда выходим
            break
    else:
        break

cap.release() #освобождаем cap
cv2.destroyAllWindows() #закрываем все окна
