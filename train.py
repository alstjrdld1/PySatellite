import gym
from libs.Environments.CircularOrbitEnv import *

from stable_baselines3 import A2C, DQN, DDPG, PPO

from stable_baselines3.common.env_util import make_vec_env
from stable_baselines3.common.env_checker import check_env

import sys 

sat_num = 16

if len(sys.argv) != 2:
    sys.exit()
else:
    sat_num = int(sys.argv[1])

print(sat_num)

gamma_map = {
    4   :   0.97,
    6   :   0.96,
    8   :   0.91,
    10  :   0.905,
    12  :   0.90 ,
    16  :   0.898
}
gamma = gamma_map[sat_num]

n_step = 10

env = CircularOrbitEnv(
    satellite_num=sat_num,
    orbit_alts=[400,1000]
)

check_env(env) 
policy_kwargs = dict(net_arch=dict(pi=[128, 128], vf=[256, 256]))
# model = A2C("MlpPolicy", env, verbose=1, policy_kwargs=policy_kwargs, tensorboard_log="./logs/", learning_rate=utilities.custom_lr_schedule, n_steps=64, gamma=0.0)

model = PPO("MlpPolicy", 
            env, 
            verbose=1,
            tensorboard_log="satellite", 
            # batch_size = 256,
            # train_freq = 16,
            # n_steps=n_step,
            # policy_kwargs=policy_kwargs,
            gamma=gamma, 
            # gradient_steps=3,
            # exploration_final_eps = 0.0005,
            # normalize_advantage=True,
            # n_steps=30,
            learning_rate=0.00003,
            )

model.learn(total_timesteps=10000000)

model.save(f"PPO_Satellite_num_{sat_num}_gamma_{gamma}_maxStep_{sat_num}_reward*0.99**current_step")