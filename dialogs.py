import pygame
import sys

DIALOG_BOX_COLOR = ''
DIALOG_FONT = ''
DIALOG_FONT_SIZE = 18
DIALOG_FONT_COLOR = ''
DIALOG_BOX_BORDER_COLOR = ''
DIALOG_MARGIN = 10

class Dialog_box:
    def __init__(self):
        self.width = WIDTH * 0.9
        self.height = HEIGHT * 0.3
        self.border = 4
        self.chars_line_length = self.width - DIALOG_MARGIN * 2 // DIALOG_FONT_SIZE
        self.top_pos = ((WIDTH - self.width) // 2, HEIGHT - self.height - 10)
        self.bottom_pos(self.top_pos[0] - self.border//2, self.top_pos[1] - self.border//2)
        self.bottom_rect = pygame.Rect(self.bottom_pos, (self.width + self.border, self.height + self.border))
        self.top_rect = pygame.Rect(self.top_pos, (self.width, self.height))
        
        self.font = pygame.font.Font(DIALOG_FONT, DIALOG_FONT_SIZE)
        self.text_rect = self.text_surf.get_rect(center = self.top_rect.center)
        
    def display(self, screen, message):
        words = message.split(' ')
        for msg in range(0, len(message), self.chars_line_length):
            
            self.text_surf = self.font.render(text, True, DIALOG_FONT_COLOR)
            self.draw(screen)
            self.get_action()
            
            
    def draw(self, screen):
        pygame.draw.rect(screen, DIALOG_BOX_COLOR, self.bottom_rect, border_radius=10)
        pygame.draw.rect(screen, DIALOG_BOX_COLOR, self.top_rect, border_radius=10)
        
        screen.blit(self.text_surf, self.text_rect)
    
    def get_action(self):
        loop = True
        while loop:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        loop == False