# -*- coding: utf-8 -*-
#Ver 0.3 edited at 2013-07-16-0:48
#Changes: solves the bug in moving animation
#         attack animation added

#scene, view of replay

from Ui_Units import *
import sys, math


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
route = ((0, 0), (0, 1), (1, 1), (1, 2), (1, 3))
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
        self.timeline = QtCore.QTimeLine()
        self.animation = QtGui.QGraphicsItemAnimation()
        #animation
    
    #def SetSoliders(self):
    def SetSoldiers(self, units):
        "set the pos of soldiers"
        #what if a soldier dies??
        for i in range(len(units)):
            self.soldierItem[i].setPos(GetPos(units[i].x, units[i].y))
            self.soldierItem[i].mapX, self.soldierItem[i].mapY = \
                                      units[i].x, units[i].y

    #def MovingAnimation(self):
    def MovingAnimation(self, idnum, route):
        "moving animation, displayed when the soldier moves"
        TIME_PER_FRAME = 1000#ms, one-step movement in a frame
        FRAMES_BEFORE_MOVE = 3
        soldier = self.soldierItem[idnum]
        #self.setPos(GetPos(route[0].x, route[0].y))
        soldier.setPos(GetPos(route[0][0], route[0][1]))
        steps = len(route)-1
        frames = steps+FRAMES_BEFORE_MOVE

        self.timeline = QtCore.QTimeLine(frames*TIME_PER_FRAME)
        self.timeline.setCurveShape(self.timeline.LinearCurve)
        self.animation = QtGui.QGraphicsItemAnimation()
        self.animation.setItem(soldier)
        self.animation.setTimeLine(self.timeline)
        for i in range(steps+1):
            #
            pos = GetPos(route[i][0], route[i][1])
            self.animation.setPosAt(float((i+FRAMES_BEFORE_MOVE))/frames, pos)
        #
        soldier.SetMapPos(route[steps][0], route[steps][1])
        #self.animation.setPosAt(1, soldier.GetPos())
        self.timeline.start()

    #def AttackAnimation(self):
    def AttackAnimation(self, selfId, targetId, damage, info = ""):
        "attack animation, displayed when the soldier launches an attack."
        TOTAL_TIME = 2000
        TIME_FOR_MOVING = 500
        TIME_WHEN_RESETING = 1960
        DIST = 0.3
        attacker = self.soldierItem[selfId]
        target = self.soldierItem[targetId]
        
        self.timeline = QtCore.QTimeLine(TOTAL_TIME)
        self.timeline.setCurveShape(self.timeline.LinearCurve)
        self.animation = QtGui.QGraphicsItemAnimation()
        self.animation.setItem(attacker)
        self.animation.setTimeLine(self.timeline)
        r = DIST/math.sqrt((attacker.mapX-target.mapX)**2+(attacker.mapY-target.mapY)**2)
        pos = attacker.GetPos()*(1-r)+target.GetPos()*r
        self.animation.setPosAt(0, attacker.GetPos())
        self.animation.setPosAt(float(TIME_FOR_MOVING)/TOTAL_TIME, pos)
        self.animation.setPosAt(float(TIME_WHEN_RESETING)/TOTAL_TIME, pos)
        self.animation.setPosAt(1, attacker.GetPos())
        #show damage and info
        self.timeline.start()

    #def DieAnimation(self, selfId):



if __name__=="__main__":
    app = QtGui.QApplication(sys.argv)
    scene = QtGui.QGraphicsScene()
    view = Ui_ReplayView(scene, maps, units)
    view.setBackgroundBrush(QtGui.QColor(255, 255, 255))
    view.setWindowTitle("Replay")
    view.show()
    #view.MovingAnimation(1, route)#for test
    print view.soldierItem[1].mapX, view.soldierItem[1].mapY#for test
    view.AttackAnimation(0, 3, 0)
    sys.exit(app.exec_())
