import pygame
from support import import_folder
from random import choice, randint
from debug import debug

class AnimationPlayer:
    
    def __init__(self):
        self.frames = {
			# magic
			'flame': (import_folder('./graphics/particles/flame/frames'),),
			'aura': (import_folder('./graphics/particles/aura'),),
			'heal': (import_folder('./graphics/particles/heal/frames'),),
			
			# attacks 
			'claw': (import_folder('./graphics/particles/claw'), 
            	self.reflect_images(import_folder('./graphics/particles/claw'))),
			'slash': (import_folder('./graphics/particles/slash'), 
             	self.reflect_images(import_folder('./graphics/particles/slash'))),
			'sparkle': (import_folder('./graphics/particles/sparkle'), 
               	self.reflect_images(import_folder('./graphics/particles/sparkle'))),
			'leaf_attack': (import_folder('./graphics/particles/leaf_attack'), 
                self.reflect_images(import_folder('./graphics/particles/leaf_attack'))),
			'thunder': (import_folder('./graphics/particles/thunder'), 
               	self.reflect_images(import_folder('./graphics/particles/thunder'))),

			# monster deaths
			'squid': (import_folder('./graphics/particles/smoke_orange'),),
			'raccoon': (import_folder('./graphics/particles/raccoon'),),
			'spirit': (import_folder('./graphics/particles/nova'),),
   			'big_frog': (import_folder('./graphics/particles/nova'),),
      		'giant_flam': (import_folder('./graphics/particles/nova'),),
        	'giant_spirit': (import_folder('./graphics/particles/nova'),),
			'bamboo': (import_folder('./graphics/particles/bamboo'),),
			'eye': (import_folder('./graphics/particles/smoke_orange'),),
			'flam': (import_folder('./graphics/particles/nova'),),
			'mushroom': (import_folder('./graphics/particles/bamboo'),),
			'octopus': (import_folder('./graphics/particles/smoke_orange'),),
			'skeleton': (import_folder('./graphics/particles/smoke_orange'),),
   			'undead_skeleton': (import_folder('./graphics/particles/smoke_orange'),),
			'skull': (import_folder('./graphics/particles/nova'),),
			'slime': (import_folder('./graphics/particles/smoke_orange'),),
			'cyclop': (import_folder('./graphics/particles/smoke_orange'),),
   			'giant_raccoon': (import_folder('./graphics/particles/raccoon'),),
			
			# leafs 
			'leaf': (
				import_folder('./graphics/particles/leaf1'),
				import_folder('./graphics/particles/leaf2'),
				import_folder('./graphics/particles/leaf3'),
				import_folder('./graphics/particles/leaf4'),
				import_folder('./graphics/particles/leaf5'),
				import_folder('./graphics/particles/leaf6'),
				self.reflect_images(import_folder('./graphics/particles/leaf1')),
				self.reflect_images(import_folder('./graphics/particles/leaf2')),
				self.reflect_images(import_folder('./graphics/particles/leaf3')),
				self.reflect_images(import_folder('./graphics/particles/leaf4')),
				self.reflect_images(import_folder('./graphics/particles/leaf5')),
				self.reflect_images(import_folder('./graphics/particles/leaf6'))
				),
   
			# footsteps
			'footstep_up': (import_folder('./graphics/particles/footsteps/up'),),
			'footstep_down': (import_folder('./graphics/particles/footsteps/down'),),
			'footstep_right': (import_folder('./graphics/particles/footsteps/right'),),
			'footstep_left': (import_folder('./graphics/particles/footsteps/left'),)
			}
    
    def reflect_images(self, frames):
        new_frames = []
        
        for frame in frames:
            fliped_frame = pygame.transform.flip(frame, True, False)
            new_frames.append(fliped_frame)
        return new_frames
    
    def create_grass_particles(self, pos, groups):
        animation_frames = choice(self.frames['leaf'])
        ParticleEffect(pos, animation_frames, groups, 'leaf')
    
    def create_particles(self, animation_type, pos, groups, sprite_type):
        animation_frames = choice(self.frames[animation_type])
        ParticleEffect(pos, animation_frames, groups, sprite_type)
    
    
class ParticleEffect(pygame.sprite.Sprite):
    
    def __init__(self, pos, animation_frames, groups, sprite_type):
        super().__init__(groups)
        self.sprite_type = sprite_type
        self.frame_index = 0
        self.animation_speed = 0.15
        self.frames = animation_frames
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect(center = pos)
        
    def animate(self):
        self.frame_index += self.animation_speed
        if self.frame_index >= len(self.frames):
            self.kill()
        else:
            self.image = self.frames[int(self.frame_index)]
            
    def update(self):
        self.animate()