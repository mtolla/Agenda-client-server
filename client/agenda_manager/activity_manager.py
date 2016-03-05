from client.gui.activity_view import *


class ActivityManager:
    def __init__(self):
        pass

    def exec_(self, informations=False):
        if informations:
            pass
        else:
            self.activity = Activity()
            self.activity.exec_()
