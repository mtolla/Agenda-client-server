import sys
import os

project_path = os.path.dirname(os.path.abspath(__file__) )
sys.path.append(project_path)

from utils.createUser import *


app = QtGui.QApplication(sys.argv)
a = CreateUser()
a.show()
sys.exit(app.exec_())
