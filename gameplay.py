# @Author: Bertan Berker
# @Language: Python
# 
#


import random
from monte_carlo_bot import MonteCarloBot
from poker_agent import PokerAgent
#from poker_agent


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
        self.monte_carlo_bot = MonteCarloBot(1000)
        self.agent = PokerAgent(1000)
        self.big_blind = 50
        self.small_blind = 25
        self.hand_count = 0 
        self.pot = 0
        self.blind_monte = True  # True if Monte Carlo Bot is the Big Blind
        self.reset()

    
    def reset(self):

        self.deck = Deck()
        self.community_cards = []
        self.monte_carlo_bot_hand = []
        self.agent_hand = []
        self.game_turn = "pre-flop"
        self.agent_bet = 0
        self.monte_carlo_bot_bet = 0

        for i in range(4):
            self.agent_hand.append(self.deck.draw_card())
            self.monte_carlo_bot_hand.append(self.deck.draw_card())
        

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


    def get_current_env(self):
        # Environment format to feed into the Agent
        return {
            "agentBigBlind": not self.big_blind,
            "gameTurn": self.game_turn,
            "pot": self.pot,
            "agentBet": self.agent_bet,
            "playerBet": self.monte_carlo_bot_bet,
            "playerMoney": self.monte_carlo_bot.money,
            "agentMoney": self.agent.money,
            "communityCards": self.community_cards,
            "playerHand": self.monte_carlo_bot_hand,
            "agentHand": self.agent_hand
        }

    # :return: winner of the round as 'agent' or 'bot'
    def play_round(self):

        # Increasing the blinds (if necessary)
        self.hand_count += 1

        if self.hand_count % 50 == 0:
            self.big_blind += 25
            self.small_blind += 50

        # Monte Carlo Bot is the Big Blind
        if self.blind_monte:
                
            self.agent_bet += self.small_blind
            self.monte_carlo_bot_bet += self.big_blind

            # Pre-flop: Agent starts first

            while self.agent_bet != self.monte_carlo_bot_bet:
                agent_move = self.agent.play_pre_flop(self.get_current_env())
                if agent_move == "fold":
                    return "bot"
                elif agent_move == "call":
                    self.agent_bet = self.monte_carlo_bot_bet
                    bot_move = self.monte_carlo_bot.play_pre_flop(self.get_current_env())
                    if bot_move == "fold":
                        return "agent"
                    elif bot_move == "check":
                        break
            

            # After Flop: Monte Carlo Bot starts first
            self.deal_flop()
            
            # After Turn: Monte Carlo Bot starts first
            self.deal_turn()
            
            # After River: Monte Carlo Bot starts first
            self.deal_river()

        # Agent is the Big Blind
        else:
            return
        
        self.big_monte = not self.big_monte