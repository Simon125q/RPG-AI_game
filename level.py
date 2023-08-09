import pygame
from support import *
from settings import *
from tile import Tile
from player import Player
from debug import debug
from random import choice, randint
from weapon import Weapon
from ui import UI
from enemy import Enemy
from particles import AnimationPlayer
from magic import PlayerMagic
from upgrade import Upgrade
from dialogs import Dialog_box


class Level:
    
    def __init__(self):
       
        # get the display surface
        self.display_surface = pygame.display.get_surface()
        self.game_paused = False
        # sprite group setup
        self.visible_sprites = YsortCameraGroup()
        self.obstacle_sprites = pygame.sprite.Group()
        # attack sprites
        self.current_attack = None
        self.attack_sprites = pygame.sprite.Group()
        self.attackable_sprites = pygame.sprite.Group()
        # dialogs
        self.dialog_box = Dialog_box(self)
        self.dialog_pause = False
        self.dialog_spots = []
        self.dialog_topic = 'TEST'
        # sprites setup
        self.create_map()
        # user interface
        self.ui = UI()
        self.upgrade = Upgrade(self.player)
        # particles
        self.animation_player = AnimationPlayer()
        self.magic_player = PlayerMagic(self.animation_player)
        # player 
        self.player_death = False
        
    
    def create_map(self):
        self.player = Player(PLAYER_POS,
                            [self.visible_sprites], 
                            self.obstacle_sprites, 
                            self.create_attack, 
                            self.destroy_attack,
                            self.create_magic,
                            self.footstep_particles)
        layouts = {
            'boundary': import_csv_layout('./map/map_FloorBlocks.csv'),
            'grass': import_csv_layout('./map/map_Grass.csv'),
            'object': import_csv_layout('./map/map_Objects.csv'),
            'entities': import_csv_layout('./map/map_Entities.csv')
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
                            Tile((x,y),
                                 [self.visible_sprites, self.obstacle_sprites, self.attackable_sprites],
                                 'grass',
                                 random_grass)
                        if style == 'object':
                            surf = graphics['objects'][int(col)]
                            Tile((x,y),
                                 [self.visible_sprites, self.obstacle_sprites],
                                 'object',
                                 surf)
                        if style == 'entities':
                            if col == PLAYER:               
                                self.dialog_spots.append((x, y, 'START'))
                            else:
                                if col == BAMBOO: monster_name = 'bamboo'
                                elif col == SPIRIT: monster_name = 'spirit'
                                elif col == RACCOON: 
                                    monster_name = 'raccoon'
                                elif col == BIG_FROG: 
                                    monster_name = 'big_frog'
                                    self.dialog_spots.append((x, y, 'boss_frog'))
                                    self.dialog_spots.append((x, y, 'narrator_boss_frog'))
                                elif col == GIANT_FLAM: 
                                    monster_name = 'giant_flam'
                                    self.dialog_spots.append((x, y, 'boss_flam'))
                                    self.dialog_spots.append((x, y, 'narrator_boss_flam'))
                                elif col == GIANT_SPIRIT: 
                                    monster_name = 'giant_spirit'
                                    self.dialog_spots.append((x, y, 'boss_spirit'))
                                    self.dialog_spots.append((x, y, 'narrator_boss_spirit'))
                                elif col == EYE: monster_name = 'eye'
                                elif col == FLAM: monster_name = 'flam'
                                elif col == MUSHROOM: monster_name = 'mushroom'
                                elif col == OCTOPUS: monster_name = 'octopus'
                                elif col == SKELETON: monster_name = 'skeleton'
                                elif col == SKULL: monster_name = 'skull'
                                elif col == SLIME: monster_name = 'slime'
                                elif col == CYCLOP: monster_name = 'cyclop'
                                elif col == GIANT_RACCOON: 
                                    monster_name = 'giant_raccoon'
                                    self.dialog_spots.append((x, y, 'boss_raccoon'))
                                    self.dialog_spots.append((x, y, 'narrator_boss_raccoon'))
                                else : monster_name = 'squid'
                                Enemy(monster_name,
                                      (x,y),
                                      [self.visible_sprites, self.attackable_sprites],
                                      self.obstacle_sprites,
                                      self.damage_player,
                                      self.trigger_death_particles,
                                      self.trigger_damage_particles,
                                      self.add_xp,
                                      self.player,
                                      self)
    
    def check_dialogs(self):
        if self.dialog_spots == []:
            self.dialog_box.messages = []
            self.dialog_pause = True
            self.dialog_topic = 'END'
        for location in self.dialog_spots:
            if abs(location[0] - self.player.rect.x) < 170 and abs(location[1] - self.player.rect.y) < 170:
                for loc in self.dialog_spots:
                    if loc[2] == location[2]:
                        self.dialog_spots.remove(loc)
                self.dialog_pause = True
                self.dialog_box.messages = []
                self.dialog_topic = location[2]
            elif abs(location[0] - self.player.rect.x) < 350 and abs(location[1] - self.player.rect.y) < 350 and location[2].split('_')[0] == 'narrator':
                for loc in self.dialog_spots:
                    if loc[2] == location[2]:
                        self.dialog_spots.remove(loc)
                self.dialog_box.messages = []
                self.dialog_pause = True
                self.dialog_topic = location[2]
                
                      
    def destroy_attack(self):
        if self.current_attack:
            self.current_attack.kill()
        self.current_attack = None
        
    def create_attack(self):
        self.current_attack = Weapon(self.player, [self.visible_sprites, self.attack_sprites])
    
    def create_magic(self, style, strength, cost):
        if style == 'heal':
            self.magic_player.heal(self.player, strength, cost, [self.visible_sprites])
        elif style == 'flame':
            self.magic_player.flame(self.player, cost, [self.visible_sprites, self.attack_sprites])
        
    def player_attack_logic(self):
        if self.attack_sprites:
            for attack_sprite in self.attack_sprites:
                collision_sprites = pygame.sprite.spritecollide(attack_sprite, self.attackable_sprites, False)
                if collision_sprites:
                    for target_sprite in collision_sprites:
                        if target_sprite.sprite_type == 'grass':
                            pos = target_sprite.rect.center
                            offset = pygame.math.Vector2(0, 50)
                            for leaf in range(randint(3,6)):
                                self.animation_player.create_grass_particles(pos - offset, [self.visible_sprites])
                            target_sprite.kill()
                        else:
                            target_sprite.get_damage(self.player, attack_sprite.sprite_type)
    
    def check_if_alive(self):
        if self.player.health <= 0:
            self.player_death = True
      
    def damage_player(self, amount, attack_type):
        if self.player.vulnerable:
            self.player.health -= amount
            self.player.vulnerable = False
            self.player.hurt_time = pygame.time.get_ticks()
            self.animation_player.create_particles(attack_type, self.player.rect.center, [self.visible_sprites], 'damage')
    
    def trigger_death_particles(self, pos, particle_type):
        self.animation_player.create_particles(particle_type, pos, [self.visible_sprites], 'death')
        
    def trigger_damage_particles(self, pos, damage):
        debug(damage)
        
    def footstep_particles(self, pos, direction):
        if direction == 'up':
            self.animation_player.create_particles('footstep_up', pos, [self.visible_sprites], 'footstep')
        elif direction == 'down':
            self.animation_player.create_particles('footstep_down', pos, [self.visible_sprites], 'footstep')
        elif direction == 'right':
            self.animation_player.create_particles('footstep_right', pos, [self.visible_sprites], 'footstep')
        else:
            self.animation_player.create_particles('footstep_left', pos, [self.visible_sprites], 'footstep')
                
    def add_xp(self, amount):
        self.player.exp += amount
                
    def toggle_menu(self):
        self.game_paused = not self.game_paused
         
    def run(self):
        self.visible_sprites.custom_draw(self.player)
        self.ui.display(self.player)
        self.check_dialogs()
        
        if self.game_paused:
            self.upgrade.display()
        elif self.dialog_pause:
            self.dialog_box.display(self.dialog_topic)
        else:
            self.visible_sprites.update()
            self.visible_sprites.enemy_update(self.player)
            self.check_if_alive()
            self.player_attack_logic()
        
        
class YsortCameraGroup(pygame.sprite.Group):
    
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.half_width = self.display_surface.get_size()[0]//2
        self.half_height = self.display_surface.get_size()[1]//2
        self.offset = pygame.math.Vector2()
        
        # create the floor
        self.floor_surf = pygame.image.load('./graphics/tilemap/final_map.png').convert()
        self.floor_rect = self.floor_surf.get_rect(topleft = (0, 0))
        
    def custom_draw(self, player):
        
        self.offset.y = self.half_height - player.rect.centery
        self.offset.x = self.half_width - player.rect.centerx
        
        #draw floor
        floor_offset_pos = self.floor_rect.topleft + self.offset
        self.display_surface.blit(self.floor_surf, floor_offset_pos)
        
        for sprite in sorted(self.sprites(), key = lambda sprite: sprite.rect.centery):
            if abs(sprite.rect.x - player.rect.x) < WIDTH//2 + 40 and abs(sprite.rect.y - player.rect.y) < HEIGHT//2 + 80:
                offset_pos = sprite.rect.topleft + self.offset
                self.display_surface.blit(sprite.image, offset_pos)
            
    def enemy_update(self,player):
        enemy_sprites = [sprite for sprite in self.sprites() if hasattr(sprite,'sprite_type') and sprite.sprite_type == 'enemy']
        
        for enemy in enemy_sprites:
            if abs(enemy.rect.x - player.rect.x) < WIDTH//2 + 40 and abs(enemy.rect.y - player.rect.y) < HEIGHT//2 + 40:
                enemy.enemy_update(player)