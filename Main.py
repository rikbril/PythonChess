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

    start_fen = "RNBQKBNR/PPPPPPPP/8/8/8/8/pppppppp/rbnqknbr"
    
    #start_fen = "RNBQKBNR/8//8/82PP4/8/8/rnbqkbnr"
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
    test = "RookWhite2"
    test2 = "PawnWhite3"
    for piece in chess_pieces:
        Moves.calculatePossibleMoves(chess_pieces, piece)
        Moves.modifyPinnedDF(chess_pieces, piece, df_pinned_by_white, df_pinned_by_black)
        #print(f"Piece: {piece} has a point total of: {chess_pieces[piece].points}")  
    print("location", chess_pieces[test2].location)
    print(chess_pieces[test2].movement)

