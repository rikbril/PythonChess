def getKeyFromDict(dictionary, location):
    for name in dictionary:
        print(dictionary, location)
        if dictionary[name] == f'"{location}"':
            return name
    return False

