from trueskill import TrueSkill, Rating
from app.elo import elo
from app.elo.player import Player
import sqlite3

players = []

def record_match(smash, text):
    # Verify smash
    smash_name = elo.parse_game(smash)
    if smash_name is None:
        return "Invalid smash"
    
    _teams = [x.strip() for x in text.split('-')]
    teams = [[] for i in range(len(_teams))]
    
    index = 0
    for p in _teams:
        _names = [x.strip() for x in p.split(' ')]
        for name in _names:
            player = get_player(smash, name)
            if player is not None:
                teams[index].append(player)
            else:
                return "Invalid player: " + name
                
        index += 1
        
    make_match(teams, smash)
    return match_confirmation(teams, smash_name)

def match_confirmation(teams, smash):
    first_loop = True
    msg = "*Match:* " + smash + "\n"
    for team in teams:
        if first_loop:
            # Winner team
            msg += "✅ "
        else:
            # Loser team
            msg += "❌ "
            
        for player in team:
                msg += player.name
                msg += " "
        
        msg += "\n"
        first_loop = False
        
    return msg
    

def make_match(teams, smash):
    #Fill results with loses (1, 2, 3...) except first one. (0) = win
    results = [0 for i in range(len(teams))]
    for index, item in enumerate(results):
        results[index] = index
        
    # Extract rank object of each player
    rating_teams = extract_ranks(teams)
    
    env = TrueSkill()
    results_teams = [[] for i in range(len(teams))]
    results_teams = env.rate(rating_teams, ranks=results)
    
    # Map results back to teams list
    for rank_team, team in zip(results_teams, teams):
        for rank, player in zip(rank_team, team):
            player.last_mu = player.rank.mu
            player.rank = rank
            
    save_ranks(teams, smash)
            
            
def save_ranks(teams, smash):
    elo.save_rank(teams, smash)


def extract_ranks(teams):
    groups = [[] for i in range(len(teams))]
    
    index = 0
    for team in teams:
        for player in team:
            groups[index].append(player.rank)
        index += 1
        
    return groups

        
def get_player(smash, name):
    # Get all players needed for this smash
    players = get_players(smash)
    if players is None:
        return None
    
    for player in players:
        if player.name.lower() == name.lower():
            return player
        
    return None


def get_players(smash):
    if not elo.is_valid_game(smash):
        return None
    else:
        return elo.get_players(smash)