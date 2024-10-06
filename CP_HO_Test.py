from libs.Environments.thesis_env import *
from stable_baselines3 import PPO
import time

satellite_num = 16

freq = 1e9 # Hz GHz = 1e9
bandwidth = 500*1024 # Hz GHz = 1e9
iteration = 180

env = ThesisEnv(satellite_num=satellite_num,
                orbit_alts=[600, 1000],
                ground_user_num=16)
model = PPO.load("D:/pySatellite/ptfiles/Thesis_channel_capacity_important_3_3hour")

model.device

handover_count = 0
ho_cmf = []
cummulative_cp = 0
cmf = []
env.reset()

startTime = time.time()
for i in range(iteration):
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

    if(not(gu.connected_sat[0] == gu.prev_connected_sat[0] and gu.connected_sat[1] == gu.prev_connected_sat[1])):
        handover_count += 1

    snr = get_snr_fspl_doppler(distance=get_distance(gu, sats[j][k]),
                               frequency=freq,
                              velocity=math.sqrt(velocities[j][k][0]**2 + velocities[j][k][1]**2 + velocities[j][k][2]**2),
                              angle=prop_anlges[j][k])
    cp = shannon_hartley(snr, bandwidth)
    cummulative_cp += cp
    cmf.append(cummulative_cp)
    ho_cmf.append(handover_count)
    env.rotate(60)
endTime = time.time()

print("##############################################################################")
print("########### Proposed")
print("cp : ", cummulative_cp, "handover : ", handover_count)
print("cmf : ", cmf)
print("ho_cmf : ", ho_cmf)
print("Total Time : ", endTime - startTime)
np.save("Proposed_"+str(freq)+"_"+str(bandwidth)+"_cmf",np.array(cmf))
np.save("Proposed_"+str(freq)+"_"+str(bandwidth)+"_ho_cmf",np.array(ho_cmf))
print("##############################################################################")

env = ThesisEnv(satellite_num=satellite_num,
                orbit_alts=[600, 1000],
                ground_user_num=16)
env.reset()

handover_count = 0
cummulative_cp = 0
cmf = []
ho_cmf = []

startTime = time.time()
for i in range(iteration):
    state = env.get_state()

    los = env.los_sats
    sats = env.orbits[1:]
    velocities = env.rel_velocities
    prop_anlges = env.prop_angles

    gu =env.orbits[0][env.gu_idx]

    losIdx = []

    max = 0
    maxIdx = -1

    for j, layer in enumerate(los):
        for k, kappa in enumerate(layer):
            if(los[j][k] == 1):
                distance = get_distance(gu, sats[j][k]) * 1e5
                curIdx = satellite_num*j + k
                
                losIdx.append(curIdx)

    selected = random.randrange(0, len(losIdx))

    env.set_action(losIdx[selected])
    j = losIdx[selected] // satellite_num
    k = losIdx[selected] % satellite_num

    if(not(gu.connected_sat[0] == gu.prev_connected_sat[0] and gu.connected_sat[1] == gu.prev_connected_sat[1])):
        handover_count += 1

    snr = get_snr_fspl_doppler(distance=get_distance(gu, sats[j][k]),
                               frequency=freq,
                               velocity=math.sqrt(velocities[j][k][0]**2 + velocities[j][k][1]**2 + velocities[j][k][2]**2),
                               angle=prop_anlges[j][k])
    cp = shannon_hartley(snr, bandwidth=bandwidth)
    cummulative_cp += cp

    cmf.append(cummulative_cp)
    ho_cmf.append(handover_count)
    env.rotate(60)
endTime = time.time()

print("##############################################################################")
print("########### RANDOM")
print("cp : ", cummulative_cp, "handover : ", handover_count)
print("cmf : ", cmf)
print("ho_cmf : ", ho_cmf)
print("Total Time : ", endTime - startTime)
np.save("Random_"+str(freq)+"_"+str(bandwidth)+"_cmf",np.array(cmf))
np.save("Random_"+str(freq)+"_"+str(bandwidth)+"_ho_cmf",np.array(ho_cmf))
print("##############################################################################")

handover_count = 0
ho_cmf = []
cummulative_cp = 0
cmf = []
env = ThesisEnv(satellite_num=satellite_num,
                orbit_alts=[600, 1000],
                ground_user_num=16)
env.reset()

startTime = time.time()
for i in range(iteration):
    gu =env.orbits[0][env.gu_idx]
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
                curIdx = satellite_num*j + k
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
endTime = time.time()

print("##############################################################################")
print("########### RSSI")
print("cp : ", cummulative_cp, "handover : ", handover_count)
print("cmf : ", cmf)
print("ho_cmf : ", ho_cmf)
print("Total Time : ", endTime - startTime)
np.save("RSSI_"+str(freq)+"_"+str(bandwidth)+"_cmf",np.array(cmf))
np.save("RSSI_"+str(freq)+"_"+str(bandwidth)+"_ho_cmf",np.array(ho_cmf))
print("##############################################################################")


###########################################################################################
# GREEDY
###########################################################################################
handover_count = 0
ho_cmf = []
cummulative_cp = 0
cmf = []
env = ThesisEnv(satellite_num=satellite_num,
                orbit_alts=[600, 1000],
                ground_user_num=16)
env.reset()

startTime = time.time()

for iter in range(iteration):
    state = env.get_state()

    los = env.los_sats
    sats = env.orbits[1:]

    gu = env.orbits[0][env.gu_idx]

    cp = 0
    cp_list = []
    cand_list = []
    selected_sat = None
    vel_vec = None
    ang = None

    # for RSSI
    for j, layer in enumerate(los):
        for k, kappa in enumerate(layer):
            if(los[j][k] == 1):
                distance = get_distance(gu, sats[j][k])
                rv = env.rel_velocities[j][k]
                ang = env.prop_angles[j][k]

                snr = get_snr_fspl_doppler(distance,
                                           frequency=freq,
                                           velocity = rv[0]**2 + rv[1]**2 + rv[2]**2,
                                           angle = ang)
                
                curCp = shannon_hartley(snr, bandwidth=bandwidth)
                cp_list.append(curCp)
                cand_list.append((j, k))

    obj_list = []
    alpha = 0.00000001
    beta = 1

    max = 0
    max_cp = 0
    maxIdx = -1

    for idx, _cp in enumerate(cp_list):
        curIdx = satellite_num*cand_list[idx][0] + cand_list[idx][1]

        handover = 1
        _obj = 0
        if(gu.connected_sat[0] == cand_list[idx][0] and gu.connected_sat[1] ==cand_list[idx][1]):
            _obj = (alpha * _cp) / (beta*handover)
        else:
            _obj = (alpha*_cp) / (beta*(handover+1))

        if(max < _obj):
            max = _obj
            max_cp = _cp
            maxIdx = curIdx

    env.set_action(maxIdx)

    if(not(gu.connected_sat[0] == gu.prev_connected_sat[0] and gu.connected_sat[1] == gu.prev_connected_sat[1])):
        handover_count += 1

    cummulative_cp += max_cp
    cmf.append(cummulative_cp)
    ho_cmf.append(handover_count)

    env.rotate(60)
endTime = time.time()

print("##############################################################################")
print("########### AB")
print("cp : ", cummulative_cp, "handover : ", handover_count)
print("cmf : ", cmf)
print("ho_cmf : ", ho_cmf)
print("Total Time : ", endTime - startTime)
np.save("AB_"+str(freq)+"_"+str(bandwidth)+"_cmf",np.array(cmf))
np.save("AB_"+str(freq)+"_"+str(bandwidth)+"_ho_cmf",np.array(ho_cmf))
print("##############################################################################")













###########################################################################################
# LONGEST TIME 
###########################################################################################
handover_count = 0
ho_cmf = []
cummulative_cp = 0
cmf = []
env = ThesisEnv(satellite_num=satellite_num,
                orbit_alts=[600, 1000],
                ground_user_num=16)
env.reset()

startTime = time.time()

for iter in range(iteration):
    state = env.get_state()

    los = env.los_sats
    sats = env.orbits[1:]

    gu = env.orbits[0][env.gu_idx]

    cp = 0
    cp_list = []
    cand_list = []
    selected_sat = None
    vel_vec = None
    ang = None

    minPropAng = env.prop_angles[gu.connected_sat[0]][gu.connected_sat[1]]
    minPropIdx = satellite_num * gu.connected_sat[0] + gu.connected_sat[1]

    prev_sat_in_los = False

    # for LONGEST
    for j, layer in enumerate(los):
        for k, kappa in enumerate(layer):
            if(los[j][k] == 1):
                if(gu.connected_sat[0] == j and gu.connected_sat[1]== k):
                    prev_sat_in_los = True
                    break
    
    if(not prev_sat_in_los):
        minPropAng = 9999
        for j, layer in enumerate(los):
            for k, kappa in enumerate(layer):
                ang = env.prop_angles[j][k]
                _curIdx  = satellite_num*j + k
                if(minPropAng > ang):
                    minPropAng = ang
                    minPropIdx = _curIdx

                elif(minPropAng == ang):
                    minPropDistance = get_distance(gu, sats[minPropIdx // satellite_num][minPropIdx % satellite_num])
                    distance = get_distance(gu, sats[j][k])
                    if(minPropDistance < distance):
                        minPropIdx = _curIdx

    env.set_action(minPropIdx)

    j = minPropIdx // satellite_num
    k = minPropIdx % satellite_num

    distance = get_distance(gu, sats[j][k])
    rv = env.rel_velocities[j][k]
    ang = env.prop_angles[j][k]
    
    snr = get_snr_fspl_doppler(distance,
                                frequency=freq,
                                velocity = rv[0]**2 + rv[1]**2 + rv[2]**2,
                                angle = ang)
    
    curCp = shannon_hartley(snr, bandwidth=bandwidth)
    
    if(not(gu.connected_sat[0] == gu.prev_connected_sat[0] and gu.connected_sat[1] == gu.prev_connected_sat[1])):
        handover_count += 1

    cummulative_cp += curCp
    cmf.append(cummulative_cp)
    ho_cmf.append(handover_count)

    env.rotate(60)
endTime = time.time()

print("##############################################################################")
print("########### LONGEST")
print("cp : ", cummulative_cp, "handover : ", handover_count)
print("cmf : ", cmf)
print("ho_cmf : ", ho_cmf)
print("Total Time : ", endTime - startTime)
np.save("LONGEST_"+str(freq)+"_"+str(bandwidth)+"_cmf",np.array(cmf))
np.save("LONGEST_"+str(freq)+"_"+str(bandwidth)+"_ho_cmf",np.array(ho_cmf))
print("##############################################################################")