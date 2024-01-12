import sys
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow, QDesktopWidget, QSizePolicy, QWidget
from PyQt5.QtGui import QFont, QMovie, QKeyEvent
from PyQt5.QtCore import Qt, QTimer

from WindowArea import *
        
class Duck(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.win_area = WindowArea()
        self.idle_movie = QMovie("idle.gif")
        self.walk_movie = QMovie("walk.gif")
        self.setMovie(self.idle_movie)
        self.idle_movie.start()
        self.setFocusPolicy(Qt.StrongFocus)  # To accept key events
        self.setFixedSize(320, 320)
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        self.win_area = WindowArea()

        self.speed = 9;
        self.dir = -1;
        #self.move_timer = QTimer(self)
        #self.move_timer.timeout.connect(self.walk)
        
        self.y = self.win_area.get_height() - 320 - 96

    def set_animation(self, state):
        if state == "idle":
            self.setMovie(self.idle_movie)
            self.idle_movie.start()
        elif state == "walk":
            self.setMovie(self.walk_movie)
            self.walk_movie.start()
        #self.adjustSize()
        
    #def walk(self):
        

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_I:
            self.set_animation("idle")
        elif event.key() == Qt.Key_W:
            self.set_animation("walk")

    def mousePressEvent(self, event):
        print("quack")
        
    def enter_scene(self):
        #init_x = self.win_area.get_width() - 500
        #self.move(self.win_area.get_width()-320, self.y)
        self.set_animation("walk")
        self.move(self.win_area.get_width(), self.y)
        self.enter_timer = QTimer(self)
        self.enter_timer.timeout.connect(self.move_to_enter)
        self.enter_timer.start(70)
        #self.move(init_x, self.y)

        
    def move_to_enter(self):
        x = self.x() + (self.speed * self.dir)
        if x < (self.win_area.get_width() - 500):
            self.enter_timer.stop()
            self.set_animation("idle")
        else: self.move(x, self.y)