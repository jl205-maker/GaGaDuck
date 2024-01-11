import sys
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow, QDesktopWidget
from PyQt5.QtGui import QFont, QMovie, QKeyEvent
from PyQt5.QtCore import Qt, QTimer

from win32api import GetMonitorInfo, MonitorFromPoint

class AnimatedDuckWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set window flags for a frameless, transparent window
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        self.setFixedWidth(1000)
        self.setFixedHeight(1000)

        # Create a label to display the animation
        self.label = QLabel(self)
        self.label.mousePressEvent = self.duck_clicked
        self.label.move(1000-460, 1000-320)

        self.quackLabel = QLabel("QUACK!!", self)
        font = QFont()
        font.setCapitalization(True)
        font.setPointSize(12)
        self.quackLabel.setFont(font)
        self.quackLabel.setStyleSheet("color: white")
        self.quackLabel.setFixedSize(100, 500)
        self.quackLabel.setHidden(True)
        
        # Load animations
        self.idle_movie = QMovie("idle.gif")
        self.walk_movie = QMovie("walk.gif")

        # Timer for moving the duck
        self.move_timer = QTimer(self)
        self.move_timer.timeout.connect(self.move_duck)
        self.duck_speed = 5
        self.duck_direction = 1  # 1 for right, -1 for left

        # Start with the idle animation
        self.set_animation("idle")

        # Position the window at the bottom of the screen
        self.position_window_at_bottom()

        # Show the window
        self.show()

    def position_window_at_bottom(self):
        """Position the window at the bottom of the screen."""
        monitor_info = GetMonitorInfo(MonitorFromPoint((0,0)))
        monitor_area = monitor_info.get("Monitor")
        work_area = monitor_info.get("Work")
        screen_geometry = QDesktopWidget().screenGeometry()
        window_height = 320  # Adjust as needed based on the size of the duck animation
        x = screen_geometry.width() - self.width()
        y = screen_geometry.height() - self.height() - (monitor_area[3]-work_area[3])
        self.setGeometry(x, y, self.width(), window_height)

    def set_animation(self, state):
        """Set the animation based on the state."""
        if state == "idle":
            self.label.setMovie(self.idle_movie)
            self.idle_movie.start()
            self.move_timer.stop()
        elif state == "walk":
            self.label.setMovie(self.walk_movie)
            self.walk_movie.start()
            self.move_timer.start(50)  # Update position every 50ms

        self.label.adjustSize()

    def move_duck(self):
        """Move the duck across the screen."""
        x = self.label.x() + (self.duck_speed * self.duck_direction)
        if x < 0 or x + self.label.width() > self.width():
            # Change direction if the duck reaches the edge of the window
            self.duck_direction *= -1
            x = self.label.x() + (self.duck_speed * self.duck_direction)

        self.label.move(x, self.label.y())

    def keyPressEvent(self, event: QKeyEvent):
        """Handle key press events to change the state."""
        if event.key() == Qt.Key_I:
            self.set_animation("idle")
        elif event.key() == Qt.Key_W:
            self.set_animation("walk")

    def duck_clicked(self, event):
        """Handle mouse click event on the duck."""
        self.quackLabel.move(self.label.x() - 50, self.label.y() - 200)
        self.quackLabel.show()
        QTimer.singleShot(1000, self.duck_unclick)
        
    def duck_unclick(self):
        self.quackLabel.setHidden(True)

# Run the application
if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = AnimatedDuckWindow()
    #hwnd = ctypes.windll.kernel32.GetConsoleWindow()  
    #print(hwnd)
    #if hwnd != 0:      
        #ctypes.windll.user32.ShowWindow(hwnd, 0)      
        #ctypes.windll.kernel32.CloseHandle(hwnd)
        #_, pid = win32process.GetWindowThreadProcessId(hwnd)
        #os.system('taskkill /PID ' + str(pid) + ' /f')
    sys.exit(app.exec_())