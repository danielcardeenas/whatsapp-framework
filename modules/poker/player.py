from app.utils import helper
from app.mac import mac
from pprint import pprint
from modules.poker.deuces import Card

class Player(object):
    def __init__(self, message):
        self.who = message.who
        self.conversation = message.conversation
        self.who_name = message.who_name
        self.hand = None
        
    def notify_hand(self):
        chat_info = "Hand: " + Card.print_pretty_cards(self.hand) 
        mac.send_message(chat_info, self.who)