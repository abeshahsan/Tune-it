import matplotlib
from matplotlib.figure import Figure
import numpy as np

from scipy.stats import norm

matplotlib.use('QtAgg')

from PyQt6 import QtCore, QtGui
from PyQt6.QtWidgets import *
from matplotlib.backends.backend_qtagg import FigureCanvas
from matplotlib.backends.backend_qtagg import NavigationToolbar2QT
class MplWidget(QWidget):
    def __init__(self, parent = None):

        QWidget.__init__(self, parent)
        
        self.canvas = FigureCanvas(Figure())
        
        vertical_layout = QVBoxLayout()
        vertical_layout.addWidget(self.canvas)
        
        self.canvas.axes = self.canvas.figure.add_subplot(111)
        self.setLayout(vertical_layout)


