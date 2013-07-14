# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'H:/��ʽ/jm/mainwindow.ui'
#
# Created: Sat Jul 13 09:36:35 2013
#      by: PyQt4 UI code generator 4.10.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_mainwindow(object):
    def setupUi(self, mainwindow):
        mainwindow.setObjectName(_fromUtf8("mainwindow"))
        mainwindow.resize(256, 426)
        self.startsingle = QtGui.QPushButton(mainwindow)
        self.startsingle.setGeometry(QtCore.QRect(40, 50, 141, 31))
        self.startsingle.setObjectName(_fromUtf8("startsingle"))
        self.webfight = QtGui.QPushButton(mainwindow)
        self.webfight.setGeometry(QtCore.QRect(40, 110, 141, 31))
        self.webfight.setObjectName(_fromUtf8("webfight"))
        self.website = QtGui.QPushButton(mainwindow)
        self.website.setGeometry(QtCore.QRect(40, 170, 141, 31))
        self.website.setObjectName(_fromUtf8("website"))
        self.team = QtGui.QPushButton(mainwindow)
        self.team.setGeometry(QtCore.QRect(40, 230, 141, 31))
        self.team.setObjectName(_fromUtf8("team"))
        self.music = QtGui.QPushButton(mainwindow)
        self.music.setGeometry(QtCore.QRect(40, 290, 141, 31))
        self.music.setObjectName(_fromUtf8("music"))
        self.exitgame = QtGui.QPushButton(mainwindow)
        self.exitgame.setGeometry(QtCore.QRect(40, 350, 141, 31))
        self.exitgame.setObjectName(_fromUtf8("exitgame"))

        self.retranslateUi(mainwindow)
        QtCore.QMetaObject.connectSlotsByName(mainwindow)

    def retranslateUi(self, mainwindow):
        mainwindow.setWindowTitle(_translate("mainwindow", "Form", None))
        self.startsingle.setText(_translate("mainwindow", "单人游戏", None))
        self.webfight.setText(_translate("mainwindow", "网络对战", None))
        self.website.setText(_translate("mainwindow", "队式官网", None))
        self.team.setText(_translate("mainwindow", "开发人员", None))
        self.music.setText(_translate("mainwindow", "音乐效果", None))
        self.exitgame.setText(_translate("mainwindow", "退出游戏", None))

