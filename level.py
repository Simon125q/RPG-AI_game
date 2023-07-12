import pygame
from settings import *
from tile import Tile
from player import Player
from debug import debug

class Level:
    def __init__(self):
        
        #get the display surface
        self.display_surface = pygame.display.get_surface()
        
        #sprite group setup
        self.visible_sprites = YsortCameraGroup()
        self.obstacle_sprites = pygame.sprite.Group()

        self.create_map()
        
    def create_map(self):
        for row_index, raw in enumerate(WORLD_MAP):
            for col_index, col in enumerate(raw):
                x = col_index * TILESIZE
                y = row_index * TILESIZE
                if col == '#':
                    # print rock
                    Tile((x,y), [self.visible_sprites, self.obstacle_sprites])
                if col == 'p':
                    # print player
                    self.player = Player((x, y), [self.visible_sprites], self.obstacle_sprites)
                
    def run(self):
        #update and draw the game
        
        self.visible_sprites.custom_draw(self.player)
        self.visible_sprites.update()
        
class YsortCameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.half_width = self.display_surface.get_size()[0]//2
        self.half_height = self.display_surface.get_size()[1]//2
        self.offset = pygame.math.Vector2()
        
    def custom_draw(self, player):
        
        self.offset.y = self.half_height - player.rect.centery
        self.offset.x = self.half_width - player.rect.centerx
        
        for sprite in sorted(self.sprites(), key = lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft + self.offset
            self.display_surface.blit(sprite.image, offset_pos)