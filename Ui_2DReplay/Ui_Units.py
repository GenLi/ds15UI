#Ver 0.0 edited at 2013-07-14-1:12

#items needed in replay scene
#grids of map
#soldiers
#cursor

from PyQt4 import QtGui, QtCore



UNIT_WIDTH = 100
UNIT_HEIGHT = 100
PEN_WIDTH = 0.5

class Ui_MapUnit(QtGui.QGraphicsItem):
    "the unit of the map. Generalized."
    def __init__(self, x, y, terrain = None, parent = None):
        "Initialize the flags and position info"
        QtGui.QGraphicsItem.__init__(self, parent)
        self.mapX = x
        self.mapY = y
        #load pixmap
        self.selected = False
        self.coverColor = None

    def boundingRect(self):
        return QtCore.QRectF(0-PEN_WIDTH, 0-PEN_WIDTH,
                             UNIT_WIDTH+PEN_WIDTH, UNIT_HEIGHT+PEN_WIDTH)
        #regard the upleft corner as origin

    def paint(self, painter, option, widget):
        #draw pixmap
        pen = QtGui.QPen()
        pen.setColor(QtGui.QColor(0, 0, 0))
        pen.setStyle(QtCore.Qt.DotLine)
        brush = QtGui.QBrush()
        brush.setColor(QtGui.QColor(255, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        painter.setPen(pen)
        painter.setBrush(brush)
        painter.drawRect(QtCore.QRect(0, 0, UNIT_WIDTH, UNIT_HEIGHT))
        #for test


class Ui_SoldierUnit(QtGui.QGraphicsItem):
    "the unit of the soldiers. Generalized."
    def __init__(self, x, y, soldiertype):
        pass

    def boundingRect(self):
        pass

    def paint(self):
        pass


