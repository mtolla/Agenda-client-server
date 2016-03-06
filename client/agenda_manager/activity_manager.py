from client.gui.activity_view import *


class ActivityManager:
    def __init__(self):
        pass

    def exec_(self, data):
        self.activity = Activity(data)

        if data['type'] != "single":
            self.activity.extend()

        self.activity.add_buttons()

        if data['modality'] == "view":
            self.activity.set_enabled_view(False)

            if data['type'] != "single":
                self.activity.checked_participants()

        self.activity.exec_()
