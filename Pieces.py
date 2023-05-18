class Piece():
    def __init__(self, name, location, is_white, has_moved=False):
        """parent class of all the chess pieces. all the possible moves and attacks are tracked from within this class. 
        this also includes the possible attack vectors for the next turn after an other piece changes it's location       

        Args:
            name (String): Concatinated name of the piece, type of piece + colour + individual number
            location (_type_): the location of the piece on the board
            is_white (bool): True if the piece is White, otherwise the piece is Black
            has_moved (bool, optional): keeps track if the piece has moved, will be used for de double start of pawns and king/rook swap. Defaults to False.
        """

        self.name = name  
        self.location = location
        self.is_white = is_white
        self.single_move = self.single_move
        self.has_moved = has_moved
        if "Pawn" not in self.name:
            self.move_directions = self.setDirections()
            self.attack_directions = self.move_directions

    def setDirections(self):
        """the movement directions are writendown in a way which is easy to understand, this function splits all the movement directions up and calls.
        a different function returns this direction in the form of [x, y] direction array

        Returns:
            [row, column]:  each value of the array represents which direction a piece can move. e.g. an knight can move 2 places up and 1 place to left.
                            This was written down as [north-north-east] and will be returned as [-2, 1]
        """
        result = []
        for direction in self.movement_directions:
            split_direction = direction.split("-")
            result.append(self.adjustDirections(split_direction))
        return result

    def adjustDirections(self, split_direction):
        """recieves a singular movement direction and translate it into [x, y] coordinates

        Args:
            split_direction ([string, string]): the strings contain the direction. e.g. if a piece can move diaginal the string could be ["north", "west"]

        Returns:
            [x, y]: returns interger array with the movement direction coordinates
        """
        x, y = 0, 0
        for direction in split_direction:
            if direction == "north":
                y -= 1
            elif direction == "south":
                y += 1
            elif direction == "east":
                x += 1
            else:
                x -= 1
        return [x,y]
    
    @property
    def movementDirections(self):
        return self.move_directions

    @property
    def getName(self):
        return self.name

    @property
    def currentLocation(self):
        return self.location
    @property
    def changeLocation(self):
        return self.location
    @changeLocation.setter
    def changeLocation(self, new_location):
        self.location = new_location

    @property
    def hasMoved(self):
        return self.has_moved
    @hasMoved.setter
    def hasMoved(self, value):
        if self.has_moved == False:
            if "pawn" in self.name:
                del self.move_directions[1]
            self.has_moved = True

class Rook(Piece):
    movement_directions = ["north", "east", "south", "west"]
    single_move = False

class Bischop(Piece):
    movement_directions = ["north-east", "south-east", "south-west", "north-west"]    
    single_move = False

class King(Piece):
    movement_directions = ["north", "north-east", "east", "south-east", "south", "south-west", "west", "north-west"]
    single_move = True

class Queen(Piece):
    movement_directions = ["north", "north-east", "east", "south-east", "south", "south-west", "west", "north-west"]
    single_move = False

class Knight(Piece):
    movement_directions = ["north-north-east", "east-east-north", "east-east-south", "south-south-east", 
                           "south-south-west", "west-west-south", "west-west-north", "north-north-west"]
    single_move = True
    
class Pawn(Piece):
    single_move = True
    def __init__(self, name, location, is_white, has_moved=False):
        """Pawns have a different movement charataristics than other pieces so they get initialized in their subclass for clarity

        Args:
            name (String): Concatinated name of the piece, type of piece + colour + individual number
            location (_type_): the location of the piece on the board
            is_white (bool): True if the piece is White, otherwise the piece is Black
            has_moved (bool, optional): keeps track if the piece has moved, will be used for de double start of pawns and king/rook swap. Defaults to False.
        """
        super().__init__(name, location, is_white, has_moved=False)
        
        self.single_move = self.single_move
        self.move_directions = []
        self.attack_directions = []
        
        # adjust the movement and attack vectors of the pawns in regards to their color
        if self.is_white == True:
            self.move_directions = [[1, 0], [2,0]]
            self.attack_directions = [[1, -1], [1 , 1]]
        else:
            self.move_directions = [[-1, 0], [-2, 0]]
            self.attack_directions = [[-1, -1], [-1 , 1]]

