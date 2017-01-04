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
        
        
# Query
####################################################################
def query(query):
    try:
        print(query)
        cursor = conn.execute(query)
        columns = list(map(lambda x: x[0], cursor.description))
        t = PrettyTable(columns)
        index = 0
        for row in cursor:
            t.add_row(row)
            index += 1
            
        return str(t)
        
    except sqlite3.OperationalError as ex:
        return str(ex)
    except:
        return "Invalid query"


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
    save_rank(teams, "n64")
    
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
    save_rank(teams, "melee")
    
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
    save_rank(teams, "brawl")
    
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
    save_rank(teams, "smash4")


# Common functions
####################################################################
def save_rank(teams, smash):
    query = ""
    for team in teams:
        for player in team:
            query += "update " + smash + " "
            query += "set mu = " + str(player.rank.mu) + ", sigma = " + str(player.rank.sigma) + ", "
            query += "last_mu = " + str(player.last_mu) + " "
            query += "where id_player = " + str(player.id_player) + ";"
            query += "\n"
            
    conn.executescript(query)
    
    save_match(teams, smash)
    
    
def save_match(teams, smash):
    # First team is the winner
    # Every team after first is loser
    winners = teams[0]
    losers = teams[1:]
    
    winners_text = ' '.join([str(x.name) for x in winners])
    losers_text = ' '.join([j.name for i in losers for j in i])
    
    query = "insert into matches(winners, losers, game) "
    query += "values ('" + winners_text + "', '" + losers_text + "', '" + smash + "');"
    
    print(query)
    conn.executescript(query)
    
    
def make_table(players, smash_name):
    t = PrettyTable(['🔰', 'Elo', 'Player'])
    index = 0
    for player in players:
        t.add_row([player_status(player, index), '*{0:.2f}*'.format(player.rank.mu), '{s:{c}^{n}}'.format(s=player.name, n=5, c=' ')])
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