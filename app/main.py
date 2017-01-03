# -*- coding: utf-8 -*-
import string

from app.poll import poll
from app.poll2.poll2 import PollKing
from app.mac import mac
from app.utils import helper
from app.yesno.yesno import YesNo
from app.youtube.mac_youtube import WAYoutube
from app.elo import elo

import wolframalpha
from cleverbot import Cleverbot

####################################################################################################################

'''
This method gets all you need in a command message.
For ex.
    In group "ITS", daniel sent "!hola a todos"
    @self = the instance (You need this to send reply with mac -> mac.send_message(instance,...))
    @command = What comes after '!'. In this case "hola"
    @predicate = What comes after command. In this case "a todos"
    @who = The whatsapp user object who sent this. In this case daniel (check below for retrieving the name)
    @conversation = The whatsapp conversation object. In this case the group "ITS".
'''
def handle_message(instance, command, predicate, message_entity, who, conversation):
    # Nigga who send the message
    who_name = helper.sender_name(message_entity)

    if command == "hi" or command == "hola":
        answer = "Hola *" + who_name + "*"
        mac.send_message(instance, answer, conversation)

    elif command == "help":
        answer = "Hola *" + who_name + "*\nNo puedo ayudarte por ahora"
        mac.send_message(instance, answer, conversation)

    elif command == "siono":
        yesno = YesNo(instance, conversation)
        yesno.send_yesno()

    elif command == "yt":
        WAYoutube(instance, who, conversation)
        
    elif command == "elo":
        ranks = elo.get_ranks(predicate)
        mac.send_message(instance, str(ranks), conversation)
        
    elif command == "poll2":
        poll2 = PollKing(instance, conversation, who, predicate)
        poll2.send_poll()
        
    elif command == "poll":
        # args = <title>, <identifier (optional)>
        args = [x.strip() for x in predicate.split(',')]
        if len(args) <= 0:
            mac.send_message(instance, "_Argumentos invalidos_", conversation)
            return
        if len(args) >= 1:
            if args[0] == "finish":
                poll.finish_my_poll(instance, who, conversation)
                return
            if len(args) == 1:
                title = args[0]
                basic_boll = poll.WAPoll(instance, conversation, who, title)
                basic_boll.send_poll()
            elif len(args) >= 2:
                title = args[0]
                identifier = args[1]
                basic_boll = poll.WAPoll(instance, conversation, who, title, identifier)
                basic_boll.send_poll()
    else:
        # No command for this so use IA
        #answer = cleverbot_answer(command + " " + predicate)
        answer = wolfram_answer(command + " " + predicate, who_name)
        mac.send_message(instance, answer, conversation)
        
    
def wolfram_answer(message, who=""):
    app_id = "WL543X-974Q523T8P"
    client = wolframalpha.Client(app_id)
    try:
        res = client.query(message)
        if hasattr(res, 'pods'):
            return next(res.results).text
        else:
            return cleverbot_answer(message)
            #return ("Sorry *" + who + "*, I don't have the answer for that")
    except:
        return "*?*"
        #return cleverbot_answer(message)
        #return ("Sorry *" + who + "*, I don't have the answer for that")


def cleverbot_answer(message):
    cb = Cleverbot()
    answer = cb.ask(message)
    return answer
