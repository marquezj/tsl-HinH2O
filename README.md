# tsl-HinH2O

This repository contains an update of the evaluated thermal scattering library
for hydrogen bound light water from [ENDF/B-VIII.0](https://www.sciencedirect.com/science/article/pii/S0090375218300206), which was based on the
[CAB Model for water](https://doi.org/10.1016/j.anucene.2013.11.014).

The basic component is the Python script tsl-HinH2O.py, which interpolates the parameters
and produces the input for LEAPR:

`./tsl-HinH2O.py -txtout tsl-HinH2O.leapr`

generates the LEAPR for the complete evaluation. This evaluation contains all the temperatures
in ENDF/B-VIII.0 plus a fine grid with a 5K interval. The complete evaluation is produced
by running this input file with [NJOY 2016.57](https://github.com/njoy/NJOY2016).

If additional temperatures are required, they can be produced with the script. As an example:

`./tsl-HinH2O.py -t 299.0 tsl-HinH2O_299.leapr`

generates the input for 299.0 K.

Two auxiliary files are also included in the repository:

- proc.njoy is a NJOY input file to process the thermal scattering library with 0.1% tolerance
  and generate an ACE file with 32 angular bins and 200 outgoing energy bins.

- plot.py is a Python script that used [OpenMC](https://docs.openmc.org/en/stable/pythonapi/data.html) to plot the total cross
  section from a thermal ACE library.

These scripts are used to produce ACE files (stored in the ace directory) and plots (stored in the plots directory) for each temperature.


The update was prepared by:

- J.I. Marquez Damian<br/>
Spallation Physics Group<br/>
European Spallation Source - Sweden (ESS)

- J.R. Granada<br/>
Nuclear Data Group - Neutron Physics Department<br/>
Centro Atomico Bariloche - Argentina (CAB)

- D. Roubtsov<br/>
Canadian Nuclear Laboratories (CNL)<br/>
Chalk River, Canada 
