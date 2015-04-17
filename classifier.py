import functools

class Classifier:

	def prior_probability_rank(self,rank):
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

	def prior_probability_hand(self, card1, card2, suitedness = False):
		if (card1 == card2):
			return 0.00452
		elif (suitedness == True):
			return 0.00302
		else:
			return 0.00905

	def probability(self, trained_probs_by_rank, action):
		ratios = []
		probabilities={}
		for rank in trained_probs_by_rank:
			prior_probability = self.prior_probability_rank(rank)
			prob = trained_probs_by_rank[rank].get(action)
			prob_ratio = prior_probability*prob
			ratios.append(prob_ratio)
		normalizer = functools.reduce(lambda x, y: x + y, ratios)
		rank = 1
		for ratio in ratios:
			posterior_probability = ratio/normalizer
			probabilities.update({rank:posterior_probability})
			rank += 1
		return probabilities
