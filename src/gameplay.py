import pokerbot
import random
import time
import sys

# Player Object
class GamePlayer(object):
    def __init__( self ):
        self._name = " "
        self._cards = []
        self._money = 500000
        self._move = " "

# Game Title and Welcome
print("\n *** Harvard Hold'em Poker Bot *** \n")
print("Welcome. Let's get the game started...")

# Creating 5 Players
numplayers = 5
players = [GamePlayer() for i in range(0, numplayers)]

# Request User's Name (User is Player[0])
players[0]._name = input("Enter your name: \n")

# Places 2 Cards in Each Player's Hand
for i in range(0, 3):
    sys.stdout.flush()
    time.sleep(.3)
    sys.stdout.write("\rDealing hole cards..")
    time.sleep(.3)
    sys.stdout.write("\rDealing hole cards....")
    time.sleep(.3)
    sys.stdout.write("\rDealing hole cards.....")
hands = pokerbot.deal(numplayers+1) #Added 1 for dealer's hand, he will be hands[5]
for i in range(0, numplayers):
    players[i]._cards = hands[i]

# Displays User's Balance and Hand
print("\n\nYour initial balance: ")
players[0]._money = 500
print("$" + str(players[0]._money))
print("Your hand:")
print(players[0]._cards)
# BDIESPLAYOFABOVE: print(hands[0][0]+ ", " + hands[0][1])

# Request User to make the first bet, then display the user's balance again.
p1firstbet = int(input("\nPre-flop round!\nYou are the small blind. How much would you like to bet?\n"))
players[0]._money -= p1firstbet
print("Your balance is now $" + str(players[0]._money) +".\n")
time.sleep(1)

# Player 2 (Big Blind) doubles the bet of the User.
# This is also considered the minimum bet in the round now.
p2firstbet = p1firstbet * 2
players[1]._money -= p2firstbet
minimumbet = 0
minimumbet = p2firstbet

# Create Table Pot and add current bets to it
pot = 0
pot += (p1firstbet + p2firstbet)

# Call - Stay in round by making minimum bet
def called(num):
    players[num]._money -= minimumbet
    global pot
    pot += minimumbet

# Raise - Double the minimum bet
def raised(num):
    global minimumbet
    players[num]._money -= (minimumbet * 2)
    global pot
    pot += (minimumbet * 2)
    minimumbet = (minimumbet * 2)

# Quit round - The player loses the money they invested
def folded(num):
    players[num]._cards = []
    hands[i] = []
    players[num]._move="folded"

# Randomly decides a round move for players
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

# Try to Determine is a Player Raised
count = 0
for i in range(1, numplayers):
    if players[i]._move == 'raised':
        count += 1

# Display the moves the players made.
print("Player 2 (Big Blind) doubled your bet with $" + str(p1firstbet * 2) + ".")
time.sleep(1)
for i in range(2, numplayers):
    print("Player " + str(i+1) + " " + players[i]._move + ".")
    time.sleep(1)

# Display New Balance of Pot
print("The pot is now at a total of $" + str(pot) + ".\n")
time.sleep(1)

# User selects a next move
def move(selectedmove):
    if selectedmove == 'call':
        called(0)
    elif selectedmove == 'raise':
        raised(0)
    elif selectedmove == 'fold':
        folded(0)
    else:
        print("Invalid move")

# User Must decide a second move if another player Raised
if count > 0:
    usermove = input("\nWould you like to call, raise , or fold? \n")
    move(usermove)
    print("Your balance is at $" + str(players[0]._money) +".\n")
    time.sleep(1)

    # Randomly decides a round move for players
    for i in range(1, numplayers):
        if players[i]._move != 'folded':
            moveoptions = ['called', 'raised', 'folded']
            players[i]._move = random.choice(moveoptions)
            if players[i]._move == 'called':
                called(i)
            elif players[i]._move == 'raised':
                raised(i)
            elif players[i]._move == 'folded':
                folded(i)
                print("Player " + str(i+1) + " folded.")
            else:
                print("Invalid move")

    # Display the moves the players made.
    time.sleep(1)
    for i in range(1, numplayers):
        if players[i]._move != 'folded':
            print("Player " + str(i+1) + " " + players[i]._move + ".")
            time.sleep(1)

    # Display the New Balance of Pot
    print("The pot is now at a total of $" + str(pot) + ".\n")
    time.sleep(1)

# Flop - Dealer shows 3 Community Cards
print("The flops cards are...")
flophands = pokerbot.flop(1)
flopcards = flophands[0]
print(flopcards)
time.sleep(2)

# Update the hands of the players with the flop cards
for i in range(0, numplayers):
    players[i]._cards += flopcards
    hands[i] = players[i]._cards

# User selects a move (bet) for the flop round
def move(selectedmove):
    if selectedmove == 'call':
        called(0)
    elif selectedmove == 'raise':
        raised(0)
    elif selectedmove == 'fold':
        folded(0)
    else:
        print("Invalid move")

# Next player move
if players[0]._move != "folded":
    # Show new hand
    print("\nWith the flop cards, your hand is now...")
    print(hands[0])
    usermove = input("\nWould you like to call, raise , or fold? \n")
    move(usermove)
    print("Your balance is at $" + str(players[0]._money) +".\n")
    time.sleep(1)

# Other player's make move in flop round
for i in range(1, numplayers):
    if players[i]._move != 'folded':
        players[i]._move = random.choice(moveoptions)
        if players[i]._move == 'called':
            called(i)
        elif players[i]._move == 'raised':
            raised(i)
        elif players[i]._move == 'folded':
            folded(i)
            print("Player " + str(i+1) + " folded.")
        else:
            print("Invalid move")

# Display the moves the players made in the flop round
time.sleep(1)
for i in range(1, numplayers):
    if players[i]._move != 'folded':
        print("Player " + str(i+1) + " " + players[i]._move + ".")
        time.sleep(1)

########################################################
####     TURN ROUND
########################################################
# Turn - Dealer shows 1 More Community Card
print("\nThe turn card is...")
turnhands = pokerbot.turn(1)
turncards = turnhands[0]
print(turncards)
time.sleep(2)

# Show all community cards
print("The 4 community cards so far are...")
print(turncards+flopcards)
time.sleep(1)

# Update the hands of the players with the turn cards
for i in range(0, numplayers):
    if players[i]._move != "folded":
        players[i]._cards += turncards
        hands[i] = players[i]._cards

# Show new hand including flop and turn cards
if players[0]._move != "folded":
    print("\nWith the flop and turn cards, your new hand is now...")
    print(hands[0])
    time.sleep(1)

# Update all then hands with the best combo of 5 cards
for i in range(0, numplayers):
    if players[i]._move != "folded":
        hands[i] = list(pokerbot.best_hand(hands[i]))

if players[0]._move != "folded":
    print("\nYour hands best 5 card rank is...")
    print(hands[0])
    usermove = input("\nWould you like to call, raise , or fold? \n")
    move(usermove)

# Other player's make move in flop round
for i in range(1, numplayers):
    if players[i]._move != 'folded':
        players[i]._move = random.choice(moveoptions)
        if players[i]._move == 'called':
            called(i)
        elif players[i]._move == 'raised':
            raised(i)
        elif players[i]._move == 'folded':
            folded(i)
            print("Player " + str(i+1) + " folded.")
        else:
            print("Invalid move")

# Display the moves the players made in the flop round
time.sleep(1)
for i in range(1, numplayers):
    if players[i]._move != 'folded':
        print("Player " + str(i+1) + " " + players[i]._move + ".")
        time.sleep(1)

########################################################
#### START OF RIVER
#######################################################
# Turn - Dealer shows 1 More Community Card
print("\nThe river card is...")
riverhands = pokerbot.turn(1)
rivercards = riverhands[0]
print(rivercards)
time.sleep(2)

# Show all community cards
print("The 5 community cards so far are...")
print(rivercards+turncards+flopcards)
time.sleep(1)

# Update the hands of the players with the turn cards
for i in range(0, numplayers):
    if players[i]._move != "folded":
        players[i]._cards += rivercards
        hands[i] = players[i]._cards


# Show new hand including flop and turn cards
if players[0]._move != "folded":
    print("\nWith the flop, turn, and river cards, your new 7 card hand is now...")
    print(hands[0])
    time.sleep(1)

# Update all then hands with the best combo of 5 cards
for i in range(0, numplayers):
    if players[i]._move != "folded":
        hands[i] = list(pokerbot.best_hand(hands[i]))

if players[0]._move != "folded":
    print("\nYour hands best 5 card rank is...")
    print(hands[0])
    usermove = input("\nWould you like to call, raise , or fold? \n")
    move(usermove)


# Other player's make move in flop round
for i in range(1, numplayers):
    if players[i]._move != 'folded':
        players[i]._move = random.choice(moveoptions)
        if players[i]._move == 'called':
            called(i)
        elif players[i]._move == 'raised':
            raised(i)
        elif players[i]._move == 'folded':
            folded(i)
            print("Player " + str(i+1) + " folded.")
        else:
            print("Invalid move")

# Display the moves the players made in the flop round
time.sleep(1)
for i in range(1, numplayers):
    if players[i]._move != 'folded':
        print("Player " + str(i+1) + " " + players[i]._move + ".")
        time.sleep(1)

########################################################
#### REVEALING HANDS AND WINNER
#######################################################


print("\nHere comes the reveal of every player's best ranked hand!")
# Turn - Dealer shows 1 More Community Card
dealerhands = pokerbot.deal(1)
dealercards = dealerhands[0]

# Call community cards to dealer's hand
dealercards = dealercards + flopcards + turncards + rivercards
hands[5] = list(pokerbot.best_hand(dealercards))
time.sleep(1)
print("The Dealer's hand is: " + str(hands[5]))

if players[0]._move != "folded":
    print("Your hand: " + str(hands[0]))
    time.sleep(1)

for i in range(1, numplayers):
    if players[i]._move == "folded":
        # If a player folded update their cards in hands[i]
        hands[i] = []
    else:
        print("Player " + str(i+1) + ": " + str(hands[i]))

# Before determining winner, make sure there are no null hands going
# going in as input in poker() func
winningHands = []
for i in range(0, numplayers+1):
    if hands[i] != []:
        winningHands += [hands[i]]

# Need more than 1 value to unpack winner
count2 = 0
for i in range(0, numplayers):
    if players[i]._move == "folded":
        count2 += 1

# Determine the winner of round
print("\nThe winning hand is...")
if count2 == 5:
    print("The dealer has won!")
    print(str(hands[5]))
else:
    winningPlayer = pokerbot.poker(winningHands)
    winner = winningPlayer[0]
    print(str(winner))
    if hands[0] == winner:
        print("You have won...Congratulations! ")
        players[0]._money += pot
        print("$" + str(pot)+" has been added to your balance!")
    elif hands[5] == winner:
        print("Sorry, the dealer has won!")
    else:
        for i in range(1, numplayers):
                if hands[i] == winner:
                    print("Player " + str(i+1) + " has won.")
                    players[i]._money += pot
                    print("$" + str(pot) + " has been added to Player " + str(i+1) + "'s balance.")

