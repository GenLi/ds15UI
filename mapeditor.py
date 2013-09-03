# -*- coding: utf-8 -*-

import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from Ui_mapeditor import *

class Mapeditor(QtGui.QDialog):
    def __init__(self, parent = None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_Mapeditor()
        self.ui.setupUi(self)
        self.dirty = False
        self.filename = None
        QtCore.QObject.connect(self.ui.newButton,\
                               QtCore.SIGNAL('clicked()'), self.NewFile)
        QtCore.QObject.connect(self.ui.openButton,\
                               QtCore.SIGNAL('clicked()'), self.Open)
        QtCore.QObject.connect(self.ui.saveButton,\
                               QtCore.SIGNAL('clicked()'), self.Save)
        QtCore.QObject.connect(self.ui.saveasButton,\
                               QtCore.SIGNAL('clicked()'), self.SaveAs)
        QtCore.QObject.connect(self.ui.exitButton,\
                               QtCore.SIGNAL('clicked()'), self.close)
        #QtCore.QObject.connect(self.ui.,\
                               #QtCore.SIGNAL('clicked()'), self.)

    def SetMap(self):
        outfile = QFile(self.filename)
        if not outfile.open(QIODevice.WriteOnly):
            box = QMessageBox(QMessageBox.Warning, "Error", "")
            box.exec_()
            return
        outfile.close()
        self.dirty = False

    def OpenFile(self):
        infile = QFile(self.filename)
        if not infile.open(QIODevice.WritenOnly):
            box = QMessageBox(QMessageBox.Warning, "Error", "")
            box.exec_()
            return
        infile.close()
        self.dirty = False
        self.SetMap()
    
    def couldSave(self):
        return True

    def isSaved(self):
        return True

    def Save(self):
        if self.couldSave():
            if self.dirty == True:
                self.filename = QFileDialog.getSaveFileName(self, "Save",
                                                        "/.", "*.map")
            if not self.filename != None:
                self.SetMap()
            else:
                self.filename = "Untitled"
        else:
            box = QMessageBox(QMessageBox.Warning, "Error", "")
            box.exec_()

    def Open(self):
        if self.isSaved():
            self.filename = QFileDialog.getOpenFileName(self, "Open File",
                                                        "/.", "*.map")
            if not self.filename != None:
                self.OpenFile()
            else:
                self.filename = "Untitled"

    def NewFile(self):
        if self.isSaved():
            Initialize()
            self.filename = "Untitled"
            self.setWindowTitle(self.filename)
            self.dirty = True

    def SaveAs(self):
        if self.couldSave():
            self.filename = QFileDialog.getSaveFileName(self, "Save",
                                                        "/.", "*.map")
            if not self.filename != None:
                self.SetMap()
            else:
                self.filename = "Untitled"
        else:
            box = QMessageBox(QMessageBox.Warning, "Error", "")
            box.exec_()

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    mapapp = Mapeditor()
    mapapp.show()
    sys.exit(app.exec_())
