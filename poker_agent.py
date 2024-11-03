# @Author: Bertan Berker
# @Language: Python
# This is a poker agent that plays Texas Hold'em Poker. 
# It is a CrewAI powered AI bot that uses multiple agents to make decisions

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from crewai import Agent, Task, Crew, Process
from crewai_tools import ScrapeWebsiteTool, SerperDevTool
import warnings
warnings.filterwarnings('ignore')
import os
from pydantic import BaseModel


load_dotenv()
openai_api_key = os.getenv('OPENAI_API_KEY')
serper_api_key = os.getenv('SERPER_API_KEY')
os.environ["OPENAI_MODEL_NAME"] = 'gpt-3.5-turbo'


# Defining the output from the AI agent system
class AgentMove(BaseModel):
    move: str
    amount: int


class PokerAgent():
    def __init__(self, money):
        self.money = money
    
    def play(self, env):
       
        # Defining the Tools
        search_tool = SerperDevTool()
        scrape_tool = ScrapeWebsiteTool()

        # AGENTS
        evaluate_situation = Agent(
            role="Hand Evaluator Agent",
            goal="Evaluates players chances of winning based on their hand and the community cards",
            backstory="Specializing in Texas Holdem Poker hand evaluation, this agent uses statistical analysis,"
                      "and calculates the exact chance of winning this hand based on the {communityCards} and the {agentHand}",
            verbose=True,
            allow_delegation=False,
            tools =[scrape_tool, search_tool]
        )


        decide_move = Agent(
            role="Decision Maker Agent",
            goal="Decides on a move for the agent to make in a Texas Hold'em Poker game",
            backstory="Specializing in Texas Holdem Poker decision making, this agent makes a decision of raising, calling, "
                      "checking or folding while using probability and statistical analysis. This is based on {communityCards}, {agentHand}, "
                      "{agentMoney}, {playerMoney}, {pot}, {gameTurn}, {agentBet} and {playerBet}",
            verbose=True,
            allow_delegation=True,
            tools=[scrape_tool, search_tool]
        )

        bluff_master = Agent(
            role="Bluff Strategy Agent",
            goal="Decides on bluffing or not based on the position in the game",
            backstory="Greatest Texas Hold'em poker strategist, this agent uses a combination of probability, psychology, statistics,"
                      "and positional play in order to make the best decision on whether to bluff or not and how much to raise to bluff if bluffing",
            verbose=True,
            allow_delegation=True,
            tools=[scrape_tool, search_tool]
        )

        # TASKS

        analyze = Task(
            description=(
                "Analyze the current situation in Texas hold'em poker game and evaluate the chances of winning "
                "based on the known information. The known information includes the {communityCards}, {agentHand}, "
                "{agentMoney}, {playerMoney}, {pot}, {gameTurn}, {agentBet} and {playerBet}"
            ),
            expected_output=(
                "The probability in the precentage of winning the game based on the current situation in addition"
                " to a paragraph explaining the situation and the reason behind the calculation"
            ),
            agent= evaluate_situation
        )

        make_move = Task(
            description=(
                "Make a move in the Texas Hold'em Poker game based on the current situation and the analysis of the situation. "
                "The move can be raising, calling, checking, or folding and based on the positional play, the player can bluff as well based on the known "
                "information. The known information includes the {agentBigBlind}, {communityCards}, {agentHand}, {agentMoney}, {playerMoney}, {pot}, {gameTurn}, {agentBet} and {playerBet}."
            ),
            expected_output=(
                "The move that the agent should make in the game in the format of a string in ONE PHRASE ONLY. The move can be raising, calling, checking, or folding. "
                "The output should be in the format: 'check', 'call', 'fold', or 'raise-$50' (where $50 is the amount to raise based on the current situation)."
            ),
            agent=decide_move,
            output_file=AgentMove
        )

        # Define the crew with agents and tasks
        poker_crew = Crew(
            agents=[evaluate_situation, bluff_master, decide_move],
            tasks=[analyze, make_move],
            manager_llm=ChatOpenAI(model="gpt-3.5-turbo", temperature=0.7),
            process=Process.sequential,
            verbose=True
        )

        # RUN
        env_parameters = {
            "agentBigBlind": env["agentBigBlind"],
            "gameTurn": env["gameTurn"],
            "pot": env["pot"],
            "agentBet": env["agentBet"],
            "playerBet": env["playerBet"],
            "playerMoney": env["playerMoney"],
            "agentMoney": env["agentMoney"],
            "communityCards": env["communityCards"],
            "agentHand": env["agentHand"]
        }

        result = poker_crew.kickoff(inputs=env_parameters)

        if result["move"] != "raise":
            return result["move"]
        
        return result["move"] + "-" + str(result["amount"])