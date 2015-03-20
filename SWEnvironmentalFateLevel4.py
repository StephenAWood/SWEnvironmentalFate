import math
from scipy.integrate import quad
from scipy.integrate import odeint
from scipy.interpolate import spline
import numpy as np
import matplotlib.pyplot as plt
# get_ipython().magic(u'matplotlib inline')


# System Definitions

# Chemical Properties
MW = 100.0 # g / mol
MW /= 1000 # Convert to kg / mol.

T = 298.15 # K
R = 8.314 # J / mol K
Z_air = 1 / R / T # mol / m^3 Pa

logKaw = -2.13 # Henry's Law Constant or Air-Water Equilibrium Partition Coefficient
Kaw = 10 ** logKaw # non-log

Z_water = Z_air / Kaw # mol / m^3 Pa

# Compartment Properties
area = 1.0e6 # 1,000,000 sq. meters or 1 sq. km

#water
water_depth = 30. # meters
water_volume = area * water_depth # m^3
#air
air_height = 1000.0 # meters
air_volume = area * air_height # m^3

# Time step, in hours.

dt = 24 # hours

# Chemical emission rate into the air

E_day = 1 # kg per day
E_hour = E_day / 24 # kg per hour.

# Mass Transfer Coefficients in m / h
MTC_air_water = 0.5
MTC_water_air = 1.00

# Degradation with OH
k_deg = 5.5e-13 # cm^3 / molecules s
k_deg = k_deg * 86400.0 # now in cm^3 / molecules day
OH = 1.0e-6 # molecules / cm^3


# In[3]:

# ODE

def f(y, t):
    f_air_i = y[0]
    f_water_i = y[1]
    
    ### AIR
    f_air = 0.0
    # Input
    f_air += gaussian(t, 182.5, 0.01) / MW
    f_air += MTC_water_air * area * Z_water * f_water_i
    # Loss
    f_air -= MTC_air_water * area * Z_air * f_air_i
    f_air -= air_volume * Z_air * k_deg * OH * f_air_i
    # Divide by VZx
    f_air /= air_volume * Z_air
    
    ### WATER
    f_water = 0.0
    # Input
    f_water += MTC_air_water * area * Z_air * f_air_i
    # Loss
    f_water -= MTC_water_air * area * Z_water * f_water_i
    # Divide by VZ
    f_water /= water_volume * Z_water
    
    # ret
    return [f_air, f_water]
    
    


def gaussian(x, mu, sig):
    return np.exp(-np.power(x - mu, 2.) / 2 * np.power(sig, 2.))



# In[5]:

f_air_0 = 0.0 # initial contamination in air
f_water_0 = 0.0 # initial contamination in water
y0 = [f_air_0, f_water_0]
t = np.linspace(0, 365, 366)

E = gaussian(t, max(t)/2, 0.01)

soln = odeint(f, y0, t)

f_air = soln[:, 0]
f_water = soln[:, 1]

C_air = f_air * Z_air
C_water = f_water * Z_water

M_air = C_air * air_volume * MW
M_water = C_water * water_volume * MW


plt.plot(t, M_water, '-', color = 'deepskyblue', linewidth = 4)
plt.show()




