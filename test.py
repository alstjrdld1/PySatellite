import gym
from libs.Environments.CircularOrbitEnv import *

from stable_baselines3 import A2C, DQN, DDPG, PPO

from stable_baselines3.common.env_util import make_vec_env
from stable_baselines3.common.env_checker import check_env

env_nums = [4, 5, 8, 10, 12]

pt_files = { 4  : 'PPO_Circular_Satellite_num_4_gamma_0.91',
             5  : 'PPO_Circular_Satellite_num_5_gamma_0.918',
             8  : 'PPO_Circular_Satellite_num_8_gamma_0.92',
             10 : 'PPO_Circular_Satellite_num_10_gamma_0.91',
             12 : 'PPO_Circular_Satellite_num_12_gamma_0.91'}

for env_num in env_nums:
    env = CircularOrbitEnv(satellite_num=env_num)
    loaded_model = PPO.load("D:/pySatellite/ptfiles/" + pt_files[env_num])
    obs = env.reset()

    while True:
        action, _states = loaded_model.predict(obs, deterministic=True)
        obs, rewards, dones, info = env.step(action)
        env.render()
