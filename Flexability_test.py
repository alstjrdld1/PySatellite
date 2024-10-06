from libs.Environments.thesis_env import *
from stable_baselines3 import PPO
import time

satellite_num = [12, 16, 20, 24]

freq = 1e9 # Hz GHz = 1e9
bandwidth = 5*1024 # Hz GHz = 1e9
iteration = 180

for number in satellite_num:
    env = ThesisEnv(satellite_num=number,
                    orbit_alts=[600, 1000],
                    ground_user_num=16)
    env.reset()

    model = PPO.load(f"D:/pySatellite/ptfiles/PPO_Thesis_channel_capacity_3hour_5M_{number}.zip")
    
    handover_count = 0
    ho_cmf = []
    cummulative_cp = 0
    cmf = []

    for iter in range(iteration):
        for i in range(16):
            env.gu_idx = i
            gu =env.orbits[0][i]
            state = env.get_state()

            los = env.los_sats
            sats = env.orbits[1:]

            velocities = env.rel_velocities
            prop_anlges = env.prop_angles

            selected, _states = model.predict(state, deterministic=True)

            env.set_action(selected)
            j = selected // number
            k = selected % number

            if(not(gu.connected_sat[0] == gu.prev_connected_sat[0] and gu.connected_sat[1] == gu.prev_connected_sat[1])):
                handover_count += 1

            dist = get_distance(gu, sats[j][k])
            vel = velocities[j][k]

            snr = get_snr_fspl_doppler(distance=dist,
                                    frequency=freq,
                                    velocity=math.sqrt(vel[0]**2 + vel[1]**2 + vel[2]**2),
                                    angle=prop_anlges[j][k])
            cp = shannon_hartley(snr, bandwidth)
            cummulative_cp += cp
        cmf.append(cummulative_cp)
        ho_cmf.append(handover_count)
        env.rotate(60)

    print("##############################################################################")
    print("########### Proposed " + str(number))
    print("cp : ", cummulative_cp, "handover : ", handover_count)
    print("cmf : ", cmf)
    print("ho_cmf : ", ho_cmf)
    np.save("Proposed_"+str(freq)+"_"+str(bandwidth)+"_cmf_"+str(number),np.array(cmf))
    np.save("Proposed_"+str(freq)+"_"+str(bandwidth)+"_ho_cmf_"+str(number),np.array(ho_cmf))
    print("##############################################################################")