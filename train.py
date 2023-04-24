import gym
from libs.Environments.CircularOrbitEnv import *

from stable_baselines3 import A2C, DQN, DDPG, PPO

from stable_baselines3.common.env_util import make_vec_env
from stable_baselines3.common.env_checker import check_env

sat_num = 16
# gamma = 0.92
# gamma = 0.9999999 # sat 4
# gamma = 0.983 # sat 6
# gamma = 0.946 # sat 10
gamma = 0.88 # sat 16

n_step = 10

env = CircularOrbitEnv(
    satellite_num=sat_num
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

model.learn(total_timesteps=1000000)

model.save(f"A2C_Circular_Satellite_num_{sat_num}_gamma_{gamma}_maxstep_50")
