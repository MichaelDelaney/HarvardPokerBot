import sqlite3
import random
from models import *

class GamePlayer(object):
	_name = " "
	_cards = []
	_money = 500000
	_move = " "
	bluff_factor = random.randint(1, 4)
	passive_factor = random.randint(1, 4)

class Player (GamePlayer):

	def __init__(self, name):
		try:
			Players.create(name = name)
		except:
			pass
		self.name = name
		player = Players.select().where(Players.name == self.name).get()
		self.id = player.id
