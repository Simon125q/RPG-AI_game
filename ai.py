import openai
import os
import pygame
import pygame.freetype
import sys
from settings import *
from prompts import *
from dotenv import load_dotenv, find_dotenv

class Dialog_AI:
    def __init__(self):
        
        _ = load_dotenv(find_dotenv())
        
        openai.api_key = os.getenv('OPENAI_API_KEY')

    def generate_dialog(self, action):
        if action == 'START':
            characters['main_character'] = self.create_character(atributes, 'main character')
            DIALOGS['START'] = self.start()
        elif 'narrator' in action:
            DIALOGS[action] = self.narrate(action.replace('narrator_', ''))
            
    def get_completion(self, prompt, model="gpt-3.5-turbo", temperature = 0):
        messages = [{"role": "user", "content": prompt}]
        response = openai.ChatCompletion.create(
            model=model,
            messages=messages,
            temperature = temperature
        )
        return response.choices[0].message["content"]

    def create_character(self, atributes, character):
        prompt = f"Your task is to create atributes of the {character} of the computer RPG game with given in triple backticks atributes names \
                        Your answer should be provided in json format in the same order as it was provided to you, provide only the filled json file dont \
                            write anything else only json, here are the atributtes ### \
                        {atributes}###"
        return self.get_completion(prompt, temperature = 0.7)
    
    def start(self):
        prompt = f"you are a narrator in a computer single player rpg game, your narrating style is provocative and at the same\
                time funny (something like deathpool). make an introductin to this game here are information about main character {characters['main_character']}"

        return self.get_completion(prompt, temperature = 0.7)

    def narrate(self, boss):
        prompt = f"you are a narrator in a computer single player rpg game, your narrating style is provocative and at the same time funny (something like deathpool). \
                The main player is coming close to fight with next boss which will be {boss_description[boss]} your task is to introduce player with who he will fight and present \
                some story about the boss. It is not fight yet"
        return self.get_completion(prompt, temperature = 0.7)