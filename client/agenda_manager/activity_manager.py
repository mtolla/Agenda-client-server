from client.gui.activity_view import *


class ActivityManager:
    def __init__(self):
        pass

    def exec_(self, data):
        self.activity = Activity(data)

        if data['type'] == "group":
            self.activity.extend_to_group()

        self.activity.exec_()
