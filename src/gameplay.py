import pokerbot
import random


# Player Object (can be placed within its own file later)
class GamePlayer(object):
    def __init__( self ):
        self._cards = []
        self._money = 50
        self._move = " "

print("\n *** Harvard Hold'em Poker Bot *** \n")

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

# Player 1 Move
p1firstbet = int(input("\nPre-flop round!\nYou are the small blind. How much would you like to bet?\n"))
players[0]._money -= p1firstbet

# Simulation of other Players
# Player 2
p2firstbet = p1firstbet * 2
players[1]._money -= p2firstbet
minimumbet = p2firstbet

pot = 0
pot += (p1firstbet + p2firstbet)
def called(num):
    players[num]._money -= minimumbet
    global pot
    pot += minimumbet

def raised(num):
    players[num]._money -= (minimumbet * 2)
    global pot
    pot += (minimumbet * 2)

def folded(num):
    players[num]._cards = []

#   Randomly decides a round move for players
for i in range(2, numplayers):
    moveoptions = ['called', 'raised', 'folded']
    players[i]._move = random.choice(moveoptions)
    if players[i]._move == 'called':
        called(i)
    elif players[i]._move == 'raised':
        raised(i)
    elif players[i]._move == 'folded':
        folded(i)
    else:
        print("Invalid move")

# Simulating the player's moves
print("Player 2 (Big Blind) doubled your bet with $" + str(p1firstbet * 2) + ".")
for i in range(2, numplayers):
    print("Player " + str(i+1) + " " + players[i]._move + ".")

print("The pot is now at a total of $" + str(pot) + ".\n")
print("The flop is...")
