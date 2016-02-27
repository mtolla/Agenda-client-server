import sys
import hashlib
import json

activity_file = sys.path[1] + "/database/.json"
group_file = sys.path[1] + "/database/group.json"
location_file = sys.path[1] + "/database/location.json"
project_file = sys.path[1] + "/database/project.json"
user_file = sys.path[1] + "/database/user.json"


def populate_user(username, password, email, name, surname):
    user = dict()
    user["username"] = username
    # Encoding password with a secure one-way encryption algorithm
    user["password"] = hashlib.sha512(password).hexdigest()
    user["email"] = email
    user["name"] = name
    user["surname"] = surname
    user["holiday"] = []
    return user

def setholidays(user, holidays):
    """
    :type user: int
    :type holidays = dictionary
    example: setholidays(1, {"begin":timestamp,"end":timestamp})
    """
    # Open user file and load data
    datafile = open(user_file)
    data = json.load(datafile)
    datafile.close()
    # Find user ID
    x = i = 0
    found = False
    holidays_list = []
    while (found == False) and (x < len(data)):
        if user == data[x]["ID"]:
            holidays_list = data[x]["holiday"]
            found = True
            # Load last holiday ID
            while i < len(holidays_list) and i == holidays_list[i]["ID"]:
                i += 1
            # Set holiday id
            holidays["ID"] = i
            # Add new holiday
            holidays_list.append(holidays)

        x += 1
        data[x]["holiday"] = holidays_list
        datafile = open(user_file, "w")
        json.dump(data,datafile)
        datafile.close()

def add_dict(dictionary, path):
    id = []
    count = 0
    datafile = open(path)
    data = json.load(datafile)
    datafile.close()

    for x in data:
        id.append(x["ID"])
    id.sort()

    # Calculate last id index
    while count < len(id) and count == id[count]:
        count += 1

    # Set id index
    dictionary["ID"] = count
    data.append(dictionary)

    with open(path, "w") as datafile:
        json.dump(data, datafile)
    datafile.close()
