import gym
from libs.Environments.CircularOrbitEnv import *

while True:
    env = CircularOrbitEnv(satellite_num=8)
    env.reset()
    env.render(5)


for env_num in env_nums:
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

    