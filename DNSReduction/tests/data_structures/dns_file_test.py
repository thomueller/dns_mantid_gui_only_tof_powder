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
import unittest

from mantidqtinterfaces.DNSReduction.data_structures.dns_file import DNSFile
from mantidqtinterfaces.DNSReduction.data_structures.object_dict import \
    ObjectDict
from mantidqtinterfaces.DNSReduction.tests.helpers_for_testing import \
    get_dataset, get_filepath


class DNSFileTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.filepath = get_filepath()
        cls.data = get_dataset()
        cls.file = DNSFile(cls.filepath, 'service_774714.d_dat')

    def test___init__(self):
        self.assertIsInstance(self.file, ObjectDict)
        self.assertIsInstance(self.file, DNSFile)

    def test_write(self):
        self.file.write(self.filepath, 'test.dat')
        filepath = self.filepath + '/test.dat'
        self.assertTrue(os.path.exists(filepath))
        os.remove(filepath)

    def test_read(self):
        # already read in init
        self.assertAlmostEqual(self.file['det_rot'], -7.01)
        self.assertEqual(self.file.counts[3, 0], 22805)


if __name__ == '__main__':
    unittest.main()
