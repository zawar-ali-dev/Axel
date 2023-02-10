# THIS PYTHON FILE WILL HANDLE THE CREATION OF THE VOCABULARIES AND BASE PROCESSING OF THE DATASETS

import random

#values
THRESHOLD = 0.7         
END = "end"
botname = "Axel" 

# Lists of potential answers based off user's small talk intent
small_talk_responses = ["I am great! you?", "yeah i guess i'm alright, how about you?", "not too bad, yourself?", "always great when assisting you!, how are you!?"]
agent_bad_responses = ["Oh come on that's not nice!", "Hey! come on don't be like that!", "OH! so it's like that huh?"]
user_good_responses = ["That is so good to hear!", "I'm very glad that's the case!", "Great stuff!"]
aquaintance_responses = [f"I am the one and only {botname}", f"I told you already! I'm {botname}", f"I am {botname}, at your disposal"]
agent_good_responses = ["oh come on youre too kind!", "Thank you so much!", "ohhh thank youuu", "do you mean that!? Thank you!"]
user_sad_responses = ["I am so sorry you feel this way!", "aw nooo that is horrible!", "i am so sorry you feel this way"]
weather_responses = ["It's looking a bit gloomy", "its very cold today!", "nice and breezy", "superrr sunny!"]
hello_responses = ["Heyy", "helloo", "what's up", "hi there!", "greetingss"]

# Checking for small talk function
def is_small_talk(intent):

    if intent == 'smalltalk_agent_acquaintance':
        response = random.choice(aquaintance_responses)
    elif intent == "smalltalk_user_sad" or intent == "smalltalk_appraisal_bad":
        response = random.choice(user_sad_responses)
    elif (intent) == "smalltalk_greetings_how_are_you":
        response = random.choice(small_talk_responses)
    elif intent == "smalltalk_agent_bad":
        response = random.choice(agent_bad_responses)
    elif intent == "smalltalk_agent_good" or intent == "smalltalk_user_likes_agent:":
        response = random.choice(agent_good_responses)
    elif intent == "smalltalk_appraisal_good" or intent == "smalltalk_user_good":
        response = random.choice(user_good_responses)
    elif intent == "smalltalk_user_weather":
        response = random.choice(weather_responses)
    elif intent == "smalltalk_greetings_hello":
        response = random.choice(hello_responses)
    elif intent == "smalltalk_greetings_bye":
        response = END
    else: 
        response = False
    return response



