import os

project_path = os.path.dirname(os.path.abspath(__file__))
path = "/".join(project_path.split("\\")[:-1])


# Db File
USER = project_path + '/../database/user.json'
PROJECT = project_path + '/../database/project.json'
LOCATION = project_path + '/../database/location.json'
GROUP = project_path + '/../database/group.json'
ACTIVITY =  project_path + '/../database/activity.json'
HOLIDAY = project_path + '/../database/holiday.json'

