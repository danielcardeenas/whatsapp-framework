# -*- coding: utf-8 -*-
import string

from app.mac import mac
from app.mac import signals
from app.utils import helper

#from modules.poll import poll
#from modules.poll2.poll2 import PollKing
#from modules.yesno.yesno import YesNo
#from modules.youtube.mac_youtube import WAYoutube
#from modules.elo import elo, match
#from modules.trip import trip

####################################################################################################################

'''
This method gets all you need in a command message.
For ex.
    In group "ITS", daniel sent "!hola a todos"
    @instance = the instance (You need this to send reply with mac -> mac.send_message(instance,...))
    @command = What comes after '!'. In this case "hola"
    @predicate = What comes after command. In this case "a todos"
    @who = The whatsapp user object who sent this. In this case daniel (check below for retrieving the name)
    @conversation = The whatsapp conversation object. In this case the group "ITS".
'''
def handle_message(instance, command, predicate, message_entity, who, conversation):
    # Nigga who send the message
    who_name = helper.sender_name(message_entity)

    
#def wolfram_answer(message, who=""):
#    app_id = "WL543X-U2TEJ4HT6J"
#    client = wolframalpha.Client(app_id)
#    try:
#        res = client.query(message)
#        if hasattr(res, 'pods'):
#            return next(res.results).text
#        else:
#            return ("Sorry *" + who + "*, I don't have the answer for that")
#    except:
#        return "?"
#        #return cleverbot_answer(message)
#        #return ("Sorry *" + who + "*, I don't have the answer for that")