# -*- coding: utf-8 -*-
#Ver 0.3 edited at 2013-07-16-0:50
#Changes: some unnecessary contents deleted

#items needed in replay scene
#grids of map
#soldiers
#cursor

from PyQt4 import QtGui, QtCore
from basic import *

TRAP_TRIGGERED = 8



UNIT_WIDTH = 100
UNIT_HEIGHT = 100
PEN_WIDTH = 0.5

def GetPos(mapX, mapY):
    return QtCore.QPointF(mapX*UNIT_WIDTH, mapY*UNIT_HEIGHT)

class Ui_MapUnit(QtGui.QGraphicsItem):
    "the unit of the map. Generalized."
    def __init__(self, x, y, terrain, parent = None):
        "Initialize the flags and position info"
        QtGui.QGraphicsItem.__init__(self, parent)
        self.mapX = x
        self.mapY = y
        self.terrain = terrain
        #load pixmap
        self.selected = False
        self.coverColor = None

    #def GetImage(self, painter, image):
    def GetPainter(self, painter):
        "change the painter according to the terrain, selection state, etc"
        terrainColor = {PLAIN:QtGui.QColor(205, 173, 0), MOUNTAIN:QtGui.QColor(139, 105, 20),
                        FOREST:QtGui.QColor(0, 139, 0), BARRIER:QtGui.QColor(139, 126, 102),
                        TURRET:QtGui.QColor(255, 0, 0), TRAP:QtGui.QColor(139, 0, 0),
                        TEMPLE:QtGui.QColor(0, 0, 139), GEAR:QtGui.QColor(139, 101, 8)}
        brush = QtGui.QBrush()
        brush.setColor(terrainColor[self.terrain])
        brush.setStyle(QtCore.Qt.SolidPattern)
        pen = QtGui.QPen()
        pen.setColor(QtGui.QColor(0, 0, 0))
        pen.setStyle(QtCore.Qt.DotLine)
        painter.setPen(pen)
        painter.setBrush(brush)
        #for test

    def boundingRect(self):
        return QtCore.QRectF(0-PEN_WIDTH, 0-PEN_WIDTH,
                             UNIT_WIDTH+PEN_WIDTH, UNIT_HEIGHT+PEN_WIDTH)
        #regard the upleft corner as origin

    def paint(self, painter, option, widget):
        #draw pixmap
        self.GetPainter(painter)
        painter.drawRect(QtCore.QRect(0, 0, UNIT_WIDTH, UNIT_HEIGHT))
        #for test


class Ui_SoldierUnit(QtGui.QGraphicsItem):
    "the unit of the soldiers. Generalized."
    #def __init__(self, units):
    def __init__(self, x, y, soldiertype, parent = None):
        "initialize the flags and map info"
        QtGui.QGraphicsItem.__init__(self, parent)
        self.mapX = x
        self.mapY = y
        self.type = soldiertype
        self.selected = False

    def SetMapPos(self, x, y):
        self.mapX = x
        self.mapY = y

    def GetPos(self):
        return GetPos(self.mapX, self.mapY)

    def boundingRect(self):
        return QtCore.QRectF(0-PEN_WIDTH, 0-PEN_WIDTH,
                             UNIT_WIDTH+PEN_WIDTH, UNIT_HEIGHT+PEN_WIDTH)
        #regard the upleft corner as origin

    def paint(self, painter, option, widget):
        imageRoute = {SABER:"saber.png",
                     LANCER:"lancer.png",
                     ARCHER:"archer.png",
                     DRAGON_RIDER:"dragonrider.png",
                     WARRIOR:"warrior.png",
                     WIZARD:"wizard.png",
                     HERO_1:"hero1.png"}
        fileRoute = "SoldierImage\\"
        image = QtGui.QImage(fileRoute+imageRoute[self.type])
        painter.setCompositionMode(painter.CompositionMode_Multiply)
        painter.drawImage(QtCore.QRectF(0, 0, UNIT_WIDTH, UNIT_HEIGHT), image)




