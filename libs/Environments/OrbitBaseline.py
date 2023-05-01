from libs.AirCraft import *
import random
from typing import List

class OrbitBaseLine:
    def __init__(self,
                 satellite_num: int = 8,
                 orbit_alts: list = [400, 1000]):
        
        self.orbit_num = len(orbit_alts)
        self.orbits = List[List[Satellite]]

        self.satellite_num = satellite_num
        self.orbit_altitude_list.sort() # Orbit sort into 100, 200, 300 

        for idx, alt in enumerate(orbit_alts): 
            orbit_alts[idx] = alt * 1000 # Km to meter

        self.orbit_altitude_list = orbit_alts

        self.source_satellite = (0, 0)
        self.current_satellite = (0, 0)
        self.destination_satellite = (0, 0)

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
    
    def get_satellite(self, layer, index) -> Satellite:
        try:
            return self.orbits[layer][index]
        except Exception as e: 
            print(e)
            raise