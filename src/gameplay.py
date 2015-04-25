import pokerbot
import players

import random
import math
import itertools
from collections import defaultdict

# Player Object (can be placed within its own file later)
class GamePlayer(object):
    def __init__( self ):
        self._cards = []
        self._money = 50
        self._move = " "

print(" *** Harvard Hold'em Poker Bot *** \n")

# Ask user # of players
print("Let's get the game started...")
numplayers = int(input("How many players will there be in this game? (3 - 9 player allowed) \n"))

# Create Player Object for specified amount of players
players = [GamePlayer() for i in range(0, (numplayers+1))]

print("\nDealing hole cards...")
hands = pokerbot.deal(numplayers)  # Creates a list of hands (lists) from # of player input
# print(hands) <-- will show the hands of all the players in the game
# Assigned a hand from the list of hands to each player
for i in range(0, numplayers):
    players[i]._cards = hands[i]

# Displays the users balance and hand
print("Your initial balance: ")
print("$" + str(players[0]._money))
print("Your hand:")
print(players[0]._cards)

# Player 1 Movie
p1firstbet = int(input("\nPre-flop round!\nYou are the small blind. How much would you like to bet?\n"))
players[0]._money -= p1firstbet

# Simulation of other Players
# Player 2
p2firstbet = p1firstbet * 2
players[1]._money -= p2firstbet
minimumbet = p2firstbet

#   Randomly decides a round move for players
#   I don't know what you want to make it based off of
#   Maybe we can change it to a baseline of what a good or bad rank is
#   pokerbot.hand_rank(players[2]._cards)
for i in range(2, numplayers):
    moveoptions = ['call', 'raised', 'fold']
    players[i]._move = random.choice(moveoptions)

# Making players make moves
if players[i]._move == 'call':
    call(i)
elif players[i]._move == 'raised':
    raised(i)
elif players[i]._move == 'fold':
    fold(i)
else:
    print("Invalid move")

def call(num):
    players[num]._money -= minimumbet

