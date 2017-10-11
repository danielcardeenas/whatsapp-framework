from enum import Enum

class TexasStatus(Enum):
    PREFLOP = 1
    FLOP = 2
    TURN = 3
    RIVER = 4
    SHOWDOWN = 5
    
class PlayerActions(Enum):
    CHECK = 1
    BET = 2
    FOLD = 3