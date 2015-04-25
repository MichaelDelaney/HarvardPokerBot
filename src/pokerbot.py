# Abstraction and Design 
# Final Project: Harvard Hold'em Poker Bot
# Collaborators: Bry Power, Michael Delaney, Esty Cohen
#
# ?? -> problem -> spec -> code
# Understand, Specify, Design
# poker(hands) -> hand
#
# Bry shared an awesome link for a Poker Framework within the package index on python.org
# (https://pypi.python.org/pypi/poker/0.22.1)
# Alternatively, we are use the light framework below that I modelled from the design course on udacity.

import random
import math
import itertools
from collections import defaultdict

# Determines winner of round
def poker(hands):
	"poker([hand, ...]) => hand"
	return allmax(hands, key=hand_rank)

# Capable of handling instance of ties
def allmax(iterable, key=None):
	result, maxval = [], None
	key = key or (lambda x: x)
	for x in iterable:
		xval = key(x)
		if not result or xval > maxval:
			result, maxval = [x], xval
		elif xval == maxval:
			result.append(x)
	return result 

# Determine rank of given hand; strengths are represented by ints
def hand_rank(hand):
	groups = group(['--23456789TJQKA'.index(r) for r,s in hand])
	counts, ranks = unzip(groups)
	if ranks == (14, 5, 4, 3, 2):
		ranks = (5, 4, 3, 2, 1)
	straight = len(ranks) == 5 and max(ranks)-min(ranks) == 4
	flush = len(set([s for r,s in hand])) == 1
	return (9 if (5,) == counts else
		8 if straight and flush else
		7 if (4, 1) == counts else
		6 if (3, 2) == counts else
		5 if flush else
		4 if straight else
		3 if (3, 1, 1) == counts else
		2 if (2, 2, 1) == counts else
		1 if (2, 1, 1, 1) == counts else
		0), ranks

# Hand_rank helper functions
def group(items):
	groups = [(items.count(x), x) for x in set(items)]
	return sorted(groups, reverse=True)
	
def unzip(pairs): return zip(*pairs)

# Each card has a value rank and suit
def card_ranks(cards):
	"Return a list of the ranks, sorted with higher first."
	ranks = ['--23456789TJQKA'.index(r) for r, s in hand] 
	ranks.sort(reverse=True)
	return [5, 4, 3, 2, 1] if (ranks == [14, 5, 4, 3, 2]) else ranks 

# RANKS
# Straight: 5-card straight
# Flush: all cards are the same suit 
# Kind: x of a kind
# Two-pairs: Two ranks are tuple
def straight(ranks):
	return (max(ranks)-min(ranks) == 4) and len(set(ranks)) == 5
	
def flush(hand):
	suits = [s for r, s in hand]
	return len(set(suits)) == 1
	
def kind(n, ranks):
	for r in ranks:
		if ranks.count(r) == n: 
			return r
	return None

def two_pair(ranks):
	pair = kind(2, ranks)
	lowpair = kind(2, list(reversed(ranks)))
	if pair and lowpair != pair:
		return(pair, lowpair)
	else:
		return None

# Deck Setup (is an arg of deal function)
deck = [r+s for r in '23456789TJQKA' for s in 'SHDC']

# Dealing:
# 'numhands' is the amount of players to receive cards
# 'n' is the amount of cards per hand
# Example: deal(2) <-- Will result is 2 hands of 2 cards

def deal(numhands, n=2, deck=[r+s for r in '23456789TJQKA' for s in 'SHDC']):
	random.shuffle(deck) #deck randomizer
	return [deck[n*i:n*(i+1)] for i in range(numhands)]

# Need to add exhaustive testing
# Some example below
def test():
    sf = "6C 7C 8C 9C TC".split() # Straight Flush
    fk = "9D 9H 9S 9C 7D".split() # Four of a Kind
    fh = "TD TC TH 7C 7D".split() # Full House
    s1 = "AS 2S 3S 4S 5C".split() # A-5 straight
    s2 = "2C 3C 4C 5S 6S".split() # 2-6 straight
    s3 = "TC JC QC KS AS".split() # 10-A straight
    tp = "5S 5D 9H 9C 6S".split() # two pair
    ah = "AS 2S 3S 4S 6C".split() # A high
    sh = "2S 3S 4S 6C 7D".split() # 7 high
    assert poker([sf, fk, fh]) == [sf]
    assert card_ranks(sf) == [10, 9, 8, 7, 6]
    assert kind(4, fkranks) == 9
    assert two_pair([10, 10, 5, 5, 2]) == (10, 5)
    assert straight([9, 8, 7, 6, 5]) == True
    assert flush(fk) == False
    return 'tests pass'
