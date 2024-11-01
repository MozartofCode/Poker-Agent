# @Author: Bertan Berker
# @Language: Python
#
#
#
# CREW
from crewai import Crew, Process
from langchain_openai import ChatOpenAI
from crewai import Agent, Task, Crew
from pydantic import BaseModel
from crewai_tools import ScrapeWebsiteTool, SerperDevTool

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



# AGENTS
evaluate_situation = Agent(
    role= "PokerAgent",
    goal ="Poker Agent that plays Texas Hold'em Poker",
    background = "Poker",
    verbose=True,
    tools = []
)


decide_move = Agent(
    role= "PokerAgent",
    goal ="Poker Agent that plays Texas Hold'em Poker",
    background = "Poker",
    verbose=True,
    tools = []
)


decide_bet = Agent(
    role= "PokerAgent",
    goal ="Poker Agent that plays Texas Hold'em Poker",
    background = "Poker",
    verbose=True,
    tools = []
)

return_decision = Agent(
    role= "PokerAgent",
    goal ="Poker Agent that plays Texas Hold'em Poker",
    background = "Poker",
    verbose=True,
    tools = []
)


# TASKS
analyze = Task(
    description=(
        ""
    ),
    expected_output=(
        ""
    ),
    agent= evaluate_situation
)

make_move = Task(
    description="Find a venue in {event_city} ",
    expected_output="",
    human_input=True,
    output_json= Move,
    output_file="venue_details.json",  
    agent= decide_move
)


bet = Task(
    description="Find a venue in {event_city} ",
    expected_output="",
    human_input=True,
    output_json= Move,
    output_file="venue_details.json",  
    agent= decide_bet
)

decision = Task(
        description="Find a venue in {event_city} ",
    expected_output="",
    human_input=True,
    output_json= Move,
    output_file="venue_details.json",  
    agent= return_decision
)


# Define the crew with agents and tasks
poker_crew = Crew(
    agents=[evaluate_situation, decide_move, decide_bet, return_decision],
    tasks=[analyze, make_move, bet],
    manager_llm=ChatOpenAI(model="gpt-3.5-turbo", temperature=0.7),
    process=Process.hierarchical,
    verbose=True
)

# RUN

poker_inputs = {
    "agentBigBlind":"",
    "gameTurn":"",
    "pot":"",
    "agentBet":"",
    "playerBet":"",
    "playerMoney":"",
    "agentMoney":"",
    "communityCards":"",
    "playerHand":"",
    "agentHand":"",
}

result = poker_crew.kickoff(inputs=poker_inputs)



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
    



