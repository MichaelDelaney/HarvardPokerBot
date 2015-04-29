import random
import time
import sys
from collections import OrderedDict
from player import Bot
from player import Player
from classifier import Classifier
from poker import Poker

class Pokergame:
	def setup (self):
		self.numplayers = 5
		self.player = Player(input("Enter your name: \n"))
		self.players = [Bot(i) for i in range(0, self.numplayers-1)]
		self.players.insert(0, self.player)
		self.poker = Poker()
		self.predicted_hand = 9
		self.action = 1
		self.minimumbet = 0
		self.pot = 0
		self.small_blind = 2
		self.big_blind = 1
		self.go_first = 0
		self.board_rank = 8
		self.communityCards = 3
		self.rounds = [(1, "Pre-flop"), (2, "Flop"), (3, "Turn"), (4, "The river")]
		self.round = self.get_next_round()
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
			hands = self.poker.deal(self.numplayers + 1 + self.communityCards) #Added 1 for dealer's hand, he will be hands[5]

		for i in range(0, self.numplayers):
	   		self.players[i]._cards = hands[i]

		self.flopCards = [hands[7][0]] + hands[6]
		self.turnCards = [hands[7][1]]
		self.riverCards = [hands[8][0]]
		self.board = self.flopCards

		# Displays User's Balance and Hand
		print("\n\nYour initial balance: ")
		self.players[0]._money = 300
		print("$" + str(self.players[0]._money))
		print("Your hand:")
		print(self.players[0]._cards)
		self.announce_round()

	def get_next_round(self):
		try:
			return self.rounds.pop(0)
		except IndexError:
			return None

	def announce_round(self):
		round_id, round = self.round
		print("\nthe min bet is {}\n".format(self.minimumbet))
		if (self.small_blind == 0):
			players[0]._money -= 1 
			self.minimumbet = 1
			print("\n{}!\nYou are the small blind. Your balance is now {}\n".format(round, str(players[0]._money)))
		elif (self.big_blind == 0):
			players[0]._money -= 2
			print("\n{}!\nYou are the big blind. Your balance is now {}\n".format(round, str(players[0]._money)))
		else:
			self.minimumbet = 2
			print("\n{}!\n".format(round))
		self.menu_loop()

	def get_menu (self):
		if (self.minimumbet == self.player.bet):
			return OrderedDict ([
				("1", self.player.checked),
				("2", self.player.bet),
				("3", self.player.raised),
				("4", self.player.folded),
			])
		else:
			return OrderedDict ([
				("1", self.player.called),
				("2", self.player.bet),
				("3", self.player.raised),
				("4", self.player.folded),
			])

	def menu_loop(self):
		"""show the menu"""
		menu = self.get_menu()
		round_id, round = self.round
		choice = None
		for key, value in menu.items():
			print('{}) {}'.format(key, value.__doc__))
		choice = input("\nWhat would you like to do?\n").strip()
		try:
			action, self.minimumbet, self.pot = menu[choice](round_id, self.minimumbet, self.pot)
		except:
			print("That is not a valid choice. Try again")
			time.sleep(1)
			self.menu_loop()
		print("Your balance is now $" + str(self.player._money) +".\n")
		time.sleep(1)
		self.bot_turns(action)

	def bot_turns(self, action):
		round_id, round = self.round
		board_rank = self.poker.board_rank(self.board, round_id-1)
		predicted_hand = self.player.classifier.predict(action, round_id, board_rank)
		for bot in self.players:
			rank = self.poker.hole_rank(bot._cards)
			bluff = random.randint(1, 10)
			play_safe = random.randint(1, 10)
			if (bot == self.player):
				pass
			else:
				if (rank < predicted_hand or bluff > bot.bluff_factor):
					self.minimumbet, self.pot = bot.raised(self.minimumbet, self.pot)
				elif (rank == predicted_hand or play_safe > bot.passive_factor):
					self.minimumbet, self.pot = bot.call(self.minimumbet, self.pot)
				else:
					self.minimumbet, self.pot = bot.fold(self.minimumbet, self.pot)

	def __init__(self):
		self.setup()


	def rotate_blinds(self):
		if (self.big_blind == self.numplayers-1):
			self.big_blind = 0
		else: 
			self.big_blind += 1
		if (self.small_blind == self.numplayers-1):
			self.small_blind = 0
		else: 
			self.small_blind += 1
		if(self.go_first == self.numplayers-1):
			self.go_first = 0
		else:
			self.go_first += 1
		return 	big_blind, small_blind

game = Pokergame()