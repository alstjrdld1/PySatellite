from libs.Environments.Circular_GU_Sat import *

env = Circular_GU_Sat(
    satellite_num=1,
    orbit_alts=[1000],
    ground_user_num=1
)

while True:
    env.plot()
    env.rotate(24*60*60)