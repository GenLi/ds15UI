# -*- coding: utf-8 -*-
#Ver 0.3.1 edited at 2013-07-23-23:56
#Changes: animation, goto func
#Changes: data updates
#Changes: initialize
#need to change: error sended in showstatus func

#replay widget

from Ui_2DReplayScene import *



class Ui_2DReplayWidget(Ui_2DReplayView):
    def __init__(self, scene, parent = None):
        Ui_2DReplayView.__init__(self, scene, parent)
        self.data = None
        self.nowRound = 0
        self.status = BEGIN_FLAG
        self.latestRound = -1
        self.latestStatus = BEGIN_FLAG
        #connecting
        self.animState = 0
    def Initialize(self, iniInfo, begInfo):
        self.data = UiD_BattleData(iniInfo, begInfo)
        Ui_2DReplayView.Initialize(self.data.map, self.data.iniUnits,
                                   self.data.side0SoldierNum)
        self.nowRound = 0
        self.status = BEGIN_FLAG
        self.latestRound = 0
        self.latestStatus = BEGIN_FLAG
        self.ShowStatus()

    def UpdateBeginData(self, begInfo):
        if (self.data.nextRoundInfo!=None):
            pass#error
        self.data.nextRoundInfo = begInfo
        self.latestRound += 1
        self.latestStatus = BEGIN_FLAG
    def UpdateEndData(self, cmd, endInfo):
        if (self.data.nextRoundInfo==None):
            pass#error
        rInfo = UiD_RoundInfo(self.data.nextRoundInfo, cmd, endInfo)
        self.data.roundInfo.append(rInfo)
        self.data.nextRoundInfo = None
        self.latestStatus = END_FLAG

    #def GetGameInfo(self):
    #def GetTerrainInfo(self):
    #def GetSolldierInfo(self):

    def ShowStatus(self):
        self.TerminateAnimation()
        self.animState = 0
        #bug: no change
        if (self.status==BEGIN_FLAG):
            units = self.data.roundInfo[self.nowRound].begUnits
        elif (self.status=="end"):
            units = self.data.roundInfo[self.nowRound].endUnits
        else:
            pass#raise TypeError, "Invalid flag when showing status"
        self.SetSoldier(units)

    def ShowMoveAnimation(self, state = None):
        if (state!=None):
            self.animState = state
        selfId = self.data.roundInfo[self.nowRound].idNum
        targetId = self.data.roundInfo[self.nowRound].cmdChanges.target
        move = self.data.roundInfo[self.nowRound].cmdChanges
        if (self.animState==0):
            self.MovingAnimation(selfId, move.route)
            self.animState = AFTER_MOVING
        elif (self.animState==AFTER_MOVING):
            pass#terrain change
            self.animState = AFTER_TERRAIN_CHANGE
        elif (self.animState==AFTER_TERRAIN_CHANGE):
            self.AttackingAnimation(selfId, targetId, move.damage[1], move.note[0])
            self.animState = AFTER_ATTACK
        elif (self.animState==AFTER_ATTACK):
            if (move.isDead[1]):
                self.DieAnimation(self, targetId)
            elif (move.fightBack):
                self.AttackingAnimation(targetId, selfId, move.damage[0], move.note[1])
            self.animState = AFTER_FIGHTING_BACK
        elif (self.animState==AFTER_FIGHTING_BACK and move.isDead[0]):
            self.DieAnimation(selfId)
            self.animState = END_STATE
        else:
            #after animation
            self.TerminateAnimation()
            self.animState = 0

    #def ShowBeginAnimation(self):

    #def Play(self, r = None, flag = None):
    def Play(self, flag = None):
        pass
    def GoToRound(self, r = None, flag = None):
        "stop the animation and set the round state"
        #Q: what if the round r hasn't been updated?
        if (flag!=None):
            self.status = flag
        if (r!=None):
            self.nowRound = r
        #self.ShowMoveAnimation(PAUSE_STATE)#no need
        self.ShowStatus()

    BEGIN_FLAG = 0
    END_FLAG = 1
    #flags showing the round state(at the beginning or the end)
    BEGIN_STATE = 0
    AFTER_MOVING = 1
    AFTER_TERRAIN_CHANGE = 2
    AFTER_ATTACK = 3
    AFTER_FIGHTING_BACK = 4
    PAUSE_STATE = 5
    END_STATE = 6
    #flags showing the state of the animation
    moveAnimEnd = QtCore.pyqtSignal(int)
    begAnimEnd = QtCore.pyqtSignal(int)
    #signals of animation
  #  unitSelected = QtCore.pyqtSignal(Map_Basic)
#    mapGridSelected = QtCore.pyqtSignal(Base_Unit)
    #signals for info display
    
