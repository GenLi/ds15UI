# -*- coding: utf-8 -*-
#Ver 0.5 edited at 2013-07-17-21:00
#Changes: a frame of data of battles

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
        self.movTimeline = QtCore.QTimeLine()
        self.atkTimeline = QtCore.QTimeLine()
        self.dieTimeline = QtCore.QTimeLine()
        self.animation = QtGui.QGraphicsItemAnimation()
        self.label = Ui_GridLabel("", 0, 0)
        #animation

    def SetSoldiers(self, units):
        "set the pos of soldiers"
        #what if a soldier dies??
        for i in range(len(units)):
            self.soldierItem[i].setPos(GetPos(units[i].x, units[i].y))
            self.soldierItem[i].mapX, self.soldierItem[i].mapY = \
                                      units[i].x, units[i].y

    def MovingAnimation(self, idnum, route):
        "moving animation, displayed when the soldier moves"
        TIME_PER_FRAME = 1000#ms, one-step movement in a frame
        FRAMES_BEFORE_MOVE = 3
        soldier = self.soldierItem[idnum]
        #self.setPos(GetPos(route[0].x, route[0].y))
        soldier.setPos(GetPos(route[0][0], route[0][1]))
        steps = len(route)-1
        frames = steps+FRAMES_BEFORE_MOVE

        self.movTimeline = QtCore.QTimeLine(frames*TIME_PER_FRAME)
        self.movTimeline.setCurveShape(self.movTimeline.LinearCurve)
        self.animation = QtGui.QGraphicsItemAnimation()
        self.animation.setItem(soldier)
        self.animation.setTimeLine(self.movTimeline)
        for i in range(steps+1):
            #
            pos = GetPos(route[i][0], route[i][1])
            self.animation.setPosAt(float((i+FRAMES_BEFORE_MOVE))/frames, pos)
        #
        soldier.SetMapPos(route[steps][0], route[steps][1])
        self.movTimeline.start()

    def AttackingAnimation(self, selfId, targetId, damage, info = ""):
        "attack animation, displayed when the soldier launches an attack."
        TOTAL_TIME = 2000
        TIME_FOR_MOVING = 500
        TIME_WHEN_RESETING = 1960
        DIST = 0.3
        attacker = self.soldierItem[selfId]
        target = self.soldierItem[targetId]
        
        self.atkTimeline = QtCore.QTimeLine(TOTAL_TIME)
        self.atkTimeline.setCurveShape(self.atkTimeline.LinearCurve)
        self.animation = QtGui.QGraphicsItemAnimation()
        self.animation.setItem(attacker)
        self.animation.setTimeLine(self.atkTimeline)
        r = DIST/math.sqrt((attacker.mapX-target.mapX)**2+(attacker.mapY-target.mapY)**2)
        pos = attacker.GetPos()*(1-r)+target.GetPos()*r
        self.animation.setPosAt(0, attacker.GetPos())
        self.animation.setPosAt(float(TIME_FOR_MOVING)/TOTAL_TIME, pos)
        self.animation.setPosAt(float(TIME_WHEN_RESETING)/TOTAL_TIME, pos)
        self.animation.setPosAt(1, attacker.GetPos())

        text = "%+d" % damage
        if (damage==0):
            text = info
        self.label = Ui_GridLabel(text, target.mapX, target.mapY)
        self.connect(self.atkTimeline, QtCore.SIGNAL("valueChanged(qreal)"),
                     self._ShowLabel)
        #set focus
        self.atkTimeline.start()
    def _ShowLabel(self, time):
        SHOW_TIME = 0.6
        DISAP_TIME = 0.9
        if (time>=SHOW_TIME):
            self.scene().addItem(self.label)
            self.label.setPos(GetPos(self.label.mapX, self.label.mapY))
        if (time>=DISAP_TIME):
            self.scene().removeItem(self.label)

    def DiedAnimation(self, selfId):
        "displayed when a soldier dies"
        TOTAL_TIME = 2000
        TIME_PER_FRAME = 40
        soldier = self.soldierItem[selfId]

        self.dieTimeline = QtCore.QTimeLine(TOTAL_TIME)
        self.dieTimeline.setCurveShape(self.dieTimeline.LinearCurve)
        self.dieTimeline.setUpdateInterval(TIME_PER_FRAME)
        self.connect(self.dieTimeline, QtCore.SIGNAL('valueChanged(qreal)'),
                     soldier.FadeOut)
        self.dieTimeline.start()

    #def TerrainChangeAnimation(self):

    def TerminateAnimation(self, units):
        "stop the animation and rearrange the units. \
        it should be called after an naimation."
        animTimeline = [self.movTimeline, self.atkTimeline, self.dieTimeline]
        self.animation.clear()
        for timeline in animTimeline:
            timeline.stop()
            try:
                timeline.valueChanged.disconnect()
            except TypeError:
                #pass
                print "No connection!"#for test
        self.SetSoldiers(units)



class UiD_RoundInfo:
    "info of every round"
    def __init__(self, bef_units, bef_changes = None,
                 aft_units = None, cmdEffect = None):
        self.begChanges = bef_changes
        self.cmdEffect = cmdEffect
        self.begUnits = bef_units
        self.endUnits = aft_units
    def __repr__():
        return UiD_RoundInfo(self.begUnits, self.begChanges,
                             self.cmdEffect, self.endUnits)

    #def ResetRoundBeginInfo(self):

class UiD_BattleData:
    "info of the entire battle(not completed)"
    def __init__(self, maps, units):
        self.map = maps
        self.roundInfo = []
        round0Info = UiD_RoundInfo(units)
        self.roundInfo.append(round0Info)

    def UpdateData(self, cmdEffect, nextUnits):
        "update the battle info"
        latestRound = len(self.roundInfo)
        self.roundInfo[latestRound].cmdEffect = cmdEffect
        self.roundInfo[latestRound].endUnits = nextUnits
        nextRoundInfo = UiD_RoundInfo(nextUnits)
        self.roundInfo.append(nextRoundInfo)

    #def GetRoundIniData(self, roundNum):
    #def GetRoundCmdData(self, roundNum):
    #def GetMap(self, roundNum):

    #def ChangeRoundInfo(self, roundNum, begUnits):
    #def RoundInfoIsChanged(self, roundNum):



if __name__=="__main__":
    app = QtGui.QApplication(sys.argv)
    scene = QtGui.QGraphicsScene()
    view = Ui_ReplayView(scene, maps, units)
    view.setBackgroundBrush(QtGui.QColor(255, 255, 255))
    view.setWindowTitle("Replay")
    view.show()
    print view.soldierItem[1].mapX, view.soldierItem[1].mapY#for test
    view.MovingAnimation(1, route)#for test
    view.TerminateAnimation(units)#for test
    print view.movTimeline.state()#for test
    print view.soldierItem[1].mapX, view.soldierItem[1].mapY#for test
    #view.AttackingAnimation(0, 3, -20, "Blocked")#for test
    #view.DiedAnimation(0)#for test
    sys.exit(app.exec_())
