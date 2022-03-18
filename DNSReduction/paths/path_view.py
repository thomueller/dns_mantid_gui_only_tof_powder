# Mantid Repository : https://github.com/mantidproject/mantid
#
# Copyright &copy; 2021 ISIS Rutherford Appleton Laboratory UKRI,
#     NScD Oak Ridge National Laboratory, European Spallation Source
#     & Institut Laue - Langevin
# SPDX - License - Identifier: GPL - 3.0 +
"""
DNS Path Configuration Widget = View - Tab of DNS Reduction GUI
"""

from qtpy.QtCore import Signal
from qtpy.QtWidgets import QFileDialog

from mantidqt.utils.qt import load_ui

from mantidqtinterfaces.DNSReduction.data_structures.dns_view import DNSView


class DNSPathView(DNSView):
    """
        Widget that lets user select DNS data directories
    """
    NAME = 'Paths'

    def __init__(self, parent):
        super().__init__(parent)
        self._content = load_ui(__file__, 'path.ui', baseinstance=self)

        self._map = {
            'data_dir': self._content.lE_data_dir,
            'logbook_dir': self._content.lE_logbook_dir,
            'psd_dir': self._content.lE_psd_dir,
            'user': self._content.lE_user,
            'prop_nb': self._content.lE_prop_nb,
            'standards_dir': self._content.lE_standards_dir,
            'script_dir': self._content.lE_script_dir,
            'export_dir': self._content.lE_export_dir,
            'nexus': self._content.cB_nexus,
            'ascii': self._content.cB_ascii,
            'export': self._content.gB_export,
        }

        # connect signals
        self._content.pB_file_data.clicked.connect(self._filedialog)
        self._content.pB_file_psd.clicked.connect(self._filedialog)
        self._content.pB_file_logbook.clicked.connect(self._filedialog)
        self._content.pB_file_standards.clicked.connect(self._filedialog)
        self._content.pB_file_script.clicked.connect(self._filedialog)
        self._content.pB_clear.clicked.connect(self._clear_directories)
        self._content.pB_export.clicked.connect(self._filedialog)
        self._content.pB_clear_cache.clicked.connect(self._clear_cache)

    # Signals

    sig_data_path_set = Signal(str)
    sig_clear_cache = Signal()
    sig_filedialog_requested = Signal(str)

    def _filedialog(self):
        sender = self.sender().objectName()[8:]
        self.sig_filedialog_requested.emit(sender)

    def open_filedialog(self, startpath):
        dir_name = QFileDialog.getExistingDirectory(
            self, "Select folder", startpath,
            QFileDialog.ShowDirsOnly | QFileDialog.DontUseNativeDialog)
        return dir_name

    def set_datapath(self, dir_name):
        self.set_path('data_dir', dir_name)
        self.sig_data_path_set.emit(dir_name)

    def _clear_cache(self):
        self.sig_clear_cache.emit()

    def _clear_directories(self):
        self.set_user('')
        self.set_prop_number('')
        self.set_path('logbook_dir', '')
        self.set_path('data_dir', '')
        self.set_path('standards_dir', '')
        self.set_path('script_dir', '')
        self.set_path('psd_dir', '')
        self.set_path('export_dir', '')

    def get_path(self, pathtype):
        return self._map[pathtype].text()

    def get_prop_number(self):
        return self._map['prop_nb'].text()

    def get_user(self):
        return self._map['user'].text()

    def set_path(self, pathtype, directory):
        self._map[pathtype].setText(directory)

    def set_prop_number(self, prop_nb):
        self._map['prop_nb'].setText(prop_nb)

    def set_user(self, user):
        self._map['user'].setText(user)
        self._map['user'].setCursorPosition(0)

    def hide_save(self, hide=True):
        self._map['nexus'].setVisible(not hide)
        self._map['ascii'].setVisible(not hide)
