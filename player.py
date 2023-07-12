import pygame
from settings import *
import math

X = 0
Y = 1

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, obstacle_sprites):
        super().__init__(groups)
        self.image = pygame.image.load('C:/Users/szomi/Dropbox/Komputer/Documents/GitHub/AIgame/graphics/test/player.png').convert_alpha()
        self.rect = self.image.get_rect(topleft = pos)
        self.direction = [0, 0]
        self.speed = 5
        self.obstacle_sprites = obstacle_sprites
        self.hitbox = self.rect.inflate(-1, -26)
    def input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            self.direction[Y] = -1
        elif keys[pygame.K_DOWN]:
            self.direction[Y] = 1
        else: self.direction[Y] = 0
            
        if keys[pygame.K_RIGHT]:
            self.direction[X] = 1
        elif keys[pygame.K_LEFT]:
            self.direction[X] = -1
        else: self.direction[X] = 0
    
    def collision(self, direction):
        if direction == "horizontal":
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction[X] > 0:
                        self.hitbox.right = sprite.hitbox.left
                    if self.direction[X] < 0:
                        self.hitbox.left = sprite.hitbox.right
        
        if direction == "vertical":
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                        if self.direction[Y] > 0:
                            self.hitbox.bottom = sprite.hitbox.top
                        if self.direction[Y] < 0:
                            self.hitbox.top = sprite.hitbox.bottom
            
    def move(self, speed):
        magnitude = math.sqrt(self.direction[X]*self.direction[X]+self.direction[Y]*self.direction[Y])
        if magnitude != 0:
            self.direction = [self.direction[X]/magnitude, self.direction[Y]/magnitude] 
            
        self.hitbox.x += self.direction[X] * speed
        self.collision("horizontal")
        self.hitbox.y += self.direction[Y] * speed
        self.collision("vertical")
        self.rect.center = self.hitbox.center
        
    def update(self):
        self.input()
        self.move(self.speed)