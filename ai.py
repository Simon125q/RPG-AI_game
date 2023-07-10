import openai
import os
import pygame
import pygame.freetype
import sys
from settings import *

from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv())

openai.api_key  = os.getenv('OPENAI_API_KEY')

def get_completion(prompt, model="gpt-3.5-turbo"):
    messages = [{"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=0, # this is the degree of randomness of the model's output
    )
    return response.choices[0].message["content"]

atributes = {
    "name":"",
    "gender":"",
    "age":"",
    "motivation":"",
    "life_story":"",
    "special_character_treits":"",
    "catch_phrase":""
}

characters = {
    "main_character":"",
    "first_boss":"",
    "secound_boss":"",
    "final_boss":""
}

def create_character(atributes, character):
    
    text = f""""""
    for key in atributes:
        text += key + ':\n'
    prompt = f"""
     Your task is to create atributes of the {character} of the game with given in triple backticks atributes names \ 
    Your answer should be provided in json format in the same order as it was provided to you, provide only the json file\
    ```{text}```
    """
    return get_completion(prompt, temperature = 0.7)

character_atributes = {}

pygame.freetype.init()
class Message:
    def __init__(self, x=WIDTH/3, y=10, width = WIDTH/3-10, height = HEIGHT-20, font = None, font_size = 12):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.font = pygame.freetype.Font(font, font_size)
        
    def display(self, message = ''):
        go = True
        display_surface = pygame.display.get_surface()
        msg_surface = pygame.freetype.Font.render(message, "Black", size = self.size)
        msg_rect = msg_surface.get_rect(top_left = (self.x, self.y))
        pygame.draw.rect(display_surface, 'White', msg_rect)
        display_surface.blit(msg_surface, msg_rect)
        while go:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        go = False
        
    def show(self, message = ''):
        self.process_message(message, 40, 20)
        
    def process_message(self, message, line_len, lines_num):
        length = 0
        lines = 0
        show_msg=''
        for char in message:
            if length <= line_len:
                show_msg += char
                length += 1
            elif lines > lines_num:
                show_msg += '\n'
                show_msg += "..."
                self.display(show_msg)
            else:
                length = 0
                lines += 1
                show_msg += '\n'
        self.display(show_msg)
               
pygame.freetype.quit()

stages = {
    "start":"Its the begining of the game introduce the player to who is our main hero, what are his/her motivations for going\
                introduce our story",
    "before_first_boss":f"The fight with fist boss is coming, describe who the boss is what are his\
                    abilities, and why he wants to fight info about boss: ###{boss_attributes}###",
    "after_first_boss":"",
    "before_secound_boss":"",
    "after_secound_boss":"",
    "before_final_boss":"",
    "ending":""
}
world_description = ""

def narrate(world_description, character_attributes, stage, boss_atributes = ''):
    prompt=f"""You are the narrator of the game which takes place in {world_description},\
                the main character is {character_atributes}, your role as a narrator is to comment \
                the game at given stages, do this in a little provocarive and funny way.\
                Current stage ###{stage}###"""
    return get_completion(prompt, temperature = 0.7)