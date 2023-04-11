from typing import List

from Constants import *
from AirCraft import *
from pySatelliteUtils import *

import random
import matplotlib.pyplot as plt

class CircularOrbit:
    def __init__(self, 
                 satellite_num: int = 8,
                 orbit_alts: list = [300, 1000]): # UNIT KM
        
        self.oribit_num = len(orbit_alts)
        self.satellite_num = satellite_num

        for idx, alt in enumerate(orbit_alts): 
            orbit_alts[idx] = alt * 1000 # Km to meter

        self.orbit_altitude_list = orbit_alts

        self.reset()

    def reset(self):
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
        self.los_propagation_angle_list = []

    def reward_function(self):
        
        return 

    def step(self, action):
        # Calculate LOS for all of orbits 

        # Calculate propagation angle and using satellite's velocity 

        # Model choose the index of will propagate and power to transmit 
        
        # Calculate Reward 

        reward = self.reward_function()
        done = np.array_equal(self.source_satellite, self.destination_satellite)

        return self._get_state(), reward, done, {}

    def _get_state(self):
        _layer = self.source_satellite[0]
        _idx = self.source_satellite[1]

        self.los_list = get_line_of_sight_list(self.get_current_satellite(), self.orbits)
        

        return self.source_satellite, self.destination_satellite, self.rest_time, self.los_list, self.los_propagation_angle_list

    def get_current_satellite(self) -> Satellite:
        _layer = self.source_satellite[0]
        _idx = self.source_satellite[1]

        return self.orbits[_layer][_idx]

    def get_destination_satellite(self) -> Satellite:
        _layer = self.destination_satellite[0]
        _idx = self.destination_satellite[1]

        return self.orbits[_layer][_idx]
    
    def get_satellite(self, layer, index):

        return self.orbits[layer][index]
    
    def plot(self):
        earth = plt.Circle((0,0), R / R, facecolor='blue', edgecolor='black')
        plt.gca().add_patch(earth)

        data = []

        for layer_idx, orbit in enumerate(self.orbits):
            for sat_idx, sat in enumerate(orbit):
                data.append(sat.get_position())

        x = [i[0]/R for i in data] 
        y = [i[1]/R for i in data]

        # layer, idx = self.los_list[0]
        # los_candidate_pos = self.orbits[layer][idx].get_position()

        # linx = [current_sat.get_position()[0] / R, los_candidate_pos[0] / R]
        # liny = [current_sat.get_position()[1] / R, los_candidate_pos[1] / R]

        plt.plot(x, y, 'ro', color = 'gray')

        current_sat = self.get_current_satellite()
        plt.plot(current_sat.get_position()[0] / R, current_sat.get_position()[1] / R, marker='o', color='orange')

        dest_sat = self.get_destination_satellite()
        plt.plot(dest_sat.get_position()[0] / R, dest_sat.get_position()[1] / R, marker='o', color='green')

        # plt.plot(linx,liny)
        plt.axis('equal')
        plt.show()

if __name__=="__main__":
    # sat1 = Satellite()
    # print(type(sat1) == Satellite)
    env = CircularOrbit()
    env._get_state()
    env.plot()