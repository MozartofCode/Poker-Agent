# @Author: Bertan Berker
# @Language: Python
# This is a simple bot that plays poker and makes decision based on the Monte Carlo simulation


import random
from hand_evaluation import choose_winner
from gameplay import Deck


# Algorithm run over a 1000 times to simulate the game
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





# Action Threshold
# <=30% - Fold
# 30% - <=60% - Call/Check
# 60% - <=90% - Raise
# >90% - All in
# Occasional bluffing is also implemented
# Risk Factor is about how much the bot is willing to take risks, how agressive it will play

def make_decision(my_hand, opponent_hand, community_cards, pot_size, risk_factor = 1.0):

    possibility = monte_carlo_simulation(my_hand, opponent_hand, community_cards)

    # Tune thresholds based on bot's risk tolerance (default = 1.0)
    fold_threshold = 0.3 * risk_factor
    call_threshold = 0.6 * risk_factor
    raise_threshold = 0.9 * risk_factor

    if possibility <= fold_threshold:

        if should_bluff():
            return 'Raise' + str(int(pot_size * random.randint(5, 10)))

        return 'Fold'
    
    if possibility > fold_threshold and possibility <= call_threshold:
        return 'Call/Check'
    
    if possibility > call_threshold and possibility <= raise_threshold:
        # Always raises %20 of the pot size    
        return 'Raise' + str(int(pot_size * 0.2))
    
    if possibility >= raise_threshold:
        return 'All-in'
    
    return 'Fold'


def should_bluff(bluff_chance=8):
    if random.randint(0, 10) <= bluff_chance:
        return True
    return False





