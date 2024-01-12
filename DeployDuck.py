from re import S
import sys
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow, QDesktopWidget
from PyQt5.QtGui import QMovie, QKeyEvent
from PyQt5.QtCore import Qt, QTimer

import Duck
import Window
from WindowArea import *

class DeployDuck:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.main_window = Window.Window()

        self.duck = Duck.Duck(self.main_window)
        self.main_window.setCentralWidget(self.duck)
        self.main_window.show()
        
        self.duck.enter_scene()

    def run(self):
        sys.exit(self.app.exec_())

if __name__ == "__main__":
    deployDuck = DeployDuck()
    deployDuck.run()
