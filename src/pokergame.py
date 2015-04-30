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
		self.minimumbet = 0
		self.pot = 0
		self.board_rank = 8
		self.communityCards = 3
		self.rounds = [(1, "Pre-flop"), (2, "Flop"), (3, "Turn"), (4, "The river")]
		self.deal_cards()
		self.round = self.get_next_round()

	def setup_starting_hand(self):
		# Game Title and Welcome
		print("\n *** Harvard Hold'em Poker Bot *** \n")
		print("Welcome. Let's get the game started...")
		self.numplayers = 5
		self.player = Player(input("Enter your name: \n"))
		self.players = [Bot(i) for i in range(0, self.numplayers-1)]
		self.players.insert(0, self.player)
		self.poker = Poker()
		self.small_blind = 2
		self.big_blind = 1
		self.go_first = 0
		self.setup()

	def setup_next_hand (self, players_still_in):
		print("\n\nYou're still in! You now have ${}".format(str(self.player._money)))
		print("Let's get the next hand started...")
		self.numplayers = len(players_still_in)
		self.players = players_still_in
		self.player._move = ""
		self.setup()

	def get_next_round(self):
		try:
			self.round = self.rounds.pop(0)
		except IndexError:
			self.round = (0, "end of round")
		self.start_round()

	def deal_cards(self):
		self.hands = self.poker.deal(self.numplayers + 1 + self.communityCards) #Added 1 for dealer's hand, he will be hands[5]
		for i in range(0, self.numplayers):
			self.players[i]._cards = self.hands[i]

		self.flopCards = [self.hands[7][0]] + self.hands[6]
		self.turnCards = [self.hands[7][1]]
		self.riverCards = [self.hands[8][0]]
		self.board = self.flopCards

	def announce_round(self):
		round_id, round = self.round
		print("\nthe min bet is {}\n".format(self.minimumbet))
		if (self.small_blind == 0):
			self.player._money -= 1 
			self.minimumbet = 1
			print("\n{}!\nYou are the small blind. Your balance is now {}\n".format(round, str(self.players[0]._money)))
		elif (self.big_blind == 0):
			self.player._money -= 2
			print("\n{}!\nYou are the big blind. Your balance is now {}\n".format(round, str(self.players[0]._money)))
		else:
			self.minimumbet = 2
			print("\n{}!\n".format(round))
		if(self.player._move == "folded"):
			self.bot_turns(2)
		else:
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
		self.rotate_blinds()

	def update_hands(self, cards):
		for i in range(0, self.numplayers):
			if (self.players[i]._move != "folded"):
			    self.players[i]._cards += cards
			    self.hands[i] = self.players[i]._cards
	
	def find_best_hands(self):
		for i in range(0, self.numplayers):
		    if self.players[i]._move != "folded":
		        self.hands[i] = list(self.poker.best_hand(self.hands[i]))

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
		self.round = self.get_next_round()

	def start_round(self):
		round_id, round = self.round
		if (round_id == 1):
			
			# Places 2 Cards in Each Player's Hand
			for i in range(0, 3):
				sys.stdout.flush()
				time.sleep(.3)
				sys.stdout.write("\rDealing hole cards..")
				time.sleep(.3)
				sys.stdout.write("\rDealing hole cards....")
				time.sleep(.3)
				sys.stdout.write("\rDealing hole cards.....")

			# Displays User's Balance and Hand
			print("\n\nYour balance: ")
			print("$" + str(self.player._money))
			print("Your hand:")
			print(self.player._cards)
			self.announce_round()
		elif(round_id == 2):
			# Reveal Flop Cards
			# Flop - Dealer shows 3 Community Cards
			print("The flops cards are...")
			print(self.flopCards)
			time.sleep(2)
			# Update the hands of the players with the flop cards
			self.update_hands(self.flopCards)
			self.announce_round()
		elif(round_id == 3):
			# Reveal Turn Card
			# Turn - Dealer shows 1 More Community Card
			print("\nThe turn card is...")
			print(self.turnCards)
			time.sleep(2)
			# Show all community cards
			print("The 4 community cards so far are...")
			print(self.turnCards + self.flopCards)
			time.sleep(1)
			# Update the hands of the players with the turn cards
			self.update_hands(self.turnCards)
			self.announce_round()
		elif(round_id == 4):
			# Reveal River Card
			# Turn - Dealer shows 1 More Community Card
			print("\nThe river card is...")
			print(self.riverCards)
			time.sleep(2)
			# Show all community cards
			print("The 5 community cards so far are...")
			print(self.riverCards + self.turnCards + self.flopCards)
			time.sleep(1)
			# Update the hands of the players with the turn cards
			self.update_hands(self.riverCards)
			# Show new hand including flop and turn cards
			if self.players[0]._move != "folded":
				print("\nWith the flop, turn, and river cards, your new 7 card hand is now...")
				print(self.hands[0])
				time.sleep(1)
				# Update all then hands with the best combo of 5 cards
			self.find_best_hands()
			self.announce_round()
		else:
		# Reveal The Winner
			print("\nHere comes the reveal of every player's best ranked hand!")
			dealercards = self.hands[5]
			print("\nThese are the dealers cards:" + str(dealercards) + "\n")
			# Call community cards to dealer's hand
			dealercards = dealercards + self.flopCards + self.turnCards + self.riverCards
			self.hands[5] = list(self.poker.best_hand(dealercards))
			time.sleep(1)
			print("The Dealer's best ranked hand is: " + str(self.hands[5]))

			if self.player._move != "folded":
				print("Your hand: " + str(self.hands[0]))
				time.sleep(1)

			for i in range(1, self.numplayers):
				if self.players[i]._move == "folded":
					# If a player folded update their cards in hands[i]
					self.hands[i] = []
				else:
					print("Player " + str(i+1) + ": " + str(self.hands[i]))
			# Before determining winner, make sure there are no null hands going
			# going in as input in poker() func
			winningHands = []
			for i in range(0, self.numplayers + 1): #Plys 1 for the dealers hand
				if self.hands[i] != []:
					winningHands += [self.hands[i]]

			# Need more than 1 value to unpack winner
			count2 = 0
			for i in range(0, self.numplayers):
				if self.players[i]._move == "folded":
					count2 += 1

			# Determine the winner of round
			print("\nThe winning hand is...")
			if count2 == 5:
				print("The dealer has won!")
				print(str(self.hands[5]))
			else:
				winningPlayer = self.poker.poker(winningHands)
				winner = winningPlayer[0]
				print(str(winner))
				if self.hands[0] == winner:
					print("You have won the round...Congratulations! ")
					self.player._money += self.pot
					print("$" + str(self.pot)+" has been added to your balance!")
				elif self.hands[5] == winner:
					print("Sorry, the dealer has won!")
				else:
					for i in range(1, self.numplayers):
						if self.hands[i] == winner:
							print("Player " + str(i+1) + " has won.")
							self.players[i]._money += self.pot
							print("$" + str(self.pot) + " has been added to Player " + str(i+1) + "'s balance.")
			players_still_in = []
			for player in self.players:
				if player._money > 0:
					players_still_in.append(self.player)
				else:
					pass
			if(self.player._money <= 0):
				print("You are out. You lost all of your money. Game over.")
			elif (len(players_still_in) == 1):
				print("You won the Game. You won{}".format(str(self.player._money)))
			else:
				self.setup_next_hand(players_still_in)

	def __init__(self):
		self.setup_starting_hand()


game = Pokergame()