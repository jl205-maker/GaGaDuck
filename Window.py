import sys
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow, QDesktopWidget
from PyQt5.QtGui import QMovie, QKeyEvent
from PyQt5.QtCore import Qt, QTimer

from win32api import GetMonitorInfo, MonitorFromPoint

from WindowArea import*

class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_UI()

    def init_UI(self):
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        
        win_area = WindowArea()
        window_height = 600  # Adjust as needed based on the size of the duck animation
        x = 0
        y = 0
        self.setGeometry(x, y, win_area.get_width() + 320, win_area.get_height())
        
    def reset_width(self, width):
        self.setGeometry(self.x(), self.y(), width, self.height())
        