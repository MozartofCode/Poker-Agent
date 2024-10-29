# @Author: Bertan Berker
# @Language: Python
# This is a simple bot that plays poker and makes decision based on the Monte Carlo simulation
# A simple bluffing and betting logic is implemented where positional play could be implemented later on

import random
from hand_evaluation import choose_winner
from gameplay import Deck


# This is the Monte Carlo Bot class
class MonteCarloBot:
    
    def __init__(self, money, risk_factor=1.0):
        self.risk_factor = risk_factor
        self.money = money

    def make_decision(self, my_hand, opponent_hand, community_cards, pot_size):
        return make_decision(my_hand, opponent_hand, community_cards, pot_size, self.risk_factor)


# This is the implementation of the Monte Carlo Simulation on Texas Hold'em
# :my_hand: The hand of the bot
# :opponent_hand: The hand of the opponent
# :community_cards: The cards on the table
# :num_simulations: The number of simulations to run
# :return: The percentage of the time the bot wins over 1000 simulations
def monte_carlo_simulation(my_hand, opponent_hand, community_cards, num_simulations=1000):

    wins = 0

    for _ in range(num_simulations):
        
        current_deck = Deck()
        current_community_cards = community_cards.copy()
        current_my_hand = my_hand.copy()
        current_opponent_hand = opponent_hand.copy()

        # Removing the existing cards from the deck to make sure it represents the current deck
        for card in (my_hand + opponent_hand + community_cards):
            current_deck.cards.remove(card)

        # Giving cards to each side until both have 7 cards = 5 community cards + 2 hand cards
        while len(current_community_cards) < 5:
            current_community_cards.append(current_deck.cards.pop())

        current_my_hand.append(current_community_cards)
        current_opponent_hand.append(current_community_cards)

        # Choose the best hand
        if choose_winner(current_my_hand, current_opponent_hand):
            wins += 1
        
    return 100 * (wins / num_simulations)


# This is the implementation of the bot's decision making process
# :my_hand: The hand of the bot
# :opponent_hand: The hand of the opponent
# :community_cards: The cards on the table
# :pot_size: The size of the pot on the table
# :risk_factor: The risk factor of the bot (Depends on the bot's risk tolerance)
# :return: The decision of the bot
def make_decision(my_hand, opponent_hand, community_cards, pot_size, risk_factor = 1.0):

    possibility = monte_carlo_simulation(my_hand, opponent_hand, community_cards)
    
    # Action Threshold
    # <=30% - Fold
    # 30% - <=60% - Call/Check
    # 60% - <=90% - Raise
    # >90% - All in
    fold_threshold = 0.3 * risk_factor
    call_threshold = 0.6 * risk_factor
    raise_threshold = 0.9 * risk_factor

    if possibility <= fold_threshold:
        if should_bluff():
            return 'Raise' + str(int(pot_size * random.randint(5, 10)))

        return 'Fold'
    
    elif possibility > fold_threshold and possibility <= call_threshold:
        return 'Call/Check'
    
    elif possibility > call_threshold and possibility <= raise_threshold:
        # Always raises %20 of the pot size    
        return 'Raise' + str(int(pot_size * 0.2))
    
    elif possibility > raise_threshold:
        return 'All-in'
    
    return 'Fold'


# This is the implementation of the bot's bluffing logic
# :bluff_chance: The chance of the bot to bluff
# :return: True if the bot should bluff, False otherwise
def should_bluff(bluff_chance=8):
    if random.randint(0, 10) <= bluff_chance:
        return True
    return False