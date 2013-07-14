# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'H:/��ʽ/jm/startsingle.ui'
#
# Created: Sat Jul 13 10:21:05 2013
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

class Ui_startsingle(object):
    def setupUi(self, startsingle):
        startsingle.setObjectName(_fromUtf8("startsingle"))
        startsingle.resize(178, 400)
        self.playervsai = QtGui.QPushButton(startsingle)
        self.playervsai.setGeometry(QtCore.QRect(30, 110, 141, 31))
        self.playervsai.setObjectName(_fromUtf8("playervsai"))
        self.levelmode = QtGui.QPushButton(startsingle)
        self.levelmode.setGeometry(QtCore.QRect(30, 170, 141, 31))
        self.levelmode.setObjectName(_fromUtf8("levelmode"))
        self.aivsai = QtGui.QPushButton(startsingle)
        self.aivsai.setGeometry(QtCore.QRect(30, 50, 141, 31))
        self.aivsai.setObjectName(_fromUtf8("aivsai"))
        self.replay = QtGui.QPushButton(startsingle)
        self.replay.setGeometry(QtCore.QRect(30, 230, 141, 31))
        self.replay.setObjectName(_fromUtf8("replay"))
        self.mapedit = QtGui.QPushButton(startsingle)
        self.mapedit.setGeometry(QtCore.QRect(30, 290, 141, 31))
        self.mapedit.setObjectName(_fromUtf8("mapedit"))
        self.returnpre = QtGui.QPushButton(startsingle)
        self.returnpre.setGeometry(QtCore.QRect(30, 350, 141, 31))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.returnpre.sizePolicy().hasHeightForWidth())
        self.returnpre.setSizePolicy(sizePolicy)
        self.returnpre.setObjectName(_fromUtf8("returnpre"))

        self.retranslateUi(startsingle)
        QtCore.QMetaObject.connectSlotsByName(startsingle)

    def retranslateUi(self, startsingle):
        startsingle.setWindowTitle(_translate("startsingle", "Form", None))
        self.playervsai.setText(_translate("startsingle", "人机对战", None))
        self.levelmode.setText(_translate("startsingle", "闯关模式", None))
        self.aivsai.setText(_translate("startsingle", "AI对战", None))
        self.replay.setText(_translate("startsingle", "战争回放", None))
        self.mapedit.setText(_translate("startsingle", "编辑地图", None))
        self.returnpre.setText(_translate("startsingle", "返回上级", None))

