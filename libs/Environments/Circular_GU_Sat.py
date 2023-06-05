'''
 This Environment is composed with ground users and satellites
'''
from abc import *

from libs.Environments.CircularOrbit_2D import *
from libs.GroundUser import *

class Circular_GU_Sat(CircularOrbit_2D):
    def __init__(self,
                 satellite_num: int = 8,
                 orbit_alts: list =[1000],
                 ground_user_num: int = 16):
        
        super().__init__(satellite_num, orbit_alts)

        self.ground_user_num = ground_user_num
        self.reset()
    
    def reset(self) -> None:
        self.orbits = []

        self.source_satellite = (1, 0)
        self.current_satellite = (1, 0)
        self.destination_satellite = (1, 0)

        _ground_user_locations = get_points_on_earth(R, self.ground_user_num)
        
        i_th_orbit = []

        for gu_loc in _ground_user_locations:
            gu = GroundUser(pos = (gu_loc[0], gu_loc[1], 0))
            i_th_orbit.append(gu)

        self.orbits.append(i_th_orbit)
        
        for altitude in self.orbit_altitude_list:
            i_th_orbit = []
            
            locations = get_points_on_earth(R + altitude, self.satellite_num)
            # velocities = get_velocities_on_earth(locations)

            for loc in locations:
                sat = Satellite(pos = (loc[0], loc[1], 0))
                # sat = Satellite(pos = (0, -(R + altitude), 0))
                
                i_th_orbit.append(sat)

            self.orbits.append(i_th_orbit)
        
        
    def calc_relative_velocities(self):
        _gus = self.orbits[0]
        _sats = self.orbits[1:]

        for gu in _gus:
            for i_sats in _sats:
                for sat in i_sats:
                    if(is_line_of_sight(gu, sat)):
                        _relative_vel = gu.calc_relative_velocity(sat)
                        return _relative_vel
                    else:
                        return None
                    
    def get_angle(self):
        _gus = self.orbits[0]
        _sats = self.orbits[1:]

        for gu in _gus:
            for i_sats in _sats:
                for sat in i_sats:
                    if(is_line_of_sight(gu, sat)):
                        x1, y1 = gu.get_position()[:2]
                        x2, y2 = sat.get_position()[:2]
                        _angle = get_angle(x1, y1, x2, y2)
                        return _angle
                    else:
                        return None
                    
    def get_distance(self):
        _gus = self.orbits[0]
        _sats = self.orbits[1:]

        for gu in _gus:
            for i_sats in _sats:
                for sat in i_sats:
                    if(is_line_of_sight(gu, sat)):
                        return get_distance(gu, sat)
                    else:
                        return None
    

    def get_reward(self) -> float:
        pass

    def step(self, action):
        pass 

    def set_action(self, action: int) -> list:
        pass

    def get_state(self):
        pass