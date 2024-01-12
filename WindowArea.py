from win32api import GetMonitorInfo, MonitorFromPoint
from PyQt5.QtWidgets import QDesktopWidget
#Further improvements: implement height calculation based on available
#art sizes and screen size.

class WindowArea():
    def __init__(self):
        monitor_info = GetMonitorInfo(MonitorFromPoint((0,0)))
        monitor_area = monitor_info.get("Monitor")
        work_area = monitor_info.get("Work")
        screen_geo = QDesktopWidget().screenGeometry()
        self.screen_height = screen_geo.height()
        self.screen_width = screen_geo.width()
        self.toolbar_height = monitor_area[3] - work_area[3]
        
    def get_height(self):
        return self.screen_height
    def get_width(self):
        return self.screen_width
    def get_toolbar_height(self):
        return self.toolbar_height