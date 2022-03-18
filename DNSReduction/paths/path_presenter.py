# Mantid Repository : https://github.com/mantidproject/mantid
#
# Copyright &copy; 2021 ISIS Rutherford Appleton Laboratory UKRI,
#     NScD Oak Ridge National Laboratory, European Spallation Source
#     & Institut Laue - Langevin
# SPDX - License - Identifier: GPL - 3.0 +
"""
presenter for dns path panel
"""

from mantidqtinterfaces.DNSReduction.data_structures.dns_observer import \
    DNSObserver


class DNSPathPresenter(DNSObserver):
    def __init__(self, name=None, parent=None, view=None, model=None):
        super().__init__(parent=parent, name=name, view=view, model=model)
        self.view.sig_data_path_set.connect(self._data_path_set)
        self.view.sig_clear_cache.connect(self._clear_cache)
        self.view.sig_filedialog_requested.connect(self._filedialog_requested)

    def _data_path_set(self, dir_name):
        for typename in ['psd', 'logbook', 'standards', 'script', 'export']:
            if not self.view.get_path(typename + '_dir'):
                self.view.set_path(typename + '_dir',
                                   dir_name + '/' + typename)
        self._set_user_prop_from_datafile(dir_name)

    def _set_user_prop_from_datafile(self, dir_name):
        user, prop_nb = self.model.get_user_and_propnumber(dir_name)
        if prop_nb or user:
            self.view.set_prop_number(prop_nb)
            self.view.set_user(user)
        else:
            self.view.show_statusmessage(
                'No DNS .d_dat file found in data'
                'directory', 30)

    def _clear_cache(self):
        path = self.own_dict.get('data_dir', False)
        if path:
            self.model.clear_cache(path)

    def _filedialog_requested(self, sender):
        path = self.view.get_path('data_dir')
        startpath = self.model.get_startpath_for_dialog(path)
        dir_name = self.view.open_filedialog(startpath)
        if sender == 'data':
            self.view.set_datapath(dir_name)
        else:
            self.view.set_path(sender + '_dir', dir_name)

    # common presenter methods
