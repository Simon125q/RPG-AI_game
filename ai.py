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

def narrate(world_description, character_attributes, stage, boss_atributes = ''):
    prompt=f"""You are the narrator of the game which takes place in {world_description},\
                the main character is {character_attributes}, your role as a narrator is to comment \
                the game at given stages, do this in a little provocarive and funny way.\
                Current stage ###{stage}###"""
    return get_completion(prompt, temperature = 0.7)