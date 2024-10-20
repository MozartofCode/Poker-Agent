# @Author: Bertan Berker
# @Language: Python
# 
#


import random
from monte_carlo_bot import Monte_Carlo_Bot
from RL_bot import RL_Bot

# value has to be a number assign Ace etc a number as well #TODO
class Card:
    def __init__(self, suit, value):
        self.suit = suit
        self.value = value

    def get_suit(self):
        return self.suit

    def get_value(self):
        return self.value

    def __str__(self):
        return self.value + " of " + self.suit

    def __eq__(self, other):
        return self.suit == other.suit and self.value == other.value
    
    def __hash__(self):
        return hash(self.suit) ^ hash(self.value)


class Deck:
    def __init__(self):
        self.cards = []
        suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
        
        # J -> 11, Q -> 12, K -> 13, A -> 14
        ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14']
        
        for suit in suits:
            for rank in ranks:
                card = Card(suit, int(rank))
                self.cards.append(card)
            
        random.shuffle(self.cards)


    def draw_card(self):
        return self.cards.pop()


class PokerEnv:
    
    def __init__(self):
        
        # Initialize the Deck and the players
        self.deck = Deck()
        self.monte_carlo_bot = Monte_Carlo_Bot(1000)
        self.rl_bot = RL_Bot(1000)

        # Setup the environment for the RL bot (actions, states, rewards etc...)
        
        



        





