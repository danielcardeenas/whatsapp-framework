from prettytable import PrettyTable
players = [
    'Leind',
    'Rob',
    'Luis',
    'Art',
    'Berni',
    'Nayo',
    'Aaron',
    'Pepe',
    'Cesar',
    'Omar',
    'Casta',
    'Roli',
    'Edgar',
    'Fabi',
    'Lucas'
]

class Elo(object):
    def __init__(self):
        self.players = []
        

def get_ranks(smash):
    if not is_valid_smash(smash):
        return "Invalid smash"
        
        
    t = PrettyTable(['Smash', 'Elo', 'Player'])
    for player in players:
        t.add_row([smash, "*1200*", player])
        
    return t
        
        
def is_valid_smash(smash):
    if smash.lower() == 'n64':
        return True
    elif smash.lower() == 'melee':
        return True
    elif smash.lower() == 'smash4':
        return True
    elif smash.lower() == 'brawl':
        return True