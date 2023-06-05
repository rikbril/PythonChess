def locationToColour(dict, value):
    for item in dict:
        if [*dict[item].location] == value:
            return dict[item].is_white
    return None

def locationToName(dict, value):
    for key in dict:
        if [*dict[key].location] == value:
            return key

def unpackNestedList(nested):
    result = []
    for item in nested:
        if isinstance(item, list):
            result.extend(unpackNestedList(item))
        else:
            result.append(item)
    return result

def repackLocationList(nested):
    """Location data is stored in sets of 2. After unpacking the nested lists with variable depth it needs
    to be repacked in row, column lists. due to the recursive nature of this process the unpacking is done
    in a seperate function

    Args:
        nested list: a nested list which needs to be flattend first and repacked in [row, column] format

    Returns:
        list: nested list with an uniform depth of 1
    """
    unnested = unpackNestedList(nested)
    temp = []
    result = []

    for item in unnested:
        temp.append(item)
        if len(temp) == 2:
            result.append(temp)
            temp = []

    return result

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
            return dict[key].location
    
def possibleMovesForPiece(dict, piece, enpassant_location=False):
    """Takes in a piece and calculates to which places the piece can move, and which locations are pinned by this piece. 
    in order to keep track of attack/defend vectors (i presume, i dont play chess).

    This function does not look for Casteling, Enpassant or piece Promotion. That is done in the move aggregator

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

    if "Pawn" in piece:
        dict[piece].movement, dict[piece].pinned = directionCounterForPawns(dict, is_white, directions_with_locations, column, enpassant_location)
    else:
        dict[piece].movement, dict[piece].pinned = directionCounter(dict, is_white, directions_with_locations)

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
    movement_result = [[]]
    pinned_result = [[]]

    print(enpassant_location)

    path_blocked = False
    for direction in directions_with_locations:
        for step in direction:
            encounter_color = locationToColour(dict, step)
            if step[1] == column:
                if encounter_color == None:
                    if path_blocked == False:
                        movement_result[0].append(step)
                else:
                    path_blocked = True
            else:
                pinned_result[0].append(step)
                if encounter_color != None:
                    if encounter_color != is_white:
                        movement_result[0].append(step)
                elif enpassant_location == step:
                    movement_result[0].append(step)

    return repackLocationList(movement_result), repackLocationList(pinned_result)

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

            if encounter >= 1 and previous_encounter == 2 :
                direction_movement_result.append(step)
            if encounter >= 0 and previous_encounter >= 1:
                direction_pinned_result.append(step)
            
            if encounter <= 0:
                break
        movement_result.append(direction_movement_result)
        pinned_result.append(direction_pinned_result)

    movement_result = repackLocationList(movement_result)
    pinned_result = repackLocationList(pinned_result)
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
        for location in pinned_result:
            df_pinned_by_white.iloc[*location] += modifier
    else:
        for location in pinned_result:
            df_pinned_by_black.iloc[*location] += modifier

def CheckForCastle(dict, is_white, df, df_pinned_by_white, df_pinned_by_black):
    """Function takes in multiple arguments which are used to look for Casteling. the is_white color 
    argument is used a couple
    of times in order to create variable names which are used to check for the special moves.

    Args:
        dict (dictionary): dictionary of all the chess pieces
        is_white (bool): color of the piece. True for white, False for black
        df (DataFrame): DataFrame of all the pieces still in the game
        df_pinned_by_white (DataFrame): DataFrame of all the places which are under attack by white
        df_pinned_by_black (DataFrame): DataFrame of all the places which are under attack by black
    
    Returns:
        list: list with 2 variables, for each castle direction one bool
    """

    castle = [False, False]
    
    color_name = "White" if is_white == True else "Black"
    king = "King" + color_name + "1"
    opposing_color_df = df_pinned_by_black.copy() if is_white == True else df_pinned_by_white.copy()  
    row = 0 if is_white else 7 

    ## Logic for casteling of the kings with the rooks. the starting positions are [0,4] for black and [7,4] for white
    if not dict[king].has_moved:
        if dict.get("Rook" + color_name + "1"):
            rook_name = "Rook" + color_name + "1"
            if dict[rook_name].has_moved == False:
                if df.iloc[row, 1] == 0 and df.iloc[row, 2] == 0 and df.iloc[row, 3] == 0:
                    if opposing_color_df.iloc[row, 2] == 0 and opposing_color_df.iloc[row, 3] == 0 and opposing_color_df.iloc[row, 4] == 0:
                        castle[0] = True
        if dict.get("Rook" + color_name + "2"):
            rook_name = "Rook" + color_name + "2"
            if dict[rook_name].has_moved == False:
                if df.iloc[row, 5] == 0 and df.iloc[row, 6] == 0:
                    if opposing_color_df.iloc[row, 4] == 0 and opposing_color_df.iloc[row, 5] == 0 and opposing_color_df.iloc[row, 6] == 0:
                        castle[1] = True

    return castle

def checkForPromotion(is_white, df):
    """check for promotion, this function is called after a move is made but before the opponents turn is.

    Args:
        dict (dictionary): dictionary of all the chess pieces
        is_white (bool): color of the pieces to be checked. True for white, False for Black
        df (DataFrame): DataFrame of all the pieces on the board with their locations.

    Returns:
        nested list: location for if their is a piece which will be promoted other wise a list without content
    """
    row = 7 if is_white else 0

    for column in df.columns:
        if df.iloc[row, column] == 0: pass
        elif "Pawn" in df.iloc[row, column]:
            return [[row, column]]

    return False

def promoteToQueen(dict, piece, is_white, new_piece_location, df, df_pinned_by_white, df_pinned_by_black, class_dictionary):
    dict.pop(piece)
    queen_name = "QueenWhite" if is_white == True else "QueenBlack"
    count = 1
    for name in dict:
        if  queen_name in name:
            count += 1
    queen_name = queen_name + str(count) 
    df.iloc[*new_piece_location] = queen_name
    dict[queen_name] = class_dictionary["Q"](queen_name, new_piece_location, is_white)

    possibleMovesForPiece(dict, queen_name)
    modifyPinnedDF(dict, queen_name, df_pinned_by_white, df_pinned_by_black)

def movePiece(dict, piece, new_location, df, df_pinned_by_white, df_pinned_by_black):
    """Moves a piece to its new location. This includes looking for all the pieces it might interact with and recalculating
    their possible moves, which places they are pinning down. 

    Args:
        dict (dictionary): dictionary of all the possible moves
        piece (dictionary[key]): piece which is moveing
        new_location ([row, column]): the location to which the piece is moveing to
        df (DataFrame): DataFrame of all the chess pieces
        df_pinned_by_white (DataFrame): DataFrame of all the places which are pinned down by White
        df_pinned_by_black (DataFrame): DataFrame of all the places which are pinned down by Black
    """
    piece_location = dict[piece].location
    df.iloc[*piece_location] = 0
    target_piece = False if df.iloc[*new_location] == 0 else df.iloc[*new_location]
    modifyPinnedDF(dict, piece, df_pinned_by_white, df_pinned_by_black, True)
    encounter_list = lookForEncounters(dict, piece, piece_location, new_location, target_piece)

    for other_piece in encounter_list:
        modifyPinnedDF(dict, other_piece, df_pinned_by_white, df_pinned_by_black, True)

    if target_piece:
        dict.pop(target_piece)
        if target_piece in encounter_list:
            encounter_list.remove(target_piece)

    df.iloc[*new_location] = piece
    dict[piece].location = new_location

    for other_piece in encounter_list:
        possibleMovesForPiece(dict, other_piece)
        modifyPinnedDF(dict, other_piece, df_pinned_by_white, df_pinned_by_black)

def moveCasteling(dict, df, king, rook, castle_location, df_pinned_by_white, df_pinned_by_black):
    modifyPinnedDF(dict, rook, df_pinned_by_white, df_pinned_by_black, True)
    modifyPinnedDF(dict, king, df_pinned_by_white, df_pinned_by_black, True)

    king_location = 2 if "1" in rook else 6
    rook_location = 3 if "1" in rook else 5

    df.iloc[castle_location[0], king_location] = king
    df.iloc[castle_location[0], rook_location] = rook
    df.iloc[castle_location[0], 4] = 0
    df.iloc[castle_location[0], 0 if "1" in rook else 7] = 0


    dict[king].location = [castle_location[0], king_location]
    dict[rook].location = [castle_location[0], rook_location]

    possibleMovesForPiece(dict, king)
    possibleMovesForPiece(dict, rook)

    modifyPinnedDF(dict, rook, df_pinned_by_white, df_pinned_by_black)
    modifyPinnedDF(dict, king, df_pinned_by_white, df_pinned_by_black)

def lookForEncounters(dict, piece, old_piece_location, new_piece_location, target_piece):
    """looping through the pinned locations of all the pieces on the board and listing all the pieces which interact with 
    either the old or the new location 

    Args:
        dict (dictionary): dictionary of all the pieces
        piece (dictionary[key]): chess piece which is being checked
        old_piece_location (location): the old location of the piece which is moveing
        new_piece_location (location): the new location of the piece which is moveing
        target_piece (dictionary[key]): chess piece which is on the new location of the piece being moved. value is False if 
        the spot is empty

    Returns:
        list: all pieces which need to be recalculated
    """
    encounter_list = [] 
    for other_piece in dict:
        if piece == other_piece:
            pass
        elif piece == target_piece:
            encounter_list.append(other_piece)
        else:
            for location in dict[other_piece].pinned:
                if location == [*old_piece_location] or location == [*new_piece_location]:
                    encounter_list.append(other_piece)
            if "Pawn" in other_piece:
                current_location = dict[other_piece].location
                for movement_Adjuster in dict[other_piece].move_directions:
                    adjusted_location = [(current_location[0] + movement_Adjuster[0]), current_location[1]]
                    if movement_Adjuster[1] == 0:
                        if adjusted_location == [*old_piece_location] or adjusted_location == [*new_piece_location]:
                            encounter_list.append(other_piece)

    encounter_list.append(target_piece) if target_piece is not False and target_piece not in encounter_list else encounter_list

    return encounter_list

def listAllMovesByColor(dict, is_white, df, df_pinned_by_white, df_pinned_by_black, enpassant_location=False):
    """lists all the moves which a color can make, including casteling

    Args:
        dict (dictionary): dictionary of all the chess pieces
        is_white (bool): color of the piece. True for white, False for black
        df (DataFrame): DataFrame of all the pieces still in the game
        df_pinned_by_white (DataFrame): DataFrame of all the places which are under attack by white
        df_pinned_by_black (DataFrame): DataFrame of all the places which are under attack by black

    Returns:
        list: all the moves by all the pieces. castle left and right are added seperatly
    """
    all_moves = []
    name_of_color = "White" if is_white == True else "Black"
    
    king_location = dict[("King" + name_of_color + "1")].location
    king_counter = df_pinned_by_black.iloc[*king_location] if is_white == True else df_pinned_by_white.iloc[*king_location]

    if king_counter > 0:
        checkKingSafety(dict, is_white, df, df_pinned_by_white, df_pinned_by_black, king_location)

    for piece in dict:
        if name_of_color in piece and dict[piece].movement != []:
            
            all_moves.append([piece, dict[piece].movement]) 

    castle = CheckForCastle(dict, is_white, df, df_pinned_by_white, df_pinned_by_black)
    for x in range(len(castle)):
        if castle[x] == True:
            color_name = "White" if is_white == True else "Black"
            king = "King" + color_name + "1"
            rook = "Rook" + color_name
            rook += "1" if x == 0 else "2"
            row = 0 if is_white else 7
            column = 0 if x == 0 else 7
            side = "Queen" if x == 0 else "King"
            all_moves.append([("Castle" + side + color_name) , [king, rook, [row, column]]])
    
    return all_moves

def move(dict, move, is_white, df, df_pinned_by_white, df_pinned_by_black, class_dictionary):
    if "Castle" in move[0]:
        king, rook, castle_location = move[1]
        moveCasteling(dict, df, king, rook, castle_location, df_pinned_by_white, df_pinned_by_black)
        if "Queen" in move[0]:
            return "0-0-0"
        else:
            return "0-0"
    else:
        piece = move[0]
        new_piece_location = move[1]
        notation = chessNotation(dict, piece, dict[piece].location, move[1], is_white)
        enpassant_location = False
        if "Pawn" in piece:
            old_place_location = dict[piece].location
            if (abs(new_piece_location[0] - old_place_location[0])) == 2:
                enpassant_location = [int(new_piece_location[0] -((new_piece_location[0] - old_place_location[0]) /2)), new_piece_location[1]] 
                print("Enpassant location", enpassant_location)
        movePiece(dict, piece, new_piece_location, df, df_pinned_by_white, df_pinned_by_black)
        
        promotion = checkForPromotion(is_white, df)

        if promotion != False:
            promoteToQueen(dict, piece, is_white, new_piece_location, df, df_pinned_by_white, df_pinned_by_black, class_dictionary)
        
        if enpassant_location:
            return [notation, enpassant_location]
        return notation

def chessNotation(dict, piece, old_location, new_location, is_white):
    """creates the notation for the move in order to keep track of the game

    Args:
        dict (dictionary): dictionary of chess pieces
        piece (dictionary[key]): chess piece which is moveing
        old_location ([row, column]): location the piece is moveing from
        new_location ([row, column]): location the piece is moveing to
        is_white (bool): True if the piece is White, False if the piece is Black

    Returns:
        String: notation which belongs to the move
    """
    board_letter = "abcdefgh"
    board_number = [8, 7, 6, 5, 4, 3, 2, 1]
    piece_fen_letter = {"King": "K", "Queen": "Q", "Knight": "N", "Rook": "R", "Bischop": "B", "Pawn": ""}
    notation = ""
    pawn_promotion = True if   (new_location[0] == 0 and is_white == False and "Pawn" in piece) or (
                                new_location[0] == 7 and is_white == True and "Pawn" in piece) else False

    simular_pieces = []
    color_name = "White" if is_white == True else "Black"
    piece_name = piece[:-1]
    hit = False
    

    for name in piece_fen_letter:    
        if name in piece:
            notation += piece_fen_letter[name]
        
    for other_pieces in dict:
        if other_pieces == piece:
            pass
        elif color_name in other_pieces:
            if piece_name in other_pieces:
                simular_pieces.append(other_pieces)
        else:
            if list(dict[other_pieces].location) == new_location:
                hit = True

    if simular_pieces != []:
        for other_pieces in simular_pieces:
            for other_move in dict[other_pieces].movement:
                if other_move == new_location:
                    if dict[other_pieces].location[0] == old_location[0]:
                        notation += board_letter[old_location[1]]
                    if dict[other_pieces].location[1] ==  old_location[1]:
                        notation += str(board_number[old_location[0]])
    
    if hit == True:
        notation += "x"

    notation += board_letter[new_location[1]]
    notation += str(board_number[new_location[0]])

    notation += "Q" if pawn_promotion == True  else ""
    return notation

def checkKingSafety(dict, is_white, df, df_pinned_by_white, df_pinned_by_black, king_location):
    """function checks which pieces blocks a check and filters out all the moves other than in the direction of the pieces which is attacking 
    the king

    Args:
        dict (dictionary): dictionary of all the pieces
        is_white (bool): is the piece white
        df (DataFrame): dataframe of all the pieces on the board
        df_pinned_by_white (DataFrame): DataFrame of all the places white attacks
        df_pinned_by_black (DataFrame): DataFrame of all the places black attacks
        king_location (int, int): location of the pieces on the board
    """

    pinners = {}
    obstructors = {}
    for piece in dict:
        name_of_color = "White" if is_white == True else "Black"
        if name_of_color not in piece:
            for move in dict[piece].pinned:
                if move == [*king_location]:
                    pinners[piece] = dict[piece].location
    
    for pinner in pinners:
        row, column = 0,0
        steps = 0
        pinner_location = pinners[pinner]
        if pinner_location[0] < king_location[0]:
            row = 1
            if steps == 0:
                steps = abs(pinner_location[0]- king_location[0])
        elif pinner_location[0] > king_location[0]:
            row = -1
            if steps == 0:
                steps = abs(pinner_location[0]- king_location[0])
        if pinner_location[1] < king_location[1]:
            column = 1
            if steps == 0:
                steps = abs(pinner_location[1]- king_location[1])
        elif pinner_location[1] > king_location[1]:
            column = -1
            if steps == 0:
                steps = abs(pinner_location[1]- king_location[1])
        
        for step in range(1, steps):
            obstruction_name = locationToName(dict, [*(pinner_location[0] + (row * step), pinner_location[1] + (column * step))])
            if obstruction_name:
                obstructors[obstruction_name] = [[*(pinner_location[0] + (row * step), pinner_location[1] + (column * step))], [row, column]]
                break

    for obstructor in obstructors:
        [direction_row, direction_column] = obstructors[obstructor][1]
        to_merge_list = []
        location = dict[obstructor].location

        modifyPinnedDF(dict, obstructor, df_pinned_by_white, df_pinned_by_black, True)

        direction_row = direction_row - (direction_row * 2)
        direction_column = direction_column - (direction_column * 2)

        for step in range (1,8):
            adjustedRow = location[0] + (step * direction_row)
            adjustedColumn = location[1] + (step * direction_column)
            to_merge_list.append([adjustedRow, adjustedColumn])
        
        old_pinned_list = dict[obstructor].pinned
        new_pinned_list = []        
        old_movement_list = dict[obstructor].movement
        new_movement_list = []
        for item in to_merge_list:
            print(item)
            if item in old_movement_list:
                new_movement_list.append(item)
            if item in old_pinned_list:
                new_pinned_list.append(item)



        dict[obstructor].movement = new_movement_list
        dict[obstructor].pinned = new_pinned_list

        #Why does this not work?
        #dict[obstructor].pinned = list(set(dict[obstructor].pinned) & set(to_merge_list))
        #dict[obstructor].movement = list(set(dict[obstructor].movement) & set(to_merge_list))

        modifyPinnedDF(dict, obstructor,df_pinned_by_white, df_pinned_by_black)
    pass
    











