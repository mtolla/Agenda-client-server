import sys
import hashlib
import json

activity_file = sys.path[1] + "/database/activity.json"
group_file = sys.path[1] + "/database/group.json"
location_file = sys.path[1] + "/database/location.json"
project_file = sys.path[1] + "/database/project.json"
user_file = sys.path[1] + "/database/user.json"

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
    i = 0
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
    return user

def setholidays(user, holidays):
    """
    :type user: int
    :type holidays = dictionary
    example: setholidays(1, {"begin":timestamp,"end":timestamp})
    """
    # Load user data
    data = load(user_file)
    # Find user ID
    x = 0
    found = False
    holidays_list = []
    while (found == False) and (x < len(data)):
        if user == data[x]["ID"]:
            holidays_list = data[x]["holiday"]
            found = True
            # Set holiday id
            holidays["ID"] = next_index(holidays_list)
            # Add new holiday
            holidays_list.append(holidays)

        x += 1
        data[x]["holiday"] = holidays_list
        # Write user data
        write(user_file, data)

def add_dict(dictionary, path):
    id = []
    count = 0
    data = load(path)
    '''for x in data:
        id.append(x["ID"])
    id.sort()

    # Calculate last id index
    while count < len(id) and count == id[count]:
        count += 1
    '''
    count = next_index(data)
    # Set id index
    dictionary["ID"] = count
    data.append(dictionary)
    write(path, data)

def add_group_to_user(group, user, role):
    """
        :type group: int
        :type user: int
        :type role: basestring
        usange: add_user_to_group(1, 5, "partecipant")
    """
    users = load(user_file)
    new_group = dict()
    new_group["ID"] = group
    new_group["level"] = role
    users[user]["groups"].append(new_group)
