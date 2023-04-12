from typing import List

from Constants import *
from AirCraft import *
from pySatelliteUtils import *

import random
import time
import matplotlib.pyplot as plt

class CircularOrbit:
    def __init__(self, 
                 satellite_num: int = 8,
                 orbit_alts: list = [400, 1000]): # UNIT KM
        
        self.oribit_num = len(orbit_alts)
        self.satellite_num = satellite_num

        for idx, alt in enumerate(orbit_alts): 
            orbit_alts[idx] = alt * 1000 # Km to meter

        self.orbit_altitude_list = orbit_alts

        self.reset()

    def reset(self) -> None:
        self.orbit_altitude_list.sort() # Orbit sort into 100, 200, 300 
        self.orbits = []

        for altitude in self.orbit_altitude_list:
            i_th_orbit = []

            locations = get_points_on_earth(R + altitude, self.satellite_num)
            # velocities = get_velocities_on_earth(locations)

            for loc in locations:
                sat = Satellite(pos = (loc[0], loc[1], 0))
                
                i_th_orbit.append(sat)

            self.orbits.append(i_th_orbit)

        self.source_satellite = (random.randint(0, len(self.orbit_altitude_list) - 1), random.randint(0, self.satellite_num - 1)) # orbit index, satellite index
        self.destination_satellite = (random.randint(0, len(self.orbit_altitude_list) - 1), random.randint(0, self.satellite_num - 1)) # orbit index, satellite index
        self.rest_time = MAXIMUM_TIME

        self.los_list = []
        self.los_propagation_angle_list = [] # The value is 0 when 

    def reward_function(self, tp, sat: tuple):
        _tp = tp
        _sat_orbit, _sat_idx = sat

        _target_sat = self.get_satellite(_sat_orbit, _sat_idx)
        _dist = get_distance(self.get_current_satellite(), _target_sat)

        _cp = channel_capacity(transmit_power=_tp, 
                               distance=_dist, 
                               velocity=self.get_current_satellite().get_velocity_mag(), 
                               propagation_velocity_angle=self.los_propagation_angle_list[_sat_orbit][_sat_idx])
        reward = _cp / _tp
        
        return reward
    
    def get_step(self):
        pass

    def step(self, sat_orbit= 0, sat_idx=0, power = 0):
        _current_state = self._get_state()

        # Model choose the index of will propagate and power to transmit 
        
        # reward = self.reward_function()
        reward = 0
        done = np.array_equal(self.source_satellite, self.destination_satellite)

        return self._get_state(), reward, done, {}
    
    def set_action(self, action: List[float, tuple(0,0)]):

        _tp = action[0]
        self.source_satellite = action[1]

    def get_state(self):
        self.los_list = get_line_of_sight_list(self.get_current_satellite(), self.orbits)

        # relative_velocity = get_relative_velocity_list(self.get_current_satellite(), self.orbits, self.los_list)
        self.los_propagation_angle_list = get_propagation_angle_list(self.get_current_satellite(), self.orbits, self.los_list)
        
        return self.source_satellite, self.destination_satellite, self.rest_time, self.los_list, self.los_propagation_angle_list

    def get_current_satellite(self) -> Satellite:
        _layer = self.source_satellite[0]
        _idx = self.source_satellite[1]
        return self.orbits[_layer][_idx]

    def get_destination_satellite(self) -> Satellite:
        _layer = self.destination_satellite[0]
        _idx = self.destination_satellite[1]
        return self.orbits[_layer][_idx]
    
    def get_satellite(self, layer, index) -> Satellite:
        return self.orbits[layer][index]
    
    def rotate(self, t) -> None:
        for orbit_idx, orbit in enumerate(self.orbits):
            for sat_idx, sat in enumerate(orbit):
                print("##############################################################")
                print("BEFORE ROTATE: ", self.orbits[orbit_idx][sat_idx].get_position())

                _alt = sat.get_altitude()
                _ang = sat.get_current_angle()
                _anv = sat.get_angular_velocity()
                _rot_ang = _ang+_anv*t

                if(_rot_ang > (2 * PI)):
                    _rot_ang = _rot_ang - (2*PI)
                
                print("_ANG => ", (_ang*180 / PI), " _rot_ang => ", (_rot_ang*180/PI))

                _new_x_pos = _alt * math.cos(_rot_ang)
                _new_y_pos = _alt * math.sin(_rot_ang)
                _new_z_pos = 0

                self.orbits[orbit_idx][sat_idx].set_position((_new_x_pos, _new_y_pos, _new_z_pos))
                print("AFTER ROTATE: ", self.orbits[orbit_idx][sat_idx].get_position())
                print("##############################################################")
    
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

        plt.close()
        

if __name__=="__main__":
    # sat1 = Satellite()
    # print(type(sat1) == Satellite)
    env = CircularOrbit()
    env.get_state()

    while True:
        env.plot()
        env.step()
        env.rotate(100)