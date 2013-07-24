#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from PyQt4.QtGui import *
from PyQt4.QtCore import *
#import basic

#two dictionaries for show types of map or unit
NumToMapType = {0:"PLAIN",1:"MOUNTAIN",2:"FOREST",3:"BARRIER",4:"TURRET",
                 5:"TRAP",6:"TEMPLE",7:"GEAR"}
NumToUnitType = {0:"SABER",1:"LANCER",2:"ARCHER",3:"DRAGON RIDER",
                4:"WARRIOR", 5:"WIZARD", 6:"HERO_1", 7:"HERO_2",
                8:"HERO_3"}

class InfoWidget(QTabWidget):
    def __init__(self, parent =None):
        super(InfoWidget, self).__init__(parent)

        self.infoWidget_Game = InfoWidget1()
        self.infoWidget_Unit = InfoWidget2()
        self.infoWidget_Map = InfoWidget3()
        self.addTab(self.infoWidget_Game, "Game info")
        self.addTab(self.infoWidget_Unit, "Unit info")
        self.addTab(self.infoWidget_Map, "Map info")
        self.setTabToolTip(1, "the global infos and game runing infos")
        self.setTabToolTip(2, "the selected unit's infos")
        self.setTabToolTip(3, "the selected map-grid's infos")

    #reimplement close event:just set invisible
    def closeEvent(self, event):
        self.hide()
        event.ignore()
    def hideEvent(self, event):
        self.emit(SIGNAL("hided()"))

    def newGameInfo(self, _round, round_info):
        self.sender = self.sender()
        self.infoWidget_Game.setRoundInfo(_round)

        if self.sender == None:
            pass
        #待实现,1在跳转回合时从回放里设置的类传出的信号设置,2从平台获取最新信息时
        ##根据得到的类们设置。需要分开吗???
    def newUnitInfo(self, base_unit):
        self.infoWidget_Unit.info_type.setText(NumToUnitType[base_unit.kind])
        self.infoWidget_Unit.info_life.setText("%d" %base_unit.life)
        self.infoWidget_Unit.info_attack.setText("%d" %base_unit.attack)
        self.infoWidget_Unit.info_defence.setText("%d" %base_unit.defence)
        self.infoWidget_Unit.info_speed.setText("%d" %base_unit.speed)
        self.infoWidget_Unit.info_moverange.setText("%d" %base_unit.move_range)
        self.infoWidget_Unit.info_attackrange.setText("%s" %base_unit.attack_range)
        self.setCurrentWidget(self.infoWidget_Unit)
    def newMapInfo(self, map_basic):
        self.infoWidget_Map.info_type.setText(NumToMapType[map_basic.kind])
        self.infoWidget_Map.info_score.setText("%d" %map_basic.score)
        self.infoWidget_Mao.info_consumption.setText("%d" %map_basic.move_consumption)
        self.setCurrentWidget(self.infoWidget_Map)
    def offSelected(self):
        self.infoWidget_Map.infoReset()
        self.infoWidget_Unit.infoReset()
        self.setCurrentWidget(self.infoWidget_Game)

class InfoWidget1(QWidget):
    def __init__(self, parent = None):
        super(InfoWidget1, self).__init__(parent)

        self.label_aifile = QLabel("AI file path:")
        self.info_aifile = QLineEdit("")
        self.info_aifile.setReadOnly(True)
        self.label_mapfile = QLabel("MAP file path:")
        self.info_mapfile = QLineEdit("")
        self.info_mapfile.setReadOnly(True)
        self.label_round = QLabel("current round:")
        self.info_round = QLineEdit("")
        self.info_round.setReadOnly(True)
        self.label_unit = QLabel("current aciton_unit:")
        self.info_unit = QLineEdit("")
        self.info_unit.setReadOnly(True)
        self.label_time = QLabel("time used:")
        self.info_time = QLineEdit("")
        self.info_time.setReadOnly(True)
        self.label_cmd = QLabel("command:")
        self.info_cmd = QLineEdit("")
        self.info_cmd.setReadOnly(True)

        self.layout = QGridLayout()
        self.layout.addWidget(self.label_aifile, 0, 0)
        self.layout.addWidget(self.info_aifile, 0, 1)
        self.layout.addWidget(self.label_mapfile, 1, 0)
        self.layout.addWidget(self.info_mapfile, 1, 1)
        self.layout.addWidget(self.label_round, 2, 0)

        self.layout.addWidget(self.info_round, 2, 1)
        self.layout.addWidget(self.label_unit, 3, 0)
        self.layout.addWidget(self.info_unit, 3, 1)
        self.layout.addWidget(self.label_time, 4, 0)
        self.layout.addWidget(self.info_time, 4, 1)
        self.layout.addWidget(self.label_cmd, 5, 0)
        self.layout.addWidget(self.info_cmd, 5, 1)

        self.setLayout(self.layout)
    def setAiFileinfo(self, str):
        self.info_aifile.setText(str)
    def setMapFileinfo(self, str):
        self.info_mapfile.setText(str)
    def setRoundinfo(self, r):
        self.info_round.setText(r)
    def setUnitinfo(self, str):
        self.info_unit.setText(str)
    def setTimeinfo(self, str):
        self.info_time.setText(str)
    def setCmdinfo(self, str):
        self.info_cmd.setText(str)


class InfoWidget2(QWidget):
    def __init__(self, parent = None):
        super(InfoWidget2, self).__init__(parent)
        self.infos = []
   #     self.label_id = QLabel("unit id:")
    #    self.info_id = QLabel("")
     #   self.info_id.setFrameStyle(QFrame.StyledPanel|QFrame.Sunken)
        self.label_type = QLabel("unit type:")
        self.info_type = QLabel("")
        self.infos.append(self.info_type)
        self.label_life = QLabel("unit life:")
        self.info_life= QLabel("")
        self.infos.append(self.info_life)
        self.label_attack = QLabel("attack:")
        self.info_attack = QLabel("")
        self.infos.append(self.info_attack)
        self.label_speed = QLabel("speed:")
        self.info_speed = QLabel("")
        self.infos.append(self.info_speed)
        self.label_defence = QLabel("defence:")
        self.info_defence = QLabel("")
        self.infos.append(self.info_defence)
        self.label_moverange = QLabel("move range:")
        self.info_moverange = QLabel("")
        self.infos.append(self.info_moverange)
        self.label_attackrange = QLabel("attack range:")
        self.info_attackrange = QLabel("")
        self.infos.append(self.info_attackrange)

        for info in self.infos:
            info.setFrameStyle(QFrame.StyledPanel|QFrame.Sunken)

        self.layout = QGridLayout()
        self.layout.addWidget(self.label_type, 0, 0)
        self.layout.addWidget(self.info_type, 0, 1)
        self.layout.addWidget(self.label_life, 1, 0)
        self.layout.addWidget(self.info_life, 1, 1)
        self.layout.addWidget(self.label_attack, 2, 0)
        self.layout.addWidget(self.info_attack, 2, 1)
        self.layout.addWidget(self.label_defence, 3, 0)
        self.layout.addWidget(self.info_defence, 3, 1)
        self.layout.addWidget(self.label_speed, 4, 0)
        self.layout.addWidget(self.info_speed, 4, 1)
        self.layout.addWidget(self.label_moverange, 5, 0)
        self.layout.addWidget(self.info_moverange, 5, 1)
        self.layout.addWidget(self.label_attackrange, 6, 0)
        self.layout.addWidget(self.info_attackrange, 6, 1)

        self.setLayout(self.layout)

    def infoReset(self):
        for info in self.infos:
            info.setText("")

class InfoWidget3(QWidget):
    def __init__(self, parent = None):
        super(InfoWidget3, self).__init__(parent)
        self.infos = []
        self.label_type = QLabel("map type:")
        self.info_type = QLabel("")
        self.infos.append(self.info_type)
        self.label_score = QLabel("map score:")
        self.info_score= QLabel("")
        self.infos.append(self.info_score)
        self.label_consumption = QLabel("move consumption:")
        self.info_consumption = QLabel("")
        self.infos.append(self.info_consumption)

        for info in self.infos:
            info.setFrameStyle(QFrame.StyledPanel|QFrame.Sunken)

        self.layout = QGridLayout()
        self.layout.addWidget(self.label_type, 0, 0)
        self.layout.addWidget(self.info_type, 0, 1)
        self.layout.addWidget(self.label_score, 1, 0)
        self.layout.addWidget(self.info_score, 1, 1)
        self.layout.addWidget(self.label_consumption, 2, 0)
        self.layout.addWidget(self.info_consumption, 2, 1)

        self.setLayout(self.layout)

    def infoReset(self):
        for info in self.infos:
            info.setText("")

#just for test
if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    form = InfoWidget()
    form.show()
    app.exec_()
