# -*- coding: UTF-8 -*-
#Thread class to realize the communication between platform and Ui
#Fox Ning
#version:

from PyQt4.QtCore import *
import socket,cPickle,sio,time,threading,basic
WaitForNext = QWaitCondition()
WaitForPause = QWaitCondition()

class AiThread(QThread):
    def __init__(self, lock, parent = None):
        super(AiThread, self).__init__(parent)

        self.lock = lock                                    #暂时...我还没有搞出共用的数据...数据处理基本都是在主线程进行的.这里只有接受数据和发出信号
        self.mutex = QMutex()
        self.isPaused = False
        self.Con = 1

    def initialize(self, gameAIPath, gameMapPath):
        self.conn = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        try:
            self.conn.connect((sio.HOST,sio.UI_PORT))
        except:
            print 'failed to connect, the program will exit...'
            time.sleep(2)
            exit(1)
        sio._sends(self.conn,(sio.AI_VS_AI, gameMapPath,gameAIPath))
        mapInfo,aiInfo = sio._recvs(conn)
        frInfo = sio._recvs(self.conn)
         #在ai_vs_ai模式里,平台并没有给用户设置自己士兵类型和英雄类型的函数,用默认的吗?
        self.emit(SIGNAL("firstRecv"),mapInfo, frInfo, aiInfo)

    def pause(self):
        try:
            self.mutex.lock()
            self.isPaused = True
        finally:
            self.mutex.unlock()

    def isPaused(self):
        try:
            self.mutex.lock()
            return self.isPaused
        finally:
            self.mutex.unlock()

    def run(self):
        global WaitForNext,WaitForPause
        if self.Con and self.isPaused():
            WaitForPause.wait()
        rCommand, reInfo = sio._recvs(self.conn)                      #第一个回合单独搞出来
        self.emit(SIGNAL("reRecv"), rCommand, reInfo)
        while reInfo.over == -1:
            if not self.Con:
                WaitForNext.wait()
            if self.Con and self.isPaused():
                WaitForPause.wait()
                try:
                    self.mutex.lock()
                    self.isPaused = False
                finally:
                    self.mutex.unlock()
            rbInfo = sio._recvs(self.conn)
            self.emit(SIGNAL("rbRecv"),rbInfo)
            if not self.Con:
                WaitForNext.wait()
            if self.Con and self.isPaused():
                WaitForPause.wait()
                try:
                    self.mutex.lock()
                    self.isPaused = False
                finally:
                    self.mutex.unlock()

            rCommand,reInfo = sio._recvs(conn)
            self.emit(SIGNAL("reRecv"),rCommand, reInfo)

        winner = sio._recvs(self.conn)
        print 'Player ',winner,' win!'               #做一些界面的赢家展示替代...print
        self.conn.close()




