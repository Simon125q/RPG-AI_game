import pygame
import sys
from settings import *

class Menu:
    def __init__(self, screen):
        self.buttons = []
        self.background = ''
        self.screen = screen
        self.play = False
        self.exit = False
        self.about = False
        
    def main_menu(self):
        options = ['PLAY', 'SETTINGS', 'ABOUT', 'EXIT']
        for num, option in enumerate(options):
            self.buttons.append(Button(option, BUTTON_WIDTH, BUTTON_HEIGHT, (WIDTH//2 - BUTTON_WIDTH // 2, HEIGHT/4 + num * (BUTTON_HEIGHT + BUTTON_SPACING))))
        
    def check_actions(self):
        if self.buttons[PLAY].active:
            self.play = True
            self.buttons[PLAY].active = False
        if self.buttons[SETTINGS].active:
            pass
        elif self.buttons[ABOUT].active:
            self.about = True
            self.buttons[ABOUT].active = False
        elif self.buttons[EXIT].active:
            self.exit = True
    
    def about_scr(self):
        pass
        # back_button = Button('BACK', BUTTON_WIDTH, BUTTON_HEIGHT, (WIDTH//2 - BUTTON_WIDTH // 2, HEIGHT/4 + 5 * (BUTTON_HEIGHT + BUTTON_SPACING)))
        # back_button.draw(self.screen)
        # if back_button.active:
        #     self.about = False
        #     self.draw()
    def settings(self):
        pass
    
    def draw(self):
        if self.about:
            self.about_scr()
        else:
            for button in self.buttons:
                button.draw(self.screen)
            
    def update(self):
        self.draw()
        self.check_actions()
        


class Button:
    def __init__(self, text, width, height, pos):
        self.active = False
        
        # button rectangles
        border = 10
        self.bottom_rect = pygame.Rect(pos, (width + border, height + border))
        self.top_rect = pygame.Rect((pos[0] + border // 2, pos[1] + border // 2), (width, height))
        self.curr_color = BUTTON_COLOR
        
        # text
        self.font = pygame.font.Font(MENU_FONT, MENU_FONT_SIZE)
        self.text_surf = self.font.render(text, True, MENU_FONT_COLOR)
        self.text_rect = self.text_surf.get_rect(center = self.top_rect.center)
        
    def draw(self, screen):
        self.check_click()
        pygame.draw.rect(screen, BUTTON_COLOR_BORDER, self.bottom_rect, border_radius = 12)
        pygame.draw.rect(screen, self.curr_color, self.top_rect, border_radius = 12)
        screen.blit(self.text_surf, self.text_rect)
        
    def check_click(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.top_rect.collidepoint(mouse_pos):
            self.curr_color = BUTTON_COLOR_SELECTED
            if pygame.mouse.get_pressed()[0]:
                self.active = True
            else:
                self.active = False
        else:
            self.curr_color = BUTTON_COLOR
            