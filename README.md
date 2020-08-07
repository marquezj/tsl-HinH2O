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

| Library | Temperaure [K] | File |
| --- | :-: | ---|
| hh2o.00t | 293.60 | lib_294.ace |
| hh2o.01t | 273.15 | lib_273.ace |
| hh2o.02t | 275.00 | lib_275.ace |
| hh2o.03t | 280.00 | lib_280.ace |
| hh2o.04t | 283.60 | lib_284.ace |
| hh2o.05t | 285.00 | lib_285.ace |
| hh2o.06t | 290.00 | lib_290.ace |
| hh2o.07t | 295.00 | lib_295.ace |
| hh2o.08t | 300.00 | lib_300.ace |
| hh2o.09t | 305.00 | lib_305.ace |
| hh2o.10t | 310.00 | lib_310.ace |
| hh2o.11t | 315.00 | lib_315.ace |
| hh2o.12t | 320.00 | lib_320.ace |
| hh2o.13t | 323.60 | lib_324.ace |
| hh2o.14t | 325.00 | lib_325.ace |
| hh2o.15t | 330.00 | lib_330.ace |
| hh2o.16t | 335.00 | lib_335.ace |
| hh2o.17t | 340.00 | lib_340.ace |
| hh2o.18t | 345.00 | lib_345.ace |
| hh2o.19t | 350.00 | lib_350.ace |
| hh2o.20t | 355.00 | lib_355.ace |
| hh2o.21t | 360.00 | lib_360.ace |
| hh2o.22t | 365.00 | lib_365.ace |
| hh2o.23t | 370.00 | lib_370.ace |
| hh2o.24t | 373.60 | lib_374.ace |
| hh2o.25t | 375.00 | lib_375.ace |
| hh2o.26t | 380.00 | lib_380.ace |
| hh2o.27t | 385.00 | lib_385.ace |
| hh2o.28t | 390.00 | lib_390.ace |
| hh2o.29t | 395.00 | lib_395.ace |
| hh2o.30t | 400.00 | lib_400.ace |
| hh2o.31t | 405.00 | lib_405.ace |
| hh2o.32t | 410.00 | lib_410.ace |
| hh2o.33t | 415.00 | lib_415.ace |
| hh2o.34t | 420.00 | lib_420.ace |
| hh2o.35t | 423.60 | lib_424.ace |
| hh2o.36t | 425.00 | lib_425.ace |
| hh2o.37t | 430.00 | lib_430.ace |
| hh2o.38t | 435.00 | lib_435.ace |
| hh2o.39t | 440.00 | lib_440.ace |
| hh2o.40t | 445.00 | lib_445.ace |
| hh2o.41t | 450.00 | lib_450.ace |
| hh2o.42t | 455.00 | lib_455.ace |
| hh2o.43t | 460.00 | lib_460.ace |
| hh2o.44t | 465.00 | lib_465.ace |
| hh2o.45t | 470.00 | lib_470.ace |
| hh2o.46t | 473.60 | lib_474.ace |
| hh2o.47t | 475.00 | lib_475.ace |
| hh2o.48t | 480.00 | lib_480.ace |
| hh2o.49t | 485.00 | lib_485.ace |
| hh2o.50t | 490.00 | lib_490.ace |
| hh2o.51t | 495.00 | lib_495.ace |
| hh2o.52t | 500.00 | lib_500.ace |
| hh2o.53t | 505.00 | lib_505.ace |
| hh2o.54t | 510.00 | lib_510.ace |
| hh2o.55t | 515.00 | lib_515.ace |
| hh2o.56t | 520.00 | lib_520.ace |
| hh2o.57t | 523.60 | lib_524.ace |
| hh2o.58t | 525.00 | lib_525.ace |
| hh2o.59t | 530.00 | lib_530.ace |
| hh2o.60t | 535.00 | lib_535.ace |
| hh2o.61t | 540.00 | lib_540.ace |
| hh2o.62t | 545.00 | lib_545.ace |
| hh2o.63t | 550.00 | lib_550.ace |
| hh2o.64t | 555.00 | lib_555.ace |
| hh2o.65t | 560.00 | lib_560.ace |
| hh2o.66t | 565.00 | lib_565.ace |
| hh2o.67t | 570.00 | lib_570.ace |
| hh2o.68t | 573.60 | lib_574.ace |
| hh2o.69t | 575.00 | lib_575.ace |
| hh2o.70t | 580.00 | lib_580.ace |
| hh2o.71t | 585.00 | lib_585.ace |
| hh2o.72t | 590.00 | lib_590.ace |
| hh2o.73t | 595.00 | lib_595.ace |
| hh2o.74t | 600.00 | lib_600.ace |
| hh2o.75t | 605.00 | lib_605.ace |
| hh2o.76t | 610.00 | lib_610.ace |
| hh2o.77t | 615.00 | lib_615.ace |
| hh2o.78t | 620.00 | lib_620.ace |
| hh2o.79t | 623.60 | lib_624.ace |
| hh2o.80t | 625.00 | lib_625.ace |
| hh2o.81t | 630.00 | lib_630.ace |
| hh2o.82t | 635.00 | lib_635.ace |
| hh2o.83t | 640.00 | lib_640.ace |
| hh2o.84t | 645.00 | lib_645.ace |
| hh2o.85t | 647.10 | lib_647.ace |
| hh2o.86t | 650.00 | lib_650.ace |
| hh2o.87t | 700.00 | lib_700.ace |
| hh2o.88t | 750.00 | lib_750.ace |
| hh2o.89t | 800.00 | lib_800.ace |
| hh2o.90t | 850.00 | lib_850.ace |
| hh2o.91t | 900.00 | lib_900.ace |
| hh2o.92t | 950.00 | lib_950.ace |
| hh2o.93t | 1000.00 | lib_1000.ace |

---

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
