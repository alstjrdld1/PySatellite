from libs.Environments.thesis_env import *

satellite_num = 16
env = ThesisEnv(satellite_num=satellite_num,
                orbit_alts=[600, 1000],
                ground_user_num=16)
env.reset()

handover_count = 0
cmf = []
ho_cmf = []
cummulative_cp = 0
i = 0
while(True):
    state = env.get_state()

    los = env.los_sats
    sats = env.orbits[1:]

    gu =env.orbits[0][env.gu_idx]

    signal_snr_list = {}

    max = 0
    maxIdx = -1

    cp = 0
    selected_sat = None
    vel_vec = None
    ang = None
    # print(env.rel_velocities)
    # print(env.prop_angles)

    # for RSSI
    for j, layer in enumerate(los):
        for k, kappa in enumerate(layer):
            if(los[j][k] == 1):
                distance = get_distance(gu, sats[j][k]) * 1e5
                snr = get_snr_fspl(distance)
                curIdx = satellite_num*j + k
                signal_snr_list[curIdx] = snr

                if(max < snr):
                    max = snr
                    maxIdx = curIdx
                    selected_sat = sats[j][k]
                    vel_vec = env.rel_velocities[j][k]
                    ang = env.prop_angles[j][k]

    env.set_action(maxIdx)

    if(gu.connected_sat[0] == gu.prev_connected_sat[0] and gu.connected_sat[1] == gu.prev_connected_sat[1]):
        pass
    else:
        handover_count += 1

    # print("vel vec : ", vel_vec)

    cp = get_snr_fspl_doppler(distance=get_distance(gu, selected_sat),
                              velocity=math.sqrt(vel_vec[0]**2 + vel_vec[1]**2 + vel_vec[2]**2),
                              angle=ang)
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