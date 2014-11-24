# SWEnvironmentalFate
This is a collection of various tools and models to do environmental fate calculations. Currently, there is just one model / tool. In the future, and time permitting, I hope to add some more useful environmental fate tools here.

By Stephen Wood. See the license file for details.

# Requirements
- Python 2.7 or later

# Documentation

## SWEnvironmentalFateLevel1

This class proceeds the framework for a basic level 1 environmental fate calculation. It works for a system with **any** number of phases.

### Equation

[Equation (pdf)](figures/level_1_equation.pdf)

### Inputs:
- Volume for each phase
- Fugacity capacity for each phase
- *(Optional)* Name of each phase

### Output:

An estimate for how much of the chemical resides in each phase (fractional amount).

## SWUnitWorld
The most basic environmental fate calculation that calculates distribution of a chemical in a basic unit world, involving 3 phases: air, water, soil/sediment.

### Inputs:

Chemical properties:

- Chemical name
- Henry's law constant (air-water partition coefficient)
- log K~ow (octanol-water partition coefficient)
- log K~oa (octanol-air partition coefficient)

Additionally, various environmental parameters, such as:

- Unit world area (m^2)
- Height of the atmosphere / air compartment (m)
- Soil depth (m)
- Fraction of area covered by soil
- Fraction of area covered by water
- Water depth (m)
- Sediment depth (m)
- Fraction of organic carbon in soil
- Fraction of organic carbon in sediment
- log K~oc SP-LFER (0.35 from Wania et al.)

### Outputs
An estimate for the fraction of chemical that resides in each of the previously mentioned phases.