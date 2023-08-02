import pygame

pygame.init()

screens = pygame.display.get_desktop_sizes()
WIDTH, HEIGHT = screens[0]
GAME_NAME = "AI game"
FPS = 60
TILESIZE = 64
HITBOX_OFFSET = {
	'player': -30,
	'object': -40,
	'grass': -12,
	'invisible': -32,
	'enemy': -16
}

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

# weapons 
weapon_data = {
	'sword': {'cooldown': 100, 'damage': 15,'graphic':'./graphics/weapons/sword/full.png'},
	'lance': {'cooldown': 400, 'damage': 30,'graphic':'./graphics/weapons/lance/full.png'},
	'axe': {'cooldown': 300, 'damage': 20, 'graphic':'./graphics/weapons/axe/full.png'},
	'rapier':{'cooldown': 50, 'damage': 8, 'graphic':'./graphics/weapons/rapier/full.png'},
	'sai':{'cooldown': 80, 'damage': 10, 'graphic':'./graphics/weapons/sai/full.png'}}
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
	'bamboo': {'health': 70,'exp':120,'damage':6,'attack_type': 'leaf_attack', 'attack_sound':'./audio/attack/slash.wav', 'speed': 3, 'resistance': 3, 'attack_radius': 50, 'notice_radius': 300}}