# @Author: Bertan Berker
# @Language: Python
# This is the main file for the poker simulation between two bots

from gameplay import PokerEnv


def choose_winner(rl_bot, monte_carlo_bot):

    if rl_bot.money > monte_carlo_bot.money:
        return "RL Bot"
    elif rl_bot.money < monte_carlo_bot.money:
        return "Monte Carlo Bot"


def main():
    
    env = PokerEnv()

    # Is Monte Carlo Bot the Big Blind
    isMonteBB = True

    while  env.rl_bot.money > 0 and env.monte_carlo_bot.money > 0:
        
        if isMonteBB:
            env.play_round(True)
            isMonteBB = False
        else:
            env.play_round(False)
            isMonteBB = True

    print("The winner is:" + choose_winner(env.rl_bot, env.monte_carlo_bot))


if __name__ == "__main__":
    main()