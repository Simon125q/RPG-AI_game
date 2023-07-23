import pygame, sys
from settings import *
from debug import debug
from level import Level

class Game:
    
    def __init__(self):

        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(GAME_NAME)
        self.clock = pygame.time.Clock()

        self.level = Level()
        
        # sound
        pygame.mixer.music.load('./audio/HoliznaCC0 - Mathamatition.mp3')
        pygame.mixer.music.set_volume(0.8)
        pygame.mixer.music.play(loops = -1)

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                    elif event.key == pygame.K_TAB:
                        self.level.toggle_menu()
                        
            self.screen.fill(WATER_COLOR)
            self.level.run()
            pygame.display.update()
            self.clock.tick(FPS)

if __name__ == "__main__":
    game = Game()
    game.run()