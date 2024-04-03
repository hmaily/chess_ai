import pygame
from const import *

class Dragger:
    def __init__(self):
        self.piece = None
        self.dragging = False 
        self.mouse_x = 0
        self.mouse_y = 0
        self.initial_row = 0
        self.initial_col = 0
    
    # Blit methods

    # Update the visual position of the piece while dragging 
    def update_blit(self, surface): 
        # Image 
        self.piece.set_image(size=128) # Image size is larger when dragging
        image = self.piece.image

        # Img
        img = pygame.image.load(image)

        # Rect
        img_center = (self.mouse_x, self.mouse_y)
        self.piece.image_rect = img.get_rect(center=img_center)

        # Update blit
        surface.blit(img, self.piece.image_rect)

    # Other methods 

    def update_mouse(self, pos):
        self.mouse_x, self. mouse_y = pos # pos = (x_cor, y_cor)

    def save_initial(self, pos):
        self.initial_row = pos[1] // SQ_SIZE
        self.initial_col = pos[0] // SQ_SIZE

    def drag_piece(self, piece):
        self.piece = piece 
        self.dragging = True 

    def undrag_piece(self):
        #self.piece.set_image(size=80) # Can also set this in show_pieces method after checking if piece is being dragged and before blitting the image 
        self.piece = None
        self.dragging = False
