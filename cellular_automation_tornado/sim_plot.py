# A script to generate plots and/or animations for the cellular automata tornado

import numpy as np
import tables as tb
import math
import matplotlib.pyplot as plt
import time

PI = np.pi #Mathematical constant pi
DELTA_R = 20 #Change in radius across a parcel; in meters
DELTA_Z = 20 #Change in altitude across a parcel; in meters
DELTA_THETA = 2*PI/10 #Change in rotation across a parcel; in radians
DELTA_T = .1 #Change in time across a time step; in seconds
MAX_R = 1000 #Maximum radius in this model; in meters
MAX_Z = 1000 #Maximum altitude in this model; in meters
MAX_THETA = 2*PI #Maximum rotation in this model (det'd by geometry); in radians
MAX_T = 10 #Running time for the model; in seconds
NUM_R = int(MAX_R/DELTA_R) #Number of parcels in the radius direction
NUM_Z = int(MAX_Z/DELTA_Z) #Number of parcels in the altitude direction
NUM_THETA = int(MAX_THETA/DELTA_THETA) #Number of parcels in the theta direction
NUM_T = int(MAX_T/DELTA_T) #Number of timesteps

# get simulation data from table file
simulation_file = tb.open_file("simulation_data.h5", mode="r", title="Tornado Simulation Data")
table = simulation_file.root.parcel_data.readout


absolute_velocity = np.ndarray(shape=(NUM_R, NUM_Z, NUM_THETA, NUM_T))
radius = height = theta = time_index = -1 # time is already in the namespace, so using time_index
last_r = last_z = last_theta = last_t = -1
for row in table.iterrows():
    # this is a sort of hacked together method of moving from r/z/theta/t values
    #   to indices.  It seems to work but it's far from glamorous.
    if last_r != row['r']:
        last_r = row['r']
        radius += 1
        if radius >= NUM_R:
            radius = 0
    if last_z != row['z']:
        last_z = row['z']
        height += 1
        if height >= NUM_Z:
            height = 0
    if last_theta != row['theta']:
        last_theta = row['theta']
        theta += 1
        if theta >= NUM_THETA:
            theta = 0
    if last_t != row['t']:
        last_t = row['t']
        time_index += 1
        if time_index >= NUM_T:
            time_index = 0

    print(row['rVel']) #DEBUG
    # TODO: the velocity values don't exist for a lot of these. Find Out Why
    absolute_velocity[radius, height, theta, time_index] = math.sqrt(row['rVel']**2 + row['zVel']**2 + row['thetaVel']**2)

#Plotting
# plt.show()
# for t in range(NUM_T):
#    plt.pcolor(absolute_velocity[:,:,0,t])
#    plt.draw()
#    time.sleep(DELTA_T)

#plotting the change in absolute velocity for a single parcel
timeList = [i*DELTA_T for i in range(NUM_T)]
veloList = [i for i in absolute_velocity[0,0,0,:]]
print(timeList)
print(veloList)
plt.plot(timeList, veloList)
plt.show()

simulation_file.close()