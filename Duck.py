from os import walk
import sys
import typing
from PyQt5 import QtGui
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow, QDesktopWidget, QSizePolicy, QWidget
from PyQt5.QtGui import QFont, QMovie, QKeyEvent, QCursor
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtCore import Qt, QTimer, QUrl

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
        self.lift_l_movie = QMovie("resources\lift_l.gif")
        self.lift_r_movie = QMovie("resources\lift_r.gif")
        self.quack_l_movie = QMovie("resources\quack_l.gif")
        self.quack_r_movie = QMovie("resources\quack_r.gif")
        self.setFocusPolicy(Qt.StrongFocus)  # To accept key events
        self.player = QMediaPlayer()
        self.player.setVolume(100)

        # setup for component sizes and timing
        self.win_area = WindowArea()
        self.m = self.win_area.get_sprite_multiplier()
        # the base size this particular sprite was made in
        self.sprite_base = 64
        # the base frequency at which the animations move in ms
        self.freq_base = 70
        self.setFixedSize(self.sprite_base * self.m, self.sprite_base * self.m)
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        
        # the brain is used to calculate probability and activity
        self.brain = DuckBrain()

        # setup for basic duck movement
        self.speed = 1
        self.dir = -1
        self.move_timer = QTimer(self)
        self.move_timer.timeout.connect(self.move_duck)
        self.action_timer = QTimer(self)
        self.action_timer.timeout.connect(self.change_action)
        
        # setup for drag and drop of the duck
        self.drag = False
        self.click_timer = QTimer(self)
        self.click_timer.setSingleShot(True)
        self.click_timer.timeout.connect(self.enable_drag)
        self.fall_timer = QTimer(self)
        self.fall_timer.timeout.connect(self.fall)
        
        self.y_base = self.win_area.get_height() - self.width() - self.win_area.get_toolbar_height()

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
        elif state == "lift":
            if self.dir == -1:
                self.setMovie(self.lift_l_movie)
                self.lift_l_movie.start()
            elif self.dir == 1:
                self.setMovie(self.lift_r_movie)
                self.lift_r_movie.start()
        elif state == "quack":
            if self.dir == -1:
                self.setMovie(self.quack_l_movie)
                self.quack_l_movie.start()
            elif self.dir == 1:
                self.setMovie(self.quack_r_movie)
                self.quack_r_movie.start()
        
    def mousePressEvent(self, event):
        self.action_timer.stop()
        self.move_timer.stop()
        self.enter_timer.stop()
        self.click_timer.start(300)
        
    def mouseMoveEvent(self, event):
        if self.drag == True:
            mouse_loc = QCursor.pos()
            self.move(mouse_loc.x() - self.width()//2, 
                      mouse_loc.y() - self.height()*2//3)
                
    def mouseReleaseEvent(self, event):
        if self.click_timer.isActive():
            self.click_timer.stop()
            self.quack()
        else:
            self.drag = False
            self.fall_timer.start(7)
                
    def enable_drag(self):
        self.set_animation("lift")
        self.drag = True    

    def idle(self):
        idle_time = self.brain.get_idle_time()
        self.set_animation("idle")
        self.action_timer.start(idle_time)

    def walk(self):
        walk_time = self.brain.get_walk_time()
        self.dir *= self.brain.choose_dir()
        self.set_animation("walk")
        self.action_timer.start(walk_time)
        self.move_timer.start(self.freq_base//10)
        
    def move_duck(self):
        x = self.x() + (self.speed * self.dir)
        if x < 0 or x + self.width() > self.win_area.get_width():
            # Change direction if the duck reaches the edge of the window
            self.dir *= -1
            x = self.x() + (self.speed * self.dir)
            self.set_animation("walk")
        self.move(x, self.y_base)
        
    def quack(self):
        self.set_animation("quack")
        self.player.setMedia(QMediaContent(QUrl.fromLocalFile("resources\quack_sound.mp3")))
        self.player.play()
        self.action_timer.start(420)

    def fall(self):
        self.set_animation("idle")
        y = self.y() + 10
        if y > self.y_base:
            y = self.y_base
            self.move(self.x(), y)
            self.fall_timer.stop()
            self.brain.make_action("idle")
            self.idle()
            return
        self.move(self.x(), y)

    def enter_scene(self):
        self.move(self.win_area.get_width(), self.y_base)
        self.brain.make_action("walk")
        self.set_animation("walk")
        self.action_timer.start(5500)
        self.enter_timer = QTimer(self)
        self.enter_timer.timeout.connect(self.move_to_enter)
        self.enter_timer.start(self.freq_base//10)
        
    def move_to_enter(self):
        x = self.x() + (self.speed * self.dir)
        self.move(x, self.y_base)