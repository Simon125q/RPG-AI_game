import pygame
from settings import *
from random import randint


class PlayerMagic:
    
    def __init__(self, animation_player):
        self.animation_player = animation_player
        self.sounds = {
            'heal': pygame.mixer.Sound('./audio/heal.wav'),
            'flame': pygame.mixer.Sound('./audio/flame.wav')
        }
        self.sounds['flame'].set_volume(0.8)
        self.sounds['heal'].set_volume(0.8)
        
    def heal(self, player, strength, cost, groups):
        if player.energy >= cost:
            self.sounds['heal'].play()
            player.health += strength
            player.energy -= cost
            if player.health >= player.stats['health']:
                player.health = player.stats['health']
            self.animation_player.create_particles('aura', player.rect.center, groups, 'heal')
            self.animation_player.create_particles('heal', player.rect.center, groups, 'heal')
    
    def flame(self, player, cost, groups):
        if player.energy >= cost:
            self.sounds['flame'].play()
            player.energy -= cost
            if player.status.split('_')[0] == 'right': flame_direction = pygame.math.Vector2(1, 0)
            elif player.status.split('_')[0] == 'left': flame_direction = pygame.math.Vector2(-1, 0)
            elif player.status.split('_')[0] == 'up': flame_direction = pygame.math.Vector2(0, -1)
            else: flame_direction = pygame.math.Vector2(0, 1)
            
            for i in range(1, 6):
                if flame_direction.x:
                    offset_x = flame_direction.x * i * TILESIZE
                    x = player.rect.centerx + offset_x + randint(-TILESIZE // 3, TILESIZE // 3)
                    y = player.rect.centery + randint(-TILESIZE // 3, TILESIZE // 3)
                    self.animation_player.create_particles('flame', (x, y), groups, 'flame')
                else:
                    offset_y = flame_direction.y * i * TILESIZE
                    x = player.rect.centerx + randint(-TILESIZE // 3, TILESIZE // 3)
                    y = player.rect.centery + offset_y + randint(-TILESIZE // 3, TILESIZE // 3)
                    self.animation_player.create_particles('flame', (x, y), groups, 'flame')

    def ligthning(self, player, cost, groups):
        pass            