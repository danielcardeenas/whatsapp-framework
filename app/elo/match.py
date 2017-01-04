from trueskill import TrueSkill, Rating
from app.elo import elo
from app.elo.player import Player
import sqlite3

players = []

def record_match(smash, text):
    # Verify smash
    smash_name = parse_smash(smash)
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
    results_teams = [[] for i in range(len(teams))]
    #Fill results with loses (1) except first one. (0) = win
    result = [1 for i in range(len(teams))]
    result[0] = 0
    
    # Extract rank object of each player
    rating_teams = extract_ranks(teams)
    
    env = TrueSkill() 
    results_teams = env.rate(rating_teams, ranks=result)
    
    # Map results back to teams list
    for rank_team, team in zip(results_teams, teams):
        for rank, player in zip(rank_team, team):
            player.last_mu = player.rank.mu
            player.rank = rank
            
    save_ranks(teams, smash)
            
            
def save_ranks(teams, smash):
    if smash.lower() == 'n64':
        elo.n64_save_rank(teams)
    elif smash.lower() == 'melee':
        elo.melee_save_rank(teams)
    elif smash.lower() == 'brawl':
        elo.brawl_save_rank(teams)
    elif smash.lower() == 'smash4':
        elo.smash4_save_rank(teams)


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
    if not elo.is_valid_smash(smash):
        return None
    
    if smash.lower() == 'n64':
        return elo.n64_players();
    elif smash.lower() == 'melee':
        return elo.melee_players();
    elif smash.lower() == 'brawl':
        return elo.brawl_players();
    elif smash.lower() == 'smash4':
        return elo.smash4_players();
        
def parse_smash(smash):
    if not elo.is_valid_smash(smash):
        return None
    
    if smash.lower() == 'n64':
        return "Smash N64";
    elif smash.lower() == 'melee':
        return "Smash Melee";
    elif smash.lower() == 'brawl':
        return "Smash Brawl";
    elif smash.lower() == 'smash4':
        return "Smash 4";