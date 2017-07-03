from prettytable import PrettyTable
from trueskill import Rating
from app.modules.elo.player import Player
import sqlite3

conn = sqlite3.connect('app/modules/elo/db/trueskill.db')

def ranks(smash):
    if not is_valid_game(smash):
        return "Invalid smash"
    else:
        return rank(smash)
        
        
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
    

def rank(game):
    players = get_players(game)
    return make_table(players, parse_game(game))


def get_players(game):
    players = []
    for row in conn.execute('select mu, sigma, name, players.id, last_mu from players join ' + game + ' on players.id = ' + game + '.id_player order by mu desc'):                                                                                                                                           
        players.append(Player(row[2], row[3], row[4], Rating(mu=row[0], sigma=row[1])))
        
    return players
    
    
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
    if smash.lower() == 'smash64':
        return True
    elif smash.lower() == 'melee':
        return True
    elif smash.lower() == 'smash4':
        return True
    elif smash.lower() == 'brawl':
        return True
    else:
        return False
        
        
def is_valid_game(smash):
    if is_valid_smash(smash):
        return True
    elif smash.lower() == 'mp2':
        return True
    else:
        return False
        
        
def parse_game(game):
    if not is_valid_game(game):
        return None
    
    if game.lower() == 'smash64':
        return "Smash N64";
    elif game.lower() == 'melee':
        return "Smash Melee";
    elif game.lower() == 'brawl':
        return "Smash Brawl";
    elif game.lower() == 'smash4':
        return "Smash 4";
    elif game.lower() == 'mp2':
        return "Mario Party 2"