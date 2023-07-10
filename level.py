import pygame
from settings import *
from tile import Tile
from player import Player

class Level:
    def __init__(self):
        
        #get the display surface
        self.display_surface = pygame.display.get_surface()
        
        #sprite group setup
        self.visible_sprites = pygame.sprite.Group()
        self.obstacle_sprites = pygame.sprite.Group()
        
        
    def create_map(self):
        for row_index, raw in enumerate(WORLD_MAP):
            for col_index, col in enumerate(raw):
                x = row_index * TILESIZE
                y = col_index * TILESIZE
                if col == 'x':
                    # print rock
                    Tile((x,y), [self.visible_sprites, self.obstacle_sprites])
                elif col == 'P':
                    # print player
                    self.player = Player((x, y), [self.visible_sprites], self.obstacle_sprites)
                
                
        
    def run(self):
        #update and draw the game
        self.visible_sprites.draw(self.display_surface)
        self.visible_sprites.update()