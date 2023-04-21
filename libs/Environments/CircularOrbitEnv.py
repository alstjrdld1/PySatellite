import gym
import numpy as np
from gym import spaces

from libs.Environments.SatelliteEnvironment import *

class CircularOrbitEnv(gym.Env):
    def __init__(self, 
                 satellite_num: int = 8,
                 orbit_alts: list = [400, 1000]):
        super(CircularOrbitEnv, self).__init__()

        self.orbit = CircularOrbit(satellite_num, orbit_alts)

        # Define action and observation spaces
        action_size = self.orbit.orbit_num * self.orbit.satellite_num
        self.action_space = spaces.Discrete(action_size)

        # Define the observation space
        # obs_length = 2 * 2 + 2 * self.orbit.orbit_num * self.orbit.satellite_num
        # obs_length = 3 * self.orbit.orbit_num * self.orbit.satellite_num
        obs_length = 6 * self.orbit.orbit_num * self.orbit.satellite_num
        # obs_length = 2 * 2
        self.observation_space = spaces.Box(low=-50000.0, high=50000.0, shape=(obs_length,), dtype=np.float64)

    def reset(self):
        self.orbit.reset()
        return self.orbit.get_state()

    def step(self, action):
        reward, done, info = self.orbit.step(action)
        return self.orbit.get_state(), reward, done, info

    def render(self, mode='human'):
        self.orbit.plot()

    def close(self):
        pass

    def seed(self, seed=None):
        random.seed(seed)
