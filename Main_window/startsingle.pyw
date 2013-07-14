import sys
form PyQt4.QtCore import *
from startsingle.py import *

class Ui_Start(QtGui.QDialog):
    def __init__(self, parent = None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        #连接信号与槽
        QtCore.QObject.connect(self.ui.aivsai,\
                               QtCore.SIGNAL('clicked()'), self.Aivsai)
        QtCore.QObject.connect(self.ui.playervsai,\
                               QtCore.SIGNAL('clicked()'), self.Playervsai)
        QtCore.QObject.connect(self.ui.levelmode,\
                               QtCore.SIGNAL('clicked()'), self.Levelmode)
        QtCore.QObject.connect(self.ui.replay,\
                               QtCore.SIGNAL('clicked()'), self.Replay)
        QtCore.QObject.connect(self.ui.mapedit,\
                               QtCore.SIGNAL('clicked()'), self.Mapedit)
        QtCore.QObject.connect(self.ui.returnpre,\
                               QtCore.SIGNAL('clicked()'), self.Returnpre)

    #槽函数定义
    def Aivsai(self):

    def Playervsai(self):

    def Levelmode(self):

    def Replay(self):

    def Mapedit(self):

    def Returnpre(self):

    #显示函数定义
    def Show(self):

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    singleapp = Ui_Start()
    singleapp.Show()
    sys.exit(app.exec_())
