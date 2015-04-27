import sqlite3
from models import *

class Player:

	
	#db = sqlite3.connect('pokerbot.db')
	#cur = db.cursor()

	def __init__(self, name):
		self.name = name
		player = Players.select().where(Players.name == self.name).get()
		self.id = player.id

	#def get_id(self):
		#self.cur.execute('SELECT id FROM players WHERE name = ?', (self.name,))
		#return self.cur.fetchone()

	

		#self.cur.execute('SELECT action, hand_rank, probability, board_rank FROM probabilities LEFT JOIN players ON probabilities.player = players.id WHERE name = ? AND round = ? AND board_rank = ?', (self.name, round, board_rank))
		#actions = []
		#columns = tuple( [d[0] for d in self.cur.description] )
		#for row in self.cur:
		  #actions.append(dict(zip(columns, row)))
		#return actions

	def get_round_id (round):
		if (round == "pre_flop"):
			return 1
		elif (round == "flop"):
			return 2
		elif (round == "turn"):
			return 3
		elif (round == "river"):
			return 4
		else:
			raise Exception('not a round')

	def get_action_id (action):
		if (action == "raised"):
			return 1
		elif (action == "folded"):
			return 2
		elif (action == "called"):
			return 3
		elif (action == "bet"):
			return 4
		elif (action == "checked"):
			return 5
		else:
			raise Exception('not an action')

	#def board_rank ():

	
	# get the probability of a rank given the action
	