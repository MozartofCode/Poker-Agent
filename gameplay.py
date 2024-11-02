# @Author: Bertan Berker
# @Language: Python
# 
#


import random
from monte_carlo_bot import MonteCarloBot
from poker_agent import PokerAgent
from hand_evaluation import choose_winner


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

        for _ in range(2):
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
    

    def round_updates_monte_first(self):
            
            bot_move = self.monte_carlo_bot.play(self.get_current_env())

            if bot_move == "fold":
                return "agent"
            
            elif "raise" in bot_move: # raise-$50
                self.monte_carlo_bot_bet += int(bot_move.split("-$")[1])

            while True:
                agent_move = self.agent.play(self.get_current_env())

                if agent_move == "fold":
                    return "bot"
                
                elif "raise" in agent_move:
                    self.agent_bet += int(agent_move.split("-$")[1])

                    bot_move = self.monte_carlo_bot.play(self.get_current_env())

                    if bot_move == "fold":
                        return "agent"
                    
                    elif bot_move == "call":
                        self.monte_carlo_bot_bet = self.agent_bet
                        return "continue"
                    
                    elif "raise" in bot_move:
                        self.monte_carlo_bot_bet += int(bot_move.split("-$")[1])

                elif agent_move == "call":
                    self.agent_bet = self.monte_carlo_bot_bet
                    return "continue"

                elif agent_move == "check":
                    return "continue"


    def round_updates_agent_first(self):
            
            agent_move = self.agent.play(self.get_current_env())

            if agent_move == "fold":
                return "agent"
            
            elif "raise" in agent_move: # raise-$50
                self.agent_bet += int(agent_move.split("-$")[1])

            while True:
                bot_move = self.monte_carlo_bot.play(self.get_current_env())

                if bot_move == "fold":
                    return "agent"
                
                elif "raise" in bot_move:
                    self.monte_carlo_bot_bet += int(bot_move.split("-$")[1])

                    agent_move = self.agent.play(self.get_current_env())

                    if agent_move == "fold":
                        return "bot"
                    
                    elif agent_move == "call":
                        self.agent_bet = self.monte_carlo_bot_bet
                        return "continue"
                    
                    elif "raise" in agent_move:
                        self.agent_bet += int(bot_move.split("-$")[1])

                elif bot_move == "call":
                    self.monte_carlo_bot_bet = self.agent_bet
                    return "continue"

                elif bot_move == "check":
                    return "continue"


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
            round_result = self.round_updates_agent_first()
                                
            if round_result == "agent":
                return "agent"
            
            elif round_result == "bot":
                return "bot"
            
            
            # After Flop: Monte Carlo Bot starts first
            self.game_turn = "flop"
            self.deal_flop()
            
            round_result = self.round_updates_monte_first()

            if round_result == "agent":
                return "agent"
            
            elif round_result == "bot":
                return "bot"
            
            # After Turn: Monte Carlo Bot starts first
            self.game_turn = "turn"
            self.deal_turn()
            
            round_result = self.round_updates_monte_first()

            if round_result == "agent":
                return "agent"
            
            elif round_result == "bot":
                return "bot"
            
            # After River: Monte Carlo Bot starts first
            self.game_turn = "river"
            self.deal_river()
            
            round_result = self.round_updates_monte_first()

            if round_result == "agent":
                return "agent"
            
            elif round_result == "bot":
                return "bot"
            
            if choose_winner(self.agent_hand + self.community_cards, self.monte_carlo_bot_hand + self.community_cards):
                return "agent"
            else:
                return "bot"         


        # Agent is the Big Blind
        else:
            self.agent_bet += self.big_blind
            self.monte_carlo_bot_bet += self.small_blind

            # Pre-flop: Bot starts first
            round_result = self.round_updates_monte_first()
                                
            if round_result == "agent":
                return "agent"
            
            elif round_result == "bot":
                return "bot"
            
            
            # After Flop: Agent starts first
            self.game_turn = "flop"
            self.deal_flop()
            
            round_result = self.round_updates_agent_first()

            if round_result == "agent":
                return "agent"
            
            elif round_result == "bot":
                return "bot"
            
            # After Turn: Agent starts first
            self.game_turn = "turn"
            self.deal_turn()
            
            round_result = self.round_updates_agent_first()

            if round_result == "agent":
                return "agent"
            
            elif round_result == "bot":
                return "bot"
            
            # After River: Agent starts first
            self.game_turn = "river"
            self.deal_river()
            
            round_result = self.round_updates_agent_first()

            if round_result == "agent":
                return "agent"
            
            elif round_result == "bot":
                return "bot"
            
            if choose_winner(self.agent_hand + self.community_cards, self.monte_carlo_bot_hand + self.community_cards):
                return "agent"
            else:
                return "bot"         

    

        
        