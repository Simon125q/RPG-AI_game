import pygame
from settings import *
from entity import Entity
from support import *
from debug import debug
from random import randint

class Enemy(Entity):
    
    def __init__(self, monster_name, pos, groups, obstacle_sprites, damage_player, trigger_death_particles, add_exp):
        super().__init__(groups)
        self.sprite_type = 'enemy'
        
        # graphics setup
        self.import_graphics(monster_name)
        self.status = 'idle'
        self.player_noticed = False
        self.image = self.animations[self.status][self.frame_index]
        
        # movement
        self.rect = self.image.get_rect(topleft = pos)
        self.hitbox = self.rect.inflate(-6, HITBOX_OFFSET['enemy'])
        self.obstacle_sprites = obstacle_sprites
        # self.change_direction = True
        self.walk_time = None
        self.walk_cooldown = 600
        self.walk_x = 0
        self.walk_y = 0
        
        # stats
        self.monster_name = monster_name
        self.monster_info = monster_data[self.monster_name]
        self.health = self.monster_info['health']
        self.exp = self.monster_info['exp']
        self.speed = self.monster_info['speed']
        self.attack_damage = self.monster_info['damage']
        self.resistance = self.monster_info['resistance']
        self.attack_radius = self.monster_info['attack_radius']
        self.notice_radius = self.monster_info['notice_radius']
        self.attack_type = self.monster_info['attack_type']
        
        # player interaction
        self.can_attack = True
        self.attack_time = None
        self.attack_cooldown = 400
        self.damage_player = damage_player
        self.trigger_death_particles = trigger_death_particles
        self.add_exp = add_exp
        
        # inbincibility timer
        self.vulnerable = True
        self.hit_time = None
        self.invincibility_duration = 400
           
    def import_graphics(self, name):
        self.animations = {'idle':[], 'move':[], 'attack':[]}
        main_path = f'./graphics/monsters/{name}/'
        for animation in self.animations.keys():
            self.animations[animation] = import_folder(main_path + animation)
    
    def get_player_direction_and_distance(self, player):
        enemy_vec = pygame.math.Vector2(self.rect.center)
        player_vec = pygame.math.Vector2(player.rect.center)
        distance = (player_vec - enemy_vec).magnitude()
        
        if distance != 0:
            direction = (player_vec - enemy_vec).normalize()
        else:
            direction = pygame.math.Vector2()
            
        return (distance, direction)
        
    def get_status(self, player):
        distance = self.get_player_direction_and_distance(player)[0]
        
        if distance <= self.attack_radius and self.can_attack:
            if self.status != "attack":
                self.frame_index = 0
            self.status = 'attack'
            self.player_noticed = True
        elif distance <= self.notice_radius:
            self.status = 'move'
            self.player_noticed = True
        else:
            self.player_noticed = False
    
    def actions(self, player):
        if self.status == 'attack':
            self.speed = self.monster_info['speed']
            self.attack_time = pygame.time.get_ticks()
            self.damage_player(self.attack_damage, self.attack_type)
        elif self.status == 'move' and self.player_noticed:
            self.speed = self.monster_info['speed']
            self.direction = self.get_player_direction_and_distance(player)[1]  
        else:
            self.speed = self.monster_info['speed'] // 2
            if self.change_direction:
                self.walk_cooldown = randint(400, 1200)
                self.walk_x = randint(-1, 1)
                self.walk_y = randint(-1, 1)
                if (self.walk_x == 0 and self.walk_y == 0) or self.monster_name == 'spirit':
                    self.status = 'idle'
                else: 
                    self.status = 'move'
                self.player_noticed = False
                self.change_direction = False
                self.walk_time = pygame.time.get_ticks()
                
            self.direction = pygame.math.Vector2(self.walk_x, self.walk_y)
    
    def animate(self):
        animation = self.animations[self.status]
        self.frame_index += self.animation_speed 
        if self.frame_index >= len(animation):
            if self.status == 'attack':
                self.can_attack = False
            self.frame_index = 0
        self.image = animation[int(self.frame_index)]
        self.rect = self.image.get_rect(center = self.hitbox.center)
        
        # flicker
        if not self.vulnerable:
            alpha = self.wave_value()
            self.image.set_alpha(alpha)
        else:
            self.image.set_alpha(255)
    
    def cooldowns(self):
        current_time = pygame.time.get_ticks()
        if not self.can_attack:
            if current_time - self.attack_time >= self.attack_cooldown:
                self.can_attack = True
        if not self.vulnerable:
            if current_time - self.hit_time >= self.invincibility_duration:
                self.vulnerable = True
        if not self.change_direction:
            if current_time - self.walk_time >= self.walk_cooldown:
                self.change_direction = True
    
    def get_damage(self, player, attack_type):
        if self.vulnerable:
            self.direction = self.get_player_direction_and_distance(player)[1]
            if attack_type == 'weapon':
                self.health -= player.get_full_weapon_damage()
            else:
                self.health -= player.get_full_magic_damage()
            self.hit_time = pygame.time.get_ticks()
            self.vulnerable = False
            self.check_death()
    
    def check_death(self):
        if self.health <= 0:
            self.kill()
            self.trigger_death_particles(self.rect.center, self.monster_name) 
            self.add_exp(self.exp)
                       
    def hit_reaction(self):
        if not self.vulnerable:
            self.direction *= -self.resistance
        
    def update(self):
        self.hit_reaction()
        self.move(self.speed)
        self.animate()
        self.cooldowns()
    
    def enemy_update(self,player):
        self.get_status(player)
        self.actions(player)