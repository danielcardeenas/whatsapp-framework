from app.mac import mac, signals
from modules.poll.poll import WAPoll

'''
Signals this module listents to:
+ When a message is received (signals.message_received)
==========================================================
'''
@signals.message_received.connect
def handle(message):
    if message.command == "poll":
        if message.predicate == "-h":
            show_help(message)
            return
        else:
            create_poll(message)
            
    else:
        handle_vote(message)
        

def show_help(message):
    answer = "*Poll*\n*Usage:* !poll [title], [voter]\n*Example:* !poll who is gay?, ✋"
    mac.send_message(answer, message.conversation)

'''
Handles the parameters to create a poll
Structure of the message: "<title>, <identifier (optional)>"
'''
def create_poll(message):
    args = [x.strip() for x in message.predicate.split(',')]
    if len(args) <= 0:
        mac.send_message("_Invalid arguments for poll_", message.conversation)
        return
    if len(args) >= 1:
        if args[0] == "finish":
            WAPoll.finish_my_poll(message.who, message.conversation)
            return
        if len(args) == 1:
            title = args[0]
            basic_boll = WAPoll(message.conversation, message.who, title)
            basic_boll.send_poll()
        elif len(args) >= 2:
            title = args[0]
            identifier = args[1]
            basic_boll = WAPoll(message.conversation, message.who, title, identifier)
            basic_boll.send_poll()


def handle_vote(message):
    pass