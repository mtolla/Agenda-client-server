# -*- coding: utf-8 -*-
import unittest
import sys
from client.gui.login_view import *
# Librerie Tia
from server.api import Api
from server.loginManager import ClassLoginManager
from server.dbManager import ClassDbManager
import time


class MyTestCase(unittest.TestCase):
    def test_login(self):
        """
        app = QtGui.QApplication(sys.argv)
        login = Login()
        login.show()
        self.assertEqual(0, app.exec_())
        """

    def test_server(self):
        api = Api()

        ###########################################################################
        # Test api
        # Login usr,psw
        login_app = api.do_login("carluca",
                                           "68c58ddae9e0cde89cf6a0589644b7fb85bc7cec4c9a00e1a52512f9a06c20c4d376a9d1e124fab52da153c13ada4b95282c7756bc747a72fa734676a4eca746",
                                           "127.0.0.2:5005")
        if login_app:
            print("Login OK")
        else:
            print("Login ERROR")
        # Login Token
        if api.do_login_token(login_app, "127.0.0.5:1592"):
            print("Login Token OK")
        else:
            print("Login Token ERROR")
        # Check Token
        if api.check_token(login_app[0], "127.0.0.5:1592"):
            print("Check Token OK")
        else:
            print("Check Token ERROR")
        """
        # Life Token, già testato, non serve più
        time.sleep(6)
        api.check_life_token(api.time_now())
        if not api.check_token(login_app, "127.0.0.5:1592"):
            print("Check Life Token Eliminato")
        else:
            print("Check Life Token ERROR")
        """
        # Delete Token
        login_app = api.do_login("carluca",
                                           "68c58ddae9e0cde89cf6a0589644b7fb85bc7cec4c9a00e1a52512f9a06c20c4d376a9d1e124fab52da153c13ada4b95282c7756bc747a72fa734676a4eca746",
                                           "127.0.0.5:1592")
        api.delete_token(False, login_app)
        if not api.check_token(login_app, "127.0.0.5:1592"):
            print("Delete Token OK")
        else:
            print("Delete Token ERROR")
        """
        # Delete Token da login
        login_app = api.do_login("carluca",
                                           "68c58ddae9e0cde89cf6a0589644b7fb85bc7cec4c9a00e1a52512f9a06c20c4d376a9d1e124fab52da153c13ada4b95282c7756bc747a72fa734676a4eca746",
                                           "127.0.0.5:1592")
        check1 = api.check_token(login_app, "127.0.0.5:1592")
        time.sleep(2)
        """
        login_app2 = api.do_login("carluca",
                                            "68c58ddae9e0cde89cf6a0589644b7fb85bc7cec4c9a00e1a52512f9a06c20c4d376a9d1e124fab52da153c13ada4b95282c7756bc747a72fa734676a4eca746",
                                            "127.0.0.5:1592")
        """
        check2 = api.check_token(login_app2, "127.0.0.5:1592")
        if check1 and check2 and not api.check_token(login_app, "127.0.0.5:1592"):
            print("Delete Token da Login OK")
        else:
            print("Delete Token da Login ERROR")
        """
        # From token get id
        if api.from_token_get_user(login_app2[0]) == 'carluca':
            print ("Get Token From Id OK")
        else:
            print ("Get Token From Id ERROR")

        # get_activity_from_id_act
        app = api.get_activity_from_id_act(0)
        if app:
            print ("get_activity_from_id_act OK: ")
            # print (app)
        else:
            print ("get_activity_from_id_act ERROR")

        # get_participants_from_group
        app = api.get_participants_from_group(0)
        if app:
            print ("get_participants_from_group OK: ")
            # print (app)
        else:
            print ("get_participants_from_group ERROR")

        # get_name_from_id_projects
        app = api.get_name_from_id_projects([0])
        if app:
            print ("get_name_from_id_projects OK: ")
            # print (app)
        else:
            print ("get_name_from_id_projects ERROR")

            # get_proj_from_id_proj
        app = api.get_proj_from_id_proj(0)
        if app:
            print ("get_proj_from_id_proj OK: ")
            # print (app)
        else:
            print ("get_proj_from_id_proj ERROR")

            # get_pjmanager_email
        app = api.get_pjmanager_email(0)
        if app:
            print ("get_pjmanager_email OK: ")
            # print app
        else:
            print ("get_pjmanager_email ERROR")

            # is_teamleader
        app = api.is_teamleader(1)
        if app:
            print ("is_teamleader OK: ")
            # print (app)
        else:
            print ("is_teamleader ERROR")

            # get_activities_from_proj
        app = api.get_activities_from_proj(0)
        if app:
            print ("get_activities_from_proj OK: ")
            # print (app)
        else:
            print ("get_activities_from_proj ERROR")

            # get_activities_from_id_act
        app = api.get_activity_from_id_act(0)
        if app:
            print ("get_activity_from_id_act OK: ")
            # print (app)
        else:
            print ("get_activity_from_id_act ERROR")

        # get_holidays_from_proj
        app = api.get_holidays_from_proj(0)
        if app:
            print ("get_holidays_from_proj OK")
        else:
            print ("get_holidays_from_proj ERROR")

        # get_group_name_from_group
        app = api.get_group_name_from_group(0)
        if app:
            print ("get_group_name_from_group OK")
        else:
            print ("get_group_name_from_group ERROR")

        # get_proj_from_user
        app = api.get_proj_from_user(1)
        if app:
            print ("get_proj_from_user OK")
        else:
            print ("get_proj_from_user ERROR")

            ###########################################################################


if __name__ == '__main__':
    unittest.main()
