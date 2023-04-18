import gym
from libs.Environments.CircularOrbitEnv import *

from stable_baselines3 import DDPG
from stable_baselines3.common.env_util import make_vec_env
from stable_baselines3.common.env_checker import check_env

env = CircularOrbitEnv(
    satellite_num=500
)

check_env(env)

model = DDPG("MlpPolicy", env, verbose=1,tensorboard_log="satellite")
model.learn(total_timesteps=1000000)
