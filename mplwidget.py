# ------------------------------------------------------
# -------------------- mplwidget.py --------------------
# ------------------------------------------------------
from PyQt5.QtWidgets import *

from matplotlib.backends.backend_qt5agg import (
    FigureCanvasQTAgg as FigureCanvas,
    NavigationToolbar2QT as NavigationToolbar)

from matplotlib.figure import Figure


class MplWidget(QWidget):

    def __init__(self, parent=None):
        QWidget.__init__(self, parent)

        self.canvas = FigureCanvas(Figure())
        # create a NavigatioToolbar
        self.ntb = NavigationToolbar(self.canvas, self)
        self.vertical_layout = QVBoxLayout()

        self.vertical_layout.addWidget(self.canvas)
        self.vertical_layout.addWidget(self.ntb)
        self.canvas.axes = self.canvas.figure.add_subplot(111)


        self.setLayout(self.vertical_layout)



