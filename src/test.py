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

def menu_loop():
	"""show the menu"""
	choice = None
	for key, value in menu.items():
		print('{}) {}'.format(key, value.__doc__))
	choice = input("\nWhat would you like to do?\n").strip()
	menu[choice](0)

def checked(num):
	"""check"""
	global action 
	action = 5


def called(num):
	"""call"""
	global action 
	action = 3
	global minimumbet
	players[num]._money -= minimumbet
	global pot
	pot += minimumbet

def bet(num):
	"""bet"""
	global action 
	action = 4
	bet = int(input("\nHow much would you like to bet?\n").strip())
	global minimumbet
	players[num]._money -= (minimumbet + bet)
	global pot
	pot += (minimumbet + bet)

# Raise - Double the minimum bet
def raised(num):
	"""raise"""
	global action 
	action = 1
	bet = int(input("\nHow much would you like to bet?\n").strip())
	global minimumbet
	players[num]._money -= (minimumbet + bet)
	global pot
	pot += (minimumbet + bet)
	minimumbet += bet

# Quit round - The player loses the money they invested
def folded(num):
	"""fold"""
	global action 
	action = 2
	players[num]._cards = []
	hands[i] = []
	players[num]._move="folded"


 
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
	hands = pokerbot.deal(numplayers+1) #Added 1 for dealer's hand, he will be hands[5]

	for i in range(0, numplayers):
	    players[i]._cards = hands[i]

	# Displays User's Balance and Hand
	print("\n\nYour initial balance: ")
	players[0]._money = 300
	print("$" + str(players[0]._money))
	print("Your hand:")
	print(players[0]._cards)
	# BDIESPLAYOFABOVE: print(hands[0][0]+ ", " + hands[0][1])

	# Request User to make the first bet, then display the user's balance again.

	print("\nthe min bet is {}\n".format(minimumbet))
	if (small_blind == 0):
		players[0]._money -= 1 
		minimumbet = 1
		print("\nPre-flop round!\nYou are the small blind. Your balance is now {}\n".format(str(players[0]._money)))
	elif (big_blind == 0):
		players[0]._money -= 2
		print("\nPre-flop round!\nYou are the big blind. Your balance is now {}\n".format(str(players[0]._money)))
	else:
		minimumbet = 2
		print("\nPre-flop round!\n")

	action = menu_loop()
	print("Your balance is now $" + str(players[0]._money) +".\n")
	time.sleep(1)

	bot_move(action, 1)

#if __name__ == '__main__':
	#game()