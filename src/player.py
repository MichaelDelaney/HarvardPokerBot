import sqlite3
import random
from models import *

class GamePlayer(object):

	_name = " "
	_cards = []
	_money = 500000
	_move = " "
	bet = 0
	

class Player (GamePlayer):

	def __init__(self, name):
		try:
			Players.create(name = name)
		except:
			pass
		self.name = name
		player = Players.select().where(Players.name == self.name).get()
		self.id = player.id

	def checked(self, round, poker, game):
		"""check"""
		action = 5
		rank = poker.hole_rank(self._cards)
		classifier.train(action, rank, round)
		self._move = "checked"

	def called(self, round, poker, game):
		"""call""" 
		action = 3
		rank = pokerbot.hole_rank(self._cards)
		classifier.train(action, rank, round)
		round_bet = minimumbet
		self._money -= game.minimumbet
		game.pot += minbet
		self._move = "called"

	def bet(self, round, poker, game):
		"""bet"""
		action = 4
		round_bet = int(input("\nHow much would you like to bet?\n").strip())
		self.bet += round_bet
		self._money -= (game.minimumbet + round_bet)
		rank = pokerbot.hole_rank(self._cards)
		classifier.train(action, rank, round)
		game.pot += (game.minimumbet + round_bet)
		self._move = "bet"

	def raised(self, round, poker, game):
		"""raise"""
		action = 4
		round_bet = int(input("\nHow much would you like to bet?\n").strip())
		self.bet += round_bet
		self._money -= (game.minimumbet + round_bet)
		rank = pokerbot.hole_rank(self._cards)
		classifier.train(action, rank, round)
		game.pot += (game.minimumbet + round_bet)
		self._move = "raised"

	def folded(self, round, poker, game):
		"""fold"""
		action = 2
		self._cards = []
		#game.hands[i] = []
		rank = pokerbot.hole_rank(self._cards)
		classifier.train(action, rank, round)
		self._move = "folded"


class Bot(GamePlayer):

	def __init__(self):
		bluff_factor = random.randint(1, 4)
		passive_factor = random.randint(1, 4)

	def call(self, i):
		global minimumbet
		players[i]._money -= minimumbet
		global pot
		pot += minimumbet
		time.sleep(1)
		print('Player {} called'.format(i + 1))
		print('The minimum bet is now {}'.format(minimumbet))

	def raised(self, i):
		bet = random.randint(1, 50)
		global minimumbet
		players[i]._money -= (minimumbet + bet)
		global pot
		pot += (minimumbet + bet)
		minimumbet += bet
		time.sleep(1)
		print('Player {} raised {}'.format(i + 1, bet))
		print('The minimum bet is now {}'.format(minimumbet))

	def fold(self, i):
		players[i]._cards = []
		hands[i] = []
		players[i]._move = "folded"
		time.sleep(1)
		print('Player {} folded'.format(i + 1))

	def move(action, round, board_rank=8):
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
