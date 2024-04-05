from const import *
from square import Square
from piece import *
from move import Move
from sound import Sound
import os
import copy

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

    def move(self, piece, move, testing=False):
        initial = move.initial
        final = move.final 
        en_passant_empty = self.squares[final.row][final.col].isempty()

        # Console board move update  
        self.squares[initial.row][initial.col].piece = None # Update initial square to be none 
        self.squares[final.row][final.col].piece = piece # Update final square to have piece

        if isinstance(piece, Pawn):
        # En passant capture 
            col_diff = final.col - initial.col
            if col_diff != 0 and en_passant_empty:
                # Console board move update
                self.squares[initial.row][initial.col + col_diff].piece = None # Update initial square to be none 
                self.squares[final.row][final.col].piece = piece # Update final square to have piece
                if not testing: # Not good code but fixes the bug where the sound plays before it captures the piece lol 
                    sound = Sound(os.path.join('assets/sounds/capture.wav'))
                    sound.play()
            else:
                # Pawn promotion
                self.check_promotion(piece, final)


        # King castling
        if isinstance(piece, King):
            if self.castling(initial, final):
                diff = final.col - initial.col 
                rook = piece.left_rook if (diff < 0) else piece.right_rook # If diff is less than 0, the king moved to the left
                self.move(rook, rook.moves[-1])

        # Mark move as true 
        piece.moved = True 

        # Clear valid moves since we are updating position
        piece.clear_moves()

        # Set last move 
        self.last_move = move

    def check_promotion(self, piece, final):
        if final.row == 0 or final.row == 7: # If pawn reaches row 0 or row 7 it can be promoted
            self.squares[final.row][final.col].piece = Queen(piece.colour)
    
    def castling(self, initial, final):
        return abs(initial.col - final.col) == 2 # Return if king moved by 2 squares
    
    def set_en_passant(self, piece):
        if not isinstance(piece, Pawn):
            return
        
        for row in range(ROWS):
            for col in range(COLS):
                if isinstance(self.squares[row][col].piece, Pawn):
                    self.squares[row][col].piece.en_passant = False
        
        piece.en_passant = True 

    def in_check(self, piece, move):
        temp_board = copy.deepcopy(self) # Temp board to move around pieces without affecting actual game board
        temp_piece = copy.deepcopy(piece) # Move temp piece on temp board without affecting original pieces
        temp_board.move(temp_piece, move, testing=True)

        for row in range(ROWS):
            for col in range(COLS):
                if temp_board.squares[row][col].has_rival_piece(piece.colour):
                    p = temp_board.squares[row][col].piece
                    temp_board.calc_moves(p, row, col, bool=False) # Calculating all the moves
                    for m in p.moves: # Looping through all possible moves 
                        if isinstance(m.final.piece, King):  # If the final square has a King aka if there will be a check 
                            return True
        
        return False

    def valid_move(self, piece, move):
        return move in piece.moves 

    def calc_moves(self, piece, row, col, bool=True):
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

                        # Check for any potential checks 
                        if bool: # Bool = true when we actually want to move a piece
                            if not self.in_check(piece, move):
                                # Append new move 
                                piece.add_move(move)
                        else:
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
                        final_piece = self.squares[possible_move_row][possible_move_col].piece
                        final = Square(possible_move_row, possible_move_col, final_piece)
                        # Create new move 
                        move = Move(initial, final)

                        # Check for any potential checks 
                        if bool: # Bool = true when we actually want to move a piece
                            if not self.in_check(piece, move):
                                # Append new move 
                                piece.add_move(move)
                        else:
                            piece.add_move(move)

            # En passant moves
            r = 3 if piece.colour == "white" else 4
            final_row = 2 if piece.colour == "white" else 5

            # Left en passant
            if Square.in_range(col-1) and row == r: # If same row in the left adj column
                if self.squares[row][col-1].has_rival_piece(piece.colour):
                    p = self.squares[row][col-1].piece
                    if isinstance(p, Pawn):
                        if p.en_passant:
                            # Create initial and final move squares
                            initial = Square(row, col)
                            final = Square(final_row, col-1, p)
                            # Create new move 
                            move = Move(initial, final)

                            # Check for any potential checks 
                            if bool: # Bool = true when we actually want to move a piece
                                if not self.in_check(piece, move):
                                    # Append new move 
                                    piece.add_move(move)
                            else:
                                piece.add_move(move)
                
            # Right en passant
            if Square.in_range(col+1) and row == r: # If same row in the left adj column
                if self.squares[row][col+1].has_rival_piece(piece.colour):
                    p = self.squares[row][col+1].piece
                    if isinstance(p, Pawn):
                        if p.en_passant:
                            # Create initial and final move squares
                            initial = Square(row, col)
                            final = Square(final_row, col+1, p)
                            # Create new move 
                            move = Move(initial, final)

                            # Check for any potential checks 
                            if bool: # Bool = true when we actually want to move a piece
                                if not self.in_check(piece, move):
                                    # Append new move 
                                    piece.add_move(move)
                            else:
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
                        final_piece = self.squares[possible_move_row][possible_move_col].piece
                        final = Square(possible_move_row, possible_move_col, final_piece) #piece=piece 

                        # Create new move
                        move = Move(initial, final)

                        # Check for any potential checks 
                        if bool: # Bool = true when we actually want to move a piece
                            if not self.in_check(piece, move):
                                # Append new move 
                                piece.add_move(move)
                            else:
                                break
                        else:
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
                        final_piece = self.squares[possible_move_row][possible_move_col].piece
                        final = Square(possible_move_row, possible_move_col, final_piece)
                        # Create new move
                        move = Move(initial, final)

                        # If square is empty, want to keep checking increment squares
                        if self.squares[possible_move_row][possible_move_col].isempty():
                            # Check for any potential checks 
                            if bool: # Bool = true when we actually want to move a piece
                                if not self.in_check(piece, move):
                                    # Append new move 
                                    piece.add_move(move)
                            else:
                                piece.add_move(move)

                        # If has enemy piece, want to stop checking for increment squares because possible move would end
                        elif self.squares[possible_move_row][possible_move_col].has_rival_piece(piece.colour):
                            # Check for any potential checks 
                            if bool: # Bool = true when we actually want to move a piece
                                if not self.in_check(piece, move):
                                    # Append new move 
                                    piece.add_move(move)
                            else:
                                piece.add_move(move)
                            break # Break after adding move

                        # If next square has same team piece, want to break
                        elif self.squares[possible_move_row][possible_move_col].has_team_piece(piece.colour):
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
                        # Check for any potential checks 
                        if bool: # Bool = true when we actually want to move a piece
                            if not self.in_check(piece, move):
                                # Append new move 
                                piece.add_move(move)
                            else:
                                break
                        else:
                            piece.add_move(move)

                # Castling moves
                if not piece.moved: # If king piece has not moved 
                    # Queen-side castling 
                    left_rook = self.squares[row][0].piece
                    if isinstance(left_rook, Rook):
                        if not left_rook.moved:
                            for column in range(1, 4): # Checking until 3rd column
                                if self.squares[row][column].has_piece(): # If there is a piece in these columns, castling is not possible 
                                    break 

                                if column == 3:
                                    # Adds left rook to king
                                    piece.left_rook = left_rook

                                    # Rook move
                                    initial = Square(row, 0)
                                    final = Square(row, 3)
                                    move_rook = Move(initial, final)

                                    # King move
                                    initial = Square(row, col)
                                    final = Square(row, 2)
                                    move_king = Move(initial, final)

                                    # Check for any potential checks 
                                    if bool: # Bool = true when we actually want to move a piece
                                        if not self.in_check(piece, move_king) and not self.in_check(left_rook, move_rook):
                                            # Append new move to king
                                            piece.add_move(move_king)
                                            # Append new move to rook
                                            left_rook.add_move(left_rook)
                                            
                                    else:
                                        piece.add_move(move_king)
                                        left_rook.add_move(left_rook)
                
                # King-side castling 
                    right_rook = self.squares[row][7].piece
                    if isinstance(right_rook, Rook):
                        if not right_rook.moved:
                            for column in range(5, 7): # Checking until 6th column
                                if self.squares[row][column].has_piece(): # If there is a piece in these columns, castling is not possible 
                                    break 
                                
                                if column == 6:
                                    # Adds right rook to king
                                    piece.right_rook = right_rook

                                    # Rook move
                                    initial = Square(row, 7)
                                    final = Square(row, 5)
                                    move_rook = Move(initial, final)
                    
                                    # King move
                                    initial = Square(row, col)
                                    final = Square(row, 6)
                                    move_king = Move(initial, final)

                                    # Check for any potential checks 
                                    if bool: # Bool = true when we actually want to move a piece
                                        if not self.in_check(piece, move_king) and not self.in_check(right_rook, move_rook):
                                            # Append new move to king
                                            piece.add_move(move_king)
                                            # Append new move to rook
                                            right_rook.add_move(right_rook)
                                            
                                    else:
                                        piece.add_move(move_king)
                                        right_rook.add_move(right_rook)
                                    

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