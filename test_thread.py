#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import threading
import time

class TestTread(threading.Thread):
    def __init__(self, name, pause = 1):
        threading.Thread.__init__(self) #вызываем функцию __init__ базового класса
        self.daemon = True
        self.count = 0
        self.running = False
        self.name = name
        self.pause = pause

    def run(self):
        self.running = True
        print('Thread %s started\n' % self.name)
        while self.running: #главный цикл потока
            print('Thread %s. Count = %d\n' % (self.name, self.count))
            self.count += 1
            time.sleep(self.pause)
        print('Thread %s stopped\n' % self.name)

    def stop(self):
        self.running = False
        self.join() #дождаться завершения потока

t1 = TestTread('t1')
t1.start()

t2 = TestTread('t2', 0.5)
t2.start()

count = 0

try:
    while count < 10:
        print('Main count: %d\n' % count)
        count += 1
        time.sleep(3)
except KeyboardInterrupt:
    print('Ctrl+C pressed\n')
    
t1.stop()
t2.stop()
