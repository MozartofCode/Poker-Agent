# @Author: Bertan Berker
# @Filename: deck.py
# @Language: Python
# This file contains the Deck and Card classes.
# The Deck class is used to create a deck of cards and shuffle them. 
# The Card class is used to create a card object with a suit and value.

import random

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
