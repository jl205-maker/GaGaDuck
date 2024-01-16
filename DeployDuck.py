from re import S
import sys
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow, QDesktopWidget, QWidget
from PyQt5.QtGui import QMovie, QKeyEvent
from PyQt5.QtCore import Qt, QTimer, QUrl

import Duck
import Window
from WindowArea import *
import Garden

class DeployDuck:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.main_window = Window.Window()
        
        self.central_widget = QWidget()
        self.main_window.setCentralWidget(self.central_widget)

        self.garden = Garden.Garden(self.central_widget)

        self.duck = Duck.Duck(self.central_widget)
        self.main_window.show()
        
        self.garden.enter_scene()
        self.duck.enter_scene()

    def run(self):
        sys.exit(self.app.exec_())

if __name__ == "__main__":
    deployDuck = DeployDuck()
    deployDuck.run()
