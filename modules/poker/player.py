from app.utils import helper
from app.mac import mac
from pprint import pprint
from modules.poker.deuces import Card
from modules.poker.constants import TexasStatus, PlayerActions
import sqlite3

conn = sqlite3.connect('modules/poker/db/poker.db')
cursor = conn.cursor()

class Player(object):
    def __init__(self, message):
        self.who = message.who
        self.conversation = message.conversation
        self.who_name = message.who_name
        self.hand = None
        self.action = None
        self.current_bet = 0
        self.money = 20
        self.locked = False
        self.play_rank = None

    def notify_hand(self):
        chat_info = "Hand: " + Card.print_pretty_cards(self.hand) 
        mac.send_message(chat_info, self.who, False)

    def pretty_status(self, highest_bet=0):
        base = "($" + str( self.money) + ") " + self.who_name + ": " + self.status_str()
        if highest_bet > 0 and highest_bet - self.current_bet > 0:
            base += " ($" + str(highest_bet - self.current_bet) + " to bet)"
            
        return base
        
    def unlock(self):
        if not self.is_all_in():
            self.locked = False
        else:
            self.locked = True
        
    def status_str(self):
        if self.action == PlayerActions.CHECK:
            return "✅"
        elif self.action == PlayerActions.BET:
            return "💵 " + str(self.current_bet)
        elif self.action == None:
            return ""
        else:
            return "Unsupported status"
            
    def reset_status(self):
        self.action = None
        self.current_bet = 0
        self.unlock()
        
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
            self.locked = True
            return True
            
    def try_fold_action(self, players):
        self.action = PlayerActions.FOLD
        return True
        
    def try_bet_action(self, players, bet):
        if bet == None or bet == "" or bet == 0:
            return False
        
        if bet <= self.money:
            self.current_bet = bet + self.current_bet
            self.money = self.money - bet
            self.action = PlayerActions.BET
            self.locked = True
            return True
        else:
            self.action = None
            return False
            
    def is_all_in(self):
        return self.money <= 0
        
    def set_money(self, money):
        self.money = money
        
    def add_money(self, money):
        self.money = self.money + money
        
    def update_money_db(self):
        conn.executescript("update players set money = " + str(self.money) + " where phone = '" + self.who + "'")
        
        
    @staticmethod
    def retrieve_players(players):
        for player in players:
            data = cursor.execute("select phone, money, name from players where phone = ?", (player.who,)).fetchone()
            if data is None:
                # New player in db
                conn.executescript("insert into players(name, money, phone) values('" + player.who_name + "', " + str(20) + ", '" + player.who + "')")
            else:
                player.set_money(float(data[1]))
    
    @staticmethod
    def update_players(players):
        for player in players:
            data = cursor.execute("select phone, money, name from players where phone = ?", (player.who,)).fetchone()
            if data:
                conn.executescript("update players set money = " + str(player.money) + " where phone = '" + player.who + "'")
                