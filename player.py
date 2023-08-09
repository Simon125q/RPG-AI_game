import pygame
from settings import *
from random import randint
from support import import_folder
from entity import Entity

MOUSE_LEFT = 0
MOUSE_RIGHT = 2

class Player(Entity):
    
    def __init__(self, pos, groups, obstacle_sprites, create_attack, destroy_attack, create_magic, footstep_particles):
        super().__init__(groups)
        self.image = pygame.image.load('./graphics/test/player.png').convert_alpha()
        self.rect = self.image.get_rect(topleft = pos)
        # set graphics
        self.import_player_assets()
        self.status = "down"
        self.footstep_particles = footstep_particles
        # movement
        self.obstacle_sprites = obstacle_sprites
        self.attacking = False
        self.attack_cooldown = 400
        self.attack_time = None
        self.footstep = True
        self.step_time = None
        self.step_duration = 120
        # player hitbox
        self.hitbox = self.rect.inflate(-5, HITBOX_OFFSET['player'])
        # weapon
        self.create_attack = create_attack
        self.destroy_attack = destroy_attack
        self.weapon_index = 0
        self.weapon = list(weapon_data.keys())[self.weapon_index]
        self.can_switch_weapon = True
        self.weapon_switch_time = None
        self.switch_duration_cooldown = 200
        # magic
        self.create_magic = create_magic
        self.magic_index = 0
        self.magic = list(magic_data.keys())[self.magic_index]
        self.can_switch_magic = True
        self.magic_switch_time = None
        # stats
        self.stats = {'health': 100, 'energy': 60, 'attack': 10, 'magic': 4, 'speed': 5}
        self.max_stats = {'health': 300, 'energy': 140, 'attack': 20, 'magic': 10, 'speed': 7}
        self.upgrade_cost = {'health': 100, 'energy': 100, 'attack': 100, 'magic': 100, 'speed': 100}
        self.health = self.stats['health']
        self.energy = self.stats['energy']
        self.exp = 500
        self.speed = self.stats['speed']
        # damage timer
        self.vulnerable = True
        self.hurt_time = None
        self.invulnerability_duration = 500
        # import sound
        self.weapon_attack_sound = pygame.mixer.Sound('./audio/sword.wav')
        self.weapon_attack_sound.set_volume(0.1)
        
    def import_player_assets(self):
        character_path = './graphics/player/'
        self.animations = {'up': [], 'down': [], 'left': [], 'right': [], 'right_idle': [],
                           'left_idle': [], 'up_idle': [], 'down_idle': [], 'right_attack': [],
                           'left_attack': [], 'up_attack': [], 'down_attack': [],}
        
        for animation in self.animations.keys():
            self.animations[animation] = import_folder(character_path + animation)
        
    def input(self):
        if not self.attacking:
            # movement input
            keys = pygame.key.get_pressed()
            mouse = pygame.mouse.get_pressed(num_buttons=5)
            
            if keys[pygame.K_UP] or keys[pygame.K_w]:
                self.direction.y = -1
                self.status = 'up'
                if self.footstep:
                    self.step_time = pygame.time.get_ticks()
                    self.footstep = False
                    self.footstep_particles(self.rect.center - pygame.math.Vector2(0, -30), "up")
                
            elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
                self.direction.y = 1
                self.status = 'down'
                if self.footstep:
                    self.step_time = pygame.time.get_ticks()
                    self.footstep = False
                    self.footstep_particles(self.rect.center - pygame.math.Vector2(0, 30), "down")
                    
            else: self.direction.y = 0
                
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                self.direction.x = 1
                if self.direction.y == 1:
                    self.status = 'down'
                elif self.direction.y == -1:
                    self.status = 'up'
                else:
                    self.status = 'right'
                if self.footstep:
                    self.step_time = pygame.time.get_ticks()
                    self.footstep = False
                    self.footstep_particles(self.rect.center - pygame.math.Vector2(30, 0), "right")
                    
            elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
                self.direction.x = -1
                if self.direction.y == 1:
                    self.status = 'down'
                elif self.direction.y == -1:
                    self.status = 'up'
                else:
                    self.status = 'left'
                if self.footstep:
                    self.step_time = pygame.time.get_ticks()
                    self.footstep = False
                    self.footstep_particles(self.rect.center - pygame.math.Vector2(-30, 0), "left")
                    
            else: self.direction.x = 0
            
            if keys[pygame.K_LSHIFT]:
                self.speed = self.stats['speed'] + 4
            else:
                self.speed = self.stats['speed']
            
            # attack input
            if mouse[MOUSE_LEFT] or keys[pygame.K_f]:
                self.attacking = True
                self.attack_time = pygame.time.get_ticks()
                self.create_attack()
                self.weapon_attack_sound.play()
                
            # magic input
            if mouse[MOUSE_RIGHT] or keys[pygame.K_e]:
                self.attacking = True
                self.attack_time = pygame.time.get_ticks()
                style = list(magic_data.keys())[self.magic_index]
                strength = list(magic_data.values())[self.magic_index]['strength'] + self.stats['magic']
                cost = list(magic_data.values())[self.magic_index]['cost']
                self.create_magic(style, strength, cost)
            
            # magic choosing
            if (keys[pygame.K_q]) and self.can_switch_magic:
                self.can_switch_magic = False
                self.magic_switch_time = pygame.time.get_ticks()
                if self.magic_index < len(list(magic_data.keys())) - 1:
                    self.magic_index += 1
                else:
                    self.magic_index = 0
                self.magic = list(magic_data.keys())[self.magic_index]
                
            # weapon choosing
            if mouse[1] and self.can_switch_weapon:
                self.can_switch_weapon = False
                self.weapon_switch_time = pygame.time.get_ticks()
                if self.weapon_index < len(list(weapon_data.keys())) - 1:
                    self.weapon_index += 1
                else:
                    self.weapon_index = 0
                self.weapon = list(weapon_data.keys())[self.weapon_index]
            
            if keys[pygame.K_1]:
                self.weapon_index = 0
                self.weapon = list(weapon_data.keys())[self.weapon_index]
            elif keys[pygame.K_2]:
                self.weapon_index = 1
                self.weapon = list(weapon_data.keys())[self.weapon_index]
            elif keys[pygame.K_3]:
                self.weapon_index = 2
                self.weapon = list(weapon_data.keys())[self.weapon_index]
            elif keys[pygame.K_4]:
                self.weapon_index = 3
                self.weapon = list(weapon_data.keys())[self.weapon_index]
            elif keys[pygame.K_5]:
                self.weapon_index = 4
                self.weapon = list(weapon_data.keys())[self.weapon_index]
                           
    def get_status(self):
        # idle status
        if self.direction.x == 0 and self.direction.y == 0:
            if not 'idle' in self.status and not 'attack' in self.status:
                self.status = self.status + '_idle'
        # attack status
        if self.attacking:
            self.direction.x = 0
            self.direction.y = 0
            if not 'attack' in self.status:
                if 'idle' in self.status:
                    self.status = self.status.replace('_idle', '_attack')
                else:
                    self.status = self.status + '_attack'
        
    def cooldowns(self):
        current_time = pygame.time.get_ticks()
        
        if self.attacking:
            if current_time - self.attack_time >= self.attack_cooldown + weapon_data[self.weapon]['cooldown']:
                self.attacking = False
                self.destroy_attack()
                self.status = self.status.replace('_attack', '_idle')
                
        if not self.can_switch_weapon:
            if current_time - self.weapon_switch_time >= self.switch_duration_cooldown:
                self.can_switch_weapon = True
                
        if not self.can_switch_magic:
            if current_time - self.magic_switch_time >= self.switch_duration_cooldown:
                self.can_switch_magic = True
                
        if not self.vulnerable:
            if current_time - self.hurt_time >= self.invulnerability_duration:
                self.vulnerable = True
                
        if not self.footstep:
            if current_time - self.step_time >= self.step_duration:
                self.footstep = True
                      
    def animate(self):
        animation = self.animations[self.status]
        
        #loop over the frame index
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0
        
        # set image
        self.image = animation[int(self.frame_index)]
        self.rect = self.image.get_rect(center = self.hitbox.center)

        # flicker
        if not self.vulnerable:
            alpha = self.wave_value()
            self.image.set_alpha(alpha)
        else:
            self.image.set_alpha(255)
            
    def get_full_weapon_damage(self):
        base_damage = self.stats["attack"]
        weapon_damage = randint(weapon_data[self.weapon]['min_damage'], weapon_data[self.weapon]['max_damage'])
        #weapon_damage = weapon_data[self.weapon]['damage']
        return base_damage + weapon_damage
    
    def get_full_magic_damage(self):
        base_damage = self.stats['magic']
        spell_damage = magic_data[self.magic]['strength']
        return base_damage + spell_damage
        
    def get_value_by_index(self, index):
        return list(self.stats.values())[index]
        
    def get_cost_by_index(self, index):
        return list(self.upgrade_cost.values())[index]
    
    def energy_recovery(self):
        if self.energy < self.stats['energy']:
            self.energy += 0.01 * self.stats['magic'] * 0.8
        else:
            self.energy = self.stats['energy']
            
    def update(self):
        self.input()
        self.cooldowns()
        self.get_status()
        self.animate()
        self.move(self.speed)
        self.energy_recovery()