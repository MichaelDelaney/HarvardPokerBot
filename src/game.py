import pokerbot
import random
import time
import sys
from collections import OrderedDict
from player import *
from classifier import Classifier



# Creating 5 Players
numplayers = 5
player = Player(input("Enter your name: \n"))
players = [GamePlayer() for i in range(0, numplayers-1)]
players.insert(0, player)
classifier = Classifier(player)
predicted_hand = 9
action = 1
minimumbet = 0
pot = 0
small_blind = 0
big_blind = 1
player_bet = 0
communityCards = 3
round = 1

def menu_loop():
	"""show the menu"""
	choice = None
	for key, value in menu.items():
		print('{}) {}'.format(key, value.__doc__))
	choice = input("\nWhat would you like to do?\n").strip()
	try:
		menu[choice](0)
	except:
		print("That is not a valid choice. Try again")
		menu_loop()

def checked(num):
	"""check"""
	global action
	global round
	rank = pokerbot.hole_rank(players[0]._cards)
	classifier.train(action, rank, round)
	action = 5


def called(num):
	"""call"""
	global action 
	action = 3
	global minimumbet
	global player_bet
	global round
	rank = pokerbot.hole_rank(players[0]._cards)
	classifier.train(action, rank, round)
	player_bet= minimumbet
	players[num]._money -= minimumbet
	global pot
	pot += minimumbet

def bot_call(i):
	global minimumbet
	players[i]._money -= minimumbet
	global pot
	pot += minimumbet
	time.sleep(1)
	print('Player {} called'.format(i + 1))
	print('The minimum bet is now {}'.format(minimumbet))

def bet(num):
	"""bet"""
	global action 
	action = 4
	global bet
	global player_bet
	round_bet = int(input("\nHow much would you like to bet?\n").strip())
	player_bet += round_bet
	global minimumbet
	global round
	rank = pokerbot.hole_rank(players[0]._cards)
	players[num]._money -= (minimumbet + round_bet)
	classifier.train(action, rank, round)
	global pot
	pot += (minimumbet + round_bet)

# Raise - Double the minimum bet
def raised(num):
	"""raise"""
	global action
	action = 1
	global player_bet
	round_bet = int(input("\nHow much would you like to bet?\n").strip())
	player_bet += round_bet
	global minimumbet
	players[num]._money -= (minimumbet + round_bet)
	global pot
	global round
	rank = pokerbot.hole_rank(players[0]._cards)
	classifier.train(action, rank, round)
	pot += (minimumbet + round_bet)
	minimumbet += round_bet

def bot_raise(i):
	bet = random.randint(1, 50)
	global minimumbet
	players[i]._money -= (minimumbet + bet)
	global pot
	pot += (minimumbet + bet)
	minimumbet += bet
	time.sleep(1)
	print('Player {} raised {}'.format(i + 1, bet))
	print('The minimum bet is now {}'.format(minimumbet))

# Quit round - The player loses the money they invested
def folded(num):
	"""fold"""
	global action
	action = 2
	global round
	players[num]._cards = []
	hands[i] = []
	rank = pokerbot.hole_rank(players[0]._cards)
	classifier.train(action, rank, round)
	players[num]._move = "folded"

def bot_fold(i):
	players[i]._cards = []
	hands[i] = []
	players[i]._move = "folded"
	time.sleep(1)
	print('Player {} folded'.format(i + 1))

def rotate_blinds(big_blind, small_blind):
	if (big_blind == 4):
		big_blind = 0
	else: 
		big_blind += 1

	if (small_blind == 4):
		small_blind = 0
	else: 
		small_blind += 1

	return 	big_blind, small_blind


def bot_move(action, round, board_rank=8):
	global predicted_hand
	predicted_hand = classifier.predict(action, round, board_rank)
	for bot in players:
		i = players.index(bot)
		if (bot == player):
			continue
		rank = pokerbot.hole_rank(bot._cards)
		bluff = random.randint(1, 10)
		play_safe = random.randint(1, 10)
		if (rank < predicted_hand or bluff > 6):
			bot_raise(i)
		elif (rank == predicted_hand or play_safe > 6):
			bot_call(i)
		else:
			bot_fold(i)
# the fist person to raise the minimum bet above big blind = bet
# anyone who raises after that = raise
if (minimumbet == bet):
	menu = OrderedDict ([
		("1", checked),
		("2", bet),
		("3", raised),
		("4", folded),
	])
else:
	menu = OrderedDict ([
		("1", called),
		("2", bet),
		("3", raised),
		("4", folded),
	])

	# Game Title and Welcome
	print("\n *** Harvard Hold'em Poker Bot *** \n")
	print("Welcome. Let's get the game started...")

	# Places 2 Cards in Each Player's Hand
	for i in range(0, 3):
	    sys.stdout.flush()
	    time.sleep(.3)
	    sys.stdout.write("\rDealing hole cards..")
	    time.sleep(.3)
	    sys.stdout.write("\rDealing hole cards....")
	    time.sleep(.3)
	    sys.stdout.write("\rDealing hole cards.....")
	hands = pokerbot.deal(numplayers+1+communityCards) #Added 1 for dealer's hand, he will be hands[5]

	for i in range(0, numplayers):
   		players[i]._cards = hands[i]

	flopCards = [hands[7][0]] + hands[6]
	turnCards = [hands[7][1]]
	riverCards = [hands[8][0]]

	# Displays User's Balance and Hand
	print("\n\nYour initial balance: ")
	players[0]._money = 300
	print("$" + str(players[0]._money))
	print("Your hand:")
	print(players[0]._cards)
	# BDIESPLAYOFABOVE: print(hands[0][0]+ ", " + hands[0][1])

	# Request User to make the first bet, then display the user's balance again.
def announce_round(round):
	global minimumbet
	print("\nthe min bet is {}\n".format(minimumbet))
	if (small_blind == 0):
		players[0]._money -= 1 
		minimumbet = 1
		print("\n{}!\nYou are the small blind. Your balance is now {}\n".format(round, str(players[0]._money)))
	elif (big_blind == 0):
		players[0]._money -= 2
		print("\n{}!\nYou are the big blind. Your balance is now {}\n".format(round, str(players[0]._money)))
	else:
		minimumbet = 2
		print("\n{}!\n".format(round))

announce_round("Pre-flop round")

choice = menu_loop()
print("Your balance is now $" + str(players[0]._money) +".\n")
time.sleep(1)

bot_move(action, 1)
big_blind, small_blind = rotate_blinds(big_blind, small_blind)


#####################
# Reveal Flop Cards
#####################
# Flop - Dealer shows 3 Community Cards
print("The flops cards are...")
print(flopCards)
time.sleep(2)

announce_round("flop round")
choice = menu_loop()

print("Your balance is now $" + str(players[0]._money) +".\n")
time.sleep(1)

board_rank = pokerbot.board_rank(flopCards, 1)
bot_move(action, 2, board_rank)
# Update the hands of the players with the flop cards
for i in range(0, numplayers):
	try:
		players[i]._cards += flopCards
		hands[i] = players[i]._cards
	except:
		pass

big_blind, small_blind = rotate_blinds(big_blind, small_blind)

#####################
# Reveal Turn Card
#####################
# Turn - Dealer shows 1 More Community Card
print("\nThe turn card is...")
print(turnCards)
time.sleep(2)

# Show all community cards
print("The 4 community cards so far are...")
print(turnCards+flopCards)
time.sleep(1)

# Update the hands of the players with the turn cards
for i in range(0, numplayers):
	try:
	    if players[i]._move != "folded":
	        players[i]._cards += turnCards
	        hands[i] = players[i]._cards
	except:
		pass


announce_round("Turn card round")
choice = menu_loop()

print("Your balance is now $" + str(players[0]._money) +".\n")
time.sleep(1)

board_rank = pokerbot.board_rank(flopCards, 3)
bot_move(action, 3, board_rank)

######################
# Reveal River Card
######################

# Turn - Dealer shows 1 More Community Card
print("\nThe river card is...")
print(riverCards)
time.sleep(2)

# Show all community cards
print("The 5 community cards so far are...")
print(riverCards+turnCards+flopCards)
time.sleep(1)

# Update the hands of the players with the turn cards
for i in range(0, numplayers):
    if players[i]._move != "folded":
        players[i]._cards += riverCards
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

announce_round("The river!")
choice = menu_loop()

print("Your balance is now $" + str(players[0]._money) +".\n")
time.sleep(1)

board_rank = pokerbot.board_rank(flopCards, 3)
bot_move(action, 4, board_rank)


####################
# Reveal The Winner
####################

print("\nHere comes the reveal of every player's best ranked hand!")
# Turn - Dealer shows 1 More Community Card
dealercards = hands[5]
print("\nThese are the dealers cards:" + str(dealercards) + "\n")

# Call community cards to dealer's hand
dealercards = dealercards + flopCards + turnCards + riverCards
hands[5] = list(pokerbot.best_hand(dealercards))
time.sleep(1)
print("The Dealer's best ranked hand is: " + str(hands[5]))

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
for i in range(0, numplayers+1): #Plys 1 for the dealers hand
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


#if __name__ == '__main__':
	#game()