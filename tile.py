import pygame
from settings import *

class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, groups, sprite_type, surface = pygame.Surface((TILESIZE, TILESIZE))):
        super().__init__(groups)
        self.sprite_type = sprite_type
        self.image = surface
        if sprite_type == "object":
            self.rect = self.image.get_rect(topleft = (pos[0], pos[1] - TILESIZE))
            self.hitbox = self.rect.inflate(-12, -34)
        else:
            self.rect = self.image.get_rect(topleft = pos)
            if sprite_type == "invisible":
                self.hitbox = self.rect.inflate(-22, -30)
            else:
                self.hitbox = self.rect.inflate(-6, -10)