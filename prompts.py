delimiter = "####"

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

text = f"""
You should express what you want a model to do by \ 
providing instructions that are as clear and \ 
specific as you can possibly make them. \ 
This will guide the model towards the desired output, \ 
and reduce the chances of receiving irrelevant \ 
or incorrect responses. Don't confuse writing a \ 
clear prompt with writing a short prompt. \ 
In many cases, longer prompts provide more clarity \ 
and context for the model, which can lead to \ 
more detailed and relevant outputs.
"""
prompt = f"""
Summarize the text delimited by triple backticks \ 
into a single sentence.
```{text}```
"""


system_message = f"""
You will be provided with customer service queries. \
The customer service query will be delimited with \
{delimiter} characters.
Classify each query into a primary category \
and a secondary category. 
Provide your output in json format with the \
keys: primary and secondary.

Primary categories: Billing, Technical Support, \
Account Management, or General Inquiry.

Billing secondary categories:
Unsubscribe or upgrade
Add a payment method
Explanation for charge
Dispute a charge

Technical Support secondary categories:
General troubleshooting
Device compatibility
Software updates

Account Management secondary categories:
Password reset
Update personal information
Close account
Account security

General Inquiry secondary categories:
Product information
Pricing
Feedback
Speak to a human

"""
