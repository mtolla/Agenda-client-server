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
