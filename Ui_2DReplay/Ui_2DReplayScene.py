# -*- coding: utf-8 -*-
#Ver 0.1 edited at 2013-07-14-15:29
#Changes: soldiers' display(not completed)

#scene, view of replay

from Ui_Units import *
import sys


class Unit_forTest:
    def __init__(self, x, y, type):
        self.x = x
        self.y = y
        self.type = type

a = Unit_forTest
maps = [[0, 0, 0, 1, 1, 1, 0, 1],
        [3, 3, 3, 4, 1, 1, 0, 0],
        [3, 3, 0, 1, 2, 2, 2, 2],
        [0, 0, 0, 0, 2, 2, 2, 2]]
units = [a(0, 0, LANCER), a(1, 3, SABER), a(2, 3, ARCHER), a(3, 4, HERO_1)]
#data for test



class Ui_ReplayView(QtGui.QGraphicsView):
    "the replay graphic view"
    def __init__(self, scene, maps, units, parent = None):
        QtGui.QGraphicsView.__init__(self, scene)
        self.mapItem = []
        for i in range(len(maps)):
            newColumn = []
            for j in range(len(maps[i])):
                newMapUnit = Ui_MapUnit(i, j, maps[i][j])
                scene.addItem(newMapUnit)
                newColumn.append(newMapUnit)
            self.mapItem.append(newColumn)
        for i in range(len(maps)):
            for j in range(len(maps[i])):
                self.mapItem[i][j].setPos(GetPos(i, j))
        #initialization of map units
        self.soldierItem = []
        for unit in units:
            newSoldierUnit = Ui_SoldierUnit(unit.x, unit.y, unit.type)
            scene.addItem(newSoldierUnit)
            self.soldierItem.append(newSoldierUnit)
        self.SetSoldiers(units)
        #initialization of soldier units
        #initialization of the cursor
    
    #def SetSoliders(self):
    def SetSoldiers(self, units):
        "set the pos of soldiers"
        for i in range(len(units)):
            self.soldierItem[i].setPos(GetPos(units[i].x, units[i].y))
            self.soldierItem[i].mapX, self.soldierItem[i].mapY = \
                                      units[i].x, units[i].y



if __name__=="__main__":
    app = QtGui.QApplication(sys.argv)
    scene = QtGui.QGraphicsScene()
    view = Ui_ReplayView(scene, maps, units)
    view.setBackgroundBrush(QtGui.QColor(255, 255, 255))
    view.setWindowTitle("Replay")
    view.show()
    sys.exit(app.exec_())
