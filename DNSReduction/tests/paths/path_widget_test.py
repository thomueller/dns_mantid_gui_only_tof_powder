# Mantid Repository : https://github.com/mantidproject/mantid
#
# Copyright &copy; 2021 ISIS Rutherford Appleton Laboratory UKRI,
#     NScD Oak Ridge National Laboratory, European Spallation Source
#     & Institut Laue - Langevin
# SPDX - License - Identifier: GPL - 3.0 +
import unittest
from unittest import mock
from mantidqt.gui_helper import get_qapplication
from mantidqtinterfaces.DNSReduction.data_structures.dns_widget \
    import DNSWidget
from mantidqtinterfaces.DNSReduction.paths.path_model import DNSPathModel
from mantidqtinterfaces.DNSReduction.paths.path_presenter \
    import DNSPathPresenter
from mantidqtinterfaces.DNSReduction.paths.path_view import DNSPathView
from mantidqtinterfaces.DNSReduction.paths.path_widget import DNSPathWidget

app, within_mantid = get_qapplication()


class DNSPathWidgetTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        parent = mock.Mock()
        parent.view = None
        cls.widget = DNSPathWidget('paths', parent)

    def test___init__(self):
        self.assertIsInstance(self.widget, DNSPathWidget)
        self.assertIsInstance(self.widget, DNSWidget)
        self.assertIsInstance(self.widget.view, DNSPathView)
        self.assertIsInstance(self.widget.model, DNSPathModel)
        self.assertIsInstance(self.widget.presenter, DNSPathPresenter)


if __name__ == '__main__':
    unittest.main()
