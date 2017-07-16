from app.utils import helper
from app.mac import mac
from pprint import pprint
from modules.poker.deuces import Card
from modules.poker.constants import TexasStatus, PlayerActions

class Player(object):
    def __init__(self, message):
        self.who = message.who
        self.conversation = message.conversation
        self.who_name = message.who_name
        self.hand = None
        self.action = None
        self.current_bet = 0
        self.money = 10

    def notify_hand(self):
        chat_info = "Hand: " + Card.print_pretty_cards(self.hand) 
        mac.send_message(chat_info, self.who)

    def pretty_status(self, highest_bet=0):
        base = "(💲" +str( self.money) + ")" + self.who_name + ": " + self.status_str()
        if highest_bet > 0 and highest_bet - self.current_bet > 0:
            base += " ($" + str(highest_bet - self.current_bet) + " to bet)"
            
        return base
        
    def status_str(self):
        if self.action == PlayerActions.CHECK:
            return "✅"
        elif self.action == PlayerActions.BET:
            return "💵" + str(self.current_bet)
        elif self.action == None:
            return ""
        else:
            return "Unsupported status"
            
    def reset_status(self):
        self.action = None
        self.current_bet = 0
        
    '''
    Tries to set an action like bet, check or fold
    '''
    def set_action(self, action, players, bet=0):
        if action == PlayerActions.CHECK:
            return self.try_check_action(players)
        elif action == PlayerActions.FOLD:
            return self.try_fold_action(players)
        elif action == PlayerActions.BET:
            return self.try_bet_action(players, bet)
            
    def try_check_action(self, players):
        if any(p.action == PlayerActions.BET for p in players):
            # Cant check cause someone placed a bet
            return False
        else:
            self.action = PlayerActions.CHECK
            return True
            
    def try_fold_action(self, players):
        # I cannot think of a condition to fold so...
        self.action = PlayerActions.FOLD
        return True
        
    def try_bet_action(self, players, bet):
        if bet == None or bet == "":
            return False
        
        if bet >= 0 and bet <= self.money:
            self.current_bet = bet
            self.money = self.money - bet
            self.action = PlayerActions.BET
            return True
        else:
            return False
