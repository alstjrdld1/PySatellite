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
        # self.max_step = int(satellite_num / 2)
        self.max_step = satellite_num
        # self.max_step = 50
        self.current_reward = 0

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
        # self.destination_satellite = (1, 2499)

        self.rest_time = MAXIMUM_TIME

        self.los_list = []
        self.los_propagation_angle_list = [] # The value is 0 when 
        self.tp = TRANSMISSION_POWER

    def get_reward(self, tp: float, sat: tuple):
        _sat_orbit, _sat_idx = sat

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
        
        return math.log(1 + (_cp / tp)) / (1+_transmission_time)

    def step(self, action:int):
        _tp = TRANSMISSION_POWER

        if(type(action) == np.ndarray):
            action = action[0][0]

        try:
            _sat_orbit, _sat_idx = self.set_action(action)
        except:
            raise

        _target_satellite = self.get_satellite(_sat_orbit, _sat_idx)
        self.jump_list.append((_sat_orbit, _sat_idx))

        reward = 0 
        done = False
        info = {}

        if action in self.los():
            # _is_prev = np.array_equal(self.current_satellite, (_sat_orbit, _sat_idx))
            # if(_is_prev):
            #     reward -= 1
            # else:
            #     reward += 5

            # self.current_reward += 0.001

            _reward = self.get_reward(tp = _tp, sat=(_sat_orbit, _sat_idx))
            # print("CP REWARD : ", _reward) # 0 ~ 28
            self.current_reward += _reward

            transmission_time = propagation_latency(self.get_current_satellite(), _target_satellite)
        
            self.rest_time -= transmission_time

            self.rotate(transmission_time)

            self.tp = TRANSMISSION_POWER
            self.current_satellite = (_sat_orbit, _sat_idx)

            done = np.array_equal(self.current_satellite, self.destination_satellite)

            if(done):
                info['reason'] = 'FINISH'
                reward = 10*self.current_reward / (self.current_step+1)
                print("#####################################################")
                print("Reward : ", reward)
                print("#####################################################")
            # else:
                # print("CURRENT SAT : ", self.source_satellite)
                # print("DEST SAT : ", self.destination_satellite)
            self.current_step +=1
        else:
            # print("#####################################################")
            # print(self.los())
            # print(action)
            # print("#####################################################")
            reward = -10
            info["reason"] = "NON LINE of sight"
            done = True

        if self.rest_time < 0:
            reward = -10
            info['reason'] = "TIME OUT"
            done = True

        if self.current_step > self.max_step:
            reward = -10
            info["reason"] = "exceed max step"
            done = True

        if done:
            print("SRC : ", self.source_satellite)
            print("CURRENT : ", self.current_satellite)
            print("DEST : ", self.destination_satellite)
            print("JUMP LIST : ", self.jump_list)
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

        # relative_velocity = get_relative_velocity_list(self.get_current_satellite(), self.orbits, self.los_list)
        # self.los_propagation_angle_list = get_propagation_angle_list(self.get_current_satellite(), self.orbits, self.los_list)
        # _distance_list = get_distance_list(self.get_current_satellite(), self.orbits)
        
        _flatten = np.array([])
        # _src_sat_flatten = np.array(self.current_satellite)
        # _flatten = np.concatenate([_flatten, _src_sat_flatten])

        # _dst_sat_flatten = np.array(self.destination_satellite)
        # _flatten = np.concatenate([_flatten, _dst_sat_flatten])

        # np.append(_flatten, self.rest_time)

        _los_list = np.array(self.los_list).flatten()
        _flatten = np.concatenate([_flatten, _los_list])

        # _dist_list = np.array(_distance_list).flatten()
        # _flatten = np.concatenate([_flatten, _dist_list])

        # _prop_angle_list = np.array(self.los_propagation_angle_list).flatten()
        # _flatten = np.concatenate([_flatten, _prop_angle_list])
        
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
    
    def plot(self) -> None:
        try:
            plt.clf()
        except:
            pass

        earth = plt.Circle((0,0), R / R, facecolor='blue', edgecolor='black')
        plt.gca().add_patch(earth)

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

        current_sat = self.get_current_satellite()
        plt.plot(current_sat.get_position()[0] / R, current_sat.get_position()[1] / R, marker='o', color='orange')

        dest_sat = self.get_destination_satellite()
        plt.plot(dest_sat.get_position()[0] / R, dest_sat.get_position()[1] / R, marker='o', color='green')

        plt.axis('equal')
        plt.show()