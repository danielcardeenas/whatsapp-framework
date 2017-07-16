# -*- coding: utf-8 -*-
from app.utils import helper
from app.mac import mac
from modules.poker.player import Player
from modules.poker.deuces import Card, Deck, Evaluator
from modules.poker.constants import TexasStatus, PlayerActions

MIN_PLAYERS = 1
active_games = []
actions = dict(
    check = ["check", "✅"],
    fold = ["fold", "culeo", "❌"],
    bet = ["bet"],
    call = ["call"]
)

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
        self.block_actions = False
        self.pot = 0
        self.highest_bet = 0
        
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
        if len(self.players) < MIN_PLAYERS:
            mac.send_message("Not enough players to start", self.conversation)
            return
        
        elif self.started:
            mac.send_message("Your game already started", self.conversation)
            return
        else:
            mac.send_message(self.print_players(), self.conversation)
            self.started = True
        
        # Block incoming
        self.block_actions = True
        
        # Dsitribute cards to each player
        self.deal_hands()
        self.deal_board_cards()
        
        # Begin game flow
        self.begin_game_flow()
        
        # Unblock
        self.block_actions = False
        
        
    def begin_game_flow(self):
        self.status = TexasStatus.PREFLOP
        self.start_preflop()
        # Wait for players bets/check/fold
    
    def start_preflop(self):
        self.show_actions()
        
    def show_actions(self):
        mac.send_message("*Actions:*\nCheck: check, ✅\nBet: bet <number>\nFold: fold, culeo, ❌", self.conversation)
    
    def show_flop(self):
        self.status = TexasStatus.FLOP
        mac.send_message("Flop:\n" + Card.print_pretty_cards(self.board[:3]) + "[ ] [ ]", self.conversation)
            
    def show_turn(self):
        self.status = TexasStatus.TURN
        mac.send_message("Turn:\n" + Card.print_pretty_cards(self.board[:4]) + "[ ]", self.conversation)
        
    def show_river(self):
        self.status = TexasStatus.RIVER
        mac.send_message("River:\n" + Card.print_pretty_cards(self.board[:5]), self.conversation)
        
    def show_results(self):
        results = "*💰*: $" + str(self.pot) + "\n*Results:*"
        evaluator = Evaluator()
        for player in self.players:
            player_score = evaluator.evaluate(self.board, player.hand)
            player_class = evaluator.get_rank_class(player_score)
            
            results += "\n• " + player.who_name + " Rank: " + str(player_score) + ", Play: " + evaluator.class_to_string(player_class) + "\n" + Card.print_pretty_cards(player.hand)
            
        mac.send_message(results, self.conversation)
        self.finish()
    
    
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
            players_str += "\n• " + player.who_name + " ($" + str(player.money) + ")"
            
        return players_str
        
    def print_players_stauts(self):
        players_status = "*💰*: " + str(self.pot) + "\n*Players:*"
        for player in self.players:
            players_status += "\n• " + player.pretty_status(self.highest_bet)
            
        return players_status
        
    
    def finish(self):
        active_games.remove(self)
        
    
    def is_creator(self, creator):
        return self.creator == creator
        
    
    def is_conversation(self, conversation):
        return self.conversation == conversation
        
    
    def is_player_in_game(self, who):
        return any(who == p.who for p in self.players)
        
    
    def player_in_game(self, who):
        for player in self.players:
            if player.who == who:
                return player
                
        return None
        
    def all_players_locked(self):
        for player in self.players:
            if not player.locked:
                return False
        
        return True
        
    def go_to_end(self):
        if self.status != TexasStatus.RIVER or self.status != TexasStatus.SHOWDOWN:
            self.show_river()
        self.show_results()
        
    def nothing_to_do(self):
        if all(player.money <= 0 for player in self.players):
            return True
        
    def can_advance(self):
        if len(self.players) <= MIN_PLAYERS:
            # Not enough players, finish the game
            self.go_to_end()
            return False
            
        if self.nothing_to_do():
            self.go_to_end()
            return False
            
        if self.all_players_locked():
            return True
        else:
            return False
    
    def do_next_turn(self):
        # Ignore incoming actions
        self.highest_bet = 0
        self.block_actions = True
        self.reset_players_status()
        
        # If preflop -> flop
        if self.status == TexasStatus.PREFLOP:
            self.show_flop()
            self.block_actions = False
            return
            
        # If flop -> turn
        elif self.status == TexasStatus.FLOP:
            self.show_turn()
            self.block_actions = False
            return
            
        # If turn -> river
        elif self.status == TexasStatus.TURN:
            self.show_river()
            self.block_actions = False
            return
            
        # If river -> showdown
        elif self.status == TexasStatus.RIVER:
            self.show_results()
            self.block_actions = False
            return
    
    def reset_players_status(self):
        for player in self.players:
            player.reset_status()
            
    
    def reset_checked_players(self):
        for player in self.players:
            if player.action == PlayerActions.CHECK:
                player.action = None
                player.unlock()
        
    def is_everyone_checked(self):
        return all(player.action == PlayerActions.CHECK for player in self.players)
        
    def reset_lower_bets(self):
        for player in self.players:
            if player.current_bet < self.highest_bet:
                player.unlock()
        
    def set_bet(self, bet, player):
        if player.current_bet > self.highest_bet:
            self.highest_bet = player.current_bet
        self.reset_checked_players()
        self.reset_lower_bets()
        self.pot = self.pot + bet
        
    
    def take_action(self, action, player, bet=0):
        if self.block_actions:
            return
        
        if action == PlayerActions.CHECK:
            if player.set_action(PlayerActions.CHECK, self.players):
                mac.send_message(self.print_players_stauts(), self.conversation)
        elif action == PlayerActions.FOLD:
            if player.set_action(PlayerActions.FOLD, self.players):
                self.players.remove(player)
                mac.send_message(player.who_name + " folded", self.conversation)
        elif action == PlayerActions.BET:
            if player.set_action(PlayerActions.BET, self.players, bet):
                self.set_bet(bet, player)
                mac.send_message(self.print_players_stauts(), self.conversation)
                
        if self.can_advance():
            self.do_next_turn()
        
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
    Finishes the game
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
    if is_check_action(message):
        return PlayerActions.CHECK
    elif is_bet_action(message):
        return PlayerActions.BET
    elif is_fold_action(message):
        return PlayerActions.FOLD
    else:
        return None
    

def is_check_action(message):
    if message.message.lower() in actions["check"]:
        return True
        
def is_bet_action(message):
    if message.message.lower().split(" ")[0] in actions["bet"]:
        return True
        
def is_fold_action(message):
    if message.message.lower() in actions["fold"]:
        return True
    
'''
Tries to interpret the action
'''
def try_action(action, message):
    game = find_chat_game(message.conversation)
    player = None
    if game:
        player = game.player_in_game(message.who)
    if game and player:
        if not player.locked:
            if action == PlayerActions.BET:
                game.take_action(action, player, bet_from_message(message))
            else:
                game.take_action(action, player)
            
def bet_from_message(message):
    try:
        arg = message.message.split(' ')[1]
        return float(arg)
    except:
        return 0