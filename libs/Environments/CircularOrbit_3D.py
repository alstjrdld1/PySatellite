from abc import abstractmethod
from libs.Environments.OrbitBaseline import *

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

from libs.Constants import *

class CircularOrbit_3D(OrbitBaseLine):
    def __init__(self,
                 satellite_num: int = 8,
                 orbit_alts: list =[400, 1000]):
        
        super.__init__(satellite_num = satellite_num,
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
        pass 

    def rotate(self, t) -> None:
        pass

    def plot(self) -> None:

        # Constants
        h = 500000      # height of satellite above Earth, m
        v = np.sqrt(G*M/(R+h))  # velocity of satellite, m/s

        # Initial conditions
        x0 = R + h    # initial x position, m
        y0 = 0        # initial y position, m
        z0 = 0        # initial z position, m
        vx0 = 0       # initial x velocity, m/s
        vy0 = v       # initial y velocity, m/s
        vz0 = 0       # initial z velocity, m/s

        # Time step and simulation time
        dt = 1         # time step, s
        tmax = 2 * np.pi * (R + h) / v # Satellite trajectory 
        # tmax = 5200    # simulation time, s

        # Create arrays to store position and velocity
        t = np.arange(0, tmax+dt, dt)
        x = np.zeros(len(t))
        y = np.zeros(len(t))
        z = np.zeros(len(t))
        vx = np.zeros(len(t))
        vy = np.zeros(len(t))
        vz = np.zeros(len(t))

        # Set initial position and velocity
        x[0] = x0
        y[0] = y0
        z[0] = z0
        vx[0] = vx0
        vy[0] = vy0
        vz[0] = vz0

        # Perform simulation
        for i in range(1, len(t)):
            # Calculate distance from Earth's center
            r = np.sqrt(x[i-1]**2 + y[i-1]**2 + z[i-1]**2)
            
            # Calculate gravitational force
            Fg = -G*M/(r**2)
            
            # Calculate x, y, and z components of gravitational force
            Fgx = Fg*x[i-1]/r
            Fgy = Fg*y[i-1]/r
            Fgz = Fg*z[i-1]/r
            
            # Calculate net force
            Fx = Fgx
            Fy = Fgy
            Fz = Fgz
            
            # Update velocity
            vx[i] = vx[i-1] + Fx*dt
            vy[i] = vy[i-1] + Fy*dt
            vz[i] = vz[i-1] + Fz*dt
            
            # Update position
            x[i] = x[i-1] + vx[i]*dt
            y[i] = y[i-1] + vy[i]*dt
            z[i] = z[i-1] + vz[i]*dt

        # 그래프 그리기
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        ax.plot(x, y, z)
        ax.plot_surface(EARTH_3D_X, EARTH_3D_Y, EARTH_3D_Z, color='b', alpha=1.0)  # 투명도를 조절하려면 alpha 값을 변경하세요.

        # 축 레이블 설정
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')

        # 그래프 보여주기
        plt.show()