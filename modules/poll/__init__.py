'''
Poll module
----------------------------------------------------------------------------

Handles the parameters to create a poll
Structure of the message: "<title>, <identifier (optional)>"
'''

from app.mac import mac, signals
from modules.poll.poll import WAPoll

'''
Main funciton, all happens after this
'''
@signals.message_received.connect
def handle(message):
    if message.command == "poll":
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
    answer = "*Poll*\n*Usage:* !poll [title], [voter]\n*Example:* !poll who is gay?, ✋\nFinish poll: !poll finish"
    mac.send_message(answer, message.conversation)