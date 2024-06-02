import numpy as np
from PyQt6.QtCore import QObject, pyqtSignal
from PyQt6.QtGui import QPixmap, QImage
from pydub import AudioSegment


class ValueProperty(QObject):
    valueChanged = pyqtSignal(object)

    def __init__(self, initial_value):
        super().__init__()
        self._value = initial_value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        if self._value != new_value:
            self._value = new_value
            self.valueChanged.emit(new_value)
