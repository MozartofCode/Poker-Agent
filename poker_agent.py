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
    verbose=True,
    allow_delegation=False,
    tools = [scrape_tool, search_tool]
)


decide_move = Agent(
    role= "Decision Maker Agent",
    goal ="Decides on a move for the agent to make in a Texas Hold'em Poker game",
    background = "Specializing in Texas Holdem Poker decision making, this agent makes a decision of raising, calling, "
                 "checking or folding while using probability and statistical analysis. This is based on {community_Cards}, {agentHand}, "
                 "{agentMoney}, {playerMoney}, {pot}, {gameTurn}, {agentBet} and {playerBet}",
    verbose=True,
    allow_delegation=True,
    tools = [scrape_tool, search_tool]
)

bluff_master = Agent(
    role= "Bluff Strategy Agent",
    goal ="Decides on bluffing or not based on the position in the game",
    background = "Greatest Texas Hold'em poker strategist, this agent uses a combination of probability, psychology, statistics,"
                 "and positional play in order to make the best decision on whether to bluff or not and how much to raise to bluff if bluffing",
    verbose=True,
    allow_delegation=True,
    tools = [scrape_tool, search_tool]
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
    agents=[evaluate_situation, decide_move],
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
    "agentHand":"",
}

result = poker_crew.kickoff(inputs=poker_inputs)



class PokerAgent():
    def __init__(self, money):
        self.money = money
    
    def play(self, env):
        return