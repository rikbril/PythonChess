class Piece():
    def __init__(self, name, location, is_white, has_moved=False):
        self.name = name  
        self.location = location
        self.is_white = is_white
        self.single_move = self.single_move
        self.has_moved = has_moved
        self.movement = []
        self.pinned = []
        if "Pawn" not in self.name:
            self.move_directions = self.setDirections()
            self.attack_directions = self.move_directions

    def setDirections(self):
        result = []
        for direction in self.movement_directions:
            split_direction = direction.split("-")
            result.append(self.adjustDirections(split_direction))
        return result

    def adjustDirections(self, split_direction):
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
        super().__init__(name, location, is_white, has_moved=False)
        self.single_move = self.single_move
        self.move_directions = []
        self.attack_directions = []
        if self.is_white == True:
            self.move_directions = [[1, 0], [2,0]]
            self.attack_directions = [[1, -1], [1 , 1]]
        else:
            self.move_directions = [[-1, 0], [-2, 0]]
            self.attack_directions = [[-1, -1], [-1 , 1]]

