# -*- coding: utf-8 -*-
import string

from modules.poll import poll
from modules.poll2.poll2 import PollKing
from app.mac import mac
from app.utils import helper
from modules.yesno.yesno import YesNo
from modules.youtube.mac_youtube import WAYoutube
from modules.elo import elo, match
from modules.trip import trip

import wolframalpha

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

    if command == "hi" or command == "hola":
        answer = "Hola *" + who_name + "*"
        mac.send_message(instance, answer, conversation)

    elif command == "siono":
        yesno = YesNo(instance, conversation)
        yesno.send_yesno()

    elif command == "yt":
        WAYoutube(instance, who, conversation)
        
    elif command == "✔":
        response = match.confirm_match()
        mac.send_message(instance, response, conversation)
        
    elif command == "elo":
        args = [x.strip() for x in predicate.split(',')]
        if args[0] == "query":
            query = predicate.split(', ', 1)[-1]
            results = elo.query(query)
            mac.send_message(instance, results, conversation)
        else:
            ranks = elo.ranks(predicate)
            mac.send_message(instance, ranks, conversation)
        
    elif command == "match":
        args = [x.strip() for x in predicate.split(',')]
        if len(args) <= 0:
            mac.send_message(instance, "missing game and results", conversation)
        elif len(args) == 1:
            mac.send_message(instance, "missgin results", conversation)
        elif len(args) >= 2:
            if elo.is_valid_smash(args[0]) and (who == helper.me):
                confirmation = match.record_match(args[0], args[1])
                mac.send_message(instance, confirmation, conversation)
            elif elo.is_valid_smash(args[0]) and (who != helper.me):
                response = "@" + who_name + ", not alllowed"
                mac.send_message(instance, response, conversation)
            else:
                confirmation = match.record_match(args[0], args[1])
                mac.send_message(instance, confirmation, conversation)
        
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
                
    elif command == "trip":
        mac.send_message(instance, trip.print_debts(), conversation)

    
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