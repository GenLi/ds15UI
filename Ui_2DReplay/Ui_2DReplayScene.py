# -*- coding: utf-8 -*-
#Ver 0.6.3 edited at 2013-07-23-19:54
#Changes: type of data changed
#Changes: change the two-dimen array into a one-dimen one(OK)
#Changes: initialization
#need to change: make the cursor fixed when playing

#scene, view of replay

from Ui_Units import *
import sys, math


class a:
    def __init__(self):
        self.b = 100
m = Map_Basic
u = Base_Unit

maps = [[m(0), m(0), m(1), m(1)],
        [m(1), m(1), m(0), m(1)],
        [m(1), m(0), m(1), m(0)],
        [m(0), m(0), m(1), m(1)]]
units = [u(1, (0, 0)), u(2, (0, 1)), u(3, (0, 2)),
         u(3, (3, 3)), u(2, (3, 2)), u(1, (3, 1))]
units2 = [[u(1, (0, 0)), u(2, (0, 1)), u(3, (0, 2))],
          [u(3, (3, 3)), u(2, (3, 2)), u(1, (3, 1))]]
iniInfo = Begin_Info(maps, units2)
begInfo = Round_Begin_Info(1, ((1, 1)), units2)

route = ((0, 1), (0, 2), (1, 2), (2, 2))
def fun():
    return route
cmd = Command(0, (2, 2), 0)
endInfo = Round_End_Info(units2, None, (0, 0), -1)

#data for test


class Ui_ReplayView(QtGui.QGraphicsView):
    "the replay graphic view"
    def __init__(self, scene, parent = None):
        QtGui.QGraphicsView.__init__(self, scene, parent)
        self.mapItem = []
        self.soldierItem = []
        self.soldierAlive = []
        self.sizeX = 0
        self.sizeY = 0
        #ini of items
        self.cursor = None
        self.timerId = self.startTimer(500)#frickering period
        #ini of the cursor
        self.movTimeline = QtCore.QTimeLine()
        self.atkTimeline = QtCore.QTimeLine()
        self.dieTimeline = QtCore.QTimeLine()
        self.animation = QtGui.QGraphicsItemAnimation()
        self.label = Ui_GridLabel("", 0, 0)
        #ini of the animation
    def Initialize(self, maps, units, side0 = 0):
        scene = self.scene()
        self.sizeX = len(maps)*UNIT_WIDTH
        self.sizeY = len(maps[0])*UNIT_HEIGHT
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
        self.soldierAlive = []
        for i in range(len(units)):
            side = 0
            if (i>=side0):
                side = 1
            newSoldierUnit = Ui_SoldierUnit(i, side, units[i])
            scene.addItem(newSoldierUnit)
            self.soldierItem.append(newSoldierUnit)
            self.soldierAlive.append(True)
        self.SetSoldiers(units)
        #initialization of soldier units
        self.cursor = Ui_GridCursor(self.timerId)
        scene.addItem(self.cursor)
        self.setMouseTracking(True)#for test
        #initialization of the cursor

    def SetSoldiers(self, units):
        "set the pos of soldiers"
        alive = map(lambda unit: (unit.life!=0), units)
        for i in range(len(units)):
            if (alive[i]!=self.soldierAlive[i] and alive[i]):
                self.scene().addItem(self.soldierItem[i])
            if (alive[i]!=self.soldierAlive[i] and not alive[i]):
                self.scene().removeItem(self.soldierItem[i])
            self.soldierAlive[i] = alive[i]
            if (self.soldierAlive[i]):
                self.soldierItem[i].setPos(GetPos(units[i].position[0],
                                                  units[i].position[1]))
                self.soldierItem[i].mapX, self.soldierItem[i].mapY = \
                                      units[i].position[0], units[i].position[1]
        print self.soldierAlive#for test

    #animation
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

    #cursor
    def TerminateAnimation(self, units = None):
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
        if (units):
            self.SetSoldiers(units)#?

    #cursor
    def timerEvent(self, event):
        if (event.timerId()==self.cursor.timerId):
            self.cursor.setOpacity(1-self.cursor.opacity()) #make the cursor fricker
        if (self.cursor.isFixed):
            self.cursor.setOpacity(1)
        print self.cursor.opacity()#for test
    def mouseMoveEvent(self, event):
        #bug: not the scene position!
        #bug: need to restrict the cursor in the scene!
        x = int(event.x()/UNIT_WIDTH)
        y = int(event.y()/UNIT_HEIGHT)
        self.cursor.setPos(GetPos(x, y))
        print x, y#for test



class UiD_BeginChanges:
    def __init__(self, beginInfo, cmd, endInfo):
        self.templeRenew = None#

class UiD_EndChanges:
    def __init__(self, begInfo, cmd, endInfo):
        self.idNum = idNum = begInfo.id[0]*len(endInfo.base[0])+begInfo.id[1]
        self.route = fun()#
        self.order = cmd.order
        if (cmd.order==1):
            target = self.target = cmd.target[0]*len(endInfo.base[0])+cmd.target[1]
            begUnits = begInfo.base[0]
            begUnits.extend(begInfo.base[1])
            endUnits = endInfo.base[0]
            endUnits.extend(endInfo.base[1])
            self.damage = (endUnits[idNum].life-begUnits[idNum].life,
                           endUnits[target].life-begUnits[target].life) #(self, enemy)
            self.note = ["", ""]
            for i in (0, 1):
                if (self.damage[i]==0):
                    if (endInfo.attack_effect[i]==1):
                        self.note[i] = "Blocked!"
                    elif (endInfo.attack_effect[i]==0):
                        self.note[i] = "Miss"
            self.fightBack = (endInfo.attack_effect[1]!=-1) and (endUnits.life!=0)
            self.isDead = (endInfo.base[idNum].life==0, endInfo.base[target].life==0)
        elif (cmd.order==2):
            pass#skill

class UiD_RoundInfo:
    "info of every round"
    def __init__(self, begInfo, cmd, endInfo):
        self.begChanges = UiD_BeginChanges(begInfo, cmd, endInfo)
        self.cmdChanges = UiD_EndChanges(begInfo, cmd, endInfo)
        self.begUnits = None #if it is none, there's no changes in the unit info
        self.endUnits = endInfo.base[0]
        self.endUnits.extend(endInfo.base[1])
        self.idNum = begInfo.id[0]*len(endInfo.base[0])+begInfo.id[1]
        self.score = endInfo.score

class UiD_BattleData:
    "info of the entire battle(not completed)"
    def __init__(self, iniInfo, begInfo):
        self.map = iniInfo.map
        self.side0SoldierNum = len(iniInfo.base[0])
        self.iniUnits = iniInfo.base[0]
        self.iniUnits.extend(iniInfo.base[1])
        self.roundInfo = []
        self.nextRoundInfo = begInfo #temporary stores the round_begin_info
        self.result = None#

    #def GetRoundIniData(self, roundNum):
    #def GetRoundCmdData(self, roundNum):
    #def GetMap(self, roundNum):

    #def ChangeRoundInfo(self, roundNum, begUnits):
    #def RoundInfoIsChanged(self, roundNum):



if __name__=="__main__":
    app = QtGui.QApplication(sys.argv)
    scene = QtGui.QGraphicsScene()
    view = Ui_ReplayView(scene)
    view.setBackgroundBrush(QtGui.QColor(255, 255, 255))
    view.Initialize(maps, units, 3)
    view.setWindowTitle("Replay")
    view.show()
    view.MovingAnimation(1, route)#for test
    #view.TerminateAnimation(units)#for test
    #view.AttackingAnimation(0, 3, -20, "Blocked")#for test
    #view.DiedAnimation(0)#for test
    sys.exit(app.exec_())
