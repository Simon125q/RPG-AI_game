import pygame, sys
from settings import *
from debug import debug
from level import Level
from menu import Menu

class Game:
    
    def __init__(self):

        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(GAME_NAME)
        self.clock = pygame.time.Clock()
        self.pause_menu = False
        self.main_menu = Menu(self.screen)
        self.main_menu.main_menu()
        
        self.restart()
        
        # sound
        pygame.mixer.music.load('./audio/HoliznaCC0 - Mathamatition.mp3')
        pygame.mixer.music.set_volume(0.8)
        pygame.mixer.music.play(loops = -1)

    def restart(self):
        self.level = Level()
    
    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.pause_menu = not self.pause_menu
                elif event.key == pygame.K_TAB:
                    self.level.toggle_menu()
                    
        if self.main_menu.play:
            self.pause_menu = False
            self.main_menu.play = False
        if self.main_menu.exit:
            pygame.quit()
            sys.exit()   
            
    def run(self):
        while True:
            self.check_events()
            if not self.pause_menu:      
                self.screen.fill(WATER_COLOR)
                self.level.run()
            else:
                self.main_menu.update()
            pygame.display.update()
            self.clock.tick(FPS)

if __name__ == "__main__":
    game = Game()
    game.run()