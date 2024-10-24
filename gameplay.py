# @Author: Bertan Berker
# @Language: Python
# 
#


import random
from monte_carlo_bot import Monte_Carlo_Bot
from RL_bot import RL_Bot
import gym
from gym import spaces
import numpy as np

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
        self.monte_carlo_bot = Monte_Carlo_Bot(1000)
        self.rl_bot = RL_Bot(1000)
        self.reset()
        # Setup the environment for the RL bot (actions, states, rewards etc...)
        
        self.action_space = spaces.Discrete(3)  # 0: Fold, 1: Call, 2: Raise
        self.observation_space = spaces.Box(low=2, high=14, shape=(7,), dtype=np.int)  

    
    def reset(self):

        self.deck = Deck()
        self.community_cards = []
        self.monte_carlo_bot_hand = []
        self.rl_bot_hand = []

        for i in range(4):
            self.rl_bot_hand.append(self.deck.draw_card())
            self.monte_carlo_bot_hand.append(self.deck.draw_card())
        
        self.done = False

        # Initial observation
        return self.get_observation()
    

    def get_observation(self):
        
        # Convert the bot's hand to numerical values
        bot_values = [self.card_value(card) for card in self.rl_bot_hand]
        
        # Add zeros for the community cards if fewer than 5
        community_values = [self.card_value(card) for card in self.community_cards] + [0] * (5 - len(self.community_cards))
        
        observation = bot_values + community_values
        
        return np.array(observation)


    def step(self, action):
        
        reward = 0

        # If the action is fold
        if action == 0:
            self.done = True
            reward -=1 

        # If the action is call
        elif action == 1:
            reward = 0 
        
        # If the action is raise
        elif action == 2:
            reward = 0

        observation = self.get_observation()

        if self.done:
            if self.agent_wins():
                reward += 1
            else:
                reward -= 1

        return observation, reward, self.done, {}
        

    def deal_flop(self):        
        self.deck.draw_card()  # Burn one card
        for _ in range(3):
            self.community_cards.append(self.deck.draw_card())

    def deal_turn(self):
        self.deck.draw_card()  # Burn one card
        self.community_cards.append(self.deck.draw_card())

    def deal_river(self):
        self.deck.draw_card()  # Burn one card
        self.community_cards.append(self.deck.draw_card())

    def play_round(self):
        return
    