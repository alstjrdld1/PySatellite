import gym
import numpy as np
from gym import spaces

from libs.Environments.thesis_env import *

import gym
from gym import spaces

class GymThesisEnv(gym.Env):
    def __init__(self, satellite_num: int = 8, orbit_alts: list = [600, 1000], ground_user_num: int = 16):
        super(GymThesisEnv, self).__init__()

        self.env = ThesisEnv(satellite_num, orbit_alts, ground_user_num)

        # Gym 환경 변수 설정
        self.action_space = spaces.Discrete(self.env.satellite_num * len(orbit_alts))
        self.observation_space = spaces.Box(low=-np.inf, high=np.inf, shape=(14 * self.env.satellite_num,))

    def step(self, action):
        reward, done, info = self.env.step(action)
        return self.env.get_state(), reward, done, info

    def reset(self):
        self.env.reset()
        return self.env.get_state()

    def render(self, mode='human'):
        self.env.render(mode)

    def close(self):
        self.env.close()
