import copy
import math
import random
from abc import ABC, abstractmethod

import connect


class Agent(ABC):
    @abstractmethod
    def next_move(self, state):
        pass


class HumanAgent(Agent):
    def next_move(self, state):
        while True:
            try:
                print("What's your next move? Available columns:")
                print(state.available_actions)
                move = input("> ").strip()
                move = int(move)
                if move not in state.available_actions:
                    print("Invalid column.")
                else:
                    return move
            except ValueError:
                print(f"Please enter valid column from: {state.available_actions}")


class ConnectAgent(Agent):
    def __init__(self, verbose=False):
        self.verbose = verbose

    def next_move(self, game):
        print("\nThe AI is thinking.", end="")

        best_action = []
        best_value = -1 * math.inf
        for action in game.available_actions:
            # important: take a copy of the entire game so we don't break things
            # memory intensive, but saves us rewriting the game
            game_copy = copy.deepcopy(game)
            # game_copy._verbose = False

            reward, game_over = game_copy.act(action)

            if game_over:
                # this code always tries to maximise the score
                # but the game returns reward for player 2 ('o')
                # if our move ended the game, then it was either win or draw
                # so absolute value will ensure we get 0 or 1 no matter if we are p1 or p2
                action_value = abs(reward)
            else:
                # our move didn't end the game, so recurse
                action_value = self.get_value(game_copy, get_min=True)
            print(".", end="", flush=True)

            if self.verbose:
                print(action_value, end=" ")
            if action_value > best_value:
                best_action = [action]
                best_value = action_value
            if action_value == best_value:
                best_action.append(action)

        if self.verbose:
            print()
        print("\n")

        return random.choice(best_action)

    def get_value(self, game, get_min, alpha=-math.inf, beta=math.inf, turn=2):
        """If get_min is set to true, returns the minimum value, otherwise the maximum value"""

        best_value = math.inf
        if not get_min:
            best_value *= -1

        for action in game.available_actions:
            game_copy = copy.deepcopy(game)

            reward, game_over = game_copy.act(action)

            if game_over:
                # there is an explanation for diving by the turn number above!
                action_value = abs(reward) / turn
                if get_min:
                    # force the reward to be -1 if this was a winning move while looking to minimise
                    # but keep it as zero if it was a draw
                    action_value *= -1
            else:
                action_value = self.get_value(game_copy, get_min=not get_min, alpha=alpha, beta=beta, turn=turn + 1)

            if not get_min:
                alpha = max(alpha, action_value)
                if action_value >= beta:
                    return action_value
            else:
                beta = min(beta, action_value)
                if action_value <= alpha:
                    return action_value

            if not get_min and action_value > best_value \
                    or get_min and action_value < best_value:
                best_value = action_value

        return best_value


def run_game(game, player1=HumanAgent(), player2=ConnectAgent()):
    game_over = False
    while not game_over:
        move = player1.next_move(game)
        reward, game_over = game.act(move)

        # reward is in terms of player 2, 'o'
        if game_over and reward == -1:
            print("Player one wins!")
            return
        elif game_over and reward == 0:
            print("It's a draw.")
            return

        move = player2.next_move(game)
        reward, game_over = game.act(move)

        if game_over and reward == 1:
            print("Player two wins!")
            return
        elif game_over and reward == 0:
            print("It's a draw.")
            return


def yes_no_input(text, prompt="> "):
    print(text + " (y/n)")
    response = input(prompt).strip()
    while response not in ['y', 'n']:
        print("Please enter y for yes or n for no.")
        print(text)
        response = input(prompt).strip()
    return response == "y"


def play():
    cols = 5
    rows = 3
    n = 3

    print(f"Let's play connect {n}!")
    game = connect.Connect(num_cols=cols, num_rows=rows, num_connect=n, verbose=False)
    again = True
    while again:
        response = yes_no_input("Would you like to play first?")
        if response:
            run_game(game=game, player1=HumanAgent(), player2=ConnectAgent())
        else:
            run_game(game=game, player1=ConnectAgent(), player2=HumanAgent())

        again = yes_no_input("Would you like to play again?")
        if again:
            game.reset()


if __name__ == '__main__':
    play()
