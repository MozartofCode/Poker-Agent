# @Author: Bertan Berker
# @Language: Python
# This is the main file for the poker simulation between two bots

from gameplay import PokerEnv


def main():
    
    game = PokerEnv()

    while  game.agent.money > 0 and game.monte_carlo_bot.money > 0:
        print("Starting the new round...\n")

        game.play_round()

        # Reseting the game
        game.blind_monte = not game.blind_monte
        game.reset()
    
    if game.agent.money == 0:
        print("Monte Carlo Bot Wins the game!")
    
    else:
        print("Agent Wins the game!")
        

if __name__ == "__main__":
    main()