from app.poll import poll
from app.mac import mac
from app.utils import helper
from app.yesno.yesno import YesNo
from app.youtube.mac_youtube import WAYoutube

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
    # Nigga who send the message (first name)
    who_name = message_entity.getNotify().split(" ")[0]

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
        cb = Cleverbot()
        answer = cb.ask(command + " " + predicate)
        mac.send_message(instance, answer, conversation)