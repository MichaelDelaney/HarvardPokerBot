import pokerbot
import random
import classifier
import player

# Integrating predictive strategy
user = player.Player()
user_classifier = classifier.Classifier(user)

# Player Object (can be placed within its own file later)
class GamePlayer(object):
    def __init__( self ):
        self._cards = []
        self._money = 50
        self._move = " "

print("\n *** Harvard Hold'em Poker Bot *** \n")

# Ask user # of players
print("Let's get the game started...")
numplayers = int(input("How many players do you want in the game (including yourself)? (3 - 9 player allowed) \n"))

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

# Generate and received the flop  - 3 cards from dealer
print("The flops cards are...")
flophands = pokerbot.flop(1)
flopcards = flophands[0]
print(flopcards)

# Update the hands of the players with the flop cards
for i in range(0, numplayers):
    players[i]._cards += flopcards
    hands[i] = players[i]._cards

# Show new hand
print("\nWith the flop cards, your hand is now...")
print(hands[0])

# We'll remove this later, this just checks the winner at the start of the flop round
# I just wanted to make sure things are working

# Reveal player's hands
print("\nHere comes the reveal of every player's hand!")
print("Your hand: " + str(hands[0]))
for i in range(1, numplayers):
    if players[i]._move == "folded":
        print("Player " + str(i) + ": folded out of round.")
    else:
        print("Player " + str(i+1) + ": " + str(hands[i]))

# Determine the winner of round
print("\nThe winning hand is...")
winninghand = pokerbot.poker(hands)
print(winninghand[0])

if hands[0] == winninghand[0]:
    print("You have won...Congratulations! ")
    players[0]._money += pot
    print("$" + str(pot)+" has been added to your balance")
else:
    for i in range(1, numplayers):
        if hands[i] == winninghand[0]:
            print("Player " + str(i+1) + " has won.")
            players[i]._money += pot
            print("$" + str(pot) +" has been added to Player " + str(i+1) +"'s balance.")
