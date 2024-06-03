import numpy as np
from PyQt6.QtCore import QObject, pyqtSignal
from PyQt6.QtGui import QPixmap, QImage
from pydub import AudioSegment


class ValueProperty(QObject):
    """
    A class representing a value property with a signal for value changes.

    Attributes:
        valueChanged: A pyqtSignal emitted when the value changes.

    Properties:
        value: The current value of the property.

    Methods:
        __init__: Initializes the ValueProperty object.
    """

    valueChanged = pyqtSignal(object)

    def __init__(self, initial_value):
        """
        Initializes the ValueProperty object.

        Args:
            initial_value: The initial value of the property.
        """
        super().__init__()
        self._value = initial_value

    @property
    def value(self):
        """
        Get the current value of the property.

        Returns:
            The current value of the property.
        """
        return self._value

    @value.setter
    def value(self, new_value):
        """
        Set the value of the property and emit the valueChanged signal if the value changes.

        Args:
            new_value: The new value to set.
        """
        if self._value != new_value:
            self._value = new_value
            self.valueChanged.emit(new_value)
