import pygame
from settings import *
import math

X = 0
Y = 1

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, obstacle_sprites):
        super().__init__(groups)
        self.image = pygame.image.load('../graphics/test/player.jpg').convert_alpha()
        self.rect = self.image.get_rect(topleft = pos)
        self.direction = [0, 0]
        self.speed = 5
        self.obstacle_sprites = obstacle_sprites
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
                if sprite.rect.colliderect(self.rect):
                    if self.direction[X] > 0:
                        self.rect.right = sprite.rect.left
                    if self.direction[X] < 0:
                        self.rect.left = sprite.rect.right
        
        if direction == "vertical":
            if sprite.rect.colliderect(self.rect):
                    if self.direction[Y] > 0:
                        self.rect.bottom = sprite.rect.top
                    if self.direction[Y] < 0:
                        self.rect.top = sprite.rect.bottom
            
    def move(self, speed):
        magnitude = math.sqrt(self.direction[X]*self.direction[X]+self.direction[Y]*self.direction[Y])
        if magnitude != 0:
            self.direction = [self.direction[X]/magnitude, self.direction[Y]/magnitude] 
        self.rect.x += self.direction[X] * speed
        self.collision("horizontal")
        self.rect.y += self.direction[Y] * speed
        self.collision("vertical")
    def update(self):
        self.input()
        self.move(self.speed)