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


