#Ver 0.0 edited at 2013-07-14-1:12

#scene, view of replay

#from logic import *
from Ui_Units import *
import sys



class Ui_ReplayView(QtGui.QGraphicsView):
    "the replay graphic view"
    #def __init__(self, scene, maps, units, parent = None):
    def __init__(self, scene, mapSizeX, mapSizeY):
        QtGui.QGraphicsView.__init__(self, scene)
        self.mapItem = []
        for i in range(mapSizeX):
            newColumn = []
            for j in range(mapSizeY):
                newMapUnit = Ui_MapUnit(i, j)
                scene.addItem(newMapUnit)
                newColumn.append(newMapUnit)
            self.mapItem.append(newColumn)

        for i in range(mapSizeX):
            for j in range(mapSizeY):
                self.mapItem[i][j].setPos(QtCore.QPointF(i*UNIT_WIDTH, j*UNIT_HEIGHT))



if __name__=="__main__":
    app = QtGui.QApplication(sys.argv)
    scene = QtGui.QGraphicsScene()
    view = Ui_ReplayView(scene, 10, 10)
    view.setBackgroundBrush(QtGui.QColor(255, 255, 255))
    view.setWindowTitle("Replay")
    view.show()
    sys.exit(app.exec_())
