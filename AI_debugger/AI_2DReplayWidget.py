#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# composite Ui_2DreplayWidget and provide a slider controling the playing

#from Ui_ReplayWidget import *
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from functools import partial

class CtrlSlider(QWidget):
    XMARGIN = 12.0
    YMARGIN = 5.0
    WSTRING = "999"
    def __init__(self, parent = None):
        super(CtrlSlider, self).__init__(parent)

        self.pausePoint = []
        self.nowRound = 2
        self.totalRound = 2
        self.nowStatus = 0
        self.totalStatus = 0
        self.setFocusPolicy(Qt.NoFocus)
        self.setSizePolicy(QSizePolicy(QSizePolicy.MinimumExpanding,
                                       QSizePolicy.Fixed))
        #default continues play mode ,enable pausePoint
        self.playMode = 0

    def sizeHint(self):
        return self.minimumSizeHint()


    def minimumSizeHint(self):
        font = QFont(self.font())
        font.setPointSize(font.pointSize() - 1)
        fm = QFontMetricsF(font)
        return QSize(fm.width(CtrlSlider.WSTRING) * \
                     self.totalRound,
                     (fm.height() * 4) + CtrlSlider.YMARGIN)

    #人工改变当前回合时调用.连续播放改变当前回合时并不调用
    def changeNowRound(self, round_, status):
        if self.nowRound != round_ or self.nowStatus != status:
            self.nowRound = round_
            self.nowStatus = status
            self.emit(SIGNAL("nowChanged(int, int)"), self.nowRound, self.nowStatus)
            self.update()
        
    #暂停点功能以后再说
    def addPausePoint(self, round_):
        if not round_ in self.pausePoint and not self.playMode:
            self.pausePoint.append(round_)
            self.update()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.moveSlider(event.x())
            event.accept()
        else:
            QWidget.mousePressEvent(self, event)

    def contextMenuEvent(self, event):
        menu = QMenu(self)
        pauseAction = menu.addAction("add pause point")
        span = self.width() - (CtrlSlider.XMARGIN * 2)
        offset =  event.pos().x() - CtrlSlider.XMARGIN
        round_ = int(round(float(offset) / span * self.totalRound))
        self.connect(pauseAction, SIGNAL("triggered()"), partial(self.addPausePoint, round_))
        menu.exec_(event.globalPos())

    def mouseMoveEvent(self, event):
        self.moveSlider(event.x())

    def moveSlider(self, x):
        span = self.width() - (CtrlSlider.XMARGIN * 2)
        offset = x - CtrlSlider.XMARGIN
        round_ = int(round(float(offset) / span * (2 * (self.totalRound-1)+ self.totalStatus)))
        round_ = max(0, min(round_, (self.totalRound-1)*2+self.totalStatus))
        nowround = 1 + round_ / 2
        nowstatus = round_ % 2                       #0回合开始,1回合结束
        self.changeNowRound(nowround, nowstatus)

      
    def changeTotalRound(self):
        if self.totalStatus == 0:
            self.totalStatus = 1
            self.nowStatus = 1
        else:
            self.totalRound += 1
        #要不要加当前回合呢...想清楚
            self.nowRound += 1
        self.emit(SIGNAL("totalChanged()"))
        self.update()

    def paintEvent(self, event=None):
        font = QFont(self.font())
        font.setPointSize(font.pointSize() - 1)
        fm = QFontMetricsF(font)
        fracWidth = fm.width(CtrlSlider.WSTRING)
        span = self.width() - (CtrlSlider.XMARGIN * 2)
        if self.totalRound == 0:
            value = 0
        else:
            value = ((self.nowRound-1) * 2 + self.nowStatus) / float((self.totalRound-1) * 2 + self.totalStatus)
            painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setRenderHint(QPainter.TextAntialiasing)
        painter.setPen(self.palette().color(QPalette.Mid))
        painter.setBrush(self.palette().brush(QPalette.AlternateBase))
        painter.drawRect(self.rect())
        segColor = QColor(Qt.green).dark(120)
        segLineColor = segColor.dark()                                #回合开始线
        segEndColor = QColor(Qt.red).dark(120)                        #回合结束线
        painter.setPen(segLineColor)
        painter.setBrush(segColor)
        painter.drawRect(CtrlSlider.XMARGIN,
                         CtrlSlider.YMARGIN, span, fm.height())
        textColor = self.palette().color(QPalette.Text)
        segWidth = span / ((self.totalRound-1) * 2 + self.totalStatus)
        segHeight = fm.height() * 2
        nRect = fm.boundingRect(CtrlSlider.WSTRING)
        x = CtrlSlider.XMARGIN
        yOffset = segHeight + fm.height()
        painter.setBrush(QColor(Qt.red))
        for i in range(1, self.totalRound + 1):
            painter.setPen(segLineColor)
            painter.drawLine(x, CtrlSlider.YMARGIN, x, segHeight)
            painter.setPen(textColor)
            y = segHeight
            rect = QRectF(nRect)
            rect.moveCenter(QPointF(x, y + fm.height() / 2.0))
            painter.drawText(rect, Qt.AlignCenter, QString.number(i))
            if i in self.pausePoint:
                rect.setHeight(rect.height() / 2)
                rect.setWidth(rect.width() / 2)
                rect.moveCenter(QPointF(x, CtrlSlider.YMARGIN))
                painter.drawEllipse(rect)
            x += segWidth
            if i == self.totalRound and self.totalStatus == 0:
                break
            else:
                painter.setPen(segEndColor)
                painter.drawLine(x, CtrlSlider.YMARGIN, x, segHeight)
                painter.setPen(textColor)
                rect.setHeight(rect.height() * 2)
                rect.setWidth(rect.width() * 2)
                rect.moveCenter(QPointF(x, y + fm.height() / 2.0))
                painter.drawText(rect, Qt.AlignCenter, QString.number(i))
                x += segWidth
        
        span = int(span)
        y = CtrlSlider.YMARGIN - 0.5
        triangle = [QPointF(value * span, y),
                    QPointF((value * span) + \
                            (2 * CtrlSlider.XMARGIN), y),
                    QPointF((value * span) + \
                            CtrlSlider.XMARGIN, fm.height())]
        painter.setPen(Qt.yellow)
        painter.setBrush(Qt.darkYellow)
        painter.drawPolygon(QPolygonF(triangle))

class AI_2DReplayWidget(QWidget):
    def __init__(self, parent = None):
        QWidget.__init__(self,parent)

        self.NowEqualTotal = True
        self.playMode = 0#默认连续播放模式0, 逐回合暂停模式为1
      #  self.TotalStatus = 0#默认在回合开始
        self.replayWidget = Ui_2DReplayWidget(self, scene, parent)
        #self.replayWidget = QLabel()
        self.ctrlSlider = CtrlSlider()
        self.totalLabel = QLabel("total round:")
        self.nowLabel = QLabel("now round:")
        self.totalInfo = QLCDNumber()
        self.totalInfo.display(2)
        self.totalInfo.setSegmentStyle(QLCDNumber.Flat)
        self.totalStatusInfo = QLabel("At begin")
        self.nowInfo = QLineEdit("")
        self.nowInfo.setText("2")
        self.nowStatusInfo = QLabel("At begin")
        self.nextRoundButton = QPushButton("Next Round")
        self.pauseButton = QPushButton("Pause")
        self.playModeLabel = QLabel("Continuous")
        self.playModeLabel.setFrameStyle(QFrame.StyledPanel | QFrame.Sunken)
        self.nowStatusInfo.setSizePolicy(QSizePolicy(QSizePolicy.Fixed|QSizePolicy.Fixed))
        self.totalStatusInfo.setSizePolicy(QSizePolicy(QSizePolicy.Fixed|QSizePolicy.Fixed))
        self.playModeLabel.setSizePolicy(QSizePolicy(QSizePolicy.Fixed|QSizePolicy.Fixed))

        hlayout = QHBoxLayout()
        hlayout.addWidget(self.totalLabel)
        hlayout.addWidget(self.totalInfo)
        hlayout.addWidget(self.totalStatusInfo)
        hlayout.addWidget(self.nowLabel)
        hlayout.addWidget(self.nowInfo)
        hlayout.addWidget(self.nowStatusInfo)
        hlayout.addWidget(self.nextRoundButton)
        hlayout.addWidget(self.pauseButton)
        hlayout.addStretch()
        hlayout.addWidget(self.playModeLabel)

        vlayout = QVBoxLayout()
        vlayout.addWidget(self.replayWidget)
        vlayout.addWidget(self.ctrlSlider)
        vlayout.addLayout(hlayout)

        self.setLayout(vlayout)

        self.connect(self.ctrlSlider, SIGNAL("nowChanged(int,int)"),
                     self.setNowRound)
        self.connect(self.ctrlSlider, SIGNAL("totalChanged()"),
                     self.updateUI)
        self.connect(self.nowInfo, SIGNAL("textEdited(QString)"), self.check)
        self.connect(self.nextRoundButton, SIGNAL("clicked()"), self.nextOrder)
        self.connect(self.pauseButton, SIGNAL("clicked()"), self.pauseGame)
    def updateUI(self):
        self.totalInfo.display(self.ctrlSlider.totalRound)
        self.nowInfo.setText(QString.number(self.ctrlSlider.nowRound))
        totalstatus = "At begin" if self.ctrlSlider.totalStatus == 0 else "At end"
        nowstatus = "At begin" if self.ctrlSlider.nowStatus == 0 else "At end"
        self.totalStatusInfo.setText(totalstatus)
        self.nowStatusInfo.setText(nowstatus)
        self.NowEqualTotal = (self.ctrlSlider.nowRound == self.ctrlSlider.totalRound
                              and self.ctrlSlider.nowStatus == self.ctrlSlider.totalStatus)
        #在不同模式里en/disable按钮,
        enable = True if self.playMode == 1 else False
        self.nextRoundButton.setEnabled(enable)
        enable = not enable and self.NowEqualTotal
        self.pauseButton.setEnabled(enable)

        modetext = "Continuous" if self.playMode == 0 else "Discontinuous"
        self.playModeLabel.setText(modetext)

    #被外部调用.
    def setPlayMode(self, mode):
        self.playMode = mode
        self.ctrlSlider.playMode = mode#与暂停点有关...暂时不管
        self.updateUI()

    def setNowRound(self, a, b):
        self.replayWidget.GoToRound(a,b)
        self.updateUI()

    #validate nowInfo的输入
    def check(self):
        now = unicode(self.nowInfo.text())
        if len(now) == 0:
            self.nowInfo.setText(QString.number(self.ctrlSlider.nowRound))
            self.nowInfo.selectAll()
            self.nowInfo.setFocus()
        elif 0 < int(now) <= self.ctrlSlider.totalRound:
            self.ctrlSlider.changeNowRound(int(now),0)                #修改nowlineedit默认跳转到该回合开始阶段
        else:
            self.nowInfo.setText(QString.number(self.ctrlSlider.nowRound))
            self.nowInfo.selectAll()
            self.nowInfo.setFocus()

   #用户在逐回合暂停模式下按下nextround按键调用次线程的某方法,向平台获得下一个回合的消息.
    #如果用户不在最新回合.自动跳转到最新回合.
    def nextOrder(self):
        pass

    #在连续播放模式下可以使用这个按键.发送消息让主界面暂停或开始次线程的一定时间向平台发出信号获取信息的行为
    def pauseGame(self):
        pass

    #在从平台获得信息时,从外部调用
    def updateBeg(self, beginfo):
        self.replayWidget.UpdateBeginData(beginfo)
        self.changeTotalRound()
        self.updateUI()

    def updateEnd(self, cmd, endinfo):
        self.replayWidget.UpdateEndData(cmd, endinfo)
        self.changeTotalRound()
        self.updateUI()

#just for test
if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    form = AI_2DReplayWidget()
    form.show()
    app.exec_()
