import sqlite3
import functools
import math
from player import Player

# when instantiating pass in the player object to be classified
class Classifier:

	def __init__(self, player):
		self.player = player

	db = sqlite3.connect('pokerbot.db')
	cursor = db.cursor()

	def prior_probability_rank(self, rank):
		if (rank == 1):
			return 0.0211
		elif (rank == 2):
			return 0.02263
		elif (rank == 3): 
			return 0.02565
		elif (rank == 4):
			return 0.03772
		elif (rank == 5):
			return 0.07093
		elif (rank == 6):
			return 0.05129
		elif (rank == 7):
			return 0.07695
		elif (rank == 8):
			return 0.09957
		else:
			return 0.59416

	def probabilities_dict (self, action, round, board_rank = 7):
		ratios = []
		probabilities={}
		for rank in range(1, 9):
			prior_probability = self.prior_probability_rank(rank)
			if (round == "pre_flop"):
				prob = self.player.get_probability(action, rank, round)
			elif (round == "flop"):
				prob = self.player.flop_actions[action][flop_rank][rank]
			elif (round == "turn"):
				prob = self.player.flop_actions[action][flop_rank][rank]
			else:
				prob = self.player.flop_actions[action][flop_rank][rank]
			prob_ratio = prior_probability*prob
			ratios.append(prob_ratio)
		normalizer = functools.reduce(lambda x, y: x + y, ratios)
		rank = 1
		for ratio in ratios:
			posterior_probability = ratio/normalizer
			probabilities.update({rank: posterior_probability})
			rank += 1
		return probabilities

	def predict (self, action):
		probabilities = self.probabilities_dict(action)
		max_prob = 0
		max_rank = ""
		for rank, value in probabilities.items():
			if (value > max_prob):
				max_prob = value
				max_rank = rank
			else:
				continue
		if (max_rank == 0):
			return 8
		else:
			return max_rank

	# give the action and the rank the player had train the probabilities
	# and return the new probability of that rank given that action
	def train (self, action, rank, round, board_rank = 7):
		params = (self.player.name, action, rank, 1)
		if (round == "pre_flop"):
			self.cursor.execute('SELECT probability FROM probabilities LEFT JOIN players ON probabilities.player = players.id WHERE players.name = ? AND action = ? AND hand_rank = ? AND round = ?', params)
			data = self.cursor.fetchall()
			if len(data)==0:
				cols = (self.player.get_id()[0], action, round, board_rank, rank)
				self.db.execute('INSERT INTO probabilities (player, action, round, board_rank, hand_rank, probability) VALUES (?, ?, ?, ?, ?, 1)', cols)
			else:
				self.db.execute('UPDATE probabilities SET probability = probability + 1 LEFT JOIN players ON probabilities.player = players.id  WHERE players.name = ? AND action = ? AND hand_rank = ? AND round = ?', params)
		elif (round == "flop"):
			self.player.flop_actions[action][board_rank][rank] += 1
		elif (round == "turn"):
			self.player.flop_actions[action][flop_rank][rank] += 1
		else:
			self.player.flop_actions[action][flop_rank][rank] += 1
		return self.player.get_probability(action, rank, round, board_rank)


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
