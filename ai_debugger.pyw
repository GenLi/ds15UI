#!/usr/bin/env python

from PyQt4.QtGui import *
from PyQt4.QtCore import *
import sys
from info_widget import *
import qrc_resource

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
        self.infoWidget = InfoWidget()
        infoDockWidget.setWidget(self.infoWidget)
        self.addDockWidget(Qt.RightDockWidgetArea, infoDockWidget)

        #add status bar

        self.status = self.statusBar()
        self.status.setSizeGripEnabled(False)
        self.status.showMessage("Ready", 5000)

        #creat game actions

        gameStartAction = self.createAction("&Start", self.startGame,
                                            "Ctrl+S","gameStart",
                                            "start game")
        gamePauseAction = self.createAction("&Pause", self.pauseGame,
                                            "Ctrl+P","gamePause",
                                            "pause game",True)
        gameEndAction = self.createAction("&End", self.endGame,
                                         "Ctrl+E","gameEnd",
                                         "end game")
        gameLoadAction1 = self.createAction("Load &AI", self.loadAIdlg,
                                          "Ctrl+A", "loadAI",
                                          "load AI")
        gameLoadAction2 = self.createAction("Load &MAP", self.loadMapdlg,
                                           "Ctrl+M", "loadMap",
                                           "load MAP")
        gameEndAction.setEnabled(self.started)

        #creat game menu and add actions
        self.gameMenu = self.menuBar().addMenu("&Game")
        self.addActions(self.gameMenu, (gameStartAction, gamePauseAction,
                                  gameEndAction, None, gameLoadAction1,
                                        gameLoadAction2))

        #creat actions and add them to config menu
        self.configMenu = self.menuBar().addMenu("&Config")
        resetAction = self.createAction("&Reset", self.reset,
                                        icon = "reset",
                                        tip = "reset all settings")
        self.configMenu.addAction(resetAction)

        modeGroup1 = QActionGroup(self)
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

        #creat toolbars and add actions

        gameToolbar =  self.addToolBar("Game")
        self.addActions(gameToolbar, (gameStartAction, gamePauseAction,
                                  gameEndAction, gameLoadAction1, gameLoadAction2))
        configToolbar = self.addToolBar("Config")
        self.addActions(configToolbar, (run_modeAction, debug_modeAction,
                                        None, continue_modeAction,
                                        discon_modeAction, None,
                                        resetAction))





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

    def loadAIdlg(self):
        dir = r"./FileAI"
        fname = unicode(QFileDialog.getOpenFileName(self,
                                                    "load AI File", dir,
                                                    "AI files (%s)" % "*.exe"))
        if fname and fname != self.loaded_ai:
            print fname
            if self.loadAI(fname):
                self.loaded_ai = fname
            else:
                m = QMessageBox.warning(self, "Error", "Failed to load the AI file %s"
                                     %fname, QMessageBox.Ok, QMessageBox.NoButton)
    def loadMapdlg(self):
        dir = r"./FileMap"
        fname = unicode(QFileDialog.getOpenFileName(self,
                                                    "load Map File", dir,
                                                    "Map files (%s)" % "*.map"))
        if fname and fname != self.loaded_map:
            print fname
            if self.loadAI(fname):
                self.loaded_map = fname
            else:
                m = QMessageBox.warning(self, "Error", "Failed to load the Map file %s"
                                     %fname, QMessageBox.Ok, QMessageBox.NoButton)

    def loadAI(self, fname):
        return False

    def loadMap(self, fname):
        return False
    
    def setRunMode(self):
        pass

    def setDebugMode(self):
        pass

    def setConMode(self):
        pass

    def setDisconMode(self):
        pass
    
    def reset(self):
        pass

if __name__ == "__main__":
    app = QApplication(sys.argv)
    form = ai_debugger()
    rect = QApplication.desktop().availableGeometry()
    form.resize(rect.size())
    form.setWindowIcon(QIcon(":/icon.png"))
    form.show()
    app.exec_()
