#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
import cv2
import numpy as np
from xmlrpc.server import SimpleXMLRPCServer

#сетевые параметры
IP_SERVER = '192.168.8.172' #IP адрес сервера
DEBUG_PORT = 8000 #порт отправки отладочных кадров XML-RPC

def debugFrame(frame): #frame = (имя, jpeg-данные)
    frameName = frame[0] #имя окна
    imgArray = np.frombuffer(frame[1].data, dtype=np.uint8) #преобразуем в массив np
    img = cv2.imdecode(imgArray, cv2.IMREAD_COLOR) #декодируем
    cv2.imshow(frameName, img) #отображаем кадр
    cv2.waitKey(1)
    return 0

# XML-RPC сервер управления в отдельном потоке
serverDebug = SimpleXMLRPCServer((IP_SERVER, DEBUG_PORT)) #запуск XMLRPC сервера
serverDebug.logRequests = False #оключаем логирование
print('Debug XML-RPC server listening on %s:%d' % (IP_SERVER, DEBUG_PORT))

serverDebug.register_function(debugFrame)

# Запускаем сервер
try:
    serverDebug.serve_forever()
except KeyboardInterrupt:
    print('Ctrl+C pressed')
    serverDebug.server_close()
cv2.destroyAllWindows()
