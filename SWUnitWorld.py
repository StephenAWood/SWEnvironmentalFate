# SWUnitWorld.py
# Written by Stephen Wood
# A simple 3-phase Unit World covering 100,000 square kilometers.
# Phases: air, water, soil/sediment (described by octanol)

import SWEnvironmentalFateLevel1

name = 'Chloroform'
log_Kow = 2.5
log_Koa = 5.19
log_Kaw = log_Kow - log_Koa # log Kow - log Koa
log_Koc = 0.35 * log_Kow

### Environmental Properties - to be defined by the user

area = 1.0e8 # (in m^2)
atmosphere_height = 1.0e3 # (in m)
soil_depth = 0.1 # (in m)
soil_land_coverage = 0.99 # (fraction)
water_coverage = 1.00 - soil_land_coverage # (again, fraction.)
water_depth = 20 # (in m)
sediment_depth = 0.01 #(in m)
soil_fraction_oc = 0.02 # (fraction of organic carbon in soil)
sediment_fraction_oc = 0.04 # (fraction of organic carbon in soil)
density_organic_carbon = 2.4 # (in grams per cubic centimetre)
koc_fraction = 0.35

### Environmental volumes calculated from above parameters

V_air = area * atmosphere_height
V_water = area * water_coverage * water_depth
V_oc = (soil_land_coverage * soil_fraction_oc * soil_depth + water_coverage * sediment_depth * sediment_fraction_oc) * area * koc_fraction * density_organic_carbon

### Calculated Fugacity Capacities

Z_air = 1.0 / (8.314 * 298.15)
Z_water = Z_air * (10 ** log_Kaw) ** -1
Z_octanol = (10 ** log_Kow) * Z_water

V_array = [V_air, V_water, V_oc]
Z_array = [Z_air, Z_water, Z_octanol]
names = ['air', 'water', 'soil/sediment']

unit_world_calculation = SWEnvironmentalFateLevel1.SWEnvironmentalFateLevel1(V_array, Z_array, names)

# End of file