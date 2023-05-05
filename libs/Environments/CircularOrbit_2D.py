from abc import abstractmethod, ABC
import matplotlib.pyplot as plt

import time

from libs.pySatelliteUtils import *
from libs.Environments.OrbitBaseline import *

class CircularOrbit_2D(OrbitBaseLine, ABC):
    def __init__(self,
                 satellite_num: int = 8,
                 orbit_alts: list =[400, 1000]):
        
        super().__init__(satellite_num = satellite_num,
                       orbit_alts = orbit_alts)
    
    @abstractmethod
    def reset(self) -> None:
        pass 

    @abstractmethod
    def get_reward(self) -> float:
        pass

    @abstractmethod
    def step(self, action):
        pass 

    @abstractmethod
    def set_action(self, action: int) -> list:
        pass

    @abstractmethod
    def get_state(self):
        pass
    
    def los(self) -> list:
        self.los_list = get_line_of_sight_list_tf(self.get_current_satellite(), self.orbits)
        # print(self.los_list)
        _los = []
        for _layer, orbit in enumerate(self.los_list):
            for _idx, sat_visible in enumerate(orbit):
                if(sat_visible):
                    _los.append(_layer * self.satellite_num + _idx)
        
        return _los

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

    # def plot(self, wtime: float = 1) -> None:
    #     earth = plt.Circle((0,0), R / R, facecolor='black', edgecolor='black')
    #     plt.gca().add_patch(earth)
    #     time.sleep(1)
        
    #     x = []
    #     y = [] 
    #     z = []
    #     for orbit in self.orbits:
    #         for sat in orbit:
    #             # print(sat.get_position())
    #             _sat_x, _sat_y, _sat_z = sat.get_position()
    #             x.append(_sat_x / R)
    #             y.append(_sat_y / R)
    #             z.append(_sat_z / R)

    #     plt.plot(x, y, 'ro', color = 'gray')

    #     for cand in self.los():
    #         cand_sat = self.get_satellite_by_sid(cand)
    #         plt.plot(cand_sat.get_position()[0] / R, cand_sat.get_position()[1] / R, marker='o', color='purple')

    #     src_sat =  self.get_satellite(self.source_satellite[0], self.source_satellite[1])
    #     plt.plot(src_sat.get_position()[0] / R, src_sat.get_position()[1] / R, marker='o', color='orange')

    #     current_sat = self.get_current_satellite()
    #     plt.plot(current_sat.get_position()[0] / R, current_sat.get_position()[1] / R, marker='o', color='blue')

    #     dest_sat = self.get_destination_satellite()
    #     plt.plot(dest_sat.get_position()[0] / R, dest_sat.get_position()[1] / R, marker='o', color='green')

    #     plt.axis('equal')
    #     plt.show(block=False)
    #     # plt.show()

    #     plt.pause(wtime)

    #     plt.close()

    def plot(self) -> None:
        from astropy import units as u

        from poliastro.bodies import Earth, Mars, Sun
        from poliastro.twobody import Orbit

        from poliastro.plotting import OrbitPlotter2D

        op=OrbitPlotter2D()

        for orbit in self.orbits:
            for sat in orbit:
                # print(sat.get_position())
                r = sat.get_position() << u.km
                v = sat.get_velocity() << u.km / u.s
                op.plot(Orbit.from_vectors(Earth, r, v))

        op.show()