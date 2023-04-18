import numpy as np
import random

class GridWorld:#예제 환경
    def __init__(self, grid_size=6):
        self.grid_size = grid_size
        self.goal = None
        self.agent_position = None

        self.observation_space = {'shape': (grid_size, grid_size), 'dtype': np.float32}
        self.action_space = {'n': 4, 'shape': (), 'dtype': int} # up down left right

        self.reset()

    def reset(self):
        self.agent_position = np.array([random.randint(0, self.grid_size -1), random.randint(0, self.grid_size - 1)], dtype=int) # position into 0~5, 0~5 random
        self.goal = (random.randint(0, self.grid_size - 1), random.randint(0, self.grid_size - 1)) # object number 목표치
        return self._get_state()

    def reward_function(self):
        target_position = np.array(self.goal)
        manhattan_distance = np.sum(np.abs(np.array(self.agent_position) - target_position))
        reward = -manhattan_distance
        return reward

    def step(self, action):
        if action == 0:  # Move up
            self.agent_position[0] = max(0, self.agent_position[0] - 1)
        elif action == 1:  # Move down
            self.agent_position[0] = min(self.grid_size - 1, self.agent_position[0] + 1)
        elif action == 2:  # Move left
            self.agent_position[1] = max(0, self.agent_position[1] - 1)
        elif action == 3:  # Move right
            self.agent_position[1] = min(self.grid_size - 1, self.agent_position[1] + 1)

        reward = self.reward_function()
        done = np.array_equal(self.agent_position, self.goal)

        return self._get_state(), reward, done, {}

    def _get_state(self):
        state = np.zeros((self.grid_size, self.grid_size)) # 000000000000 initialize
        state[tuple(self.agent_position)] = 1
        state[tuple(self.goal)] = 0.5
        return state

    def render(self):
        grid_repr = np.zeros((self.grid_size, self.grid_size), dtype=object)
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                if np.array_equal(self.agent_position, [i, j]):
                    grid_repr[i, j] = "A"
                elif np.array_equal(self.goal, [i, j]):
                    grid_repr[i, j] = "G"
                else:
                    grid_repr[i, j] = "."

        print("\n".join([" ".join(row) for row in grid_repr]))
        print("")