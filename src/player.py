import sqlite3

class Player:

	db = sqlite3.connect('pokerbot.db')
	cur = db.cursor()

	def __init__(self, name):
		self.name = name
		db = sqlite3.connect('pokerbot.db')
		cur = db.cursor()
		id = db.execute('SELECT id FROM players WHERE name = ?', (name,))
		cur.execute('SELECT action, hand_rank, probability FROM probabilities LEFT JOIN players ON probabilities.player = players.id WHERE name = ? AND round = ?', (name, 1))
		pre_flop_actions = []
		columns = tuple( [d[0] for d in cur.description] )
		for row in cur:
		  pre_flop_actions.append(dict(zip(columns, row)))
		cur.close()
		db.close()

	def get_id(self):
		self.cur.execute('SELECT id FROM players WHERE name = ?', (self.name,))
		return self.cur.fetchone()

	def get_pre_flop(self):
		cur.execute('SELECT action, hand_rank, probability FROM probabilities LEFT JOIN players ON probabilities.player = players.id WHERE name = ? AND round = ?', (name, 1))
		pre_flop_actions = []
		columns = tuple( [d[0] for d in cur.description] )
		for row in cur:
		  pre_flop_actions.append(dict(zip(columns, row)))
		return pre_flop_actions

	# get the number of times this player has been trained for a given action
	def times_trained (self, action, round, flop_rank = 7):
		if (round == "pre_flop"):
			pre_flop_actions = self.get_pre_flop()
			total = 0
			for row in pre_flop_actions:
				if (row['action'] == action):
					total += row['probability']
			return total
		elif (round == "flop"):
			total = 0
			for row in self.pre_flop_actions:
				if (row['action'] == action):
					total += row['probability']
			return total
		elif (round == "turn"):
			total = 0
			for row in self.pre_flop_actions:
				if (row['action'] == action):
					total += row['probability']
			return total
		else:
			total = 0
			for row in self.pre_flop_actions:
				if (row['action'] == action):
					total += row['probability']
			return total
	# get the probability of a rank given the action
	def get_probability(self, action, rank, round, board_rank=7):
		if (round == "pre_flop"):
			prob = 0
			for row in self.pre_flop_actions:
				if (row['action'] == action):
					if (row['hand_rank'] == rank):
						return row['probability'] / self.times_trained(action, round)
		elif (round == "flop"):
			return self.actions[action].get(rank) / self.times_trained(action, round, board_rank)
		elif (round == "turn"):
			return self.actions[action].get(rank) / self.times_trained(action, round, board_rank)
		else:
			return self.actions[action].get(rank) / self.times_trained(action, round, board_rank)
