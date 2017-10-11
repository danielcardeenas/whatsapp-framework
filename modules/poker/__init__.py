'''
Poker module
----------------------------------------------------------------------------
'''

from app.mac import mac, signals
from modules.poker.poker import WAPoker
from app.utils import helper

'''
Main funciton, all happens after this
'''
@signals.message_received.connect
def handle(message):
    if helper.is_command(message.text) and message.command.lower() == "poker":
        if message.predicate == "-h":
            show_help(message)
        else:
            handle_command(message)
            
    else:
        handle_action(message)
        
    
'''
Handles command
- Create a game
- Start a game
!poll <argument>

'''
def handle_command(message):
    arg = message.predicate.split(' ')[0]
    if arg == "start":
        game = WAPoker.find_my_game(message.conversation, message.who)
        if game:
            game.start()
        else:
            mac.send_message("No game found in this chat", message.conversation)
    elif arg == "status":
        game = WAPoker.find_chat_game(message.conversation)
        if game:
            mac.send_message(game.print_players_stauts(), message.conversation)
    else:
        if arg == '':
            game = WAPoker(message.conversation, message.who)
            game.initialize_game()
        else:
            game = WAPoker(message.conversation, message.who, arg)
            game.initialize_game()


'''
Handles action
- Join game action
- Playing actions

'''
def handle_action(message):
    WAPoker.handle_action(message)


'''
Prints help (how to use example)
'''
def show_help(message):
    answer = "*Poker*\n*Usage:* !poker [join_identifier]\n*Example:* !poker ✋️"
    mac.send_message(answer, message.conversation)