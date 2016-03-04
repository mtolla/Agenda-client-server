import os

project_path = os.path.dirname(os.path.abspath(__file__))
path = "\\".join(project_path.split("\\")[:-2])

# Icone
ALERT = path + "/client/gui/icon/alert.png"
INFO = path + "/client/gui/icon/info.png"
MANAGE_IT = path + "/client/gui/icon/ManageIT.png"
QUIT = path + "/client/gui/icon/quit.png"
LOGOUT = path + "/client/gui/icon/logout.png"
NOTIFICATION = path + "/client/gui/icon/notifications.png"

# Altro
LOCAL_SAVE = path + "/client/local/local_save.json"
