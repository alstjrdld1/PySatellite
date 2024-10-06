from libs.Environments.thesis_env import *
from stable_baselines3 import PPO

import random

satellite_num = 16
env = ThesisEnv(satellite_num=satellite_num,
                orbit_alts=[600, 1000],
                ground_user_num=16)
env.reset()

model = PPO.load("D:/pySatellite/ptfiles/Thesis_channel_capacity_more_important_3hour")

handover_count = 0
cummulative_cp = 0
i = 0
cmf = []
ho_cmf = []
while(True):
    state = env.get_state()

    los = env.los_sats
    sats = env.orbits[1:]
    velocities = env.rel_velocities
    prop_anlges = env.prop_angles

    gu =env.orbits[0][env.gu_idx]

    selected, _states = model.predict(state, deterministic=True)

    env.set_action(selected)
    j = selected // satellite_num
    k = selected % satellite_num

    if(gu.connected_sat[0] == gu.prev_connected_sat[0] and gu.connected_sat[1] == gu.prev_connected_sat[1]):
        pass
    else:
        handover_count += 1

    # print("vel vec : ", vel_vec)

    cp = get_snr_fspl_doppler(distance=get_distance(gu, sats[j][k]),
                              velocity=math.sqrt(velocities[j][k][0]**2 + velocities[j][k][1]**2 + velocities[j][k][2]**2),
                              angle=prop_anlges[j][k])
    cummulative_cp += cp
    cmf.append(cummulative_cp)
    # print("cp : ", cp, "handover : ", handover_count)
    ho_cmf.append(handover_count)
    env.rotate(60)
    i+=1
    if(i > 180):
        break

print("cp : ", cummulative_cp, "handover : ", handover_count)
print("cmf : ", cmf)
print("ho_cmf : ", ho_cmf)
