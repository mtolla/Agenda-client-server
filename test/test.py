import unittest
import sys
from client.gui.login_view import *


class MyTestCase(unittest.TestCase):
    def test_login(self):
        app = QtGui.QApplication(sys.argv)
        login = Login()
        login.show()
        self.assertEqual(0, app.exec_())


if __name__ == '__main__':
    unittest.main()
