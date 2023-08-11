import pygame

pygame.init()

screens = pygame.display.get_desktop_sizes()
WIDTH, HEIGHT = screens[0]
GAME_NAME = "AI game"
FPS = 60
TILESIZE = 64
HITBOX_OFFSET = {
	'player': -30,
	'object': -42,
	'grass': -14,
	'invisible': -32,
	'enemy': -16
}

# Map spowns
PLAYER_POS = (1919,4678)
PLAYER = '13'
BAMBOO = '14'
SPIRIT = '16'
RACCOON = '15'
GIANT_RACCOON = '11'
SQUID = '17'
BIG_FROG = '10'
GIANT_FLAM = '9'
GIANT_SPIRIT = '12'
CYCLOP = '7'
EYE = '0'
FLAM = '1'
MUSHROOM = '2'
OCTOPUS = '3'
SKELETON = '4'
SKULL = '5'
SLIME = '6'

# UI
BAR_HEIGHT = 20
HEALTH_BAR_WIDTH = 200
ENERGY_BAR_WIDTH = 140
ITEM_BOX_SIZE = 80
UI_FONT = './graphics/font/joystix.ttf'
UI_FONT_SIZE = 18

# general colors
WATER_COLOR = '#71DDEE'
UI_BG_COLOR = '#222222'
UI_BORDER_COLOR = '#111111'
TEXT_COLOR = '#EEEEEE'

# UI colors
HEALTH_COLOR = 'red'
ENERGY_COLOR = 'blue'
UI_BORDER_COLOR_ACTIVE = 'gold'

# upgrade menu
TEXT_COLOR_SELECTED = '#111111'
BAR_COLOR = '#EEEEEE'
BAR_COLOR_SELECTED = '#111111'
UPGRADE_BG_COLOR_SELECTED = '#EEEEEE'

# Menu
BUTTON_SPACING = 15
BUTTON_HEIGHT = 70
BUTTON_WIDTH = 250
MENU_FONT = './graphics/font/joystix.ttf'
MENU_FONT_SIZE = 30
MENU_FONT_COLOR = '#F2E8CF'
BUTTON_COLOR_SELECTED = '#A7C957'
BUTTON_COLOR = '#6A994E'
BUTTON_COLOR_BORDER = '#386641'
MATCHING_RED = '#BC4749'
PLAY = 0
SETTINGS = 1
ABOUT = 2
EXIT = 3

# Dialogs
DIALOG_BOX_COLOR = '#F2E8CF'
DIALOG_FONT = './graphics/font/joystix.ttf'
DIALOG_FONT_SIZE = 18
DIALOG_FONT_COLOR = '#111111'
DIALOG_BOX_BORDER_COLOR = '#386641'
DIALOG_MARGIN = 10
LINE_HEIGHT = 30

# weapons 
weapon_data = {
	'sword': {'cooldown': 100, 'min_damage': 10, 'max_damage': 15,'graphic':'./graphics/weapons/sword/full.png'},
	'lance': {'cooldown': 400, 'min_damage': 15, 'max_damage': 30,'graphic':'./graphics/weapons/lance/full.png'},
	'axe': {'cooldown': 300, 'min_damage': 15, 'max_damage': 20, 'graphic':'./graphics/weapons/axe/full.png'},
	'rapier':{'cooldown': 50, 'min_damage': 5, 'max_damage': 8, 'graphic':'./graphics/weapons/rapier/full.png'},
	'sai':{'cooldown': 80, 'min_damage': 8, 'max_damage': 10, 'graphic':'./graphics/weapons/sai/full.png'},
 	'hammer':{'cooldown': 1000, 'min_damage': 20, 'max_damage': 45, 'graphic':'./graphics/weapons/hammer/full.png'},
  	'big_sword':{'cooldown': 400, 'min_damage': 15, 'max_damage': 30, 'graphic':'./graphics/weapons/big_sword/full.png'},
   	'fork':{'cooldown': 350, 'min_damage': 15, 'max_damage': 25, 'graphic':'./graphics/weapons/fork/full.png'},}
# magic
magic_data = {
	'flame': {'strength': 5, 'cost': 20, 'graphic': './graphics/particles/flame/fire.png'},
 	'heal': {'strength': 20, 'cost': 10, 'graphic': './graphics/particles/heal/heal.png'}
}

# enemy
monster_data = {
	'squid': {'health': 100,'exp':100,'damage':20,'attack_type': 'slash', 'attack_sound':'./audio/attack/slash.wav', 'speed': 3, 'resistance': 3, 'attack_radius': 80, 'notice_radius': 360},
	'raccoon': {'health': 350,'exp':250,'damage':50,'attack_type': 'claw',  'attack_sound':'./audio/attack/claw.wav','speed': 2, 'resistance': 2, 'attack_radius': 130, 'notice_radius': 500},
	'spirit': {'health': 100,'exp':110,'damage':8,'attack_type': 'thunder', 'attack_sound':'./audio/attack/fireball.wav', 'speed': 4, 'resistance': 3, 'attack_radius': 60, 'notice_radius': 350},
	'big_frog': {'health': 200,'exp':170,'damage':13,'attack_type': 'slash', 'attack_sound':'./audio/attack/slash.wav', 'speed': 3, 'resistance': 3, 'attack_radius': 80, 'notice_radius': 340},
 	'giant_flam': {'health': 280,'exp':200,'damage':40,'attack_type': 'thunder', 'attack_sound':'./audio/attack/fireball.wav', 'speed': 4, 'resistance': 2, 'attack_radius': 100, 'notice_radius': 360},
  	'bamboo': {'health': 70,'exp':120,'damage':6,'attack_type': 'leaf_attack', 'attack_sound':'./audio/attack/slash.wav', 'speed': 3, 'resistance': 3, 'attack_radius': 50, 'notice_radius': 300},
   	'giant_spirit': {'health': 280,'exp':200,'damage':35,'attack_type': 'thunder', 'attack_sound':'./audio/attack/fireball.wav', 'speed': 4, 'resistance': 2, 'attack_radius': 100, 'notice_radius': 360},
   	'eye': {'health': 70,'exp':120,'damage':6,'attack_type': 'slash', 'attack_sound':'./audio/attack/slash.wav', 'speed': 3, 'resistance': 3, 'attack_radius': 50, 'notice_radius': 300},
    'flam': {'health': 70,'exp':120,'damage':6,'attack_type': 'thunder', 'attack_sound':'./audio/attack/fireball.wav', 'speed': 3, 'resistance': 3, 'attack_radius': 50, 'notice_radius': 300},
    'mushroom': {'health': 70,'exp':120,'damage':6,'attack_type': 'leaf_attack', 'attack_sound':'./audio/attack/slash.wav', 'speed': 3, 'resistance': 3, 'attack_radius': 50, 'notice_radius': 300},
    'octopus': {'health': 70,'exp':120,'damage':6,'attack_type': 'slash', 'attack_sound':'./audio/attack/slash.wav', 'speed': 3, 'resistance': 3, 'attack_radius': 50, 'notice_radius': 300},
    'skeleton': {'health': 70,'exp':120,'damage':6,'attack_type': 'slash', 'attack_sound':'./audio/attack/slash.wav', 'speed': 3, 'resistance': 3, 'attack_radius': 50, 'notice_radius': 300},
    'undead_skeleton': {'health': 60,'exp':30,'damage':6,'attack_type': 'slash', 'attack_sound':'./audio/attack/slash.wav', 'speed': 3, 'resistance': 2, 'attack_radius': 50, 'notice_radius': 250},
    'skull': {'health': 70,'exp':120,'damage':6,'attack_type': 'thunder', 'attack_sound':'./audio/attack/fireball.wav', 'speed': 3, 'resistance': 3, 'attack_radius': 50, 'notice_radius': 300},
    'slime': {'health': 70,'exp':120,'damage':6,'attack_type': 'slash', 'attack_sound':'./audio/attack/slash.wav', 'speed': 3, 'resistance': 3, 'attack_radius': 50, 'notice_radius': 300},
    'cyclop': {'health': 70,'exp':120,'damage':6,'attack_type': 'thunder', 'attack_sound':'./audio/attack/slash.wav', 'speed': 3, 'resistance': 3, 'attack_radius': 50, 'notice_radius': 300},
	'giant_raccoon': {'health': 70,'exp':120,'damage':6,'attack_type': 'claw', 'attack_sound':'./audio/attack/claw.wav', 'speed': 3, 'resistance': 3, 'attack_radius': 50, 'notice_radius': 300},}