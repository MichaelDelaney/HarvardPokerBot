class Player:

	def __init__(self, name="new player"):
		actions = {
					'raised': {1:0,2:0,3:0,4:0,5:0,6:0,7:0,8:0},
					'folded': {1:0,2:0,3:0,4:0,5:0,6:0,7:0,8:0},
					'called': {1:0,2:0,3:0,4:0,5:0,6:0,7:0,8:0},
					'bet': {1:0,2:0,3:0,4:0,5:0,6:0,7:0,8:0},
					'checked': {1:0,2:0,3:0,4:0,5:0,6:0,7:0,8:0}
				  }
		self.actions = actions.copy()
		self.name = name

	# get the number of times this player has been trained for a given action
	def times_trained (self, action):
		return sum(self.actions[action].values())

	# get the probability of a rank given the action
	def get_probability(self, action, rank):
		return self.actions[action].get(rank) / self.times_trained(action)

	def train (self, action, rank):
		self.actions[action][rank] = self.actions[action][rank] + 1
		return self.get_probability(action, rank)
