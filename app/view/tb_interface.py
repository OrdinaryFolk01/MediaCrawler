# coding:utf-8
from PyQt6.QtWidgets import QFrame


class TbInterface(QFrame):
    """Text interface"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("tbInterface")
