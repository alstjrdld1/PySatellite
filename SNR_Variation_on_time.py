from stable_baselines3 import PPO
from libs.Environments.thesis_env import *
import time
number = 16

freq = 1e9 # Hz GHz = 1e9
bandwidth = 5*1024 # Hz GHz = 1e9
iteration = 180

env = ThesisEnv(satellite_num=number,
                orbit_alts=[600, 1000],
                ground_user_num=16)
env.reset()

model = PPO.load(f"D:/pySatellite/ptfiles/PPO_Thesis_channel_capacity_3hour_5M_{number}.zip")

while(True):
    gu =env.orbits[0][0]
    state = env.get_state()

    los = env.los_sats
    sats = env.orbits[1:]

    velocities = env.rel_velocities
    prop_anlges = env.prop_angles

    start_time = time.time()
    selected, _states = model.predict(state, deterministic=True)
    end_time = time.time()
    inf_time = end_time - start_time

    print("INFERENCING TIME : ", inf_time)

    env.set_action(selected)
    j = selected // number
    k = selected % number
    dist = get_distance(gu, sats[j][k])
    vel = velocities[j][k]

    snr = get_snr_fspl_doppler(distance=dist,
                            frequency=freq,
                            velocity=math.sqrt(vel[0]**2 + vel[1]**2 + vel[2]**2),
                            angle=prop_anlges[j][k])
    cp = shannon_hartley(snr, bandwidth)

    print("BEFORE ROTATE CP : ", cp)

    env.rotate(inf_time) # ROTATE 

    state = env.get_state()

    los = env.los_sats
    sats = env.orbits[1:]
    velocities = env.rel_velocities
    prop_anlges = env.prop_angles

    dist = get_distance(gu, sats[j][k])
    vel = velocities[j][k]

    snr = get_snr_fspl_doppler(distance=dist,
                            frequency=freq,
                            velocity=math.sqrt(vel[0]**2 + vel[1]**2 + vel[2]**2),
                            angle=prop_anlges[j][k])
    cp = shannon_hartley(snr, bandwidth)

    print("AFTER ROTATE CP : ", cp)
    

