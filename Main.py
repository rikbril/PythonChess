import pandas as pd
import Pieces

# one general dataframe and one for each color for easier computation
df = pd.DataFrame(index=range(8), columns=range(8))
df_white = df.copy(deep=False)
df_black = df.copy(deep=False)

# function to create the startboard for easier testing of different starting positions
def createBoard():
    """Creates the playing board with all the pieces for both colours. you can change the start_fen to generate a different start board

    Returns:
        dictionary: contains the list of all the pieces, with as keys their name and the class they belong to
    """
    chess_pieces = {}
    chess_pieces_name_counter = {}

    start_fen = "RNBQKBNR/PPPPPPPP/8/8/8/8/pppppppp/rbnqkbnr"
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
            location = [count//8, count%8]
            if letter in chess_pieces_name_counter:
                chess_pieces_name_counter[letter] += 1
            else:
                chess_pieces_name_counter[letter] = 1
            name = class_name + f"{chess_pieces_name_counter[letter]}"
            df.iloc[location] = name

            chess_pieces[name] = class_dictionary[letter.capitalize()](name, location, is_white)
            count += 1
    return chess_pieces

if __name__ == "__main__":
    chess_pieces = createBoard()

    test = "KingWhite1"

    print(chess_pieces[test].getName)
    print(chess_pieces[test].changeLocation)
    
    print(chess_pieces[test].hasMoved)
    chess_pieces[test].hasMoved = True

    print(chess_pieces[test].hasMoved)

    chess_pieces[test].changeLocation = [8,8]

    print(chess_pieces[test].changeLocation)
