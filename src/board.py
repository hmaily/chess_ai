from const import *
from square import Square
from piece import *
from move import Move

class Board:
    """
    Creates the board onto the game screen and adds pieces onto the board
    """

    def __init__(self):
        self.squares = [[0, 0, 0, 0, 0, 0, 0, 0] for col in range(COLS)]
        self.last_move = None 
        self._create()
        self._add_pieces('white')
        self._add_pieces('black')

    def move(self, piece, move):
        initial = move.initial
        final = move.final 

        # Console board move update  
        self.squares[initial.row][initial.col].piece = None # Update initial square to be none 
        self.squares[final.row][final.col].piece = piece # Update final square to have piece

        # Mark move as true 
        piece.moved = True 

        # Clear valid moves since we are updating position
        piece.clear_moves()

        # Set last move 
        self.last_move = move

    def valid_move(self, piece, move):
        return move in piece.moves 

    def calc_moves(self, piece, row, col):
        """
        Calculate all the possible and valid moves of a specific piece in a specific position
        """
        def pawn_moves():
            # Check if pawn has previously moved
            steps = 1 if piece.moved else 2 # On a pawn's first move, it can advance 2 squares

            # Vertical moves
            start = row + piece.dir
            end = row + (piece.dir * (1 + steps)) # This is exclusive, so pawn is actually only able to move piece.dir - 1 steps 
            for possible_move_row in range(start, end, piece.dir):
                if Square.in_range(possible_move_row):
                    if self.squares[possible_move_row][col].isempty():
                        # Create initial and final move squares
                        initial = Square(row, col)
                        final = Square(possible_move_row, col)
                        # Create new move
                        move = Move(initial, final)
                        # Append new move 
                        piece.add_move(move)
                
                    # If there is no empty square, pawn is blocked from making a move 
                    else:
                        break
                # If out of range, pawn cannot make a move
                else:
                    break 

            # Diagonal moves (when taking rival piece)
            possible_move_row = row + piece.dir
            possible_move_cols = [col-1, col+1]
            for possible_move_col in possible_move_cols:
                if Square.in_range(possible_move_row, possible_move_col):
                    if self.squares[possible_move_row][possible_move_col].has_rival_piece(piece.colour):
                        # Create initial and final move squares
                        initial = Square(row, col)
                        final = Square(possible_move_row, possible_move_col)
                        # Create new move 
                        move = Move(initial, final)
                        # Append new move 
                        piece.add_move(move)

        def knight_moves():
            # 8 possible moves
            possible_moves = [
                (row-2, col+1),
                (row-1, col+2),
                (row+1, col+2),
                (row+2, col+1),
                (row+2, col-1),
                (row+1, col-2),
                (row-1, col-2),
                (row-2, col-1),
            ]

            for possible_move in possible_moves:
                possible_move_row, possible_move_col = possible_move

                # Check if possible move is in the range of the board
                if Square.in_range(possible_move_row, possible_move_col):
                    # Now need to check if square is empty or if square has a rival piece 
                    if self.squares[possible_move_row][possible_move_col].isempty_or_rival(piece.colour):
                        # Create squares to move to 
                        initial = Square(row, col)
                        final = Square(possible_move_row, possible_move_col) #piece=piece 

                        # Create new move
                        move = Move(initial, final)
                        # Append new valid move 
                        piece.add_move(move)

        def straightline_moves(increments):
            """
            Rook, Bishop & Queen all use this move but in different increments e.g.

            Bishop: (row-1, col-1), (row+1, col+1), (row-1, col+1), (row+1, col-1) increments
            Rook: row-1, row+1, col-1, coL+1 increments
            Queen: combination of Bishop & Rook: (row-1, col-1), (row+1, col+1), (row-1, col+1), (row+1, col-1), row-1, row+1, col-1, coL+1 increments 
            """
            for incr in increments:
                row_incr, col_incr = incr
                possible_move_row = row + row_incr
                possible_move_col = col + col_incr
            
                while True:
                    if Square.in_range(possible_move_row, possible_move_col):
                        # Create initial and final move squares
                        initial = Square(row, col)
                        final = Square(possible_move_row, possible_move_col)
                        # Create new move
                        move = Move(initial, final)

                        # If square is empty, want to keep checking increment squares
                        if self.squares[possible_move_row][possible_move_col].isempty():
                            # Append new move 
                            piece.add_move(move)

                        # If has enemy piece, want to stop checking for increment squares because possible move would end
                        if self.squares[possible_move_row][possible_move_col].has_rival_piece(piece.colour):
                            # Create new move 
                            piece.add_move(move)
                            break # Break after adding move

                        # If next square has same team piece, want to break
                        if self.squares[possible_move_row][possible_move_col].has_team_piece(piece.colour):
                            break
                    
                    # Break if not in range 
                    else:
                        break
                    
                    # Adding increments to the possible moves 
                    possible_move_row = possible_move_row + row_incr
                    possible_move_col = possible_move_col + col_incr
        
        def king_moves():
            # 8 possible moves 
            adj = [
                (row-1, col-1), # up-left
                (row-1, col), # up
                (row-1, col+1), # up-right
                (row, col-1), # left
                (row, col+1), # right
                (row+1, col-1), # down-left 
                (row+1, col), # down
                (row+1, col+1) # down-right 
            ]

            for possible_move in adj:
                possible_move_row, possible_move_col = possible_move

                # Check if possible move is in the range of the board
                if Square.in_range(possible_move_row, possible_move_col):
                    # Now need to check if square is empty or if square has a rival piece 
                    if self.squares[possible_move_row][possible_move_col].isempty_or_rival(piece.colour):
                        # Create squares to move to 
                        initial = Square(row, col)
                        final = Square(possible_move_row, possible_move_col) #piece=piece 

                        # Create new move
                        move = Move(initial, final)
                        # Append new valid move 
                        piece.add_move(move)

                # Castling moves - queen castling, king castling 

        if isinstance(piece, Pawn):
            pawn_moves()
        
        if isinstance(piece, Knight):
            knight_moves()

        if isinstance(piece, Bishop):
            straightline_moves([
                (-1, 1), # Ascending right diagonal 
                (-1, -1), # Ascending left diagonal
                (1, -1), # Descending left diagonal
                (1, 1) # Descending right diagonal 
            ])

        if isinstance(piece, Rook):
            straightline_moves([
                (-1, 0), # Up
                (0, 1), # Right
                (1, 0), # Down
                (0, -1) # Left 
            ])

        if isinstance(piece, Queen):
            straightline_moves([
                (-1, 1), # Ascending right diagonal 
                (-1, -1), # Ascending left diagonal
                (1, -1), # Descending left diagonal
                (1, 1), # Descending right diagonal
                (-1, 0), # Up
                (0, 1), # Right
                (1, 0), # Down
                (0, -1) # Left 
            ])

        if isinstance(piece, King):
            king_moves()

    def _create(self): # Underscore as a prefix to indicate these are private methods (only to be called within the Board class)
        for row in range(ROWS):
            for col in range(COLS):
                self.squares[row][col] = Square(row, col)

    def _add_pieces(self, colour):
        row_pawn, row_other = (6, 7) if colour == 'white' else (1, 0) # White pawns will spawn in row 6 and other white pieces will spawn in row 7, same logic for black pawns

        # Create all pawns
        for col in range(COLS):
            self.squares[row_pawn][col] = Square(row_pawn, col, Pawn(colour))
        
        # Create all knights
        self.squares[row_other][1] = Square(row_other, 1, Knight(colour))
        self.squares[row_other][6] = Square(row_other, 6, Knight(colour))

        # Create all bishops
        self.squares[row_other][2] = Square(row_other, 2, Bishop(colour))
        self.squares[row_other][5] = Square(row_other, 5, Bishop(colour))

        # Create all rooks
        self.squares[row_other][0] = Square(row_other, 0, Rook(colour))
        self.squares[row_other][7] = Square(row_other, 7, Rook(colour))
    
        # Create queen
        self.squares[row_other][3] = Square(row_other, 3, Queen(colour))

        # Create king
        self.squares[row_other][4] = Square(row_other, 4, King(colour))