import sqlite3
import random
import time
from models import *
from poker import Poker
from classifier import Classifier

class GamePlayer(object):

	_name = " "
	_cards = []
	_money = 300
	_move = "checked"
	_bet = 0
	poker = Poker()

	def get_action(self):
		return (1 if self._move == "raised" else
		2 if self._move == "folded" else
		3 if self._move == "called" else
		4 if self._move == "bet" else
		5)
	
class Player (GamePlayer):

	def __init__(self, name):
		try:
			Players.create(name = name)
		except:
			pass
		self.name = name
		player = Players.select().where(Players.name == self.name).get()
		self.id = player.id
		self.classifier = Classifier(self)
		self.index = 0

	def checked(self, round, minbet, pot):
		"""check"""
		action = 5
		rank = self.poker.hole_rank(self._cards)
		self.classifier.train(action, rank, round)
		self._move = "checked"
		return (action, minbet, pot, False)

	def called(self, round, minbet, pot):
		"""call""" 
		action = 3
		rank = self.poker.hole_rank(self._cards)
		self.classifier.train(action, rank, round)
		round_bet = minbet
		if round_bet > self._money:
			print("You don't have that much, you are all in at {}".format(self._money))
			round_bet == self._money
		else:
			self._bet += round_bet
		if round_bet == 0:
			return (minbet, pot, True)
		self._money -= minbet
		pot += minbet
		self._move = "called"
		return (action, minbet, pot, False)

	def bet(self, round, minbet, pot):
		"""bet"""
		action = 4
		round_bet = int(input("\nHow much would you like to bet?\n").strip())
		if round_bet > self._money:
			print("You don't have that much, you are all in at {}".format(self._money))
			round_bet = self._money
			self._money = 0
		else:
			self._bet += (round_bet + minbet)
			self._money -= (minbet + round_bet)
		if round_bet == 0:
			return (action, minbet, pot, True)
		minbet += round_bet
		rank = self.poker.hole_rank(self._cards)
		self.classifier.train(action, rank, round)
		pot += (minbet + round_bet)
		self._move = "bet"
		return (action, minbet, pot, False)

	def raised(self, round, minbet, pot):
		"""raise"""
		action = 1
		round_bet = int(input("\nHow much would you like to bet?\n").strip())
		if round_bet > self._money:
			print("You don't have that much, you are all in at {}".format(self._money))
			round_bet = self._money
			self._money = 0
		else:
			self._bet += (round_bet + minbet)
			self._money -= (minbet + round_bet)
		if round_bet == 0:
			return (action, minbet, pot, True)
		minbet += round_bet
		rank = self.poker.hole_rank(self._cards)
		self.classifier.train(action, rank, round)
		pot += (minbet + round_bet)
		self._move = "raised"
		return (action, minbet, pot, False)

	def folded(self, round, minbet, pot):
		"""fold"""
		action = 2
		self._cards = []
		self._bet = minbet
		rank = self.poker.hole_rank(self._cards)
		self.classifier.train(action, rank, round)
		self._move = "folded"
		return (action, minbet, pot, False)


class Bot(GamePlayer):

	def __init__(self, i):
		self.bluff_factor = random.randint(6, 10)
		self.passive_factor = random.randint(6, 10)
		self.index = i

	def call(self, minbet, pot):
		round_bet = minbet
		if round_bet > self._money:
			round_bet == self._money
		else:
			self._bet += round_bet
		if round_bet == 0:
			print ("\nPlayer {} is out")
			return (minbet, pot, True)
		self._money -= minbet
		pot += minbet
		self._move = "called"
		time.sleep(2)
		print('\nPlayer {} called'.format(self.index))
		print('The minimum bet is now {}'.format(minbet))
		return (minbet, pot, False)

	def raised(self, minbet, pot):
		round_bet = random.randint(1, 20)
		if round_bet >= self._money:
			round_bet = self._money
		else:
			self._bet += round_bet
		if round_bet == 0:
			print ("\nPlayer {} is out")
			return (minbet, pot, True)
		self._money -= (minbet + round_bet)
		minbet += round_bet
		pot += (minbet + round_bet)
		self._move = "raised"
		time.sleep(2)
		print('\nPlayer {} raised {}'.format(self.index, round_bet))
		print('The minimum bet is now {}'.format(minbet))
		return (minbet, pot, False)

	def fold(self, minbet, pot):
		self._cards = []
		#game.hands[i] = []
		self._move = "folded"
		self._bet = minbet
		time.sleep(2)
		print('Player {} folded'.format(self.index))
		return (minbet, pot, False)
