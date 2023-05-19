def locationToColour(dict, value):
    for item in dict:
        if [*dict[item].location] == value:
            return dict[item].is_white
    return None

def getLocationFromName(dict, value):
    """unnesesary function, though i needed this function to acces class values from a memory location.
       However, this can be done directly. will remove this function in the next commit

    Args:
        dict (_type_): _description_
        value (_type_): _description_

    Returns:
        _type_: _description_
    """
    for key in dict:
        if key == value:
            return dict[key].currentLocation
    
def calculatePossibleMoves(dict, piece):
    """Takes in a piece and calculates to which places the piece can move, and which locations are pinned by this piece. 
    in order to keep track of attack/defend vectors (i presume, i dont play chess)

    This function uses 2 child functions: 
     - directionsWithLocations: returns a nested array of all the places the piece can move to
     - directionCounter: takes in the nested array which is provided by directionsWithLocations and per direction looks
     at which pieces it encounters.

    Args:
        dict (dict): Dictionary of all the chess pieces and their memory adress of their class instance
        piece (dict[key]): The name of the piece which is going to be used to calculate their possible moves.

    Returns:
        nested array: a nested array for each direction with the corresponding locations as steps.
        Both for the possible movements of the piece and which pieces are pinned down.
    """

    single_move = dict[piece].single_move
    is_white = dict[piece].is_white
    row, column = dict[piece].location

    directions_with_locations = directionsWithLocations(dict, piece, single_move, row, column)

    if "Pawn" not in piece:
        dict[piece].movement, dict[piece].pinned = directionCounter(dict, is_white, directions_with_locations)
    else:
        dict[piece].movement, dict[piece].pinned = directionCounterForPawns(dict, is_white, directions_with_locations, column)
    
def directionCounterForPawns(dict, is_white, directions_with_locations, column, enpassant_location=False):
    """takes in the theoretical movement data and transforms into possible movement or attack vectors for pawns

    Args:
        dict (dict): dictionary of all the chess pieces
        is_white (bool): if the piece is white
        directions_with_locations (nested list): list of all the locations the pawns can move to
        enpassant_location (bool, optional): temp value for later implentation of the enpassant rule. Defaults to False.

    Returns:
        2 nested lists: 1 list for all the regular moves and a list for all the attack moves
    """
    
    movement_result = []
    pinned_result = []
    
    for direction in directions_with_locations:
        path_blocked = False
        for step in direction:
            encounter_color = locationToColour(dict, step)
            if encounter_color == None and path_blocked == False:
                if step[1] == column:
                    movement_result.append(step)
            elif encounter_color != is_white or step == enpassant_location:
                if step[1] != column:
                    pinned_result.append(step)
                else:
                    path_blocked = True

    return movement_result, pinned_result

def directionCounter(dict, is_white, directions_with_locations):
    """ Takes in a nested array of each direction a piece can move into and the location of the steps in each direction
    Args:
        dict (dict): dictionary of all the pieces
        is_white (bool): color of the piece
        directions_with_locations (nested array): array of each direction the piece may move to.
        an array of all the steps in a direction is nested within

    Returns:
        nested array: a nested array for each direction with the corresponding locations as steps.
        Both for the possible movements of the piece and which pieces are pinned down.
    """

    movement_result = []
    pinned_result = []
    for direction in directions_with_locations:
        direction_movement_result = []
        direction_pinned_result = []
        encounter = 2
        for step in direction:
            previous_encounter = encounter
            encounter_color = locationToColour(dict, step)
            if encounter_color == None:
                pass
            elif encounter_color == is_white:
                encounter -= 2
            else:
                encounter -= 1

            if encounter == 2:
                direction_movement_result.append(step)
            if encounter >= 0 and previous_encounter > 1:
                direction_pinned_result.append(step)

            if encounter <= 0:
                break
        movement_result.append(direction_movement_result)
        pinned_result.append(direction_pinned_result)
    return movement_result, pinned_result

def directionsWithLocations(dict, piece, single_move, row, column):
    """transforms a list which contains all the directions a piece can move into a nested array of all the steps, per direction

    Args:
        dict (dict): dictionary of all the pieces
        piece (dict[key]): name of the piece
        single_move (bool): Breaks the direction loop if the piece can only move 1 spot
        row (int): DF row of the piece
        column (int): DF column of the piece

    Returns:
        _type_: _description_
    """
    
    movement_directions = dict[piece].move_directions
    result = []

    for direction in movement_directions:
        step_counter = 1
        rowAdjuster, columnAdjuster = direction
        directionResult = []
        while True:
            adjustedRow = row + (rowAdjuster * step_counter)
            adjustedColumn = column + (columnAdjuster * step_counter)

            if adjustedRow < 0 or adjustedRow > 7:
                break
            if adjustedColumn < 0 or adjustedColumn > 7:
                break

            directionResult.append([adjustedRow, adjustedColumn])
            
            if single_move == True:
                break
            
            step_counter += 1
        
        result.append(directionResult)

    return result

def modifyPinnedDF(dict, piece, df_pinned_by_white, df_pinned_by_black, substract=False):
    """takes in a chess piece and modifies a df which keeps track of all the positions this color pins down

    Args:
        dict (dict): dictonary of all the chess pieces
        piece (dict[key]): the chess piece in question
        df_pinned_by_white (pandasDF): df of all the locations the white pieces could attack in the next turn (from
        the perspective of the opposite colour)
        df_pinned_by_black (pandasDF): df of all the locations the black pieces could attack in the next turn (from
        the perspective of the opposite colour)
        substract (bool, optional): if True then it substracks the pinned locations from the DF.
        Done before moveing or after being killed. Defaults to False.
    """

    pinned_result = dict[piece].pinned
    modifier = 1

    if substract == True:
        modifier = -1

    if "White" in piece:
        for direction in pinned_result:
            for step in direction:
                df_pinned_by_white.iloc[*step] += modifier
    else:
        for direction in pinned_result:
            for step in direction:
                df_pinned_by_black.iloc[*step] += modifier



    





















