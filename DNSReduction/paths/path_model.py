# Mantid Repository : https://github.com/mantidproject/mantid
#
# Copyright &copy; 2021 ISIS Rutherford Appleton Laboratory UKRI,
#     NScD Oak Ridge National Laboratory, European Spallation Source
#     & Institut Laue - Langevin
# SPDX - License - Identifier: GPL - 3.0 +
"""
presenter for dns path panel
"""

import glob
import os
from os.path import expanduser

from mantidqtinterfaces.DNSReduction.data_structures.dns_file import DNSFile
from mantidqtinterfaces.DNSReduction.data_structures.dns_obs_model import \
    DNSObsModel


class DNSPathModel(DNSObsModel):
    @staticmethod
    def get_user_and_propnumber(dir_name):
        try:
            firstfilename = next(glob.iglob('{}/*.d_dat'.format(dir_name)))
        except StopIteration:
            return ['', '']
        dns_file = DNSFile(dir_name, firstfilename)
        return [dns_file['users'], dns_file['proposal']]

    @staticmethod
    def clear_cache(path):
        if path and os.path.isfile(path + '/last_filelist.txt'):
            os.remove(path + '/last_filelist.txt')

    @staticmethod
    def get_startpath_for_dialog(path):
        if path:
            return path
        return expanduser("~")
