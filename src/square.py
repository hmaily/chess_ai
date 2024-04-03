
class Square:

    ALPHACOLS = {0: 'a', 1: 'b', 2: 'c', 3: 'd', 4: 'e', 5: 'f', 6: 'g', 7: 'h'}

    def __init__(self, row, col, piece=None):
        self.row = row
        self.col = col
        self.piece = piece
        self.alphacol = self.ALPHACOLS[col]

    # Special method
    # Tell python when a move is equal to another move 
    def __eq__(self, other):
        return self.row == other.row and self.col == other.col

    def has_piece(self):
        return self.piece != None
    
    def isempty(self):
        return not self.has_piece()
    
    def has_team_piece(self, colour):
        return self.has_piece() and self.piece.colour == colour
    
    def has_rival_piece(self, colour):
        return self.has_piece() and self.piece.colour != colour
    
    def isempty_or_rival(self, colour):
        return self.isempty() or self.has_rival_piece(colour)
    
    @staticmethod # Call method with class, not instance 
    def in_range(*args):
        for arg in args:
            # If row/col less than 0 or row/col more than 7, there is no position on the baord 
            if arg < 0 or arg > 7:
                return False 
        
        return True

    @staticmethod
    def get_alphacol(col):
        ALPHACOLS = {0: 'a', 1: 'b', 2: 'c', 3: 'd', 4: 'e', 5: 'f', 6: 'g', 7: 'h'}
        return ALPHACOLS[col]