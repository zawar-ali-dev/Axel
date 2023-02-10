# THIS PYTHON FILE WILL HANDLE THE CHATBOTS NAME MANAGEMENT

import random
import nltk
from nltk import ne_chunk
nltk.download('maxent_ne_chunker')
nltk.download('words')
import pandas as pd

# values
THRESHOLD = 0.7
END = "end"
CHANGE = "change"
botname = "Axel"

# Extracting name from the initial query
def find_name(query):
    # Assuming that if the user states their name, it is of length < 2 tokens
    tokens = nltk.word_tokenize(query)
    if len(tokens) <= 2:
        return query

    tokens = [token.capitalize() for token in tokens]

    pos = nltk.pos_tag(tokens)
    print(pos)
    chunks = ne_chunk(pos)
    print(chunks)
    quit()


    person = []
    for subtree in chunks.subtrees():
        if subtree.label() == "PERSON":
            for leaf in subtree.leaves():
                #only aquire first value of leaf tuple, as the second value is the tag
                person.append(leaf[0])
    name = " ".join(person)
    if len(name) < 1:
        return False
    else:
        return name

# Loop to prompt user to provide their name
def get_name():
    while(1):
        user = "user"
        name_input = input(f">> {user}: ")
        user = find_name(name_input)
        if user:
            print(f">> {botname}: Alright {user}, let's do this!")
            break
        else:
            print(f">> {botname}: I'm sorry I didn't quite catch that!, could you try again?")
    return user

# Checking for precise intent response for name management 
def is_name_management(intent, user):
    respones = False
    if intent == "name_recall":
        # Lists of potential answers if user wants their name recalled
        recall_responses = [f"of course i know you! {user}", f"how could i forget, {user}", f"well you told me to call you, {user}"]
        response = random.choice(recall_responses)
    elif intent == "name_change":
        response = CHANGE 
    return response




