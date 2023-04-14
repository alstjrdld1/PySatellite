import os 

try:
    import numpy as np
    
except:
    os.system("pip install numpy")
try:
    import torch
except:
    os.system("pip install torch")

DATA_AMOUNT = 0
BAND_WIDTH = 50e9 # Hz GHz = 1e9
FREQUENCY = 340e9 # Hz GHz = 1e9
MAXIMUM_TIME = 0.1 # s
EARTH_CENTER_LOC = (0,0,0)

TRANSMISSION_POWER = 30 # dB

#### ABOUT ANTENNA
ANTENNA_DIAMETER                = 1.2 # m
ANTENNA_EFFICIENCY              = 0.9
RECEIVER_ANTENNA_EFFICIENCY     = 0.9
TRANSMITTER_ANTENNA_EFFICIENCY  = 0.9

TRANSMITTER_ANTENNA_GAIN        = 0.9
RECEIVER_ANTENNA_GAIN           = 0.9

#### NOISE CONSTANTS
ADDITIONAL_NOISE_RECEIVER = 0.1

#### SPACE CONDITION 
TEMPERATURE = 300            # K

#### SCIENTIFIC CONSTANTS
PI = np.pi
G = 6.6743e-11               # gravitational constant, m^3/(kg s^2)
M = 5.972e24                 # mass of Earth, kg
R = 6371000                  # radius of Earth, m
C = 3e9                      # m/s
BOLTZMAN_CONSTANT = 1.38e-23 # J/K

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