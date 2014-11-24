# This program is designed to do a simple level I environmental fate calculation
# Equilibrium partitioning is assumed between all phases
# No transport, Input = Output (steady state)
# 3 phase system (Air, organic carbon (from soil + sediment), and water)
# (c) 2014 Stephen Wood, see accompanying license file.

# Other assumptions:
# T = 25 degrees Celcius. All partition coefficients are valid for that temperature.

class SWEnvironmentalFateLevel1(object):
	"""docstring for SWEnvironmentalFateLevel1
	Accepts an array for both arguments.

	Volumes: volume of phases


	"""

	def __init__(self, volumes, fugacity_capacities, names = None):
		super(SWEnvironmentalFateLevel1, self).__init__()
		if len(volumes) != len(fugacity_capacities):
			raise Exception('error, number of volumes must be equal to number of fugacity capacities')

		self.volumes = volumes
		self.fugacity_capacities = fugacity_capacities
		self.names = names
		if not self.names: self.names = [i + 1 for i in range(0, len(volumes))]
		self.results = self.calculate()
		self.print_results()

	def calculate(self):
		
		# denominator_sum = 0.0
		# for Z, V in zip(self.fugacity_capacities, self.volumes):
		# 	denominator_sum += Z * V

		denominator_sum = sum([Z * V for Z, V in zip(self.fugacity_capacities, self.volumes)])

		ret = {}
		for name, Z, V in zip(self.names, self.fugacity_capacities, self.volumes):
			phi = Z * V / denominator_sum # Calculate fraction in specific phase
			ret.update({name : phi})
		return ret

	def print_results(self):
		for name, phi in self.results.items():
			print 'The fraction in %s is %.3f' % (str(name), phi)



###




###

		

### Chemical Properties
name = 'Chloroform'
log_Kow = 5
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

### Fractions in environmental media

fraction_air = (1.0 + (10 ** log_Kaw) ** -1 * V_water / V_air + (10 ** log_Koa) * V_oc / V_air) ** -1
fraction_oc = (1.0 + (10 ** log_Koa) ** -1 * V_air / V_oc + (10 ** log_Kow) ** -1 * V_water / V_oc) ** -1
fraction_water = (1.0 + (10 ** log_Kaw) * V_air / V_water + (10 ** log_Kow) * V_oc / V_water) ** -1

print 'The fraction in air is %.3f' % fraction_air
print 'The fraction in organic carbon is %.3f' % fraction_oc
print 'The fraction in water is %.3f' % fraction_water

# Sanity Check
check = abs((fraction_air + fraction_oc + fraction_water) - 1.0) < 1.0e-6

if not check: raise Exception('Error, fraction in all 3 phases does not add up to 1')



##### Testing Other Part

Z_air = 1.0 / (8.314 * 298.15)
Z_water = Z_air * (10 ** log_Kaw) ** -1
Z_octanol = (10 ** log_Kow) * Z_water

calc = SWEnvironmentalFateLevel1([V_air, V_water, V_oc], [Z_air, Z_water, Z_octanol], names = ['air', 'water', 'octanol'])



