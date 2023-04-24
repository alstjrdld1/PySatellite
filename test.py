import gym
from libs.Environments.CircularOrbitEnv import *

from stable_baselines3 import A2C, DQN, DDPG, PPO

from stable_baselines3.common.env_util import make_vec_env
from stable_baselines3.common.env_checker import check_env
import time

env_nums = [8, 12]

pt_files = { 
            #  4  : 'PPO_Circular_Satellite_num_4',
            #  5  : 'PPO_Circular_Satellite_num_5',
             8  : 'PPO_Circular_Satellite_num_8',
            #  10 : 'PPO_Circular_Satellite_num_10',
             12 : 'PPO_Circular_Satellite_num_12'}

for env_num in env_nums:
    env = CircularOrbitEnv(satellite_num=env_num)
    loaded_model = PPO.load("D:/workspace/Minseok/pySatellite/ptfiles/" + pt_files[env_num])
    obs = env.reset()
    _dest = env.orbit.destination_satellite

    _dest_idx = _dest[0]*env_num + _dest[1]

    _prev_act = -1

    while True:
        action, _states = loaded_model.predict(obs, deterministic=True)

        if(action == _prev_act):
            continue

        _prev_act = action

        env.render()

        print("ACTION :  ", action)

        _los = env.orbit.los()

        if(action not in _los):
            continue
        
        # if(_dest_idx in _los):
        #     action = _dest_idx

        obs, rewards, done, info = env.step(action)
        if done:
            env.render(5)
            break

    