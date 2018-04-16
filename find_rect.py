#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import cv2
import numpy as np
import math

# создаем объект cap для захвата кадров с камеры
cap = cv2.VideoCapture(0) # /dev/video0

#красная метка
#hsvMin = np.array((150, 142, 115), np.uint8)
#hsvMax = np.array((207, 241, 189), np.uint8)

#зеленая метка
hsvMin = np.array((71, 120, 98), np.uint8)
hsvMax = np.array((93, 216, 183), np.uint8)


while True:
    ret, frame = cap.read() #захватываем кадр
    if ret:
        # преобразуем RGB картинку в HSV модель
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        blur = cv2.GaussianBlur(hsv, (5, 5), 2)   # размываем изображение blur

        # применяем цветовой фильтр, получили ч/б изображение
        thresh = cv2.inRange(blur, hsvMin, hsvMax)

        #находим контуры
        _, contours, hierarchy = cv2.findContours(thresh.copy(), cv2.RETR_TREE,
                                                  cv2.CHAIN_APPROX_SIMPLE)

        # перебираем все найденные контуры в цикле
        for contour in contours:
            rect = cv2.minAreaRect(contour) # пытаемся вписать прямоугольник
            area = int(rect[1][0]*rect[1][1]) #площадь прямоугольника
            if area > 500:
                center = (int(rect[0][0]), int(rect[0][1]))
                box = cv2.boxPoints(rect) # поиск четырех вершин прямоугольника
                box = np.int0(box) # округление координат

                #вычисляем точки граней прямоугольника
                edge1 = np.int0((box[1][0] - box[0][0], box[1][1] - box[0][1]))
                edge2 = np.int0((box[2][0] - box[1][0], box[2][1] - box[1][1]))

                #определяем бОльшую грань
                usedEdge = edge1
                if cv2.norm(edge2) > cv2.norm(edge1):
                    usedEdge = edge2

                horizont = (1, 0) # горизонт
                angle = 180.0/math.pi * math.acos((horizont[0]*usedEdge[0] +
                        horizont[1]*usedEdge[1]) / (cv2.norm(horizont)*cv2.norm(usedEdge)))

                #отрисовываем данные на кадре                
                cv2.drawContours(frame, [box], 0, (255, 0, 0), 2) # рисуем прямоугольник
                cv2.circle(frame, center, 5, (0, 255, 0), 2) #рисуем центр прямоугольника
                cv2.putText(frame, '%d' % int(angle), (center[0]+20, center[1]-20),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
            
        cv2.imshow('frame', frame) #отображаем кадр
        #cv2.imshow('thresh', thresh) #отображаем кадр
        
        key = cv2.waitKey(1) & 0xFF  #ждем нажатия клавиши
        if key == ord('q'): #если нажата Q тогда выходим
            break
    else:
        break
    
cv2.destroyAllWindows() #закрываем все окна
cap.release() #освобождаем cap

