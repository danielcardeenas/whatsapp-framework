'''
Poll module
----------------------------------------------------------------------------

Handles the parameters to create a poll
Structure of the message: "!poll <title>, <identifier (optional)>"
'''

from app.mac import mac, signals
from modules.poll.poll import WAPoll
from app.utils import helper

'''
Main funciton, all happens after this
'''
@signals.message_received.connect
def handle(message):
    if helper.is_command(message.text) and message.command.lower() == "poll":
        if message.predicate == "-h":
            show_help(message)
        else:
            WAPoll.handle_command(message)
            
    else:
        WAPoll.handle_vote(message)
        

'''
Prints help (how to use example)
'''
def show_help(message):
    answer = "*Poll*\n*Usage:* !poll [title], [voter]\n*Example:* !poll who is gay?, ✋\n*To finish poll:* !poll finish"
    mac.send_message(answer, message.conversation)