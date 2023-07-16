import pygame
from pygame.sprite import AbstractGroup

class Weapon(pygame.sprite.Sprite):
    def __init__(self, player, groups):
        super().__init__(groups)
        diretction = player.status.split('_')[0]
        
        # graphics
        path = f'./graphics/weapons/{player.weapon}/{diretction}.png'
        self.image = pygame.image.load(path).convert_alpha()
        
        # placement
        if diretction == 'right':
            self.rect = self.image.get_rect(midleft = player.rect.midright + pygame.math.Vector2(0, 16))
        elif diretction == 'left':
            self.rect = self.image.get_rect(midright = player.rect.midleft + pygame.math.Vector2(0, 16))
        elif diretction == 'up':
            self.rect = self.image.get_rect(midbottom = player.rect.midtop + pygame.math.Vector2(-10, 0))
        elif diretction == 'down':
            self.rect = self.image.get_rect(midtop = player.rect.midbottom + pygame.math.Vector2(-10, 0))
            