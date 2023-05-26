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

class_dictionary = {"R": Pieces.Rook, "N": Pieces.Knight, "B": Pieces.Bischop, "Q": Pieces.Queen, "K": Pieces.King, "P": Pieces.Pawn}
class_spelled_out = {"R": "Rook", "N": "Knight", "B":"Bischop", "Q": "Queen", "K": "King", "P":"Pawn"}

# function to create the startboard for easier testing of different starting positions
def createBoard():
    """Creates the playing board with all the pieces for both colours. you can change the start_fen to generate a different start board

    Returns:
        dictionary: contains the list of all the pieces, with as keys their name and the class they belong to
    """
    chess_pieces = {}
    chess_pieces_name_counter = {}

    ## Black start on the top of the board, white at the bottom
    start_fen = "RNBQKBNR/PPPPPPPP/8/8/8/8/pppppppp/rbnqknbr"

    start_fen = "R3K2R/PPPPPPPP/8/8/8/8/pppppppp/rbnqknbr"
    #start_fen = "8/8/2Q1Q3/8/8/2q5/8/7k"
    #start_fen = "3P4/8/2P5/8/8/8/8/2q5"
    #start_fen = "3P4/3n4/8/8/8/8/8/8"


    count = 0

    for letter in start_fen:
        if letter == "/":
            pass
        elif letter.isdigit():
            count += int(letter)
        else:
            is_white = True if letter.capitalize() == letter else False
            class_name = class_spelled_out[letter.capitalize()]
            class_name += "White" if is_white == True else "Black"

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
    print(Moves.checkForPromotion(chess_pieces, False, df))
    print(Moves.CheckForCastle(chess_pieces, False, df, df_pinned_by_white, df_pinned_by_black))
    Moves.listAllMovesByColor(chess_pieces, False, df, df_pinned_by_white, df_pinned_by_black)
    Moves.activateMove(chess_pieces, move, False, df, df_pinned_by_white, df_pinned_by_black, class_dictionary)

def promoteToQueen(queen_name, location, is_white):
    chess_pieces[queen_name] = class_dictionary["Q"](queen_name, location, is_white)
    

if __name__ == "__main__":
    ## Black start on the top of the board, white at the bottom
    chess_pieces = createBoard()
    temp = "KnightBlack1"
    temp2 = "PawnWhite1"
    
    for piece in chess_pieces:
        Moves.possibleMovesForPiece(chess_pieces, piece)
        Moves.modifyPinnedDF(chess_pieces, piece, df_pinned_by_white, df_pinned_by_black)

    print(df)
    print()


    move = ["PawnBlack1", [0,1]]
    Moves.activateMove(chess_pieces, move, False, df, df_pinned_by_white, df_pinned_by_black, class_dictionary)

    print(df)
    print(chess_pieces)

    
















