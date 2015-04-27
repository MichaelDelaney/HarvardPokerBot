import sqlite3

class Player:

	db = sqlite3.connect('pokerbot.db')
	cur = db.cursor()

	def __init__(self, name):
		self.name = name

	def get_id(self):
		self.cur.execute('SELECT id FROM players WHERE name = ?', (name,))
		return self.cur.fetchone()

	def get_trained_data(self, round, board_rank=8):
		self.cur.execute('SELECT action, hand_rank, probability, board_rank FROM probabilities LEFT JOIN players ON probabilities.player = players.id WHERE name = ? AND round = ? AND board_rank = ?', (self.name, round, board_rank))
		actions = []
		columns = tuple( [d[0] for d in self.cur.description] )
		for row in self.cur:
		  actions.append(dict(zip(columns, row)))
		return actions

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

	# get the number of times this player has been trained for a given action
	def times_trained (self, action, round, board_rank=8):
		actions = self.get_trained_data(round, board_rank)
		total = 0
		for row in actions:
			if (row['action'] == action):
				total += row['probability']
		return total

	# get the probability of a rank given the action
	def get_probability(self, action, rank, round, board_rank=8):
		actions = self.get_trained_data(round, board_rank)
		prob = 0
		for row in actions:
			if (row['action'] == action):
				if (row['hand_rank'] == rank):
					return row['probability'] / self.times_trained(action, round, board_rank)
