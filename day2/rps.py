P_WIN = 6
P_DRAW = 3
P_LOST = 0

P_ROCK = 1
P_PAPER = 2
P_SCISSOR = 3

from enum import Enum
class RPS(Enum):
    ROCK = 1
    PAPER = 2
    SCISSOR = 3

MAP = {
    'A':RPS.ROCK,
    'B':RPS.PAPER,
    'C':RPS.SCISSOR,
    'X':RPS.ROCK,
    'Y':RPS.PAPER,
    'Z':RPS.SCISSOR,
}

MAP_SCORE = {
    RPS.ROCK: P_ROCK,
    RPS.PAPER : P_PAPER,
    RPS.SCISSOR: P_SCISSOR
}

def get_winner (a, b):
    if a == RPS.ROCK:
        if b == RPS.ROCK:
            return 0
        elif b == RPS.PAPER:
            return 1
        else:
            return -1
    elif a == RPS.PAPER:
        if b == RPS.ROCK:
            return -1
        elif b == RPS.PAPER:
            return 0
        else:
            return 1
    else:
        if b == RPS.ROCK:
            return 1
        elif b == RPS.PAPER:
            return -1
        else:
            return 0

lines = None
with open("rps_input.txt") as file:
    lines = [line.strip("\n") for line in file]

score = 0
player_one = None
Player_two = None
for line in lines:
    if len(line) != 3:
        raise ValueError("An error occurred")

    player_one = MAP[line[0]]
    player_two = MAP[line[2]]

    result = get_winner(player_one, player_two)
    if result == 1:
        score += P_WIN
    elif result == 0:
        score += P_DRAW
    else:
        score += P_LOST

    score += MAP_SCORE[player_two]

print(f"score one: {score}")


### SECOND

MAP_ONE = {
    'A':RPS.ROCK,
    'B':RPS.PAPER,
    'C':RPS.SCISSOR
}

MAP_STRATEGY = {
    'X':-1,
    'Y':0,
    'Z':1
}

def get_win(a):
    if a == RPS.ROCK:
        return RPS.PAPER
    elif a == RPS.PAPER:
        return RPS.SCISSOR
    else:
        return RPS.ROCK

def get_draw(a):
    return a

def get_lost(a):
    if a == RPS.ROCK:
        return RPS.SCISSOR
    elif a == RPS.PAPER:
        return RPS.ROCK
    else:
        return RPS.PAPER


score = 0
player_one = None
Player_two = None
for line in lines:
    if len(line) != 3:
        raise ValueError("An error occurred")

    player_one = MAP_ONE[line[0]]
    strategy = MAP_STRATEGY[line[2]]

    if strategy == 1:
        player_two = get_win(player_one)
        score += P_WIN
    elif strategy == 0:
        player_two = get_draw(player_one)
        score += P_DRAW
    else:
        player_two = get_lost(player_one)
        score += P_LOST
    score += MAP_SCORE[player_two]

print(f"score two: {score}")