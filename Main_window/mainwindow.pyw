import sys
from PyQt4.QtCore import *
from mainwindow.py import *

class Ui_Begin(QtGui.QDialog):
    def __init__(self, parent = None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_mainwindow()
        self.ui.setupUi(self)
        #连接信号与槽
        QtCore.QObject.connect(self.ui.startsingle,\
                               QtCore.SIGNAL('clicked()'), self.Startsingle)
        QtCore.QObject.connect(self.ui.webfight,\
                               QtCore.SIGNAL('clicked()'), self.Webfight)
        QtCore.QObject.connect(self.ui.website,\
                               QtCore.SIGNAL('clicked()'), self.Website)
        QtCore.QObject.connect(self.ui.team,\
                               QtCore.SIGNAL('clicked()'), self.Team)
        QtCore.QObject.connect(self.ui.music,\
                               QtCore.SIGNAL('clicked()'), self.Music)
        QtCore.QObject.connect(self.ui.exitgame,\
                               QtCore.SIGNAL('clicked()'), self.Exitgame)

    #槽函数定义    
    def Startsingle(self):
        startapp = Ui_Start()
        startapp.Show()

    def Webfight(self):
        webfightapp = Ui_webfight()
        webfightapp.Show()

    def Website(self):

    def Team(self):

    def Music(self):

    def Exitgame(self):

    #显示函数定义
    def Showmax(self):

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    mainapp = Ui_Begin()
    mainapp.Showmax()
    sys.exit(app.exec_())
