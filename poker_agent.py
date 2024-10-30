# @Author: Bertan Berker
# @Language: Python
#
#
#

from crewai import Agent, Task, Crew
from pydantic import BaseModel


# Agent1 - Evaluate Poker Hand + community cards to evaluate the chances of winning
# Agent2 - Decide on a move based on the chances
# Agent3 - Decide on a bet (if raising)
# Agent4 - Return the move-bet to the environment



# Created the class for this format for easier output/input from and for the agents

class Move(BaseModel):
    agentBigBlind: bool
    gameTurn: str
    pot: int
    agentBet: int
    playerBet: int
    playerMoney: int
    agentMoney: int
    communityCards: list
    playerHand: list
    agentHand: list




class PokerAgent():
    def __init__(self, money):
        self.money = money
    
    def play_pre_flop(self):
        return
    
    def play_flop(self):
        return

    def play_turn(self):
        return

    def play_river(self):
        return
    



