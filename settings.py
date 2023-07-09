import pygame

pygame.init()

screens = pygame.display.get_desktop_sizes()
WIDTH, HEIGHT = screens[0]
GAME_NAME = "AI game"
FPS = 60
