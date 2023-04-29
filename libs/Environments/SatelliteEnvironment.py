from typing import List

from libs.Constants import *
from libs.AirCraft import *
from libs.pySatelliteUtils import *

from libs.Channels.Loss import *
from libs.Channels.DataRate import *
from libs.Channels.SNR import *

import random
import matplotlib.pyplot as plt

class CircularOrbit:
    def __init__(self, 
                 satellite_num: int = 8,
                 orbit_alts: list = [400, 1000]): # UNIT KM
        
        self.orbit_num = len(orbit_alts)
        self.satellite_num = satellite_num

        for idx, alt in enumerate(orbit_alts): 
            orbit_alts[idx] = alt * 1000 # Km to meter

        self.orbit_altitude_list = orbit_alts

        self.current_step = 0
        self.current_reward = 0
        self.max_step = satellite_num

        self.reset()

    def reset(self) -> None:
        self.orbit_altitude_list.sort() # Orbit sort into 100, 200, 300 
        self.orbits = []
        self.current_step = 0
        self.current_reward = 0
        self.jump_list = []

        for altitude in self.orbit_altitude_list:
            i_th_orbit = []
            
            locations = get_points_on_earth(R + altitude, self.satellite_num)
            # velocities = get_velocities_on_earth(locations)

            for loc in locations:
                sat = Satellite(pos = (loc[0], loc[1], 0))
                
                i_th_orbit.append(sat)

            self.orbits.append(i_th_orbit)

        self.source_satellite = (random.randint(0, len(self.orbit_altitude_list) - 1), random.randint(0, self.satellite_num - 1)) # orbit index, satellite index
        self.current_satellite = self.source_satellite
        self.destination_satellite = (random.randint(0, len(self.orbit_altitude_list) - 1), random.randint(0, self.satellite_num - 1)) # orbit index, satellite index
        # self.destination_satellite = (1, 4) # orbit index, satellite index
        # self.destination_satellite = (1, 2499)

        self.rest_time = MAXIMUM_TIME

        self.los_list = []
        self.los_propagation_angle_list = [] # The value is 0 when 
        self.tp = TRANSMISSION_POWER

    def get_reward(self, tp: float, sat: tuple):
        _sat_orbit, _sat_idx = sat

        if((self.get_current_satellite().get_position()[0] == _sat_orbit) and 
           (self.get_current_satellite().get_position()[1] == _sat_idx)):
            return 0
        
        _target_sat = self.get_satellite(_sat_orbit, _sat_idx)
        _dist = get_distance(self.get_current_satellite(), _target_sat)
        _dist = _dist * 1e5

        # print("DISTANCE : ", _dist)
        # _cp = channel_capacity(transmit_power=self.tp, 
        #                        distance=_dist, 
        #                        velocity=self.get_current_satellite().get_velocity_mag(), 
        #                        propagation_velocity_angle=self.los_propagation_angle_list[_sat_orbit][_sat_idx])
        _snr = get_snr_fspl(distance=_dist)
        _cp = shannon_hartley(_snr)
        
        _transmission_time = propagation_latency(self.get_current_satellite(), _target_sat)
        
        return math.log(_cp / tp)

    def step(self, action:int):
        # self.plot()
        _tp = TRANSMISSION_POWER

        try:
            _sat_orbit, _sat_idx = self.set_action(action)
        except:
            raise

        _target_satellite = self.get_satellite(_sat_orbit, _sat_idx)
        self.current_step +=1

        reward = 0 
        done = False
        info = {}

        _los = self.los()

        # print("#####################################################")
        # print("SOURCE : ", self.source_satellite)
        # print("CURRENT SAT : ", self.current_satellite)
        # print("DESTINATION : ", self.destination_satellite)
        # print("LOS LIST : ", _los)
        # print("ACTION : ",  _sat_orbit, _sat_idx, action)
        # print("#####################################################")
        
        # if self.current_step > self.max_step:
            # reward = -1
            # info["reason"] = "exceed max step"
            # print(info)
            # done = True

        if self.rest_time < 0:
            reward = -1
            info['reason'] = "TIME OUT"
            print(info)
            done = True

        if action not in _los:
            reward = -1
            info["reason"] = "NON LINE of sight"
            # print(info)
            done = True

        if action in self.jump_list:
            reward = -1
            info["reason"] = "Jump Again"
            # print(info)
            done = True

        if (action in _los) and (not done):
            if self.current_step > self.max_step:
                self.current_reward -= 1
            else:
                _reward = self.get_reward(tp = _tp, sat=(_sat_orbit, _sat_idx))
                # print("CP REWARD : ", _reward) # 0 ~ 28
                self.current_reward += _reward

            transmission_time = propagation_latency(self.get_current_satellite(), _target_satellite)
        
            self.rest_time -= transmission_time

            self.rotate(transmission_time)

            self.tp = TRANSMISSION_POWER
            self.current_satellite = (_sat_orbit, _sat_idx)
            done = np.array_equal(self.current_satellite, self.destination_satellite)

            self.jump_list.append(action)

            if(done):
                info['reason'] = 'FINISH'
                # reward = 10 * self.current_reward / self.current_step
                # reward = 10 * self.current_reward 
                if self.current_step > self.max_step:
                    reward = 10 * self.current_reward * (0.95**(self.current_step))
                else:
                    reward = 10 * self.current_reward * (0.995**(self.current_step))
                # reward = 10
                # print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
                # print("Reward : ", reward)
                # print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
        
        if done:
            print(info)

        return reward, done, info
    
    def set_action(self, action: int) -> list:
        # Target_satellite 정해줌
        _sat_orbit = action // self.satellite_num
        _sat_idx = action % self.satellite_num

        return [_sat_orbit, _sat_idx]

    def get_state(self):
        self.los_list = get_line_of_sight_list(ac1    = self.get_current_satellite(), 
                                               srcsat = self.get_satellite(self.source_satellite[0], self.source_satellite[1]),
                                               dstsat = self.get_satellite(self.destination_satellite[0], self.destination_satellite[1]),
                                               orbits = self.orbits)

        relative_velocity = get_relative_velocity_list(self.get_current_satellite(), self.orbits, self.los_list)
        self.los_propagation_angle_list = get_propagation_angle_list(self.get_current_satellite(), self.orbits, self.los_list)
        _distance_list = get_distance_list(self.get_current_satellite(), self.orbits)
        
        # _pos_list = self.get_pos_list()
        
        _flatten = np.array([])

        _los_list = np.array(self.los_list).flatten()
        _flatten = np.concatenate([_flatten, _los_list])

        _dist_list = np.array(_distance_list).flatten()
        _flatten = np.concatenate([_flatten, _dist_list])

        _vel_list = np.array(relative_velocity).flatten()
        _flatten = np.concatenate([_flatten, _vel_list])

        _prop_angle_list = np.array(self.los_propagation_angle_list).flatten()
        _flatten = np.concatenate([_flatten, _prop_angle_list])
        
        _length = len(_flatten)
        return _flatten

    def get_current_satellite(self) -> Satellite:
        _layer = self.current_satellite[0]
        _idx = self.current_satellite[1]
        return self.orbits[_layer][_idx]

    def get_destination_satellite(self) -> Satellite:
        _layer = self.destination_satellite[0]
        _idx = self.destination_satellite[1]
        return self.orbits[_layer][_idx]
    
    def get_satellite(self, layer, index) -> Satellite:
        try:
            # print("GET_SATELLITE_LAYER : ", layer)
            # print("GET_SATELLITE_INDEX : ", index)
            return self.orbits[layer][index]
        except Exception as e: 
            print(e)
            raise

    def get_satellite_by_sid(self, sid) -> Satellite:
        _layer, _idx = self.set_action(sid)
        return self.get_satellite(_layer, _idx)
    
    def rotate(self, t) -> None:
        for orbit_idx, orbit in enumerate(self.orbits):
            for sat_idx, sat in enumerate(orbit):
                # print("##############################################################")
                # print("BEFORE ROTATE: ", self.orbits[orbit_idx][sat_idx].get_position())

                _alt = sat.get_altitude()
                _ang = sat.get_current_angle()
                _anv = sat.get_angular_velocity()
                _rot_ang = _ang+_anv*t

                if(_rot_ang > (2 * PI)):
                    _rot_ang = _rot_ang - (2*PI)
                
                # print("_ANG => ", (_ang*180 / PI), " _rot_ang => ", (_rot_ang*180/PI))

                _new_x_pos = _alt * math.cos(_rot_ang)
                _new_y_pos = _alt * math.sin(_rot_ang)
                _new_z_pos = 0

                self.orbits[orbit_idx][sat_idx].set_position((_new_x_pos, _new_y_pos, _new_z_pos))
                # print("AFTER ROTATE: ", self.orbits[orbit_idx][sat_idx].get_position())
                # print("##############################################################")

    def los(self) -> list:
        self.los_list = get_line_of_sight_list_tf(self.get_current_satellite(), self.orbits)
        # print(self.los_list)
        _los = []
        for _layer, orbit in enumerate(self.los_list):
            for _idx, sat_visible in enumerate(orbit):
                if(sat_visible):
                    _los.append(_layer * self.satellite_num + _idx)
        
        return _los
    
    def plot(self, wtime = 1) -> None:
        import time
        earth = plt.Circle((0,0), R / R, facecolor='black', edgecolor='black')
        plt.gca().add_patch(earth)
        time.sleep(1)
        
        x = []
        y = [] 
        z = []
        for orbit in self.orbits:
            for sat in orbit:
                # print(sat.get_position())
                _sat_x, _sat_y, _sat_z = sat.get_position()
                x.append(_sat_x / R)
                y.append(_sat_y / R)
                z.append(_sat_z / R)

        plt.plot(x, y, 'ro', color = 'gray')

        for cand in self.los():
            cand_sat = self.get_satellite_by_sid(cand)
            plt.plot(cand_sat.get_position()[0] / R, cand_sat.get_position()[1] / R, marker='o', color='purple')

        src_sat =  self.get_satellite(self.source_satellite[0], self.source_satellite[1])
        plt.plot(src_sat.get_position()[0] / R, src_sat.get_position()[1] / R, marker='o', color='orange')

        current_sat = self.get_current_satellite()
        plt.plot(current_sat.get_position()[0] / R, current_sat.get_position()[1] / R, marker='o', color='blue')

        dest_sat = self.get_destination_satellite()
        plt.plot(dest_sat.get_position()[0] / R, dest_sat.get_position()[1] / R, marker='o', color='green')

        plt.axis('equal')
        plt.show(block=False)

        plt.pause(wtime)

        plt.close()