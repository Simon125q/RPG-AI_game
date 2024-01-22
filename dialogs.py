import pygame
from settings import *
from prompts import *


class Dialog_box:
    def __init__(self, level):
        
        self.display_surface = pygame.display.get_surface()
        
        self.level = level
        
        self.width = WIDTH * 0.9
        self.height = HEIGHT * 0.3
        self.border = 10
        self.top_pos = ((WIDTH - self.width) // 2, HEIGHT - self.height - 10)
        self.bottom_pos = (self.top_pos[0] - self.border//2, self.top_pos[1] - self.border//2)
        self.bottom_rect = pygame.Rect(self.bottom_pos, (self.width + self.border, self.height + self.border))
        self.top_rect = pygame.Rect(self.top_pos, (self.width, self.height))
        
        self.font = pygame.font.Font(DIALOG_FONT, DIALOG_FONT_SIZE)
        self.text_surf = self.font.render('', True, DIALOG_FONT_COLOR)
        
        self.chars_line_length = (self.width) // DIALOG_FONT_SIZE
        self.counter = 0
        self.line_counter = 0
        self.active_message = 0
        self.messages = []
        self.to_show = []
        self.done = False
        self.line = 0
        
    def cut_messages(self, message):
        lines = []
        paragraph = []
        line = ''
        for word in message.split(' '):
            if len(line + word) <= self.chars_line_length:
                line = line + ' ' + word
            else:
                lines.append(line)
                line = word
        lines.append(line)
        
        paragraph_height = 0
        for line in lines:
            if paragraph_height + 1 <= (self.height - DIALOG_MARGIN * 2) / LINE_HEIGHT - 2:
                paragraph.append(line)
                paragraph_height += 1
            else:
                paragraph.append('...')
                self.messages.append(paragraph)
                paragraph = [line]
                paragraph_height = 0
                    
        self.messages.append(paragraph)
            
    def display(self, event = 'ERROR',):
        
        if self.messages == []:
            self.cut_messages(DIALOGS[event])
        
        self.input()
        text_speed = 2
        
        self.paragraph = self.messages[self.active_message]
        
        if self.counter < text_speed * len(self.paragraph):
            self.counter += 1
        elif self.counter >= text_speed * len(self.paragraph):
            self.done = True
        
        line_done = False
        
        text_line = self.paragraph[self.line] if self.line < len(self.paragraph) else []
        if text_line != []:
            if self.line_counter < text_speed * len(text_line):
                self.line_counter += 1
            elif self.line_counter >= text_speed * len(text_line):
                line_done = True
                
            if line_done:
                self.text_surf = self.font.render(text_line[0: self.line_counter // text_speed], True, DIALOG_FONT_COLOR)
                self.text_rect = self.text_surf.get_rect(topleft = (self.top_rect.left + 6 * DIALOG_MARGIN, self.top_rect.y + (self.line+1) * LINE_HEIGHT + DIALOG_MARGIN))
                self.to_show.append((self.text_surf, self.text_rect))
                self.text_surf = self.font.render('', True, DIALOG_FONT_COLOR)
                self.line_counter = 0
                self.line += 1
                
            else:
                self.text_surf = self.font.render(text_line[0: self.line_counter // text_speed], True, DIALOG_FONT_COLOR)
                self.text_rect = self.text_surf.get_rect(topleft = (self.top_rect.left + 6 * DIALOG_MARGIN, self.top_rect.y + (self.line + 1) * LINE_HEIGHT + DIALOG_MARGIN))
        self.draw()
        
    def draw(self):
        
        pygame.draw.rect(self.display_surface, DIALOG_BOX_BORDER_COLOR, self.bottom_rect, border_radius=10)
        pygame.draw.rect(self.display_surface, DIALOG_BOX_COLOR, self.top_rect, border_radius=10)
        
        for surf, rect in self.to_show:
            self.display_surface.blit(surf, rect)
            
        self.display_surface.blit(self.text_surf, self.text_rect)
    
    def input(self):
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_SPACE] and self.done and self.active_message < len(self.messages) - 1:
            self.to_show = []
            self.active_message += 1
            self.done = False
            self.counter = 0
            self.line = 0
        elif keys[pygame.K_SPACE] and self.done and self.active_message >= len(self.messages) - 1:
            self.to_show = []
            self.active_message = 0
            self.done = False
            self.counter = 0
            self.line = 0
            self.level.dialog_pause = False
            
        