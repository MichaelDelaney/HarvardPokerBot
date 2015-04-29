import sqlite3
import random
from models import *

class GamePlayer(object):
	def __init__(self):
		self._name = " "
		self._cards = []
		self._money = 500000
		self._move = " "
		self.bluff_factor = random.randint(1, 4)
		self.passive_factor = random.randint(1, 4)

class Player (GamePlayer):

	def __init__(self, name):
		try:
			Players.create(name = name)
		except:
			pass
		self.name = name
		player = Players.select().where(Players.name == self.name).get()
		self.id = player.id
