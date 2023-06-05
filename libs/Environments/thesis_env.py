# from Circular_GU_Sat import *
from libs.Environments.Circular_GU_Sat import *
from libs.pySatelliteUtils import *

from libs.Channels.DataRate import *
from libs.Channels.SNR import *

class ThesisEnv(Circular_GU_Sat):
    def __init__(self,
                 satellite_num: int = 8,
                 orbit_alts: list =[600, 1000],
                 ground_user_num: int = 16):
        
        super().__init__(satellite_num, orbit_alts, ground_user_num)

        self.gu_idx = 0
        self.los_sats = []
        self.prop_angles = []
        self.rel_velocities = []
        self.x_doppler = []
        self.y_doppler = []
        self.s_comp = []
    
    def get_reward(self, sat: tuple) -> float:
        _sat_orbit, _sat_idx = sat
        print("CHOOSE : ", _sat_orbit, _sat_idx)

        sats = self.orbits[1:]
        _target_sat = sats[_sat_orbit][_sat_idx]

        _dist = get_distance(self.orbits[0][self.gu_idx], _target_sat)
        _dist = _dist * 1e5
        _v = math.sqrt(self.rel_velocities[_sat_orbit][_sat_idx][0]**2 + self.rel_velocities[_sat_orbit][_sat_idx][1] ** 2 + self.rel_velocities[_sat_orbit][_sat_idx][2] **2)
        _snr = get_snr_fspl_doppler(distance=_dist, 
                                    velocity=_v, 
                                    angle=self.prop_angles[_sat_orbit][_sat_idx])
        _cp = shannon_hartley(_snr)
        
        handover= 1
        cur_sat = self.orbits[0][self.gu_idx].get_connected_sat()
        prev_sat = self.orbits[0][self.gu_idx].get_prev_connected_sat()

        if(cur_sat[0] == prev_sat[0] and cur_sat[1] == prev_sat[1]):
            handover += 1
        alpha = 0.000000001
        return (alpha*_cp) / handover

    def step(self, action):
        try:
            _sat_orbit, _sat_idx = self.set_action(action)
        except:
            raise
        
        reward = 0 
        done = False
        info = {}

        gu = self.orbits[0][self.gu_idx]
        sats = self.orbits[1:]
        self.los_sats = get_line_of_sight_list(gu, sats)

        if(self.los_sats[_sat_orbit][_sat_idx] == 0):
            reward = -1
            done = True
            info = {"reason" : "NON LOS"}
            print(info)
        else:
            reward = self.get_reward(sat=(_sat_orbit, _sat_idx))
            print("reward : ", reward)
            self.rotate(100)

        return reward, done, info

    def set_action(self, action: int) -> list:
        # Target_satellite 정해줌
        _sat_orbit = action // self.satellite_num
        _sat_idx = action % self.satellite_num

        self.orbits[0][self.gu_idx].set_connected_sat((_sat_orbit, _sat_idx))

        return [_sat_orbit, _sat_idx]

    def get_state(self) -> list:
        gu = self.orbits[0][self.gu_idx]
        sats = self.orbits[1:]
        self.los_sats = get_line_of_sight_list(gu, sats)
        # print("los_sats : ", self.los_sats)

        self.prop_angles = get_propagation_angle_list(gu, sats, self.los_sats)
        # print("prop_angles : ", self.prop_angles)

        self.rel_velocities = get_relative_velocity_list(gu, sats, self.los_sats)
        # print("rel_velocities : ", self.rel_velocities)

        # get x axis frequency
        self.x_doppler= calc_doppler_shift_on_x_list(FREQUENCY, self.rel_velocities, self.prop_angles)
        # print("x_doppler : ", self.x_doppler)

        # get y axis frequency
        self.y_doppler= calc_doppler_shift_on_y_list(FREQUENCY, self.rel_velocities, self.prop_angles)
        # print("y_doppler : ", self.y_doppler)

        # get computing resources
        self.s_comp = get_computing_resources(self.los_sats, sats)

        _flatten = np.array([], dtype=np.float32)

        _x_doppler = np.array(self.x_doppler, dtype=np.float32).flatten()
        _flatten = np.concatenate([_flatten, _x_doppler])

        _y_doppler = np.array(self.y_doppler, dtype=np.float32).flatten()
        _flatten = np.concatenate([_flatten, _y_doppler])

        _s_comp = np.array(self.s_comp, dtype=np.float32).flatten()
        _flatten = np.concatenate([_flatten, _s_comp])

        return _flatten