import wolframalpha
import re

from app.mac import mac, signals
from modules.wolfram import config
from modules import pokedex

'''
Signals this module listents to:
1. When a message is received (signals.message_received)
==========================================================
'''
@signals.message_received.connect
def handle(message):
    request = should_answer(message)
    if request != '':
        if is_pokemon_case(request):
            pokemon = pokedex.get_pokemon(request.split(' ')[1])
            if pokemon:
                #mac.send_message(pokemon.name.capitalize(), message.conversation)
                mac.send_message(wolfram_answer("pokemon " + pokemon.name.capitalize()), message.conversation)
                
        else:
            mac.send_message(wolfram_answer(request), message.conversation)


'''
Actual module code
==========================================================
'''
def wolfram_answer(message):
    app_id = config.api_key
    client = wolframalpha.Client(app_id)
    answer = ""
    try:
        res = client.query(message)
        if hasattr(res, 'pods'):
            answer = next(res.results).text
        else:
            answer = "I don't have an answer for that"
    except:
        answer = "I cannot show the answer here"
        
    # Hehe
    if answer == "I was created by Stephen Wolfram and his team.":
        answer = "Daniel Cardenas created me but I get these answers from an engine made by Stephen Wolfram and his team."
    
    return answer
        
def should_answer(message):
    if message.message[:4].lower() == 'mac,':
        return message.message[4:].strip()
    elif message.message[:4].lower() == 'mac ':
        return message.message[3:].strip()
    else:
        return ""
        

def is_pokemon_case(request):
    regex = r"pokemon [0-9]*$"
    if re.match(regex, request, re.IGNORECASE):
        return True
    else:
        return False