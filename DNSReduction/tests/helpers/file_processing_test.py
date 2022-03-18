# Mantid Repository : https://github.com/mantidproject/mantid
#
# Copyright &copy; 2021 ISIS Rutherford Appleton Laboratory UKRI,
#     NScD Oak Ridge National Laboratory, European Spallation Source
#     & Institut Laue - Langevin
# SPDX - License - Identifier: GPL - 3.0 +
"""
DNS file helpers
"""

import unittest
from unittest.mock import patch

from mantidqtinterfaces.DNSReduction.helpers.file_processing import (
    create_dir, filter_filenames, return_filelist, return_standard_zip,
    save_txt, unzip_latest_standard, load_txt, open_editor,
    create_dir_from_filename, get_path_and_prefix)
from mantidqtinterfaces.DNSReduction.tests.helpers_for_testing \
    import get_3filenames


def mock_mtime(filename):
    times = {'standard.zip': 5, 'standard123.zip': 4}
    return times[filename]


class DNSfile_processingTest(unittest.TestCase):
    def setUp(self):
        self.filenames = get_3filenames()

    def test_filter_filenames(self):
        filtered = filter_filenames(self.filenames, 774714, 788058)
        self.assertEqual(filtered, self.filenames)
        filtered = filter_filenames(self.filenames, 774714, 788057)
        self.assertEqual(filtered, self.filenames[0:2])
        filtered = filter_filenames(self.filenames, 787464, 788057)
        self.assertEqual(filtered, [])

    @patch('mantidqtinterfaces.DNSReduction.helpers.file_processing.'
           'os.listdir')
    @patch('mantidqtinterfaces.DNSReduction.helpers.file_processing.'
           'os.path.isdir')
    def test_return_filelist(self, mock_is_dir, mock_listdir):
        mock_listdir.return_value = self.filenames + ['a.d_dat', '123.d_dat']
        mock_is_dir.return_value = True
        filelist = return_filelist('a')
        self.assertEqual(filelist, self.filenames)
        mock_is_dir.return_value = False
        filelist = return_filelist('a')
        self.assertEqual(filelist, [])

    @patch('mantidqtinterfaces.DNSReduction.helpers.file_processing.'
           'os.path.getmtime',
           new=mock_mtime)
    @patch('mantidqtinterfaces.DNSReduction.helpers.file_processing.'
           'glob.glob')
    @patch('mantidqtinterfaces.DNSReduction.helpers.file_processing.'
           'os.path.isdir')
    def test_return_standard_zip(self, mock_is_dir, mock_glob):
        mock_is_dir.return_value = False
        mock_glob.return_value = ['standard.zip', 'standard123.zip']
        testv = return_standard_zip('a')
        self.assertEqual(testv, '')
        mock_is_dir.return_value = True
        testv = return_standard_zip('a')
        self.assertEqual(testv, 'standard.zip')

    @patch('mantidqtinterfaces.DNSReduction.helpers.file_processing.'
           'zipfile.ZipFile')
    @patch('mantidqtinterfaces.DNSReduction.helpers.file_processing.'
           'return_standard_zip')
    def test_unzip_latest_standard(self, mock_return_standard, mock_zip):
        mock_extract = mock_zip.return_value.__enter__.return_value.extractall
        mock_return_standard.return_value = 'standard.zip'
        self.assertTrue(unzip_latest_standard('datab', 'stan'))
        mock_zip.assert_called_once_with('standard.zip', 'r')
        mock_extract.assert_called_once_with('stan')
        mock_extract.reset_mock()
        mock_return_standard.reset_mock()
        mock_return_standard.return_value = ''
        self.assertFalse(unzip_latest_standard('datab', 'stan'))
        mock_extract.assert_not_called()
        self.assertEqual(mock_return_standard.call_count, 2)

    @patch('mantidqtinterfaces.DNSReduction.helpers.file_processing.'
           'create_dir')
    @patch('mantidqtinterfaces.DNSReduction.helpers.file_processing.'
           'os.path.dirname')
    def test_create_dir_from_filename(self, mock_dirname, mock_cdir):
        create_dir_from_filename('123')
        mock_dirname.assert_called_once_with('123')
        mock_cdir.assert_called_once_with(mock_dirname.return_value)

    @patch('mantidqtinterfaces.DNSReduction.helpers.file_processing.'
           'os.makedirs')
    @patch('mantidqtinterfaces.DNSReduction.helpers.file_processing.'
           'os.path.exists')
    def test_create_dir(self, mock_path, mock_mdir):
        mock_path.return_value = True
        create_dir('a')
        mock_mdir.assert_not_called()
        mock_path.return_value = False
        create_dir('a')
        mock_mdir.assert_called_once_with('a')

    @patch('mantidqtinterfaces.DNSReduction.helpers.file_processing.' 'open')
    def test_save_txt(self, mock_open):
        mockwrite = mock_open.return_value.__enter__.return_value.write
        testv = save_txt(txt='abc', filename='123.dat', crdir=None)
        self.assertEqual(testv, ['123.dat', '123.dat'])
        mock_open.assert_called_once_with('123.dat', 'w')
        mockwrite.assert_called_once_with('abc')
        testv = save_txt(txt='abc', filename='123.dat', crdir='d')
        self.assertEqual(testv, ['123.dat', 'd/123.dat'])

    @patch('mantidqtinterfaces.DNSReduction.helpers.file_processing.' 'open')
    def test_load_txt(self, mock_open):
        mockread = mock_open.return_value.__enter__.return_value.readlines
        mockread.return_value = 'hzu'
        testv = load_txt(filename='123.dat', crdir=None)
        mock_open.assert_called_once_with('123.dat', 'r')
        mockread.assert_called_once()
        mock_open.reset_mock()
        mockread.rset_mock()
        testv = load_txt(filename='123.dat', crdir='d')
        mock_open.assert_called_once_with('d/123.dat', 'r')
        self.assertEqual(testv, 'hzu')

    @staticmethod
    @patch('mantidqtinterfaces.DNSReduction.helpers.file_processing.'
           'os.startfile')
    @patch('mantidqtinterfaces.DNSReduction.helpers.file_processing.'
           'os.path.exists')
    def test_open_editor(mock_path_exist, mock_startfile):
        mock_path_exist.return_value = False
        open_editor('123.d_dat', crdir=None)
        mock_path_exist.assert_called_once_with('123.d_dat')
        mock_startfile.assert_not_called()
        mock_path_exist.return_value = True
        mock_path_exist.reset_mock()
        open_editor('123.d_dat', crdir='d')
        mock_path_exist.assert_called_once_with('d/123.d_dat')
        mock_startfile.assert_called_once_with('d/123.d_dat')

    def test_get_path_and_prefix(self):
        testv = get_path_and_prefix('C:/123')
        self.assertEqual(testv, ('C:/', '123'))


if __name__ == '__main__':
    unittest.main()
