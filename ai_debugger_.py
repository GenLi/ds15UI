#!/usr/bin/env python

from PyQt4.QtGui import *
from PyQt4.QtCore import *
import sys

RUN_MODE = 0
DEBUG_MODE = 1
MAX_REPLAY_SPEED = 100
MIN_REPLAY_SPEED = 1

class ai_debugger(QMainWindow):
    def __init__(self, parent = None):
        super(ai_debugger, self).__init__(parent)

        self.started = False
        self.loaded_ai = None
        self.loaded_map = None
        self.replay_speed = MIN_REPLAY_SPEED
        self.pausepoints = []
        #temporary label
        self.replay_label = QLabel()
        self.replay_label.setMinimumSize(250, 250)
        self.setCentralWidget(self.replay_label)

        #add a dock widget to show infomations of the running AI and loaded files

        infoDockWidget = QDockWidget("Infos", self)
        infoDockWidget.setObjectName("InfoDockWidget")
        infoDockWidget.setAllowedAreas(Qt.LeftDockWidgetArea|
                                       Qt.RightDockWidgetArea)
        self.listWidget = QListWidget()
        infoDockWidget.setWidget(self.listWidget)
        self.addDockWidget(Qt.RightDockWidgetArea, infoDockWidget)

        #add status bar

        self.status = self.statusBar()
        self.status.setSizeGripEnabled(False)
        self.status.showMessage("Ready", 5000)

        #creat game actions

        gameStartAction = self.createAction("&Start", self.startGame,
                                            "Ctrl+S","gameStart",
                                            "start game",True)
        gamePauseAction = self.createAction("&Pause", self.pauseGame,
                                            "Ctrl+P","gamePause",
                                            "pause game",True)
        gameEndAction = self.createAction("&End", self.endGame,
                                         "Ctrl+E","gameEnd",
                                         "end game")
        gameLoadAction = self.createAction("&Load", self.loadDlg,
                                          "Ctrl+L", "gameLoad",
                                          "load AI and map")
        #creat game menu and add actions
        self.gameMenu = self.menuBar().addMenu("&Game")
        self.addActions(self.gameMenu, (gameStartAction, gamePauseAction,
                                  gameEndAction, None, gameLoadAction))

        #creat actions and add them to config menu
        self.configMenu = self.menuBar().addMenu("&Config")
        resetAction = self.createAction("&Reset", self.reset)
        self.configMenu.addAction(resetAction)

        modeGroup = QActionGroup(self)
        run_modeAction = self.createAction("Run_mode", self.setRunMode,
                                          "Ctrl+R",
                                         checkable = True, signal = "toggled(bool)")
        debug_modeAction = self.createAction("Debug_mode", self.setDebugMode,
                                            "Ctrl+D", checkable =True,
                                            signal = "toggled(bool)")
        modeGroup.addAction(run_modeAction)
        modeGroup.addAction(debug_modeAction)
        run_modeAction.setChecked(True)

        modeMenu = self.configMenu.addMenu("&Mode")
        self.addActions(modeMenu, (run_modeAction, debug_modeAction))

        #action group's resetable values

        self.resetableActions = ((run_modeAction, True),
                                 (debug_modeAction, False))

        #creat toolbars and add actions

        gameToolbar =  self.addToolBar("Game")
        self.addActions(gameToolbar, (gameStartAction, gamePauseAction,
                                  gameEndAction, gameLoadAction))
        configToolbar = self.addToolBar("Config")
        self.addActions(configToolbar, (run_modeAction, debug_modeAction))





    #    self.speed_slider = QSlider()
   #     self.speed_slider.setRange(MIN_REPLAY_SPEED, MAX_REPLAY_SPEED)

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

    #game operation slot
    def startGame(self):
        pass

    def pauseGame(self):
        pass

    def endGame(self):
        pass

    def loadDlg(self):
        pass

    def setRunMode(self):
        pass

    def setDebugMode(self):
        pass

    def reset(self):
        pass

if __name__ == "__main__":
    app = QApplication(sys.argv)
    form = ai_debugger()
    rect = QApplication.desktop().availableGeometry()
    form.resize(rect.size())
    form.show()
    app.exec_()
