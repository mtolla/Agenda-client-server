import sys
import os

project_path = os.path.dirname(os.path.abspath(__file__) )
sys.path.append(project_path)

from client.login_manager import *


app = QtGui.QApplication(sys.argv)
a = LoginManager()
a.exec_()
sys.exit(app.exec_())
