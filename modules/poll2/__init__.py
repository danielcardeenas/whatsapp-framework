'''
Poll2 module
----------------------------------------------------------------------------
'''

from app.mac import mac, signals
from modules.poll2 import poll2
from app.utils import helper

'''
Main funciton, all happens after this
'''
@signals.message_received.connect
def handle(message):
    if helper.is_command(message.text) and message.command.lower() == "poll2":
        if message.predicate == "-h":
            show_help(message)
        else:
            poll2.handle_command(message)
    else:
        poll2.handle_vote(message)
        

'''
Prints help (how to use example)
'''
def show_help(message):
    answer = "*Poll2*\n*Usage:* !poll2 [title], [options...]\n*Example:* !poll who is the gayest?, Lucas, Berni, Dany \n*To finish poll:* !poll2 finish"
    mac.send_message(answer, message.conversation)