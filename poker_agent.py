# @Author: Bertan Berker
# @Language: Python
# This is a poker agent that plays Texas Hold'em Poker. 
# It is a CrewAI powered AI bot that uses multiple agents to make decisions

from crewai import Crew, Process
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from crewai import Agent, Task, Crew
from pydantic import BaseModel
from crewai_tools import ScrapeWebsiteTool, SerperDevTool
import warnings
warnings.filterwarnings('ignore')
import os

load_dotenv()
openai_api_key = os.getenv('OPENAI_API_KEY')
serper_api_key = os.getenv('SERPER_API_KEY')
os.environ["OPENAI_MODEL_NAME"] = 'gpt-3.5-turbo'

# Defining the Tools

search_tool = SerperDevTool()
scrape_tool = ScrapeWebsiteTool()

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
    agentHand: list


# AGENTS
evaluate_situation = Agent(
    role= "Hand Evaluator Agent",
    goal ="Evaluates players chances of winning based on their hand and the community cards",
    background = "Specializing in Texas Holdem Poker hand evaluation, this agent uses statistical analysis,"
                 "and calculates the exact chance of winning this hand based on the {community_Cards} and the {agentHand}",
    verbose=False,
    allow_delegation=False,
    tools = [scrape_tool, search_tool]
)


decide_move = Agent(
    role= "Decision Maker Agent",
    goal ="Poker Agent that plays Texas Hold'em Poker",
    background = "Specializing in Texas Holdem Poker decision making, this agent uses statistical analysis,",
    verbose=True,
    tools = [scrape_tool, search_tool]
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
    
    def play(self, env):
        return