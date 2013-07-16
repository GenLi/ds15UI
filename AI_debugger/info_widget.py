from PyQt4.QtGui import *
from PyQt4.QtCore import *

class InfoWidget(QWidget):
    def __init__(self, parent = None):
        super(InfoWidget, self).__init__(parent)

        self.label_aifile = QLabel("AI file path:")
        self.info_aifile = QLabel("")
        self.label_mapfile = QLabel("MAP file path:")
        self.info_mapfile = QLabel("")
        self.label_round = QLabel("current round:")
        self.info_round = QLabel("")
        self.label_unit = QLabel("current aciton_unit:")
        self.info_unit = QLabel("")
        self.label_time = QLabel("time used:")
        self.info_time = QLabel("")
        self.label_order = QLabel("order:")
        self.info_order = QLabel("")

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
        self.layout.addWidget(self.info_unit, 4, 1)
        self.layout.addWidget(self.label_order, 5, 0)
        self.layout.addWidget(self.info_order, 5, 1)

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
    def setOrderinfo(self, str):
        self.info_order.setText(str)

    #reimplement close event:just set invisible
    def closeEvent(self, event):
        self.setVisible(False)
        event.ignore()
