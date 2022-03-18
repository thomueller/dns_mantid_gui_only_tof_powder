# Mantid Repository : https://github.com/mantidproject/mantid
#
# Copyright &copy; 2021 ISIS Rutherford Appleton Laboratory UKRI,
#     NScD Oak Ridge National Laboratory, European Spallation Source
#     & Institut Laue - Langevin
# SPDX - License - Identifier: GPL - 3.0 +

import unittest
from unittest import mock
from unittest.mock import patch

from mantidqt.gui_helper import get_qapplication

from mantidqtinterfaces.DNSReduction.dns_modus import DNSModus
from mantidqtinterfaces.DNSReduction.main_presenter \
    import DNSReductionGUIPresenter
from mantidqtinterfaces.DNSReduction.main_view import DNSReductionGUIView
from mantidqtinterfaces.DNSReduction.parameter_abo import ParameterAbo
from mantidqtinterfaces.DNSReduction.command_line.command_check \
    import CommandLineReader

app, within_mantid = get_qapplication()


class DNSReductionGUIPresenterTest(unittest.TestCase):
    # pylint: disable=protected-access, too-many-public-methods

    modus = None
    widget = None
    parameter_abo = None
    view = None
    parent = None
    command_line_reader = None

    @classmethod
    def setUpClass(cls):
        cls.parent = mock.Mock()
        cls.view = mock.create_autospec(DNSReductionGUIView)
        cls.parameter_abo = mock.create_autospec(ParameterAbo)
        cls.command_line_reader = mock.create_autospec(CommandLineReader)
        cls.modus = mock.create_autospec(DNSModus)
        cls.widget = mock.Mock()
        cls.modus.widgets = {'observer1': cls.widget}
        cls.widget.view = mock.Mock()
        # cls.widget.view.has_tab = True
        cls.widget.view.menues = True
        cls.widget.presenter = mock.Mock()
        cls.widget.presenter.view = cls.widget.view
        cls.parameter_abo.observers = [cls.widget.presenter]
        dummy_observer = mock.Mock()
        # needed only for automatic reduction #todo remove after testing
        cls.parameter_abo.observer_dict = {
            'paths': dummy_observer,
            'file_selector': dummy_observer
        }

        cls.view.sig_tab_changed.connect = mock.Mock()
        cls.view.sig_save_as_triggered.connect = mock.Mock()
        cls.view.sig_save_triggered.connect = mock.Mock()
        cls.view.sig_open_triggered.connect = mock.Mock()
        cls.view.sig_modus_change.connect = mock.Mock()

        cls.presenter = DNSReductionGUIPresenter(
            name='reduction_gui',
            view=cls.view,
            parameter_abo=cls.parameter_abo,
            modus=cls.modus,
            parent=cls.parent,
            command_line_reader=cls.command_line_reader)

    def setUp(self):
        self.modus.reset_mock()
        self.view.reset_mock()
        self.parameter_abo.reset_mock()

    def test___init__(self):
        self.presenter = DNSReductionGUIPresenter(
            name='reduction_gui',
            view=self.view,
            parameter_abo=self.parameter_abo,
            modus=self.modus,
            parent=self.parent)
        self.assertIsInstance(self.presenter, DNSReductionGUIPresenter)
        self.assertIsInstance(self.presenter, object)
        self.view.clear_subviews.assert_called_once()
        self.view.add_subview.assert_called_once()
        self.view.add_submenu.assert_called_once()
        self.parameter_abo.register.assert_called_once()

    def test__load_xml(self):
        self.presenter._load_xml()
        self.parameter_abo.xml_load.assert_called_once()

    def test__save_as(self):
        self.presenter._save_as()
        self.parameter_abo.xml_save_as.assert_called_once()

    def test__save(self):
        self.presenter._save()
        self.parameter_abo.xml_save.assert_called_once()

    def test__switch_mode(self):
        self.view.clear_subviews.reset_mock()
        self.presenter._switch_mode('powder_tof')
        self.view.clear_subviews.assert_called_once()
        self.view.clear_submenues.assert_called_once()
        self.modus.change.assert_called_once()
        self.parameter_abo.register.assert_called_once()
        self.view.add_subview.assert_called_once()
        self.view.add_submenu.assert_called_once()
        self.parameter_abo.notify_modus_change.assert_called_once()

    def test__tab_changed(self):
        self.view.get_view_for_tabindex.return_value = self.widget.view
        self.presenter._tab_changed(1, 2)
        self.assertEqual(self.view.get_view_for_tabindex.call_count, 2)
        self.parameter_abo.update_from_observer.assert_called_once()
        self.parameter_abo.notify_focused_tab.assert_called_once()

    @patch(
        'mantidqtinterfaces.DNSReduction.main_presenter.DNSReductionGUI'
        'Presenter._switch_mode'
    )
    @patch('mantidqtinterfaces.DNSReduction.main_presenter.sys')
    def test_command_line_launch(self, mock_sys, mock_switch):
        self.command_line_reader.read.return_value = 1
        mock_sys.argv = [0]
        self.presenter._command_line_launch()
        self.view.switch_to_plot_tab.assert_not_called()
        mock_sys.argv = [0, 0, '-tof', '-powder']
        self.presenter._command_line_launch()
        mock_switch.assert_called_with('powder_tof')
        mock_sys.argv = [0, 0, '', '-powder']
        self.presenter._command_line_launch()
        mock_switch.assert_called_with('powder_elastic')
        mock_sys.argv = [0, 0, '', '']
        self.presenter._command_line_launch()
        mock_switch.assert_called_with('sc_elastic')
        mock_sys.argv = [0, 0, '-tof', '']
        self.presenter._command_line_launch()
        mock_switch.assert_called_with('sc_tof')
        self.command_line_reader.read.assert_called_with([0, 0, '-tof', ''])
        self.parameter_abo.process_commandline_request.assert_called_with(1)
        self.view.switch_to_plot_tab.assert_called()


if __name__ == '__main__':
    unittest.main()
