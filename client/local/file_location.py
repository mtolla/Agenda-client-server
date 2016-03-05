import os

project_path = os.path.dirname(os.path.abspath(__file__))
path = "\\".join(project_path.split("\\")[:-1])

# Icone
ALERT = path + "/gui/icon/alert.png"
INFO = path + "/gui/icon/info.png"
MANAGE_IT = path + "/gui/icon/ManageIT.png"
QUIT = path + "/gui/icon/quit.png"
LOGOUT = path + "/gui/icon/logout.png"
NOTIFICATION = path + "/gui/icon/notifications.png"

# Altro
LOCAL_SAVE = path + "/local/local_save.json"
