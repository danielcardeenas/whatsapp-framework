# -*- coding: utf-8 -*-
from enum import Enum
from app.utils import helper
from app.mac import mac
from modules.poker.player import Player
from modules.poker.deuces import Card, Deck, Evaluator

active_games = []
actions_arr = [
    "check",
    "✅",
    "bet",
    "culeo",
    "fold",
    "❌"
]

actions = dict(
    check = ["check", "✅"],
    fold = ["fold", "culeo", "❌"],
    bet = ["bet"]
)

class TexasStatus(Enum):
    PREFLOP = 1
    FLOP = 2
    TURN = 3
    RIVER = 4
    SHOWDOWN = 5
    BLOCKED = 6
    
class TexasActions(Enum):
    CHECK = 1
    BET = 2
    FOLD = 3

class WAPoker(object):
    def __init__(self, conversation, creator, join_identifier="#"):
        # Finish poll if user already has one in this conversation
        self.finish_my_game(creator, conversation)
        self.conversation = conversation
        self.creator = creator
        self.join_identifier = join_identifier
        self.started = False
        self.players = []
        self.deck = Deck()
        self.board = None
        self.status = TexasStatus.PREFLOP
        
    # Ask "who's playing?"
    def initialize_game(self):
        if chat_has_game(self.conversation):
            mac.send_message("There is already a game going on", self.conversation)
            return
        
        answer = "*Texas Hold'em*" + "\n" + self.join_identifier + " to join"
        mac.send_message(answer, self.conversation)
        active_games.append(self)
        
    # Show players and start game
    def start(self):
        # If no players
        if len(self.players) <= 1:
            mac.send_message("Not enough players to start", self.conversation)
            return
        
        elif self.started:
            mac.send_message("Your game already started", self.conversation)
            return
        else:
            print("Starting game")
            mac.send_message(self.print_players(), self.conversation)
            self.started = True
        
        # Dsitribute cards to each player
        self.deal_hands()
        self.deal_board_cards()
        
        # Begin game flow
        self.begin_game_flow()
        
        # Start flops
        #self.show_flop()
        #self.show_turn()
        self.show_river()
        self.show_results()
        
    def begin_game_flow(self):
        self.status = TexasStatus.PREFLOP
        self.start_preflop()
        # Wait for players bets/check/fold
    
    def start_preflop(self):
        self.show_actions()
        
    def show_actions(self):
        mac.send_message("*Actions:*\nCheck: check, ✅\nBet: bet <number>\nFold: fold, culeo, ❌", self.conversation)
    
    def show_flop(self):
        mac.send_message("Flop:\n" + Card.print_pretty_cards(self.board[:3]) + "[ ] [ ]", self.conversation)
            
    def show_turn(self):
        mac.send_message("Turn:\n" + Card.print_pretty_cards(self.board[:4]) + "[ ]", self.conversation)
        
    def show_river(self):
        mac.send_message("River:\n" + Card.print_pretty_cards(self.board[:5]), self.conversation)
        
    def show_results(self):
        results = "*Results:*"
        evaluator = Evaluator()
        for player in self.players:
            print(player.who_name, Card.print_pretty_cards(player.hand))
            player_score = evaluator.evaluate(self.board, player.hand)
            player_class = evaluator.get_rank_class(player_score)
            
            results += "\n• " + player.who_name + " Rank: " + str(player_score) + ", Play: " + evaluator.class_to_string(player_class) + " " + Card.print_pretty_cards(player.hand)
            
        mac.send_message(results, self.conversation)
    
    
    def deal_hands(self):
        for player in self.players:
            player.hand = self.deck.draw(2)
            player.notify_hand()
            
    
    def deal_board_cards(self):
        self.board = self.deck.draw(5)
        
    
    def join(self, player):
        # If haven't already voted in this poll
        if not any(player.who == p.who for p in self.players):
            self.players.append(player)
        
    
    def print_players(self):
        players_str = "*Players:*"
        for player in self.players:
            players_str += "\n+ " + player.who_name
            
        return players_str
        
    
    def finish(self):
        active_games.remove(self)
        
    
    def is_creator(self, creator):
        return self.creator == creator
        
    
    def is_conversation(self, conversation):
        return self.conversation == conversation
        
    
    def is_player_in_game(self, who):
        return who in self.players
        
    
    def take_action(self, action, who):
        if self.status == TexasStatus.BLOCKED:
            return
        if self.status == TexasStatus.PREFLOP:
            pass
        
    '''
    Public function of the inside function called basically
    '''
    @classmethod
    def find_my_game(self, conversation, creator):
        return game_from_user_conversation(conversation, creator)
        
    
    '''
    Interprets the action
    '''
    @classmethod
    def handle_action(self, message):
        if try_join_game(message):
            return
        
        action = get_action(message)
        if action:
            try_action(action, message)
    
    '''
    Finds the poll of this user in this conversation
    Finishes the poll
    '''
    @classmethod
    def finish_my_game(self, creator, conversation):
        game = game_from_user_conversation(conversation, creator)
        if game:
            game.finish()
            

            
'''
Verifies if this chat has a game going on
'''
def chat_has_game(conversation):
    for game in active_games:
        if game.is_conversation(conversation):
            return True
    
    return False
    

'''
Finds the game of the current conversation
'''
def find_chat_game(conversation):
    for game in active_games:
        if game.is_conversation(conversation):
            return game
    
    return None    


'''
Finds game by it's creator and its conversation
'''
def game_from_user_conversation(conversation, creator):
    for game in active_games:
        if game.is_creator(creator):
            if game.is_conversation(conversation):
                return game

    return None
    
'''
Tries to join a game
Returns True if the action was meant to be for this.
I mean, if the player tried to join the game
'''
def try_join_game(message):
    for game in active_games:
        if game.join_identifier in message.message:
            if game.is_conversation(message.conversation):
                if game.started:
                    mac.send_message("Sorry " + message.who_name + ", the game already started", message.conversation)
                    return True
                else:
                    game.join(Player(message))
                    return True
                    
    return False
    

'''
Returns the action chosed by the player
'''
def get_action(message):
    if is_action(message):
        if is_check_action(message):
            return TexasActions.CHECK
        elif is_bet_action(message):
            return TexasActions.BET
        elif is_fold_action(message):
            return TexasActions.FOLD
    
    return None
    

def is_check_action(message):
    if message.message in actions["check"]:
        return True
        
def is_bet_action(message):
    if message.message in actions["bet"]:
        return True
        
def is_fold_action(message):
    if message.message in actions["fold"]:
        return True
    
'''
Check if the message is an action
'''
def is_action(message):
    if message.message in actions_arr:
        return True
    else:
        return False
    
'''
Tries to interpret the action
'''
def try_action(action, message):
    game = find_chat_game(message.conversation)
    if game and game.is_player_in_game(message.who):
        game.take_action(action, message.who)