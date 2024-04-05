import os 

class Piece:
    def __init__(self, name, colour, value, image=None, image_rect=None):
        self.name = name
        self.colour = colour
        value_sign = 1 if colour == 'white' else -1
        self.value = value * value_sign # Black pieces will have negative values and white pieces will have positive values
        self.moves = []
        self.moved = False 
        self.image = image
        self.set_image()
        self.image_rect = image_rect

    def set_image(self, size=80):
        self.image = os.path.join(
            f'assets/images/imgs-{size}px/{self.colour}_{self.name}.png')

    def add_move(self, move):
        self.moves.append(move)

    def clear_moves(self):
        self.moves = []

class Pawn(Piece):
    def __init__(self, colour):
        self.dir = -1 if colour == 'white' else 1 # If colour is white, it will move up the board, if black it will move down the board 
        super().__init__('Pawn', colour, 1.0)

class Knight(Piece):
    def __init__(self, colour):
        super().__init__('Knight', colour, 3.0)

class Bishop(Piece):
    def __init__(self, colour):
        super().__init__('Bishop', colour, 3.001) # AI will use values in the game, bishop is normally 3.0 but want to tell the AI bishop is a little more important than Knight

class Rook(Piece):
    def __init__(self, colour):
        super().__init__('Rook', colour, 5.0)

class Queen(Piece):
    def __init__(self, colour):
        super().__init__('Queen', colour, 9.0)

class King(Piece):
    def __init__(self, colour):
        self.left_rook = None 
        self.right_rook = None 
        super().__init__('King', colour, 10000.0) # Tell AI that it is a very important game, if you lose it you will lose the game
