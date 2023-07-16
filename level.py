import pygame
from support import *
from settings import *
from tile import Tile
from player import Player
from debug import debug
from random import choice
from weapon import Weapon

class Level:
    def __init__(self):
        
        # get the display surface
        self.display_surface = pygame.display.get_surface()
        
        # sprite group setup
        self.visible_sprites = YsortCameraGroup()
        self.obstacle_sprites = pygame.sprite.Group()
        
        # attack sprites
        self.current_attack = None
        # sprites setup
        self.create_map()
        
    def create_map(self):
        layouts = {
            'boundary': import_csv_layout('./map/map_FloorBlocks.csv'),
            'grass': import_csv_layout('./map/map_Grass.csv'),
            'object': import_csv_layout('./map/map_Objects.csv')
        }
        graphics = {
            'grass': import_folder('./graphics/grass'),
            'objects': import_folder('./graphics/objects')
        }
        for style, layout in layouts.items():
            for row_index, row in enumerate(layout):
                for col_index, col in enumerate(row):
                    if col != '-1':
                        x = col_index * TILESIZE
                        y = row_index * TILESIZE
                        if style == 'boundary':
                            Tile((x,y), [self.obstacle_sprites], "invisible")
                        if style == 'grass':
                            random_grass = choice(graphics['grass'])
                            Tile((x,y), [self.visible_sprites, self.obstacle_sprites], 'grass', random_grass)
                        if style == 'object':
                            surf = graphics['objects'][int(col)]
                            Tile((x,y), [self.visible_sprites, self.obstacle_sprites], 'object', surf)
                            
        self.player = Player((2000, 1440), [self.visible_sprites], self.obstacle_sprites, self.create_attack, self.destroy_attack)
    
    def destroy_attack(self):
        if self.current_attack:
            self.current_attack.kill()
        self.current_attack = None
        
    def create_attack(self):
        self.current_attack = Weapon(self.player, [self.visible_sprites])
        
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
        
        # create the floor
        self.floor_surf = pygame.image.load('./graphics/tilemap/ground.png').convert()
        self.floor_rect = self.floor_surf.get_rect(topleft = (0, 0))
        
    def custom_draw(self, player):
        
        self.offset.y = self.half_height - player.rect.centery
        self.offset.x = self.half_width - player.rect.centerx
        
        #draw floor
        floor_offset_pos = self.floor_rect.topleft + self.offset
        self.display_surface.blit(self.floor_surf, floor_offset_pos)
        
        for sprite in sorted(self.sprites(), key = lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft + self.offset
            self.display_surface.blit(sprite.image, offset_pos)