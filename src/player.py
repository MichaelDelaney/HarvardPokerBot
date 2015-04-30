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
	_move = " "
	_bet = 0
	poker = Poker()
	

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

	def checked(self, round, minbet, pot):
		"""check"""
		action = 5
		rank = self.poker.hole_rank(self._cards)
		self.classifier.train(action, rank, round)
		self._move = "checked"
		return (action, minbet, pot)

	def called(self, round, minbet, pot):
		"""call""" 
		action = 3
		rank = self.poker.hole_rank(self._cards)
		self.classifier.train(action, rank, round)
		round_bet = minbet
		self._money -= minbet
		pot += minbet
		self._move = "called"
		return (action, minbet, pot)

	def bet(self, round, minbet, pot):
		"""bet"""
		action = 4
		round_bet = int(input("\nHow much would you like to bet?\n").strip())
		self._bet += round_bet
		self._money -= (minbet + round_bet)
		minbet += round_bet
		rank = self.poker.hole_rank(self._cards)
		self.classifier.train(action, rank, round)
		pot += (minbet + round_bet)
		self._move = "bet"
		return (action, minbet, pot)

	def raised(self, round, minbet, pot):
		"""raise"""
		action = 1
		round_bet = int(input("\nHow much would you like to bet?\n").strip())
		self._bet += round_bet
		self._money -= (minbet + round_bet)
		minbet += round_bet
		rank = self.poker.hole_rank(self._cards)
		self.classifier.train(action, rank, round)
		pot += (minbet + round_bet)
		self._move = "raised"
		return (action, minbet, pot)

	def folded(self, round, minbet, pot):
		"""fold"""
		action = 2
		self._cards = []
		#game.hands[i] = []
		rank = self.poker.hole_rank(self._cards)
		self.classifier.train(action, rank, round)
		self._move = "folded"
		return (action, minbet, pot)


class Bot(GamePlayer):

	def __init__(self, i):
		self.bluff_factor = random.randint(6, 10)
		self.passive_factor = random.randint(6, 10)
		self.index = i

	def call(self, minbet, pot):
		round_bet = minbet
		self._money -= minbet
		pot += minbet
		self._move = "called"
		time.sleep(2)
		print('\nPlayer {} called'.format(self.index + 1))
		print('The minimum bet is now {}'.format(minbet))
		return (minbet, pot)

	def raised(self, minbet, pot):
		round_bet = random.randint(1, 50)
		self._bet += round_bet
		self._money -= (minbet + round_bet)
		minbet += round_bet
		pot += (minbet + round_bet)
		self._move = "raised"
		time.sleep(2)
		print('\nPlayer {} raised {}'.format(self.index + 1, round_bet))
		print('The minimum bet is now {}'.format(minbet))
		return (minbet, pot)

	def fold(self, minbet, pot):
		self._cards = []
		#game.hands[i] = []
		self._move = "folded"
		time.sleep(2)
		print('Player {} folded'.format(self.index + 1))
		return (minbet, pot)
