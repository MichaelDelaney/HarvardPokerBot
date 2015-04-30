import sqlite3
import functools
import math
from decimal import *
from models import *

# when instantiating pass in the player object to be classified
class Classifier:

	def __init__(self, player):
		self.player = player

	database.connect()

	def prior_probability_rank(self, rank):
		if (rank == 1):
			return Decimal(0.0211)
		elif (rank == 2):
			return Decimal(0.02263)
		elif (rank == 3): 
			return Decimal(0.02565)
		elif (rank == 4):
			return Decimal(0.03772)
		elif (rank == 5):
			return Decimal(0.07093)
		elif (rank == 6):
			return Decimal(0.05129)
		elif (rank == 7):
			return Decimal(0.07695)
		elif (rank == 8):
			return Decimal(0.09957)
		else:
			return Decimal(0.59416)

	def get_trained_data(self, round, board_rank=8):
		actions = []
		query = (Probabilities.select(Probabilities.action, Probabilities.hand_rank, Probabilities.probability, Probabilities.board_rank)
				.join(Players)
				.where(Players.name == self.player.name)
				.where(Probabilities.round == round)
				.where(Probabilities.board_rank == board_rank))
		d = query.execute()
		for row in d:
			actions.append(row.__dict__)
		return actions

	# get the number of times this player has been trained for a given action
	def times_trained (self, action, round, board_rank=8):
		actions = self.get_trained_data(round, board_rank)
		total = 0
		for row in actions:
			if (row['_data']['action'] == action):
				total += row['_data']['probability']
		return total

	def get_probability(self, action, rank, round, board_rank=8):
		actions = self.get_trained_data(round, board_rank)
		prob = 0
		for row in actions:
			if row['_data']['action'] == action and row['_data']['hand_rank'] == rank:
				prob = row['_data']['probability'] / self.times_trained(action, round, board_rank)
		return prob

	def _probabilities_dict (self, action, round, board_rank=8):
		ratios = []
		probabilities={}
		for rank in range(1, 9):
			prior_probability = self.prior_probability_rank(rank)
			prob = self.get_probability(action, rank, round, board_rank)
			prob_ratio = prior_probability * prob
			ratios.append(prob_ratio)
		normalizer = functools.reduce(lambda x, y: x + y, ratios)
		rank = 1
		for ratio in ratios:
			if (normalizer != 0):
				posterior_probability = ratio/normalizer
			else:
				posterior_probability = 0
			probabilities.update({rank: posterior_probability})
			rank += 1
		return probabilities

	
	def _row_exists(self, action, rank, round, board_rank = 8):
		rows = []
		query = (Probabilities.select()
				.where(Probabilities.action == action)
				.where(Probabilities.hand_rank ==  rank)
				.where(Probabilities.round == round)
				.where(Probabilities.board_rank == board_rank))
		d = query.execute()
		for row in d:
			rows.append(row.__dict__)
		if (rows == []):
			False
		else:
			True

	# give the action and the rank the player had train the probabilities
	# and return the new probability of that rank given that action
	def train (self, action, rank, round, board_rank = 8):
		try:
			row = (Probabilities.select()
					.where(Probabilities.action == action)
					.where(Probabilities.hand_rank ==  rank)
					.where(Probabilities.round == round)
					.where(Probabilities.board_rank == board_rank).get())
			row.probability += 1
			row.save()
		except:
			(Probabilities.create(
				player = self.player.id, 
				action = action, 
				hand_rank = rank, 
				round = round, 
				board_rank = board_rank, 
				probability = 1))
		return self.get_probability(action, rank, round, board_rank)

	def predict (self, action, round, board_rank=8):
		probabilities = self._probabilities_dict(action, round, board_rank)
		max_prob = 0
		max_rank = ""
		for rank, value in probabilities.items():
			if (value > max_prob):
				max_prob = value
				max_rank = rank
			else:
				pass
		if (max_rank == 0 or not max_rank):
			return 9
		else:
			return max_rank


    # predicting the test set
	def predict_probability(self, test):
		probabilities = []
		for i in range(len(test)):
			result = predict(self, test[i])
			probabilities.append(result)
		return probabilities


    # def mean(action):
    #      return sum(action)/float(len(action))

    #    def stdev(action):
    #       avg = mean(action)
    #      variance = sum([pow(x-avg,2) for x in action])/float(len(action)-1)
    #    return math.sqrt(variance)


	def accuracy(test, probabilities):
		exponent = math.exp(-(math.pow(x - mean, 2) / (2 * math.pow(stdev, 2))))
		return (1 / (math.sqrt(2 * math.pi) * stdev)) * exponent

#   def normalize(possibilities):
#        possibility_sum = sum(possibilities)
#        for hypothesis in xrange(0,101):
#            possibility = possibilities[hypothesis]
#            possibilities[hypothesis] = possibility/possibility_sum
