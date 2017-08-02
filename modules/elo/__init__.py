from app.mac import mac, signals
from app.utils import helper
from modules.elo import elo, match

'''
Main funciton, all happens after this
'''
@signals.command_received.connect
def handle(message):
    if message.command == "elo":
        handle_elo(message)
        
    elif message.command == "match":
        handle_match(message)
        
        
'''
Handles elo command
Prints elo ranking of certain game or makes a query to the database
'''
def handle_elo(message):
    args = [x.strip() for x in message.predicate.split(',')]
    
    if args[0] == "query":
        query = message.predicate.split(', ', 1)[-1]
        results = elo.query(query)
        mac.send_message(results, message.conversation)
    else:
        ranks = elo.ranks(message.predicate)
        mac.send_message(ranks, message.conversation)
        
        
'''
Handles match command
Registers a match into database
'''        
def handle_match(message):
    args = [x.strip() for x in message.predicate.split(',')]
        
    if len(args) <= 0:
        mac.send_message("Missing game and results", message.conversation)
    elif len(args) == 1:
        mac.send_message("missgin results", message.conversation)
    elif len(args) >= 2:
        if elo.is_valid_game(args[0]) and (message.who == helper.me):
            confirmation = match.record_match(args[0], args[1])
            mac.send_message(confirmation, message.conversation)
        elif elo.is_valid_game(args[0]) and (message.who != helper.me):
            response = "@" + message.who_name + ", not alllowed"
            mac.send_message(response, message.conversation)
        else:
            confirmation = match.record_match(args[0], args[1])
            mac.send_message(confirmation, message.conversation)
            