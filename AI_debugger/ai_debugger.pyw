#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from PyQt4.QtGui import *
from PyQt4.QtCore import *
import sys
import qrc_resource
from info_widget import *
#from Ai_Thread import *
from AI_2DReplayWidget import *
import sio

DEBUG_MODE = 1
DEFAULT_SCILENT_AI = ""#默认的ai路径

WaitForNext = QWaitCondition()
WaitForPause = QWaitCondition()

class AiThread(QThread):
    def __init__(self, lock, parent = None):
        super(AiThread, self).__init__(parent)

        self.lock = lock
        self.mutex = QMutex()
        self.isPaused = False
        self.Con = 1

    def initialize(self, gameAIPath, gameMapPath):
        self.conn = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        try:
            self.conn.connect((sio.HOST,sio.UI_PORT))
        except:
            QMessageBox.critical(self, "Connection Error",
                                 "Failed to connect to UI_PORT,program is shutting down",
                                 QMessageBox.Ok, QMessageBox.NoButton)
            time.sleep(2)
            exit(1)
        sio._sends(self.conn,(sio.AI_VS_AI, gameMapPath,gameAIPath))
        mapInfo,aiInfo = sio._recvs(self.conn)
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
        #为了实现逐步暂停播放模式中用户自己下达下一回合命令和连续播放模式中
        #暂停接受数据设置的QWaitCondition全局变量
        global WaitForNext,WaitForPause
        if self.Con and self.isPaused():
            WaitForPause.wait()
        rCommand, reInfo = sio._recvs(self.conn)
        #第一个回合单独搞出来
        self.emit(SIGNAL("reRecv"), rCommand, reInfo)
        while reInfo.over == -1:
            if not self.Con:
                WaitForNext.wait()
            if self.Con and self.isPaused():
                #等待WaitForPause被主界面wakeall
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

            rCommand,reInfo = sio._recvs(self.conn)
            self.emit(SIGNAL("reRecv"),rCommand, reInfo)

        winner = sio._recvs(self.conn)
         #做一些界面的赢家展示替代print
        print 'Player ',winner,' win!'
        self.conn.close()






#调试器主界面
class ai_debugger(QMainWindow):
    def __init__(self, parent = None):
        super(ai_debugger, self).__init__(parent)

#        self.gameMode = sio.AI_VS_AI
        self.started = False
        self.loaded_ai = []
        self.loaded_map = None
        self.lock = QReadWriteLock()#留着备用...暂时我还没有设置共同数据
        #先init这个与平台交互的线程
        self.pltThread = Ai_Thread(self.lock)
#        self.replay_speed = MIN_REPLAY_SPEED
        self.ispaused = False

        #composite replay widget
        self.replayScene = QGraphicsScene()
        self.replayWindow = AiReplayWidget(self.replayScene)

        #add a dock widget to show infomations of the running AI and loaded files

        self.infoDockWidget = QDockWidget("Infos", self)
        self.infoDockWidget.setObjectName("InfoDockWidget")
        self.infoDockWidget.setAllowedAreas(Qt.LeftDockWidgetArea|
                                            Qt.RightDockWidgetArea)
        self.infoWidget = InfoWidget(self)
        self.infoDockWidget.setWidget(self.infoWidget)
        self.addDockWidget(Qt.RightDockWidgetArea, self.infoDockWidget)
        self.info_visible = self.infoDockWidget.isVisible()
        
        #add status bar

        self.status = self.statusBar()
        self.status.setSizeGripEnabled(False)
        self.status.showMessage("Ready", 5000)

        #creat game actions

        self.gameStartAction = self.createAction("&Start", self.startGame,
                                            "Ctrl+S","gameStart",
                                            "start game")
        #游戏暂停功能在进度条里实现,不在这里实现了(不过如果需要加入,也可以..)
      #  self.gamePauseAction = self.createAction("&Pause", self.pauseGame,
       #                                     "Ctrl+P","gamePause",
        #                                    "pause game",True)
        self.gameEndAction = self.createAction("&End", self.endGame,
                                         "Ctrl+E","gameEnd",
                                         "end game")
        self.gameLoadAction1 = self.createAction("Load &AI", self.loadAIdlg,
                                          "Ctrl+A", "loadAI",
                                          "load AI")
        self.gameLoadAction2 = self.createAction("Load &MAP", self.loadMapdlg,
                                           "Ctrl+M", "loadMap",
                                           "load MAP")

        #creat game menu and add actions
        self.gameMenu = self.menuBar().addMenu("&Game")
        self.addActions(self.gameMenu, (self.gameStartAction,
                                  self.gameEndAction, None, self.gameLoadAction1,
                                        self.gameLoadAction2))

        #creat actions and add them to config menu
        self.configMenu = self.menuBar().addMenu("&Config")
        resetAction = self.createAction("&Reset", self.reset,
                                        icon = "reset",
                                        tip = "reset all settings")
        self.configMenu.addAction(resetAction)

        modeGroup1 = QActionGroup(self)
        #还没有实现如何设置debug模式
        run_modeAction = self.createAction("Run_mode", self.setRunMode,
                                          "Ctrl+R", "modeRun", "run mode",
                                           True, "toggled(bool)")
        debug_modeAction = self.createAction("Debug_mode", self.setDebugMode,
                                            "Ctrl+D", "modeDebug", "debug mode",
                                             True, "toggled(bool)")
        modeGroup1.addAction(run_modeAction)
        modeGroup1.addAction(debug_modeAction)
        run_modeAction.setChecked(True)

        modeGroup2 = QActionGroup(self)
        continue_modeAction = self.createAction("Continuous_mode", self.setConMode,
                                               icon = "modeCon",
                                               tip = "set continuous mode",
                                               checkable = True,
                                               signal = "toggled(bool)")
        discon_modeAction = self.createAction("DisContinuous_mode", self.setDisconMode,
                                              icon = "modeDiscon",
                                              tip = "set discontinuous mode",
                                              checkable = True,
                                              signal = "toggled(bool)")
        modeGroup2.addAction(continue_modeAction)
        modeGroup2.addAction(discon_modeAction)
        continue_modeAction.setChecked(True)

        modeMenu = self.configMenu.addMenu("&Mode")
        self.addActions(modeMenu, (run_modeAction, debug_modeAction, None,
                                   continue_modeAction, discon_modeAction))

        #action group's resetable values

        self.resetableActions = ((run_modeAction, True),
                                 (debug_modeAction, False),
                                 (continue_modeAction, True),
                                 (discon_modeAction, False))
        #creat action and add it to window menu

        self.dockAction = self.createAction("(dis/en)able infos", self.setInfoWidget,
                                       tip = "enable/disable info dock-widget",
                                       checkable = True,
                                       signal = "toggled(bool)")
        self.windowMenu = self.menuBar().addMenu("&Window")
        self.windowMenu.addAction(self.dockAction)
        self.dockAction.setChecked(True)
        #creat toolbars and add actions

        gameToolbar =  self.addToolBar("Game")
        self.addActions(gameToolbar, (self.gameStartAction,
                                  self.gameEndAction, self.gameLoadAction1, self.gameLoadAction2))
        configToolbar = self.addToolBar("Config")
        self.addActions(configToolbar, (run_modeAction, debug_modeAction,
                                        None, continue_modeAction,
                                        discon_modeAction, None,
                                        resetAction))


        self.connect(self.infoWidget, SIGNAL("hided()"), self.synhide)
        #to show messages
        self.connect(self.replayWindow.replayWidget, SIGNAL("unitSelected"),
                     self.infoWidget, SLOT("newUnitInfo"))
        self.connect(self.replayWindow.replayWidget, SIGNAL("mapGridSelected"),
                     self.infoWidget, SLOT("newMapInfo"))
        self.connect(self.pltThread, SIGNAL("finished()"), self.pltThread,
                     SLOT("deleteLater()"))
        #进度条到主界面的通信
        self.connect(self.replayWindow, SIGNAL("nextRound()"), self.nextRound)
        self.connect(self.replayWindow, SIGNAL("pauseRound()"), self.pauseRound)
        self.connect(self.replayWindow, SIGNAL("nonpauseRound()"), self.nonPauseRound)
        #次线程到界面的通信
        self.connect(self.pltThread, SIGNAL("firstRecv"), self.on_firstRecv)
        self.connect(self.pltThread, SIGNAL("rbRecv"), self.on_rbRecv)
        self.connect(self.pltThread, SIGNAL("reRecv"), self.on_reRecv)
        self.updateUi()
        self.setWindowTitle("DS15_AIDebugger")



    #wrapper function for reducing codes
    def createAction(self, text, slot=None, shortcut=None, icon=None,
                     tip=None, checkable=False, signal="triggered()"):
        action = QAction(text, self)
        if icon is not None:
            action.setIcon(QIcon(":/%s.png" % icon))
        if shortcut is not None:
            action.setShortcut(shortcut)
        if tip is not None:
            action.setToolTip(tip)
            action.setStatusTip(tip)
        if slot is not None:
            self.connect(action, SIGNAL(signal), slot)
        if checkable:
            action.setCheckable(True)
        return action

    def addActions(self, target, actions):
        for action in actions:
            if action is None:
                target.addSeparator()
            else:
                target.addAction(action)

    #enable/disable actions according to the game status
    def updateUi(self):
        if len(self.loaded_ai) != 0 and self.loaded_map:
            if not self.started:
                self.gameStartAction.setEnabled(True)
              #  self.gamePauseAction.setEnabled(False)
                self.gameEndAction.setEnabled(False)
                self.gameLoadAction1.setEnabled(True)
                self.gameLoadAction2.setEnabled(True)
            else:
                self.gameStartAction.setEnabled(False)
               # self.gamePauseAction.setEnabled(True)
                self.gameEndAction.setEnabled(True)
                self.gameLoadAction1.setEnabled(False)
                self.gameLoadAction2.setEnabled(False)
        else:
            self.gameStartAction.setEnabled(False)
           # self.gamePauseAction.setEnabled(False)
            self.gameEndAction.setEnabled(False)
            self.gameLoadAction1.setEnabled(True)
            self.gameLoadAction2.setEnabled(True)
    #game operation slot
    def startGame(self):
        if len(self.loaded_ai) == 1:
            self.loaded_ai.append(DEFAULT_SCILENT_AI)
        #开始这个线程开始交互
        self.pltThread.initialize(self.loaded_ai,self.loaded_map)
        self.pltThread.start()
        self.started = True

        self.updateUi()

 #   def pauseGame(self):
  #      self.replayWindow.pauseGame()

    def endGame(self):

        #强制在游戏没有进行到胜利条件的时候结束游戏
        self.started = False
        self.loaded_ai = []
        self.updateUi()
#设置两个loadai而且只要把文件路径得到就好了.传给平台时如果得到错误再打印错误信息
    def loadAIdlg(self):
        dir = QDir.toNativeSeparators(r"./FileAI")
        fname = unicode(QFileDialog.getOpenFileName(self,
                                                    "load AI File", dir,
                                                    "AI files (%s)" % "*.exe"))
        if len(loaded_ai) < 2 and fname:
            self.loaded_ai.append(fname)
            self.updateUi()

    def loadMapdlg(self):
        dir = QDir.toNativeSeparators(r"./FileMap")
        fname = unicode(QFileDialog.getOpenFileName(self,
                                                    "load Map File", dir,
                                                    "Map files (%s)" % "*.map"))
        if fname and fname != self.loaded_map:
            self.loaded_map = fname
            self.updateUi()

    def nextRound(self):
        global WaitForNext
        #唤醒所有在waitfornext的线程
        WaitForNext.wakeAll()

    def nonPauseRound(self):
        global WaitForPause
        #唤醒所有在waitforpause的线程
        WaitForPause.wakeAll()

    def on_firstRecv(self, mapInfo, frInfo, aiInfo):
        self.replayWindow.updateIni(basic.Begin_Info(mapinfo, base), frInfo)
        #这个base...要怎么给...平台组貌似没有给aivsai的base接口和hero接口???
        self.infoWidget.beginRoundInfo(frInfo)
        #这个aiInfo是什么...

    def on_rbRecv(self, rbInfo):
        self.replayWindow.updateBeg(rbInfo)
        self.infoWidget.beginRoundInfo(rbInfo)

    def on_reRecv(self, rCommand, reInfo):
        self.replayWindow.updateEnd(rCommand, reInfo)
        self.infoWidget.endRoundInfo(rCommand, reInfo)

    def setRunMode(self):
        pass

    def setDebugMode(self):
        pass

    def setConMode(self):
        self.replayWindow.setPlayMode(1)
        self.pltThread.Con = 1
         #没有考虑清楚此处是否需要用mutexlock


    def setDisconMode(self):
        self.replayWindow.setPlayMode(0)
        self.pltThread.Con = 0


    def reset(self):
        pass
#为了同步窗口菜单和信息栏的关闭和打开
    def synhide(self):
        self.dockAction.setChecked(False)
        self.info_visible = False
    def setInfoWidget(self):
        if (self.info_visible):
            self.infoDockWidget.close()
            self.info_visible = False
        else:
            self.infoDockWidget.show()
            self.info_visible = True

if __name__ == "__main__":
    app = QApplication(sys.argv)
    form = ai_debugger()
    rect = QApplication.desktop().availableGeometry()
    form.resize(rect.size())
    form.setWindowIcon(QIcon(":/icon.png"))
    form.show()
    app.exec_()
