# Mantid Repository : https://github.com/mantidproject/mantid
#
# Copyright &copy; 2021 ISIS Rutherford Appleton Laboratory UKRI,
#     NScD Oak Ridge National Laboratory, European Spallation Source
#     & Institut Laue - Langevin
# SPDX - License - Identifier: GPL - 3.0 +
"""
presenter for dns path panel
"""

import unittest
from unittest import mock

from mantidqtinterfaces.DNSReduction.data_structures.dns_observer \
    import DNSObserver
from mantidqtinterfaces.DNSReduction.paths.path_model import DNSPathModel
from mantidqtinterfaces.DNSReduction.paths.path_presenter \
    import DNSPathPresenter
from mantidqtinterfaces.DNSReduction.paths.path_view import DNSPathView


class DNSPathPresenterTest(unittest.TestCase):
    # pylint: disable=protected-access, too-many-public-methods

    @classmethod
    def setUpClass(cls):
        # cls.parent = mock.patch(DNSReductionGUI_presenter)
        cls.view = mock.create_autospec(DNSPathView)
        cls.model = mock.create_autospec(DNSPathModel)
        # view signals
        cls.view.sig_data_path_set = mock.Mock(return_value='dummypath')
        cls.view.sig_clear_cache = mock.Mock()
        cls.view.sig_filedialog_requested = mock.Mock(return_value='data')
        # view functions
        cls.view.get_path.return_value = ''
        cls.view.open_filedialog.return_value = 'C:/dummy/test.py'

        # model functions
        cls.model.get_startpath_for_dialog.return_value = 'C:/dummy'
        cls.model.get_user_and_propnumber.return_value = ['Thomas', 'p123456']
        # create presenter
        cls.presenter = DNSPathPresenter(view=cls.view, model=cls.model)

    def setUp(self):
        self.model.get_user_and_propnumber.reset_mock()
        self.view.set_datapath.reset_mock()
        self.view.set_prop_number.reset_mock()
        self.view.set_user.reset_mock()
        self.view.get_path.reset_mock()
        self.view.set_path.reset_mock()

    def test__init__(self):
        self.assertIsInstance(self.presenter, DNSObserver)

    def test_data_path_set(self):
        self.presenter._data_path_set(dir_name='C:/test')
        self.assertEqual(self.view.set_path.call_count, 5)
        self.view.set_path.assert_called_with('export_dir', 'C:/test/export')

    def test_set_user_prop_from_datafile(self):
        self.presenter._set_user_prop_from_datafile(dir_name='C:/test')
        self.model.get_user_and_propnumber.assert_called_once()
        self.view.set_prop_number.assert_called_once()
        self.view.set_user.assert_called_once()
        self.view.show_statusmessage.assert_not_called()

    def test_clear_cache(self):
        self.presenter._clear_cache()
        self.model.clear_cache.assert_not_called()
        self.presenter.own_dict = {'data_dir': '123'}
        self.presenter._clear_cache()
        self.model.clear_cache.assert_called_once()

    def test_on_modus_change(self):
        self.presenter.on_modus_change()
        self.view.hide_save.assert_called_once()

    def test_process_commandline_request(self):
        self.presenter.process_commandline_request(
            {'files': [{
                'path': 'C:/test'
            }]})
        self.view.set_datapath.assert_called_once()

    def test_filedialog_requested(self):
        self.presenter._filedialog_requested(sender='data')
        self.view.get_path.assert_called_once_with('data_dir')
        self.model.get_startpath_for_dialog.assert_called_once()
        self.view.open_filedialog.assert_called_once()
        self.view.set_datapath.assert_called_once()
        self.view.set_path.assert_not_called()


if __name__ == '__main__':
    unittest.main()
