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
    def next_move(self, state):

        # best value for MAX player
        best_value = -1 * math.inf

        best_actions = []
        for action in state.available_actions:
            new_state = copy.deepcopy(state)
            new_state._verbose = False
            reward, game_over = new_state.act(action)
            if game_over:
                action_value = reward
            else:
                action_value = self.get_value(new_state)
            best_value = max(action_value, best_value)
            if action_value == best_value:
                best_actions.append(action)
            else:
                best_actions = [action]

        return random.choice(best_actions)

    def get_value(self, state, maxPlayer=False, depth_limit=6, cur_depth=2, alpha=-math.inf, beta=math.inf):
        # if depth_limit == cur_depth:
        #     return 0

        if maxPlayer:
            best_value = -math.inf
        else:
            best_value = math.inf

        for action in state.available_actions:
            new_state = copy.deepcopy(state)
            reward, game_over = new_state.act(action)
            if game_over:
                # action_value = reward
                action_value = abs(reward) / cur_depth
            else:
                action_value = self.get_value(new_state, maxPlayer=not maxPlayer, cur_depth=cur_depth + 1)

            if maxPlayer:
                alpha = max(alpha, action_value)
                if action_value >= beta:
                    return action_value
            else:
                beta = min(beta, action_value)
                if action_value <= alpha:
                    return action_value

            if maxPlayer:
                best_value = max(action_value, best_value)
            else:
                best_value = min(action_value, best_value)

        return best_value


connect = connect.Connect(num_cols=5)
humanAgent = HumanAgent()
connectAgent = ConnectAgent()
game_over = False

while not game_over:
    move = humanAgent.next_move(connect)
    reward, game_over = connect.act(action=move)
    if game_over and reward == 1:
        print("Player one wins!")
        break
    elif game_over and reward == -1:
        print("It's a draw.")
        break

    move = connectAgent.next_move(connect)
    reward, game_over = connect.act(action=move)
    if game_over and reward == 1:
        print("Player two wins!")
        break
    elif game_over and reward == -1:
        print("It's a draw.")
        break
