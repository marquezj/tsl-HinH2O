#!/usr/bin/env python3

'''
Reads a thermal ACE file and plots the inelastic,
elastic (if available) and total cross section.
'''
import sys
import argparse
import openmc.data
import os.path
import numpy as np
import warnings
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.pyplot as plt


class CustomFormatter(argparse.RawDescriptionHelpFormatter,
                      argparse.ArgumentDefaultsHelpFormatter):
    pass


def energy(string):
    value = float(string)
    if (value < 1e-5):
        msg = '{} less than 1e-5 eV'.format(value)
        raise argparse.ArgumentTypeError(msg)
    return value


def number(string):
    value = int(string)
    if (value < 50):
        msg = '{} too few points to plot'.format(value)
        raise argparse.ArgumentTypeError(msg)
    return value


def parse_args(args=sys.argv[1:]):
    '''Parse arguments.'''
    parser = argparse.ArgumentParser(
        description=sys.modules[__name__].__doc__,
        formatter_class=CustomFormatter)
    parser.add_argument('input',
                        help='ACE file to plot')
    parser.add_argument('-pdfout', '--pdf_output',
                        help='Output pdf file', default='plot.pdf')
    parser.add_argument('-txtout', '--txt_output',
                        help='Output txt file', default=None)
    parser.add_argument('-s', '--start',
                        help='Minimum energy', type=energy, default=1e-5)
    parser.add_argument('-e', '--end',
                        help='Maximum energy', type=energy, default=None)
    parser.add_argument('-t', '--plot_type',
                        help='Plot type', type=str,
                        choices=['linlin', 'loglog', 'loglin', 'linlog'],
                        default='loglog')
    parser.add_argument('-n', '--npoints',
                        help='Number of points to plot',
                        type=number, default=1000)
    return parser.parse_args(args)


def plot(x, y, label, type):
    if (type == 'linlin'):
        plt.plot(x, y, label=label)
    elif (type == 'loglog'):
        plt.loglog(x, y, label=label)
    elif (type == 'linlog'):
        plt.semilogy(x, y, label=label)
    elif (type == 'loglin'):
        plt.semilogx(x, y, label=label)
    return


if __name__ == '__main__':
    options = parse_args()
    file_in = options.input
    pdf_out = options.pdf_output
    txt_out = options.txt_output
    start = options.start
    plot_type = options.plot_type
    npoints = options.npoints
    lib = openmc.data.ace.Library(file_in)
    with PdfPages(pdf_out) as pdf:
        for table in lib.tables:
            name, xs = table.name.split('.')
            if xs.endswith('t'):
                try:
                    data = openmc.data.ThermalScattering.from_ace(table)
                except Exception as e:
                    print('Failed to convert {}: {}'.format(table.name, e))
            else:
                raise ValueError('{} is not a thermal library'.
                                 format(table.name))
            if (options.end is None):
                end = data.energy_max
            else:
                end = options.end
            if (end > data.energy_max):
                end = data.energy_max
                msg = 'Setting plot limit to maximum energy '\
                    'in the library = {}'.format(end)
                warnings.warn(msg)
            if (start >= end):
                msg = 'Minium energy {} must be less than maximum energy {}'\
                    .format(start, end)
                raise argparse.ArgumentTypeError(msg)
            if (plot_type.startswith('log')):
                E = np.logspace(np.log10(start), np.log10(end), npoints)
            else:
                E = np.linspace(start, end, npoints)
            for T in data.temperatures:
                plt.rc('text', usetex=False)
                xs_inel = data.inelastic.xs[T](E)
                plt.title('File: {}, Lib: {}, Temperature: {}'.
                          format(file_in, table.name, T))
                plot(E, xs_inel, 'Inelastic XS', plot_type)
                if (data.elastic is not None):
                    xs_el = data.elastic.xs[T](E)
                    plot(E, xs_el, 'Elastic XS', plot_type)
                    xs_scat = xs_inel+xs_el
                    data_out = np.column_stack((E, xs_inel, xs_el, xs_scat))
                else:
                    xs_scat = xs_inel
                    data_out = np.column_stack((E, xs_inel))
                plot(E, xs_scat, 'Scattering XS', plot_type)
                plt.xlabel('Energy [eV]')
                plt.ylabel('Cross section [b]')
                plt.legend()
                pdf.savefig()
                plt.close()
                if (txt_out is not None):
                    dirname, basename = os.path.split(txt_out)
                    txt = table.name
                    txt = txt.replace('/', '_')
                    txt = txt.replace('.', '_')
                    txtname = 'xs_' + txt + '_' + T + '_' + basename
                    np.savetxt(os.path.join(dirname, txtname), data_out)
    sys.exit(0)
