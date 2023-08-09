import pygame
from settings import *
from entity import Entity
from support import *
from debug import debug
from random import randint

class Enemy(Entity):
    
    def __init__(self, monster_name, pos, groups, obstacle_sprites, damage_player, trigger_death_particles, trigger_damage_particles, add_exp, player, level):
        super().__init__(groups)
        self.sprite_type = 'enemy'
        self.player = player
        # graphics setup
        self.import_graphics(monster_name)
        self.status = 'idle'
        self.player_noticed = False
        self.image = self.animations[self.status][self.frame_index]
        
        # movement
        self.rect = self.image.get_rect(topleft = pos)
        self.hitbox = self.rect.inflate(-6, HITBOX_OFFSET['enemy'])
        self.obstacle_sprites = obstacle_sprites
        self.collision_time = 0
        self.chase_time = randint(250, 400)
        self.change_direction = True
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
        self.trigger_damage_particles = trigger_damage_particles
        self.add_exp = add_exp
        
        # inbincibility timer
        self.vulnerable = True
        self.hit_time = None
        self.invincibility_duration = 400
        
        # sound
        self.attack_sound = pygame.mixer.Sound(self.monster_info['attack_sound'])
        self.death_sound = pygame.mixer.Sound('./audio/death.wav')
        self.hit_sound = pygame.mixer.Sound('./audio/hit.wav')
        self.attack_sound.set_volume(0.2)
        self.death_sound.set_volume(0.2)
        self.hit_sound.set_volume(0.2)
        
        # after life
        self.level = level
           
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
            self.attack_sound.play()
            self.speed = self.monster_info['speed']
            self.attack_time = pygame.time.get_ticks()
            self.damage_player(self.attack_damage, self.attack_type)
        elif self.status == 'move' and self.player_noticed:
            self.speed = self.monster_info['speed']  
            self.direction = self.get_player_direction_and_distance(player)[1]
            if self.collided:
                self.collision_time = pygame.time.get_ticks()
                
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
        if self.collided:
            if current_time - self.collision_time >= self.chase_time:
                self.collided = False
                self.collision_time = 0
    
    def get_damage(self, player, attack_type):
        if self.vulnerable:
            self.hit_sound.play()
            self.direction = self.get_player_direction_and_distance(player)[1]
            if attack_type == 'weapon':
                damage = player.get_full_weapon_damage()
            else:
                damage = player.get_full_magic_damage()
            self.health -= damage
            self.hit_time = pygame.time.get_ticks()
            self.invincibility_duration = 200 + weapon_data[self.player.weapon]['cooldown']
            self.vulnerable = False
            self.trigger_damage_particles(self.rect.center, str(damage))
            self.check_death()
    
    def display_damage(self, damage):
        debug(str(damage), self.rect.x + 20, self.rect.y + 20)
    
    def check_death(self):
        if self.health <= 0:
            self.death_sound.play()
            if self.monster_name != 'undead_skeleton':
                Enemy('undead_skeleton',
                        (self.rect.x, self.rect.y),
                        [self.level.visible_sprites, self.level.attackable_sprites],
                        self.level.obstacle_sprites,
                        self.level.damage_player,
                        self.level.trigger_death_particles,
                        self.level.trigger_damage_particles,
                        self.level.add_xp,
                        self.player,
                        self.level)
            self.kill()
            
            self.trigger_death_particles(self.rect.center, self.monster_name) 
            self.add_exp(self.exp)
                       
    def hit_reaction(self):
        if not self.vulnerable:
            self.direction *= -self.resistance
        
    def update(self):
        if abs(self.rect.x - self.player.rect.x) < WIDTH//2 + 40 and abs(self.rect.y - self.player.rect.y) < HEIGHT//2 + 80:
            self.hit_reaction()
            self.move(self.speed)
            self.animate()
            self.cooldowns()
    
    def enemy_update(self,player):
        self.get_status(player)
        self.actions(player)