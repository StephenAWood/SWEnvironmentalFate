# This program is designed to do a simple level I environmental fate calculation
# Equilibrium partitioning is assumed between all phases
# No transport, Input = Output (steady state)
# Supports any number of phases
# (c) 2014 Stephen Wood, see accompanying license file.

# Other assumptions:
# T = 25 degrees Celcius. All partition coefficients are valid for that temperature.

class SWEnvironmentalFateLevel1(object):
	"""docstring for SWEnvironmentalFateLevel1
	Accepts an array for both arguments.

	Volumes: volume of phases
	fugacity_capacities: fugacity capacity of the previously mentioned phases
	names: names of the phases.
	"""

	def __init__(self, volumes, fugacity_capacities, names = None):
		super(SWEnvironmentalFateLevel1, self).__init__()
		if len(volumes) != len(fugacity_capacities):
			raise Exception('error, number of volumes must be equal to number of fugacity capacities')
		number_of_phases = len(volumes)
		self.volumes = volumes
		self.fugacity_capacities = fugacity_capacities
		self.names = names
		if not self.names: self.names = [i + 1 for i in range(0, number_of_phases)]
		self.results = self.calculate()
		self.sanity_check()
		self.print_results()

	def sanity_check(self):
		check = abs(1.000000000000000000 - sum(self.results.values())) <= 1.0e-6
		if not check: raise Exception('Error, the total fraction of all the phases does not add up to one!')

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

# End of file
