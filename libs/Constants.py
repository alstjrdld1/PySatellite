import os 

try:
    import numpy as np
except:
    os.system("pip install numpy")

DATA_AMOUNT = 0
BAND_WIDTH = 0
FREQUENCY = 0
MAXIMUM_TIME = 0.1 # s
EARTH_CENTER_LOC = (0,0)

PI = np.pi
G = 6.6743e-11  # gravitational constant, m^3/(kg s^2)
M = 5.972e24    # mass of Earth, kg
R = 6371000     # radius of Earth, m
C = 300000000   # m/s