from typing import List

from Constants import *
from AirCraft import *
from pySatelliteUtils import *

import random

class CircularOrbit:
    def __init__(self, 
                 satellite_num: int = 8,
                 orbit_alts: list = [300]):
        
        self.oribit_num = len(orbit_alts)
        self.satellite_num = satellite_num
        self.orbit_altitude_list = orbit_alts

        self.reset()

    def reset(self):
        self.orbit_altitude_list.sort() # Orbit sort into 100, 200, 300 
        self.orbits = []

        for altitude in self.orbit_altitude_list:
            i_th_orbit = []

            locations = get_points_on_earth(altitude, self.satellite_num)
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

        for orbit in self.orbits:
            for sat in orbit:
                # print(sat)
                print(sat.get_position())

        return self.source_satellite, self.destination_satellite, self.rest_time, self.los_list, self.los_propagation_angle_list

if __name__=="__main__":
    sat1 = Satellite()
    # print(type(sat1) == Satellite)
    env = CircularOrbit()
    env._get_state()