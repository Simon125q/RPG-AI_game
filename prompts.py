delimiter = "####"
boss = ''
atributes = "atributes= {\
    'name':'',\
    'gender':'',\
    'age':'',\
    'motivation':'',\
    'life_story':'',\
    'catch_phrase':''\
    }"

characters = {
    "main_character": {
                        "name": "Eleanor",
                        "gender": "Female",
                        "age": "27",
                        "motivation": "To uncover the truth behind her father's mysterious disappearance.",
                        "life_story": "Born in a small village, Eleanor grew up hearing stories of her father's \
                            legendary adventures as an explorer. He vanished without a trace when she was just a \
                                child. Determined to follow in his footsteps and find out what happened, Eleanor \
                                    has trained tirelessly in combat and survival skills.",
                        "catch_phrase": "Adventure awaits, and I'm ready to uncover the secrets of the past!"
                    },
    "boss_flame":"",
    "boss_spirit":"",
    "boss_frog":"",
    "boss_raccoon":""
}

boss_description = {
    'giant_spirit': "giant spitit located in the woods in circle made of stone",
    'giant_flame': "giant flame located on a desert in a circle made of stone",
    'giant_raccoons': "group of giant raccoons located on a snow desert",
    'giant_raccoon': "giant dark raccoon located on an island with blooming cherry trees",
    'giant_frog': "group of red giant frogs located near swamp and graveyard "
}

get_main_character = f"Your task is to create atributes of the main character of the computer RPG game with given in triple backticks atributes names \
                        Your answer should be provided in json format in the same order as it was provided to you, provide only the filled json file dont \
                            write anything else only json, here are the atributtes ### \
                        {atributes}###"

start_prompt = f"you are a narrator in a computer single player rpg game, your narrating style is provocative and at the same\
                time funny (something like deathpool). make an introductin to this game here are information about main character {characters['main_character']}"

boss_narration_prompt = f"you are a narrator in a computer single player rpg game, your narrating style is provocative and at the same time funny (something like deathpool). \
    The main player is coming close to fight with next boss which will be {boss_description[boss]} your task is to introduce player with who he will fight and present \
        some story about the boss. It is not fight yet"
                

