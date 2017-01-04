from prettytable import PrettyTable
from trueskill import Rating
from app.elo.player import Player
import sqlite3

conn = sqlite3.connect('app/elo/db/elo.db')

def ranks(smash):
    if not is_valid_smash(smash):
        return "Invalid smash"
    
    if smash.lower() == 'n64':
        return n64_rank();
    elif smash.lower() == 'melee':
        return melee_rank();
    elif smash.lower() == 'brawl':
        return brawl_rank();
    elif smash.lower() == 'smash4':
        return smash4_rank();

# Smash N64
####################################################################
def n64_rank():
    players = n64_players()
    return make_table(players, "Smash N64")
        

def n64_players():
    players = []
    for row in conn.execute('select mu, sigma, name, players.id, last_mu from players join n64 on players.id = n64.id_player order by mu desc'):                                                                                                                                           
        players.append(Player(row[2], row[3], row[4], Rating(mu=row[0], sigma=row[1])))
        
    return players
    

def n64_save_rank(teams):
    query = ""
    for team in teams:
        for player in team:
            query += "update n64 "
            query += "set mu = " + str(player.rank.mu) + ", sigma = " + str(player.rank.sigma) + ", "
            query += "last_mu = " + str(player.last_mu) + " "
            query += "where id_player = " + str(player.id_player) + ";"
            query += "\n"
            
    conn.executescript(query)
    
# Melee
####################################################################
def melee_rank():
    players = melee_players()
    return make_table(players, "Smash Melee")
        

def melee_players():
    players = []
    for row in conn.execute('select mu, sigma, name, players.id, last_mu from players join melee on players.id = melee.id_player order by mu desc'):                                                                                                                                           
        players.append(Player(row[2], row[3], row[4], Rating(mu=row[0], sigma=row[1])))
        
    return players
    
    
def melee_save_rank(teams):
    query = ""
    for team in teams:
        for player in team:
            query += "update melee "
            query += "set mu = " + str(player.rank.mu) + ", sigma = " + str(player.rank.sigma) + ", "
            query += "last_mu = " + str(player.last_mu) + " "
            query += "where id_player = " + str(player.id_player) + ";"
            query += "\n"
            
    conn.executescript(query)
    
# Brawl
####################################################################
def brawl_rank():
    players = brawl_players()
    return make_table(players, "Smash Brawl")
        

def brawl_players():
    players = []
    for row in conn.execute('select mu, sigma, name, players.id, last_mu from players join brawl on players.id = brawl.id_player order by mu desc'):                                                                                                                                           
        players.append(Player(row[2], row[3], row[4], Rating(mu=row[0], sigma=row[1])))
        
    return players
    
    
def brawl_save_rank(teams):
    query = ""
    for team in teams:
        for player in team:
            query += "update brawl "
            query += "set mu = " + str(player.rank.mu) + ", sigma = " + str(player.rank.sigma) + ", "
            query += "last_mu = " + str(player.last_mu) + " "
            query += "where id_player = " + str(player.id_player) + ";"
            query += "\n"
            
    conn.executescript(query)
    
# Smash4
####################################################################
def smash4_rank():
    players = smash4_players()
    return make_table(players, "Smash4")

def smash4_players():
    players = []
    for row in conn.execute('select mu, sigma, name, players.id, last_mu from players join smash4 on players.id = smash4.id_player order by mu desc'):                                                                                                                                           
        players.append(Player(row[2], row[3], row[4], Rating(mu=row[0], sigma=row[1])))
        
    return players
    
    
def smash4_save_rank(teams):
    query = ""
    for team in teams:
        for player in team:
            query += "update smash4 "
            query += "set mu = " + str(player.rank.mu) + ", sigma = " + str(player.rank.sigma) + ", "
            query += "last_mu = " + str(player.last_mu) + " "
            query += "where id_player = " + str(player.id_player) + ";"
            query += "\n"
            
    conn.executescript(query)


def make_table(players, smash_name):
    t = PrettyTable(['🔰', 'Elo', 'Player'])
    index = 0
    for player in players:
        t.add_row([player_status(player, index), '*{0:.2f}*'.format(player.rank.mu), player.name])
        index += 1
        
    return "*" + smash_name + " ranking:*\n" + str(t)


def player_status(player, position):
    if position == 0:
        return "🔝"
    elif player.rank.mu == player.last_mu:
        return "➖"
    elif player.rank.mu > player.last_mu:
        return "⬆"
    else:
        return "⬇"

def is_valid_smash(smash):
    if smash.lower() == 'n64':
        return True
    elif smash.lower() == 'melee':
        return True
    elif smash.lower() == 'smash4':
        return True
    elif smash.lower() == 'brawl':
        return True