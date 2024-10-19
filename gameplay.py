# @Author: Bertan Berker
# @Language: Python
# 
#


import random

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


class Deck:
    def __init__(self):
        self.cards = []
        suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
        ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace']
        
        for suit in suits:
            for rank in ranks:
                card = Card(suit, rank)
                self.cards.append(card)
            
        random.shuffle(self.cards)



class Game:
    def __init__(self):
        # Initilize the deck, RL bot and monte carlo bot
        return

    def play(self):
        return
