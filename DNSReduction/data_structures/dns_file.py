# Mantid Repository : https://github.com/mantidproject/mantid
#
# Copyright &copy; 2021 ISIS Rutherford Appleton Laboratory UKRI,
#     NScD Oak Ridge National Laboratory, European Spallation Source
#     & Institut Laue - Langevin
# SPDX - License - Identifier: GPL - 3.0 +
"""
Class which loads and stores a single DNS datafile in a dictionary
"""

import os

import numpy as np

from mantidqtinterfaces.DNSReduction.data_structures.object_dict import \
    ObjectDict


class DNSFile(ObjectDict):
    """
    class for reading, writing and storing data of a single dns datafile
    this is a dictionary  but can also be accessed like atributes
    """
    def __init__(self, datapath, filename):
        super().__init__()
        self.new_format = self.read(datapath, filename)

    def write(self, datapath, filename):
        # mostly stolen form nicos
        txt = ''
        separator = "#" + "-" * 74 + "\n"
        wavelength = self['wavelength'] / 10.0  # written in nm
        txt += "# DNS Data userid={},exp={},file={},sample={}\n".format(
            self['users'], self['proposal'], self['filenumber'],
            self['sample'])
        txt += separator

        txt += "# 2\n"
        txt += "# User: {}\n".format(self['users'])
        txt += "# Sample: {}\n".format(self['sample'])
        txt += separator

        txt += "# DNS   Mono  d-spacing[nm]  Theta[deg]   " \
               "Lambda[nm]   Energy[meV]   Speed[m/sec]\n"
        txt += "#      {}   {:6.4f}         {:6.2f}" \
               "         {:6.3f}{:6.3f}      {:7.2f}\n" \
               "".format("PG-002", 0.3350, self['mon_rot'],
                         wavelength, self['energy'], self['speed'])

        txt += "# Distances [cm] Sample_Chopper    " \
               "Sample_Detector    Sample_Monochromator\n"
        txt += "#                  36.00            80.00            220.00\n"
        txt += separator

        txt += "# Motors                      Position\n"
        txt += "# Monochromator              {:6.2f} deg\n" \
            .format(self['mon_rot'])
        txt += "# DeteRota                   {:6.2f} deg\n" \
            .format(self['det_rot'])
        txt += "#\n"
        txt += "# Huber                      {:6.2f} deg\n" \
            .format(self['sample_rot'])
        txt += "# Cradle_lower               {:6.2f} deg\n" \
            .format(self['cradle_lo'])
        txt += "# Cradle_upper               {:6.2f} deg\n" \
            .format(self['cradle_up'])
        txt += "#\n"
        txt += "# Slit_i_vertical upper      {:6.1f} mm\n" \
            .format(self['ap_sam_y_upper'])
        txt += "#                 lower      {:6.1f} mm\n" \
            .format(self['ap_sam_y_lower'])
        txt += "# Slit_i_horizontal left     {:6.1f} mm\n" \
            .format(self['ap_sam_x_left'])
        txt += "#                   right    {:6.1f} mm\n" \
            .format(self['ap_sam_x_right'])
        txt += "#\n"
        # dummy line
        txt += "# Slit_f_upper                {:4d} mm\n".format(0)
        # dummy line
        txt += "# Slit_f_lower                {:4d} mm\n".format(0)
        # dummy line
        txt += "# Detector_Position_vertical  {:4d} mm\n".format(0)
        txt += "#\n"
        txt += "# Polariser\n"
        txt += "#    Translation              {:4d} mm\n".format(
            int(round(self['pol_trans_x'])))
        txt += "#    Rotation              {:6.2f} deg\n".format(
            self['pol_rot'])
        txt += "#\n"
        txt += "# Analysers                 undefined\n"
        txt += separator
        # write currents
        txt += "# B-fields                   current[A]  field[G]\n"
        txt += "#   Flipper_precession        {:6.3f} A     {:6.2f} G\n" \
            .format(self['Co'], 0.0)
        txt += "#   Flipper_z_compensation    {:6.3f} A     {:6.2f} G\n" \
            .format(self['Fi'], 0.0)
        txt += "#   C_a                       {:6.3f} A     {:6.2f} G\n" \
            .format(self['A'], 0.0)
        txt += "#   C_b                       {:6.3f} A     {:6.2f} G\n" \
            .format(self['B'], 0.0)
        txt += "#   C_c                       {:6.3f} A     {:6.2f} G\n" \
            .format(self['C'], 0.0)
        txt += "#   C_z                       {:6.3f} A     {:6.2f} G\n" \
            .format(self['ZT'], 0.0)
        txt += separator

        txt += "# Temperatures/Lakeshore      T\n"
        txt += "#  T1                         {:6.3f} K\n" \
            .format(self['temp_tube'])
        txt += "#  T2                         {:6.3f} K\n" \
            .format(self['temp_samp'])
        txt += "#  sample_setpoint            {:6.3f} K\n" \
            .format(self['temp_set'])
        txt += separator

        txt += "# TOF parameters\n"
        txt += "#  TOF channels                {:4d}\n" \
            .format(self['tofchannels'])
        txt += "#  Time per channel            {:6.1f} microsecs\n" \
            .format(self['channelwidth'])
        txt += "#  Delay time                  {:6.1f} microsecs\n" \
            .format(self['tofdelay'])

        txt += "#  Chopper slits\n"
        txt += "#  Elastic time channel\n"
        txt += "#  Chopper frequency\n"
        txt += separator

        txt += "# Active_Stop_Unit           TIMER\n"
        txt += "#  Timer                    {:6.1f} sec\n" \
            .format(self['timer'])
        txt += "#  Monitor           {:16d}\n".format(self['monitor'])
        txt += "#\n"
        txt += "#    start   at      {}\n".format(self['starttime'])
        txt += "#    stopped at      {}\n".format(self['endtime'])
        txt += separator

        txt += "# Extended data\n"
        if self['scannumber']:
            txt += "#  Scannumber               {:8d}\n" \
                .format(int(self['scannumber']))
        else:
            txt += "#  Scannumber                       \n"
        txt += "#  Scancommand              {}\n".format(self['scancommand'])
        txt += "#  Scanposition             {:>8s}\n" \
            .format(self['scanposition'])
        txt += "#  pol_trans_x              {:8.1f} mm\n" \
            .format(self['pol_trans_x'])
        txt += "#  pol_trans_y              {:8.1f} mm\n" \
            .format(self['pol_trans_y'])
        txt += "#  field                    {:>8s}\n".format(self['field'])
        txt += "#  selector_lift            {:8.1f} mm\n" \
            .format(self['selector_lift'])
        txt += "#  selector_speed           {:8.1f} rpm\n" \
            .format(self['selector_speed'])
        txt += separator

        # write array
        txt += "# DATA (number of detectors, number of TOF channels)\n"
        txt += "# 64 {:4d}\n".format(self['tofchannels'])
        for ch in range(24):
            txt += "{:2d} ".format(ch)
            for q in range(self['tofchannels']):
                txt += " {:8d}".format(self.counts[ch, q])
            txt += "\n"
        for ch in range(24, 64):
            txt += "{:2d} ".format(ch)
            for q in range(self['tofchannels']):
                txt += " {:8d}".format(0)
            txt += "\n"
        with open(os.path.join(datapath, filename), 'w') as myfile:
            myfile.write(txt)

    def read(self, datapath, filename):
        with open(os.path.join(datapath, filename), 'r') as f:
            txt = f.readlines()
        del f
        if len(txt) < 138 or not txt[0].startswith('# DNS Data'):
            del txt
            return False
        self['filename'] = filename
        line = txt[0]
        line = line.split('userid=')[1].split(',exp=')
        self['users'] = line[0]
        line = line[1].split(',file=')
        self['proposal'] = line[0]
        line = line[1].split(',sample=')
        self['filenumber'] = line[0]
        self['sample'] = line[1][:-1]
        line = txt[7].split()
        self['mon_rot'] = float(line[3])
        self['wavelength'] = float(line[4]) * 10
        self['energy'] = float(line[5])
        self['speed'] = float(line[6])
        self['mon_rot'] = float(txt[12][25:-5])
        self['det_rot'] = float(txt[13][25:-5])
        self['sample_rot'] = float(txt[15][25:-5])
        self['cradle_lo'] = float(txt[16][25:-5])
        self['cradle_up'] = float(txt[17][25:-5])
        self['ap_sam_y_upper'] = float(txt[19][25:-4])
        self['ap_sam_y_lower'] = float(txt[20][25:-4])
        self['ap_sam_x_left'] = float(txt[21][25:-4])
        self['ap_sam_x_right'] = float(txt[22][25:-4])
        self['pol_trans_x'] = float(txt[29][25:-3])
        self['pol_rot'] = float(txt[30][25:-4])
        self['Co'] = float(txt[35][25:-16])
        self['Fi'] = float(txt[36][27:-16])
        self['A'] = float(txt[37][25:-16])
        self['B'] = float(txt[38][25:-16])
        self['C'] = float(txt[39][25:-16])
        self['ZT'] = float(txt[40][25:-16])
        self['temp_tube'] = float(txt[43][25:-3])
        self['temp_samp'] = float(txt[44][25:-3])
        self['temp_set'] = float(txt[45][25:-3])
        self['tofchannels'] = int(txt[48][25:-1])
        self['channelwidth'] = float(txt[49][25:-11])
        self['tofdelay'] = float(txt[50][25:-11])
        self['timer'] = float(txt[56][15:-5])
        self['monitor'] = int(txt[57][15:-1])
        self['starttime'] = txt[59][21:-1]
        self['endtime'] = txt[60][21:-1]
        self['scannumber'] = txt[63][15:-1].strip()
        self['scancommand'] = txt[64][28:-1]
        self['scanposition'] = txt[65][15:-1].strip()
        self['pol_trans_x'] = float(txt[66][15:-4])
        self['pol_trans_y'] = float(txt[67][15:-4])
        self['field'] = txt[68][10:-1].strip()
        self['selector_lift'] = float(txt[69][17:-4])
        self['selector_speed'] = float(txt[70][17:-4])
        if '/' in self['scanposition']:
            self['scanpoints'] = self['scanposition'].split('/')[1]
        else:
            self['scanpoints'] = ''
        self['counts'] = np.zeros((24, self['tofchannels']),
                                  dtype=int)  # for python 2 use long
        for ch in range(24):
            self['counts'][ch, :] = txt[74 + ch].split()[1:]
        del txt
        return True
