import pygame
from const import *
from board import Board
from square import *
from dragger import Dragger
from config import Config

class Game:
    """
    Renders the game into something we can actually view - renders the board image and then the game pieces on to the board 
    """
    def __init__(self):
        self.next_player = 'white'
        self.hovered_sq = None 
        self.board = Board()
        self.dragger = Dragger()
        self.config = Config()

    # Show/render methods
    
    def show_bg(self, surface):
        theme = self.config.theme
        for row in range(ROWS):
            for col in range(COLS):
                if (row + col) % 2 == 0:
                    colour = theme.bg.light 
                else:
                    colour = theme.bg.dark

                rect = (col * SQ_SIZE, row * SQ_SIZE, SQ_SIZE, SQ_SIZE)

                pygame.draw.rect(surface, colour, rect)

                # Row coordinates
                if col == 0:
                    # Create new colour
                    colour = theme.bg.dark if row % 2 == 0 else theme.bg.light
                    # Create label
                    label = self.config.font.render(str(ROWS-row), 1, colour)
                    label_pos = (5, 5 + row * SQ_SIZE)
                    # Blit label
                    surface.blit(label, label_pos)


                # Col coordinates 
                if row == 7:
                    # Create new colour
                    colour = theme.bg.dark if (row + col) % 2 == 0 else theme.bg.light
                    # Create label
                    label = self.config.font.render(Square.get_alphacol(col), 1, colour)
                    label_pos = (col * SQ_SIZE + SQ_SIZE - 20, HEIGHT - 20)
                    # Blit label
                    surface.blit(label, label_pos)
                

    def show_pieces(self, surface):
        for row in range(ROWS):
            for col in range(COLS):

                # Check if there is a piece on specific square
                if self.board.squares[row][col].has_piece():
                    piece = self.board.squares[row][col].piece
                    
                    # Show pieces except dragger piece
                    if piece is not self.dragger.piece:
                        piece.set_image(size=80)
                        # Saving the piece image to img variable
                        img = pygame.image.load(piece.image)

                        # Making sure image is centered 
                        img_center = col * SQ_SIZE + SQ_SIZE // 2, row * SQ_SIZE + SQ_SIZE // 2
                        piece.image_rect = img.get_rect(center=img_center)

                        # Blit the image inside the image rectangle 
                        surface.blit(img, piece.image_rect)


    def show_moves(self, surface):
        theme = self.config.theme 
        if self.dragger.dragging:
            piece = self.dragger.piece

            # Loop through all valid moves 
            for move in piece.moves:
                # Create colour
                colour = theme.moves.light if (move.final.row + move.final.col) % 2 == 0 else theme.moves.dark
                # Create rect
                rect = (move.final.col * SQ_SIZE, move.final.row * SQ_SIZE, SQ_SIZE, SQ_SIZE)
                # Blit 
                pygame.draw.rect(surface, colour, rect)

    def show_last_move(self, surface):
        theme = self.config.theme
        if self.board.last_move:
            initial = self.board.last_move.initial
            final = self.board.last_move.final 

            for pos in [initial, final]:
                # Create colour
                colour = theme.trace.light if (pos.row + pos.col) % 2 == 0 else theme.trace.dark
                # Create rect
                rect = (pos.col * SQ_SIZE, pos.row * SQ_SIZE, SQ_SIZE, SQ_SIZE)
                # Blit 
                pygame.draw.rect(surface, colour, rect)

    def show_hover(self, surface):
        if self.hovered_sq:
            # Create colour
            colour = (180, 180, 180)
            rect = (self.hovered_sq.col * SQ_SIZE, self.hovered_sq.row * SQ_SIZE, SQ_SIZE, SQ_SIZE)
            # Blit 
            pygame.draw.rect(surface, colour, rect, width=3)
                
    # Other methods
                
    def next_turn(self):
        self.next_player = 'white' if self.next_player == 'black' else 'black'

    def set_hover(self, row, col):
        self.hovered_sq = self.board.squares[row][col]

    def change_theme(self):
        self.config.change_theme()
    
    def play_sound(self, captured=False):
        if captured:
            self.config.capture_sound.play()
        else:
            self.config.move_sound.play()
    def reset(self):
        self.__init__() # Basically creating a new game 

                