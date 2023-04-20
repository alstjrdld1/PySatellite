import gym
from libs.Environments.CircularOrbitEnv import *

from stable_baselines3 import A2C, DQN, DDPG, PPO

from stable_baselines3.common.env_util import make_vec_env
from stable_baselines3.common.env_checker import check_env

sat_num = 5
gamma = 0.99
n_step = 10

env = CircularOrbitEnv(
    satellite_num=sat_num
)

check_env(env)
policy_kwargs = dict(net_arch=dict(pi=[128, 128], vf=[256, 256]))
# model = A2C("MlpPolicy", env, verbose=1, policy_kwargs=policy_kwargs, tensorboard_log="./logs/", learning_rate=utilities.custom_lr_schedule, n_steps=64, gamma=0.0)

model = DQN("MlpPolicy", 
            env, 
            verbose=1,
            tensorboard_log="satellite", 
            # batch_size = 64,
            # train_freq = 16
            # n_steps=n_step,
            # policy_kwargs=policy_kwargs,
            # gamma=gamma, 
            # exploration_final_eps = 0.0005,
            # normalize_advantage=True,
            # n_steps=30,
            # learning_rate=0.001,
            )

model.learn(total_timesteps=1000000)

model.save(f"A2C_Circular_Satellite_num_{sat_num}_gamma_{gamma}_maxstep_50")
