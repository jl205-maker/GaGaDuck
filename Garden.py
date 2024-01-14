import sys
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow, QDesktopWidget, QSizePolicy, QWidget
from PyQt5.QtGui import QFont, QMovie, QKeyEvent
from PyQt5.QtCore import Qt, QTimer

from WindowArea import *
        
class Garden(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.win_area = WindowArea()
        self.idle_movie = QMovie("resources\grass_stationary.gif")
        self.entrance_movie = QMovie("resources\grass_entrance.gif")
        self.setMovie(self.idle_movie)
        self.idle_movie.start()
        self.setFixedSize(960, 320)
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        self.win_area = WindowArea()
        
        self.y = self.win_area.get_height() - 320 - self.win_area.get_toolbar_height()
        self.x = self.win_area.get_width() - 960
        
    def enter_scene(self):
        self.move(self.x, self.y)
        self.setMovie(self.entrance_movie)
        self.entrance_movie.start()