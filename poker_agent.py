# @Author: Bertan Berker
# @Language: Python
#
#
#

from crewai import Agent, Task, Crew


# Agent1 - Evaluate Poker Hand + community cards to evaluate the chances of winning
# Agent2 - Decide on a move based on the chances
# Agent3 - Decide on a bet (if raising)
# Agent4 - Return the move-bet to the environment


class PokerAgent(Agent):
    def __init__(self, money):
        self.money = money

