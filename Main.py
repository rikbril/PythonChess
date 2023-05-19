import pandas as pd
import Pieces 
import Moves

# one general dataframe and one for each color for easier computation
df = pd.DataFrame(index=range(8), columns=range(8))

for row in range(len(df.index)):
    for column in df.columns:
        df.iloc[row, column] = 0
df_pinned_by_white = df.copy()
df_pinned_by_black = df.copy()

# function to create the startboard for easier testing of different starting positions
def createBoard():
    """Creates the playing board with all the pieces for both colours. you can change the start_fen to generate a different start board

    Returns:
        dictionary: contains the list of all the pieces, with as keys their name and the class they belong to
    """
    chess_pieces = {}
    chess_pieces_name_counter = {}

    start_fen = "RNBQKBNR/PPPPPPPP/8/8/8/8/pppppppp/rbnqkbnr"
    
    start_fen = "RNBQKBNR/PPPPPPPP/8/8/8/8/8/rbnqkbnr"
    #start_fen = "8/8/1q6/8/4P3/8/8/1p6"

    class_dictionary = {"R": Pieces.Rook, "N": Pieces.Knight, "B": Pieces.Bischop, "Q": Pieces.Queen, "K": Pieces.King, "P": Pieces.Pawn}
    class_spelled_out = {"R": "Rook", "N": "Knight", "B":"Bischop", "Q": "Queen", "K": "King", "P":"Pawn"}

    count = 0

    for letter in start_fen:
        if letter == "/":
            pass
        elif letter.isdigit():
            count += int(letter)
        else:
            class_name = class_spelled_out[letter.capitalize()]
            is_white = True
            if letter == letter.capitalize():
                is_white = False
                class_name += "Black"
            else:
                class_name += "White"
            location = count//8, count%8
            if letter in chess_pieces_name_counter:
                chess_pieces_name_counter[letter] += 1
            else:
                chess_pieces_name_counter[letter] = 1
            name = class_name + f"{chess_pieces_name_counter[letter]}"

            df.iloc[location] = name
            chess_pieces[name] = class_dictionary[letter.capitalize()](name, location, is_white)

            count += 1
    return chess_pieces

def Test():
    result = Moves.getLocationFromName(chess_pieces, piece)
    print(chess_pieces[piece].currentLocation)
    print(chess_pieces[piece].is_white)
    print(chess_pieces[piece].location)

if __name__ == "__main__":
    chess_pieces = createBoard()
    for piece in chess_pieces:
        if piece == "QueenWhite1":
            result = Moves.getLocationFromName(chess_pieces, piece)
            #print(chess_pieces[piece].movementDirections)
            
            movement_result, pinned_result = Moves.calculatePossibleMoves(chess_pieces, piece)

            chess_pieces[piece].movement = movement_result
            chess_pieces[piece].pinned = pinned_result

            for x in range (0,3):
                Moves.modifyPinnedDF(chess_pieces, piece, df_pinned_by_white, df_pinned_by_black)

            Moves.modifyPinnedDF(chess_pieces, piece, df_pinned_by_white, df_pinned_by_black, substract=True)

            print(df_pinned_by_white)

        
        elif piece == "QueenWhite2":

        
            result = Moves.getLocationFromName(chess_pieces, piece)
            #print(chess_pieces[piece].movementDirections)
            
            movement_result, pinned_result = Moves.calculatePossibleMoves(chess_pieces, piece)

            chess_pieces[piece].movement = movement_result
            chess_pieces[piece].pinned = pinned_result

            if "White" in piece:
                for direction in pinned_result:
                    for step in direction:
                        df_pinned_by_white.iloc[*step] += 1
            else:
                for direction in pinned_result:
                    for step in direction:
                        df_pinned_by_black.iloc[*step] += 1
