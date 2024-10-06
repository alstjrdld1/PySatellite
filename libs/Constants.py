import os 
os.environ['KMP_DUPLICATE_LIB_OK']='True'

try:
    import numpy as np
    
except:
    os.system("pip install numpy")
try:
    import torch
except:
    os.system("pip install torch")

DATA_AMOUNT = 0
# BAND_WIDTH = 50e9 # Hz GHz = 1e9
BAND_WIDTH = 1e9 # Hz GHz = 1e9
FREQUENCY = 3e9 # Hz GHz = 1e9
MAXIMUM_TIME = 5 # s
EARTH_CENTER_LOC = (0,0,0)

TRANSMISSION_POWER = 1 # W

#### ABOUT ANTENNA
ANTENNA_DIAMETER                = 1.2 # m
ANTENNA_EFFICIENCY              = 0.9
RECEIVER_ANTENNA_EFFICIENCY     = 0.9
TRANSMITTER_ANTENNA_EFFICIENCY  = 0.9

TRANSMITTER_ANTENNA_GAIN        = 2 # dBi
RECEIVER_ANTENNA_GAIN           = 2 # dBi

#### NOISE CONSTANTS
ADDITIONAL_NOISE_RECEIVER       = 5 # dB

#### SPACE CONDITION 
TEMPERATURE = 288            # K

#### SCIENTIFIC CONSTANTS
PI = np.pi
G = 6.6743e-11               # gravitational constant, m^3/(kg s^2)
M = 5.972e24                 # mass of Earth, kg
# R = 6371000                  # radius of Earth, m
R = 6371                  # radius of Earth, km
C = 3e9                      # m/s
BOLTZMAN_CONSTANT = 1.38e-23 # J/K

EARTH_ROTATE_PERIOD = 24 * 60 * 60 # second
EARTH_ANGULAR_VELOCITY = 2 * PI / EARTH_ROTATE_PERIOD # rad/s
EARTH_SURFACE_ROTATE_SPEED = 1670 / (60 * 60) # km/s

##### 3D Simulation 
# 좌표를 생성하기 위한 각도 범위 설정
E_PHI = np.linspace(0, PI, 100)
E_THETA = np.linspace(0, 2 * PI, 100)

# 각도를 좌표로 변환
E_PHI, E_THETA = np.meshgrid(E_PHI, E_THETA)

# 구의 좌표를 계산
EARTH_3D_X = R * np.sin(E_PHI) * np.cos(E_THETA)
EARTH_3D_Y = R * np.sin(E_PHI) * np.sin(E_THETA)
EARTH_3D_Z = R * np.cos(E_PHI)

##### FOR DRL 
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")

NUM_STATES = 5
HIDDEN_SIZE = 256
NUM_ACTIONS = 5

BATCH_SIZE              = 128
LR                      = 0.01
GAMMA                   = 0.9
Q_NETWORK_ITERATION     = 100

RUN_STEP                = 50000
TEST_STEP               = 5000
EXPLORE_STEP            = RUN_STEP * 0.8

########## FOR DQN
EPSILON_EVAL = 0.05
EPSILON_INIT = 1.0 
EPSILON_MIN = 0.1

EPISILO = 0.9
DISCOUNT_FACTOR = 0.9
MEMORY_CAPACITY = 2000

############# FOR UTILS

SAVE_PATH = "runs/satellite"