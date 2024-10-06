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
    
    handover_count = 0
    ho_cmf = []
    cummulative_cp = 0
    cmf = []

    for i in range(iteration):
        for i in range(16):
            env.gu_idx = i
            gu =env.orbits[0][i]
            state = env.get_state()

            los = env.los_sats
            sats = env.orbits[1:]

            signal_snr_list = {}

            max = 0
            maxIdx = -1

            cp = 0
            selected_sat = None
            vel_vec = None
            ang = None

            # for RSSI
            for j, layer in enumerate(los):
                for k, kappa in enumerate(layer):
                    if(los[j][k] == 1):
                        distance = get_distance(gu, sats[j][k])
                        rv = env.rel_velocities[j][k]
                        snr = get_snr_fspl_doppler(distance,
                                                frequency=freq,
                                                velocity = rv[0]**2 + rv[1]**2 + rv[2]**2,
                                                angle = env.prop_angles[j][k])
                        curIdx = number*j + k
                        signal_snr_list[curIdx] = snr

                        if(max < snr):
                            max = snr
                            maxIdx = curIdx
                            selected_sat = sats[j][k]
                            vel_vec = env.rel_velocities[j][k]
                            ang = env.prop_angles[j][k]

            env.set_action(maxIdx)

            if(not(gu.connected_sat[0] == gu.prev_connected_sat[0] and gu.connected_sat[1] == gu.prev_connected_sat[1])):
                handover_count += 1

            snr = get_snr_fspl_doppler(distance=get_distance(gu, selected_sat),
                                    frequency=freq,
                                    velocity=math.sqrt(vel_vec[0]**2 + vel_vec[1]**2 + vel_vec[2]**2),
                                    angle=ang)
            cp = shannon_hartley(snr, bandwidth=bandwidth)
            cummulative_cp += cp
        cmf.append(cummulative_cp)
        ho_cmf.append(handover_count)
        env.rotate(60)

    print("##############################################################################")
    print("########### RSSI")
    print("cp : ", cummulative_cp, "handover : ", handover_count)
    print("cmf : ", cmf)
    print("ho_cmf : ", ho_cmf)
    np.save("RSSI_"+str(freq)+"_"+str(bandwidth)+"_cmf_" +str(number),np.array(cmf))
    np.save("RSSI_"+str(freq)+"_"+str(bandwidth)+"_ho_cmf_"+str(number),np.array(ho_cmf))
    print("##############################################################################")