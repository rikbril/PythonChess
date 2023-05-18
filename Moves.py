def getKeyFromDict(dictionary, value):
    for key in dictionary:
        if key == value:
            return dictionary[key]
    return False

def getLocationFromName(dict, value):
    for key in dict:
        if key == value:
            return dict[key].currentLocation
    

def calculatePossibleMoves():
    pass