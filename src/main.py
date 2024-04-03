import pygame 
import sys 

from const import *
from game import Game
from square import Square
from move import Move 

class Main:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('Chess')
        self.game = Game()

    def main_loop(self): # Call other classes 
        game = self.game
        screen = self.screen
        board = self.game.board 
        dragger = self.game.dragger

        while True:
            # Show methods 
            game.show_bg(screen)
            game.show_last_move(screen)
            game.show_moves(screen)
            game.show_pieces(screen)
            game.show_hover(screen)

            if dragger.dragging:
                dragger.update_blit(screen)

            for event in pygame.event.get():

                # Click
                if event.type == pygame.MOUSEBUTTONDOWN:
                    dragger.update_mouse(event.pos)

                    # Check if the pos has a piece 
                    clicked_row = dragger.mouse_y // SQ_SIZE
                    clicked_col = dragger.mouse_x // SQ_SIZE

                    # If clicked square has a piece, then 
                    if board.squares[clicked_row][clicked_col].has_piece():
                        piece = board.squares[clicked_row][clicked_col].piece
                        board.calc_moves(piece, clicked_row, clicked_col)

                        # Check if correct colour is playing
                        if piece.colour == game.next_player:

                            dragger.save_initial(event.pos)
                            dragger.drag_piece(piece)

                            # Show methods
                            game.show_bg(screen)
                            game.show_last_move(screen)
                            game.show_moves(screen)
                            game.show_pieces(screen)

                # Mouse motion/drag 
                elif event.type == pygame.MOUSEMOTION:
                    motion_row = event.pos[1] // SQ_SIZE
                    motion_col = event.pos[0] // SQ_SIZE
                
                    game.set_hover(motion_row, motion_col)

                    if dragger.dragging:
                        dragger.update_mouse(event.pos)

                        # Show methods 
                        game.show_bg(screen)
                        game.show_last_move(screen)
                        game.show_moves(screen)
                        game.show_pieces(screen)
                        game.show_hover(screen)
                        dragger.update_blit(screen)
                
                # Mouse/click release
                elif event.type == pygame.MOUSEBUTTONUP:
                    if dragger.dragging:
                        dragger.update_mouse(event.pos)

                        released_row = dragger.mouse_y // SQ_SIZE
                        released_col = dragger.mouse_x // SQ_SIZE

                        # Create possible moves
                        initial = Square(dragger.initial_row, dragger.initial_col)
                        final = Square(released_row, released_col)
                        move = Move(initial, final)

                        # Determining if move is valid 
                        if board.valid_move(dragger.piece, move):
                            captured = board.squares[released_row][released_col].has_piece()
                            board.move(dragger.piece, move)

                            # Play sound
                            game.play_sound(captured)

                            # Show methods 
                            game.show_bg(screen)
                            game.show_last_move(screen)
                            game.show_pieces(screen)

                            # Swap turns (colour)
                            game.next_turn()

                    dragger.undrag_piece()

                # When pressing keys 
                elif event.type == pygame.KEYDOWN:

                    # Changing themes by pressing keys 
                    if event.key == pygame.K_t:
                        game.change_theme()

                    # Restart game
                    if event.key == pygame.K_r:
                        game.reset()
                        game = self.game
                        board = self.game.board 
                        dragger = self.game.dragger
                
                # Exit/quit game 
                elif event.type == pygame.QUIT: 
                    pygame.quit
                    sys.exit()

            pygame.display.update()
            
main = Main()
main.main_loop()