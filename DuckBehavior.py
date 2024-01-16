import sys
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow, QDesktopWidget, QSizePolicy, QWidget
from PyQt5.QtGui import QFont, QMovie, QKeyEvent
from PyQt5.QtCore import Qt, QTimer

from WindowArea import *

import numpy as np
import random

class DuckBrain ():
    def __init__(self):
        self.prev_actions = [None] * 10
        
    def get_walk_time(self):
        return self.normal_rand(2000, 5000, 8000, 5000)
    
    def get_idle_time(self):
        return self.normal_rand(1000, 9000, 15000, 7000)

    def normal_rand(self, base, peak, max, std_dev):
        while True:
            # Generate a random distance using a normal distribution
            x = int(np.random.normal(peak, std_dev))

            # Check if the distance is within the allowed range
            if base <= x <= max:
                return x
    def choose_dir(self):
        return random.choice([-1, -1, 1, 1, 1])
    
    def make_action(self, action):
        self.prev_actions.pop(0)
        self.prev_actions.append(action)

    def get_next_action(self):
        if self.prev_actions[-1] != "idle":
            self.make_action("idle")
            return "idle"
        elif self.prev_actions[-1] == "idle":
            self.make_action("walk")
            return "walk"