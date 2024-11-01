# @Author: Bertan Berker
# @Language: Python
# This is the main file for the poker simulation between two bots

from gameplay import PokerEnv


def main():
    
    game = PokerEnv()

    while  game.agent.money > 0 and game.monte_carlo_bot.money > 0:
        game.play_round(True)
        

if __name__ == "__main__":
    main()