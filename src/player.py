import sqlite3
from models import *

class GamePlayer(object):
    def __init__( self ):
        self._name = ""
        self._cards = []
        self._money = 500000
        self._move = " "

class Player (GamePlayer):

	def __init__(self, name):
		try:
			Players.create(name = name)
		except:
			pass
		self.name = name
		player = Players.select().where(Players.name == self.name).get()
		self.id = player.id
