#!/usr/bin/env python3

'''
Creates a LEAPR input for hydrogen bound in light
water based on the CAB Model.
'''

import sys
import argparse
import numpy as np

fit_params = np.array([[-1.16341924e-05,  5.72431970e-08, -4.99523507e-11, 5.56527202e-03],
                       [-3.39071658e-05,  1.47463653e-07, -1.40959279e-10, 1.26163985e-02],
                       [-7.63785717e-05,  2.02767139e-07, -6.47794880e-11, 2.90169482e-02],
                       [-3.33982404e-05, -4.93941967e-07,  1.15324681e-09, 6.26559361e-02],
                       [ 8.21470459e-05, -1.18072642e-06,  2.16039005e-09, 8.85464107e-02],
                       [ 5.84551624e-05, -5.86676411e-07,  5.85894659e-10, 1.46032192e-01],
                       [-2.95519307e-06,  1.74864109e-11,  2.91516560e-11, 2.54078029e-03],
                       [-1.00544627e-05,  2.53106863e-08,  6.98665630e-12, 5.17496669e-03],
                       [ 7.11175567e-06, -8.01286354e-08,  1.80506419e-10, 8.84920348e-03],
                       [ 7.97405592e-05, -4.30402284e-07,  5.91820571e-10, 1.32074015e-02],
                       [-7.27762470e-06,  1.06070857e-07, -2.29561496e-10, 2.12308848e-02],
                       [-4.66957498e-05,  1.39558013e-06, -2.86846017e-09, 7.49086643e-03],
                       [-6.25741458e-05,  2.29236817e-07, -1.71524226e-10, 1.08306039e-02],
                       [ 2.25579241e-06,  4.76374532e-08,  5.28370625e-11, 1.06868732e-02],
                       [-3.15013830e-05, -5.38504184e-07,  2.31094668e-09, 4.40074120e-02],
                       [ 1.45191606e-03, -1.03983345e-05,  1.68807552e-08, 1.92865122e-01],
                       [-1.28973896e-03,  8.96343823e-06, -1.60755108e-08, 2.59626344e-01],
                       [-9.19195432e-05,  2.35458200e-06, -4.73627039e-09, 6.69828635e-03],
                       [ 5.72965829e-05, -3.29588700e-08,  4.85753614e-11, 7.91800000e-03],
                       [ 8.30959927e-02, -1.07761895e-04,  2.66509168e-07, 3.96900000e+00]])

def gaussian(E, E0, sigma, weight):
    return weight/np.sqrt(2.0*np.pi*sigma**2)*np.exp(-(E-E0)**2/(2.0*sigma**2))

def cubic(x, p=[1.0, 1.0, 1.0, 1.0], x0=293.6):
  return p[0]*(x-x0) + p[1]*(x-x0)**2 + p[2]*(x-x0)**3 + p[3]

def n_columns(data, fmt='{:.4e} ', ncolumns=5):
    s = ""
    i = 0

    for d in data:
      s += fmt.format(d)
      i = i + 1 
      if (i % ncolumns == 0):
        s += '\n'

    if s[-1] != '\n':
        s += '\n'
    return s

def middle_text(temp, fit_params):
    max_temp = 650.0
    min_temp = 273.15
    E = np.linspace(0,0.149270,119)
    temp2 = min(max_temp, temp)
    temp2 = max(min_temp, temp2)
    rho = np.zeros(len(E))
    for i in range(6):
      rho = rho + gaussian(E, cubic(temp2, fit_params[i,:]),
                              cubic(temp2, fit_params[i+6,:]),
                              cubic(temp2, fit_params[i+12,:]))
    rho[0] = 0.0
    rho[1] = (E[1]/E[2])**2.0*rho[2]
    s = "{:.2f}".format(temp)+" /\n"+
           "{:.4e}".format(E[1])+" "+"{:d}".format(len(E))+" /\n"+
           n_columns(rho) +
           "{:.4e}".format(cubic(temp2, fit_params[18,:]))+" "+
           "{:.4e}".format(cubic(temp2, fit_params[19,:]))+" "+
           "{:.4e}".format(0.530-cubic(temp2, fit_params[18,:]))+" /\n"
    return s

top_leapr_text = """leapr
24  /NOUT
H in H2O, CAB Model from molecular dynamics calculations / TITLE
{:d} 2 200  / NTEMPR IPRINT IPHON
1 1001 0 0  / MAT ZA ISABT ILOG
0.9991673 20.43608 2 0 0 0  / AWR SPR NPR IEL NCOLD NSK
1 1 15.85751 3.7939 1  / NSS B7 AWS SPS MSS
222 317 1 / NALPHA NBETA LAT
1.0023e-05 1.3363e-05 1.7818e-05 2.3757e-05 3.1676e-05
4.2235e-05 5.6314e-05 7.5085e-05 1.0011e-04 1.3348e-04
1.7798e-04 2.3730e-04 3.1641e-04 4.2188e-04 5.6250e-04
7.5000e-04 1.0000e-03 1.5000e-03 2.5000e-03 3.5000e-03
5.0000e-03 7.0000e-03 1.0000e-02 1.5000e-02 2.5000e-02
3.5000e-02 5.0000e-02 7.0000e-02 1.0000e-01 1.2500e-01
1.5000e-01 2.0000e-01 2.5000e-01 3.0000e-01 3.2500e-01
3.5000e-01 3.7500e-01 4.0000e-01 4.2500e-01 4.5000e-01
4.7500e-01 5.0000e-01 5.2500e-01 5.5000e-01 5.8000e-01
6.1000e-01 6.5000e-01 6.9000e-01 7.3000e-01 7.8000e-01
8.3000e-01 8.8000e-01 9.4000e-01 1.0000e+00 1.0800e+00
1.1600e+00 1.2400e+00 1.3300e+00 1.4300e+00 1.5400e+00
1.6600e+00 1.7900e+00 1.9400e+00 2.0900e+00 2.2600e+00
2.4800e+00 2.7127e+00 2.8900e+00 3.1100e+00 3.3800e+00
3.6700e+00 3.9800e+00 4.3200e+00 4.6500e+00 5.0000e+00
5.4255e+00 6.0000e+00 6.5600e+00 7.1300e+00 7.6000e+00
8.1026e+00 8.8000e+00 9.5000e+00 1.0200e+01 1.0815e+01
1.1700e+01 1.2600e+01 1.3528e+01 1.4400e+01 1.5300e+01
1.6205e+01 1.7233e+01 1.8200e+01 1.8920e+01 2.0300e+01
2.1630e+01 2.2900e+01 2.4308e+01 2.5600e+01 2.7020e+01
2.8400e+01 2.9730e+01 3.1000e+01 3.2410e+01 3.3440e+01
3.4466e+01 3.6150e+01 3.7180e+01 3.8800e+01 4.0513e+01
4.1540e+01 4.2570e+01 4.4200e+01 4.6000e+01 4.7000e+01
4.8615e+01 4.9600e+01 5.1200e+01 5.2500e+01 5.4410e+01
5.5200e+01 5.6720e+01 5.8400e+01 5.9800e+01 6.1200e+01
6.2510e+01 6.3800e+01 6.5230e+01 6.6500e+01 6.7900e+01
6.8930e+01 7.0610e+01 7.1640e+01 7.2920e+01 7.5900e+01
8.0000e+01 8.4000e+01 8.9000e+01 9.4000e+01 1.0000e+02
1.0500e+02 1.1300e+02 1.2063e+02 1.2600e+02 1.3200e+02
1.4000e+02 1.4700e+02 1.5400e+02 1.6200e+02 1.7000e+02
1.7700e+02 1.8400e+02 1.9100e+02 1.9900e+02 2.0800e+02
2.1800e+02 2.2700e+02 2.3700e+02 2.4600e+02 2.5500e+02
2.6500e+02 2.7572e+02 2.8400e+02 2.9358e+02 3.0200e+02
3.1100e+02 3.2000e+02 3.2900e+02 3.3800e+02 3.4700e+02
3.5600e+02 3.6500e+02 3.7400e+02 3.8300e+02 3.9200e+02
4.0100e+02 4.1000e+02 4.1900e+02 4.2800e+02 4.3700e+02
4.4600e+02 4.5500e+02 4.6400e+02 4.7300e+02 4.8200e+02
4.9100e+02 5.0000e+02 5.0900e+02 5.1800e+02 5.2700e+02
5.3600e+02 5.4500e+02 5.5400e+02 5.6300e+02 5.7200e+02
5.8100e+02 5.9000e+02 5.9700e+02 6.0400e+02 6.1100e+02
6.1800e+02 6.2500e+02 6.3290e+02 6.6454e+02 6.9777e+02
7.3266e+02 7.6929e+02 8.0776e+02 8.4815e+02 8.9055e+02
9.3508e+02 9.8184e+02 1.0309e+03 1.0825e+03 1.1366e+03
1.1934e+03 1.2531e+03 1.3158e+03 1.3815e+03 1.4506e+03
1.5231e+03 1.5810e+03  /   end of alpha grid
0.0000e+00 5.0170e-06 6.6893e-06 8.9190e-06 1.1892e-05
1.5856e-05 2.1141e-05 2.8189e-05 3.7585e-05 5.0113e-05
6.6817e-05 8.9090e-05 1.1879e-04 1.5838e-04 2.1118e-04
2.8157e-04 3.7542e-04 5.0056e-04 6.6742e-04 8.8989e-04
1.1865e-03 1.5820e-03 2.1094e-03 2.8125e-03 3.7500e-03
5.0000e-03 1.0000e-02 1.5000e-02 2.0000e-02 2.5000e-02
3.0000e-02 4.0000e-02 5.0000e-02 6.0000e-02 7.0000e-02
8.0000e-02 1.0000e-01 1.2500e-01 1.5000e-01 1.7500e-01
2.0000e-01 2.2500e-01 2.5000e-01 3.0000e-01 3.5000e-01
4.0000e-01 4.5000e-01 5.0000e-01 5.5000e-01 6.0000e-01
6.5000e-01 7.0000e-01 7.5000e-01 8.0000e-01 8.5000e-01
9.0000e-01 9.5000e-01 1.0000e+00 1.0500e+00 1.1000e+00
1.1500e+00 1.2000e+00 1.2500e+00 1.3000e+00 1.3500e+00
1.4000e+00 1.4500e+00 1.5000e+00 1.5500e+00 1.6000e+00
1.6500e+00 1.7000e+00 1.7500e+00 1.8000e+00 1.8500e+00
1.9000e+00 1.9500e+00 2.0000e+00 2.0500e+00 2.1000e+00
2.1500e+00 2.2000e+00 2.2500e+00 2.3000e+00 2.3500e+00
2.4000e+00 2.4500e+00 2.5000e+00 2.5500e+00 2.6000e+00
2.6500e+00 2.7127e+00 2.7700e+00 2.8300e+00 2.9000e+00
2.9600e+00 3.0300e+00 3.1100e+00 3.1800e+00 3.2600e+00
3.3400e+00 3.4300e+00 3.5200e+00 3.6100e+00 3.7100e+00
3.8100e+00 3.9200e+00 4.0300e+00 4.1400e+00 4.2600e+00
4.3900e+00 4.5200e+00 4.6500e+00 4.8000e+00 4.9400e+00
5.1000e+00 5.2600e+00 5.4255e+00 5.6000e+00 5.7000e+00
5.9700e+00 6.1700e+00 6.3700e+00 6.5900e+00 6.8100e+00
7.0400e+00 7.2900e+00 7.5400e+00 7.8100e+00 7.9000e+00
8.0000e+00 8.1028e+00 8.2000e+00 8.2800e+00 8.3700e+00
8.6700e+00 8.9800e+00 9.3000e+00 9.6400e+00 1.0000e+01
1.0400e+01 1.0815e+01 1.1160e+01 1.1570e+01 1.2000e+01
1.2460e+01 1.2980e+01 1.3528e+01 1.3940e+01 1.4480e+01
1.5030e+01 1.5620e+01 1.6206e+01 1.6403e+01 1.6800e+01
1.7000e+01 1.7500e+01 1.8200e+01 1.8920e+01 1.9400e+01
1.9950e+01 2.0700e+01 2.1630e+01 2.2100e+01 2.2660e+01
2.3500e+01 2.4308e+01 2.4506e+01 2.4800e+01 2.6200e+01
2.7020e+01 2.7500e+01 2.8050e+01 2.8900e+01 2.9730e+01
3.0200e+01 3.0760e+01 3.1500e+01 3.2410e+01 3.2609e+01
3.2806e+01 3.2900e+01 3.4000e+01 3.5300e+01 3.6150e+01
3.6600e+01 3.7180e+01 3.7900e+01 3.8800e+01 3.9890e+01
4.0200e+01 4.0513e+01 4.0909e+01 4.1000e+01 4.1540e+01
4.2000e+01 4.3200e+01 4.4200e+01 4.5280e+01 4.6000e+01
4.7000e+01 4.7990e+01 4.8300e+01 4.8615e+01 4.9209e+01
4.9600e+01 5.0670e+01 5.1200e+01 5.2500e+01 5.3380e+01
5.3900e+01 5.4410e+01 5.5200e+01 5.6000e+01 5.6720e+01
5.7120e+01 5.8400e+01 5.9800e+01 6.1200e+01 6.2510e+01
6.3800e+01 6.5230e+01 6.6500e+01 6.7900e+01 6.8400e+01
6.8930e+01 6.9800e+01 7.0610e+01 7.1100e+01 7.1640e+01
7.2200e+01 7.2920e+01 7.3334e+01 7.4000e+01 7.4800e+01
7.5600e+01 7.6400e+01 7.7200e+01 7.8000e+01 7.8900e+01
7.9800e+01 8.0700e+01 8.1600e+01 8.2500e+01 8.3400e+01
8.4300e+01 8.5200e+01 8.6100e+01 8.7000e+01 8.8000e+01
8.9000e+01 9.0000e+01 9.1000e+01 9.2000e+01 9.3000e+01
9.4000e+01 9.5000e+01 9.6000e+01 9.7000e+01 9.8000e+01
9.9000e+01 1.0000e+02 1.0120e+02 1.0240e+02 1.0360e+02
1.0480e+02 1.0600e+02 1.0720e+02 1.0840e+02 1.0960e+02
1.1080e+02 1.1200e+02 1.1350e+02 1.1500e+02 1.1650e+02
1.1800e+02 1.1950e+02 1.2100e+02 1.2250e+02 1.2400e+02
1.2550e+02 1.2700e+02 1.2850e+02 1.3000e+02 1.3200e+02
1.3400e+02 1.3600e+02 1.3800e+02 1.4000e+02 1.4200e+02
1.4400e+02 1.4600e+02 1.4800e+02 1.5000e+02 1.5200e+02
1.5400e+02 1.5600e+02 1.5810e+02 1.6600e+02 1.7431e+02
1.8302e+02 1.9217e+02 2.0178e+02 2.1187e+02 2.2246e+02
2.3359e+02 2.4526e+02 2.5753e+02 2.7040e+02 2.8392e+02
2.9812e+02 3.1303e+02 3.2868e+02 3.4511e+02 3.6237e+02
3.8049e+02 3.9526e+02 /                  end of beta grid
"""

osc_leapr_text = """2 /
2.0500E-01 4.1500E-01      
1.5667E-01 3.1333E-01
"""

bottom_leapr_text1 = """' H(H2O)     ARCAB     EVAL-JUL20 Marquez Damian                   '
'                      DIST-                                       '
'----ENDF/B-VIII.0+    MATERIAL 1                                  '
'-----THERMAL NEUTRON SCATTERING DATA                              '
'------ENDF-6 FORMAT                                               '
'                                                                  '
'******************************************************************'
'*                                                                *'
'* UPDATE - JULY 2020                                             *'
'*                                                                *'
'* The evaluation was modified to include a refined temperature   *'
'* grid, including the freezing point (273.15 K), critical point  *'
'* (674.1 K) and a grid with 5 K interval between 285 K and 650 K.*'
'* Extrapolated temperature points between 650 K and 1000 K       *'
'* every 50 K were also added.                                    *'
'*                                                                *'
'* The model used for the ENDF/B-VIII.0 evaluation was            *'
'* described using a gaussian expansion, following the work by    *'
'* Maul, Marquez Damian, et al. [1]. The parameters for the       *'
'* gaussians were adjusted using third order polynomials          *'
'* that preserve the values at room temperature                   *'
'*                                                                *'
'* The ENDF-6 file was prepared using NJOY2016.57                 *'
'*                                                                *'
'* The update was prepared by:                                    *'
'*                                                                *'
'* J.I. Marquez Damian                                            *'
'* Spallation Physics Group                                       *'
'* European Spallation Source - Sweden (ESS)                      *'
'*                                                                *'
'* J.R. Granada                                                   *'
'* Nuclear Data Group - Neutron Physics Department                *'
'* Centro Atomico Bariloche - Argentina (CAB)                     *'
'*                                                                *'
'* D. Roubtsov                                                    *'
'* Canadian Nuclear Laboratories (CNL)                            *'
'* Chalk River, Canada                                            *'
'*                                                                *'
'* [1] Ann. Nucl. Energy, 121, 232 (2018)                         *'
'*                                                                *'
'******************************************************************'
'*                                                                *'
'* Interpolated temperatures:                                     *'
"""

comment_leapr_text = """'* T = {:7.2f}                                                    *'
"""

bottom_leapr_text2 = """'*                                                                *'
'******************************************************************'
'*                                                                *'
'* Temperatures = 283.6, 293.6, 300.0,                            *'
'*         323.6, 350.0, 373.6, 400.0,                            *'
'*         423.6, 450.0, 473.6, 500.0,                            *'
'*         523.6, 550.0, 573.6, 600.0 K, 623.6 K                  *'
'*                                                                *'
'* Extrapolated temperatures = 650.0, 800.0 K                     *'
'*                                                                *'
'* This evaluation is based on the CAB Model for light water[1]   *'
'* in a liquid state, T < T-crit(H2O) = 647.1 K. Two extrapolated *'
'* temperature points at 650 K and 800 K were added for backwards *'
'* compatibility with ENDF/B-VII.1 scripts. The file (MF7) was    *'
'* generated using NJOY 99.396[1] with a patch (upcab).           *'
'*                                                                *'
'* The CAB model is a further improvement of ENDF/B-VII (2006)    *'
'* and IKE, Stuttgart (2005) models for light water (incoherent   *'
'* inelastic approximation for n + H-in-H2O & vibrational         *'
'* spectrum decomposition). The continuous spectrum[2] is based   *'
'* on MD GROMACS Calculations[2] and diffusion coefficients       *'
'* measured by Yoshida[3] and Mills[4].                           *'
'*                                                                *'
'* For oxygen in H2O, free gas approximation is acceptable.       *'
'*                                                                *'
'* The evaluation was prepared by:                                *'
'*                                                                *'
'* J.I. Marquez Damian, F. Cantargi, and J.R. Granada             *'
'* Nuclear Data Group - Neutron Physics Department                *'
'* Centro Atomico Bariloche - Argentina (CAB):                    *'
'*                                                                *'
'*  and                                                           *'
'*                                                                *'
'* D. Roubtsov                                                    *'
'* Canadian Nuclear Laboratories (CNL)                            *'
'* Chalk River, Canada                                            *'
'*                                                                *'
'* References:                                                    *'
'*  [1] Ann. Nucl. Energy, 65, 280 (2014)                         *'
'*      http://dx.doi.org/10.1016/j.anucene.2013.11.014           *'
'*  [2] J. Chem. Phys. 139, 024504 (2013)                         *'
'*      http://dx.doi.org/10.1063/1.4812828                       *'
'*  [3] J. Chem. Phys. 123, 164506 (2005)                         *'
'*      http://dx.doi.org/10.1063/1.2056542                       *'
'*  [4] J. Phys. Chem. 77, 685 (1973)                             *'
'*      http://dx.doi.org/10.1021/j100624a025                     *'
'*                                                                *'
'******************************************************************'
'                                                                  '
/ end leapr
"""

class CustomFormatter(argparse.RawDescriptionHelpFormatter,
                      argparse.ArgumentDefaultsHelpFormatter):
    pass

def parse_args(args=sys.argv[1:]):
    '''Parse arguments.'''
    parser = argparse.ArgumentParser(
        description=sys.modules[__name__].__doc__,
        formatter_class=CustomFormatter)
    parser.add_argument('-t','--temperatures', nargs='+',
                        help='Temperatures to interpolate in Kelvin. '+ 
                              'If none is given uses default temperatures',
                        type=float, default=None)
    parser.add_argument('-txtout', '--txt_output',
                        help='Output txt file. '+
                             'If none is given prints to stdout', default=None)
    return parser.parse_args(args)

if __name__ == '__main__':
    options = parse_args()
    temps = options.temperatures
    txt_out = options.txt_output
    if temps == None:
        default_temps = True
        temps = np.array([273.15, 275, 280, 283.6, 285, 290, 293.6, 295, 300, 305, 
                          310, 315, 320, 323.6, 325, 330, 335, 340, 345, 350, 355, 
                          360, 365, 370, 373.6, 375, 380, 385, 390, 395, 400, 405, 
                          410, 415, 420, 423.6, 425, 430, 435, 440, 445, 450, 455, 
                          460, 465, 470, 473.6, 475, 480, 485, 490, 495, 500, 505, 
                          510, 515, 520, 523.6, 525, 530, 535, 540, 545, 550, 555, 
                          560, 565, 570, 573.6, 575, 580, 585, 590, 595, 600, 605, 
                          610, 615, 620, 623.6, 625, 630, 635, 640, 645, 647.1, 
                          650, 700, 750, 800, 850, 900, 950, 1000])
    else:
        default_temps = False
        temps = np.array(temps)
    s = top_leapr_text.format(len(temps))
    for t in temps:
        s = s + middle_text(t, fit_params) + osc_leapr_text
    if default_temps:
        s = s + "\n".join(bottom_leapr_text1.split("\n")[:-5])
        s = s + "\n"
    else:
        s = s + bottom_leapr_text1
        for t in temps:
            s = s + comment_leapr_text.format(t)
    s = s + bottom_leapr_text2
    s = s + "stop"
    if txt_out == None:
        print(s)
    else:
        with open(txt_out, 'w+') as fh:
            fh.write(s)     
    sys.exit(0)

