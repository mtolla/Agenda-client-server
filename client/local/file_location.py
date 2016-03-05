import os

project_path = os.path.dirname(os.path.abspath(__file__))
print "Il tuo file si trova qui: " + project_path
path = "/".join(project_path.split("\\")[:-1])
print "l'ALERT si trova in: " + project_path + "/../gui/icon/alert.png"
print "Local save si trova qui: " + project_path + "/local_save.json"

# Icone
ALERT = project_path + "/../gui/icon/alert.png"
INFO = project_path + "/../gui/icon/info.png"
MANAGE_IT = project_path + "/../gui/icon/ManageIT.png"
QUIT = project_path + "/../gui/icon/quit.png"
LOGOUT = project_path + "/../gui/icon/logout.png"
NOTIFICATION = project_path + "/../gui/icon/notifications.png"

# Altro
LOCAL_SAVE = project_path + "/local_save.json"
