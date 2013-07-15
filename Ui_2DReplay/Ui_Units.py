#回放界面、地图编辑器界面场景所需图元
#地图格点：
#单位：
#光标：

from PyQt4 import QtGui, QtCore



UNIT_WIDTH = 50
UNIT_HEIGHT = 50
PEN_WIDTH = 0.5

class Ui_MapUnit(QtGui.QGraphicsItem):
    "the unit of the map. Generalized."
    def __init__(self, x, y, terrain):
        "Initialize the flags and position info"
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
        pen.setStyle(Qt.DotLine)
        brush = QtGui.QBrush()
        brush.setColor(QtGui.QColor(255, 0, 0))
        brush.setStyle(Qt.SolidPattern)
        painter.setPen(pen)
        painter.setBrush(brush)
        painter.drawRect()
        #for test


class Ui_SoldierUnit(QtGuiQGraphicsItem):
    "the unit of the soldiers. Generalized."
    def __init__(self, x, y, soldiertype):
        pass

    def boundingRect(self):
        pass

    def paint(self):
        pass


