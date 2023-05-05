from libs.AirCraft import *
import random
from typing import List
from libs.pySatelliteUtils import *

class OrbitBaseLine:
    def __init__(self,
                 satellite_num: int = 8,
                 orbit_alts: list = [400, 1000]):
        
        self.orbit_num = len(orbit_alts)

        self.satellite_num = satellite_num
        self.orbit_altitude_list = orbit_alts

        self.orbit_altitude_list.sort() # Orbit sort into 100, 200, 300 

        for idx, alt in enumerate(self.orbit_altitude_list): 
            self.orbit_altitude_list[idx] = alt * 1000 # Km to meter

        self.source_satellite = (0, 0)
        self.current_satellite = (0, 0)
        self.destination_satellite = (0, 0)

        self.orbits = []

        for altitude in self.orbit_altitude_list:
            i_th_orbit = []
            
            locations = get_points_on_earth(R + altitude, self.satellite_num)
            # velocities = get_velocities_on_earth(locations)

            for loc in locations:
                sat = Satellite(pos = (loc[0], loc[1], 0))
                
                i_th_orbit.append(sat)

            self.orbits.append(i_th_orbit)

    def reset(self) -> None:
        self.orbits = []

        for altitude in self.orbit_altitude_list:
            i_th_orbit = []
            
            locations = get_points_on_earth(R + altitude, self.satellite_num)
            # velocities = get_velocities_on_earth(locations)

            for loc in locations:
                sat = Satellite(pos = (loc[0], loc[1], 0))
                
                i_th_orbit.append(sat)

            self.orbits.append(i_th_orbit)

    ## GET Already defined satellites
    def get_source_satellite(self) -> Satellite:
        _layer = self.source_satellite[0]
        _idx = self.source_satellite[1]
        return self.orbits[_layer][_idx]
    
    def get_current_satellite(self) -> Satellite:
        _layer = self.current_satellite[0]
        _idx = self.current_satellite[1]
        return self.orbits[_layer][_idx]

    def get_destination_satellite(self) -> Satellite:
        _layer = self.destination_satellite[0]
        _idx = self.destination_satellite[1]
        return self.orbits[_layer][_idx]        
    ########################################################### 
    
    ## GET specific satellites
    def get_satellite(self, layer, index) -> Satellite:
        try:
            return self.orbits[layer][index]
        except Exception as e: 
            print(e)
            raise

    def get_satellite_by_sid(self, sid) -> Satellite:
        _sat_orbit = sid // self.satellite_num
        _sat_idx = sid % self.satellite_num
        return self.get_satellite(_sat_orbit, _sat_idx)
    ########################################################### 