import sys
import hashlib
import json

activity_file = sys.path[1] + "/database/activity.json"
group_file = sys.path[1] + "/database/group.json"
location_file = sys.path[1] + "/database/location.json"
project_file = sys.path[1] + "/database/project.json"
user_file = sys.path[1] + "/database/user.json"
holiday_file = sys.path[1] + "/database/holiday.json"

# Load json utility
def load(path):
    datafile = open(path)
    data = json.load(datafile)
    datafile.close()
    return data

# Write json utility
def write(path, data):
        datafile = open(path, "w")
        json.dump(data,datafile)
        datafile.close()

# Find next index
def next_index(dict):
    i = 1
    while i < len(dict) and i == dict[i]["ID"]:
        i += 1
    return i

def populate_user(username, password, email, name, surname):
    user = dict()
    user["username"] = username
    # Encoding password with a secure one-way encryption algorithm
    user["password"] = hashlib.sha512(password).hexdigest()
    user["email"] = email
    user["name"] = name
    user["surname"] = surname
    user["holiday"] = []
    user["groups"] = [{"ID": 7, "level": "participant"}]
    return user

def setholidays(user, holidays):
    """
    :param user: int
    :param holidays = dictionary
    example: setholidays(1, {"begin":timestamp,"end":timestamp})
    """
    # Load user and holidays data
    found = False
    x = 0
    data_user = load(user_file)
    data_holiday = load(holiday_file)
    holiday_index = next_index(holidays)
    holidays["ID"] = holiday_index
    while (found == False) and (x < len(data_user)):
        if data_user[x]["ID"] == user:
            data_user[x]["holiday"].append(holiday_index)
        x += 1
    write(holiday_file, data_holiday)
    write(user_file, data_user)
    
def add_dict(dictionary, path):
    data = load(path)
    count = next_index(data)
    # Set id index
    dictionary["ID"] = count
    data.append(dictionary)
    write(path, data)

def remove_dict(id, path):
    """
    :param id: int
    :param path: string
    :return:
    """
    file_to_remove = load(path)
    for x in file_to_remove:
        if x["ID"] == id:
           file_to_remove.remove(x)
    write(path, file_to_remove)

def add_group_to_user(group, user, role):
    """
        :param group: int
        :param user: int
        :param role: basestring
        usange: add_group_to_user(1, 5, "partecipant")
    """
    users = load(user_file)
    new_group = dict()
    new_group["ID"] = group
    new_group["level"] = role
    users[user]["groups"].append(new_group)
    write(user_file, user)

def remove_group_from_user(group, user):
    """
    :param group: int
    :param user: int
    :param role: basestring
    usange: remove_group_from_user(1, 5)
    """
    users = load(user_file)
    for x in users[user]["groups"]:
        if x["ID"] == group:
            users[user]["groups"].remove(x)
    write(user_file, users)
