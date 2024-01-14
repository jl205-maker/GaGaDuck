from os import walk
import sys
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow, QDesktopWidget, QSizePolicy, QWidget
from PyQt5.QtGui import QFont, QMovie, QKeyEvent
from PyQt5.QtCore import Qt, QTimer

from WindowArea import *
from DuckBehavior import *
        
class Duck(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.win_area = WindowArea()
        self.idle_l_movie = QMovie("resources\idle_l.gif")
        self.idle_r_movie = QMovie("resources\idle_r.gif")
        self.walk_l_movie = QMovie("resources\walk_l.gif")
        self.walk_r_movie = QMovie("resources\walk_r.gif")
        self.setFocusPolicy(Qt.StrongFocus)  # To accept key events
        self.setFixedSize(320, 320)
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        self.win_area = WindowArea()
        
        self.brain = DuckBrain()

        self.speed = 9
        self.dir = -1
        self.move_timer = QTimer(self)
        self.move_timer.timeout.connect(self.move_duck)
        self.action_timer = QTimer(self)
        self.action_timer.timeout.connect(self.change_action)
        
        self.y = self.win_area.get_height() - 320 - 96

        self.set_animation("idle")

    def change_action(self):
        self.move_timer.stop()
        self.action_timer.stop()
        self.enter_timer.stop()
        action = self.brain.get_next_action()
        if action == "walk": self.walk()
        elif action == "idle": self.idle()

    def set_animation(self, state):
        if state == "idle":
            if self.dir == -1:
                self.setMovie(self.idle_l_movie)
                self.idle_l_movie.start()
            elif self.dir == 1:
                self.setMovie(self.idle_r_movie)
                self.idle_r_movie.start()
        elif state == "walk":
            if self.dir == -1:
                self.setMovie(self.walk_l_movie)
                self.walk_l_movie.start()
            elif self.dir == 1:
                self.setMovie(self.walk_r_movie)
                self.walk_r_movie.start()
        
    def idle(self):
        idle_time = self.brain.get_idle_time()
        self.set_animation("idle")
        self.action_timer.start(idle_time)

    def walk(self):
        walk_time = self.brain.get_walk_time()
        self.dir *= self.brain.choose_dir()
        self.set_animation("walk")
        self.action_timer.start(walk_time)
        self.move_timer.start(70)
        
    def move_duck(self):
        x = self.x() + (self.speed * self.dir)
        if x < 0 or x + self.width() > self.win_area.get_width():
            # Change direction if the duck reaches the edge of the window
            self.dir *= -1
            x = self.x() + (self.speed * self.dir)
            self.set_animation("walk")
        self.move(x, self.y)

    def mousePressEvent(self, event):
        print("quack")
        
    def enter_scene(self):
        self.move(self.win_area.get_width(), self.y)
        self.brain.make_action("walk")
        self.set_animation("walk")
        self.action_timer.start(5500)
        self.enter_timer = QTimer(self)
        self.enter_timer.timeout.connect(self.move_to_enter)
        self.enter_timer.start(70)
        
    def move_to_enter(self):
        x = self.x() + (self.speed * self.dir)
        self.move(x, self.y)