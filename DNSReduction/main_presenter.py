# Mantid Repository : https://github.com/mantidproject/mantid
#
# Copyright &copy; 2021 ISIS Rutherford Appleton Laboratory UKRI,
#     NScD Oak Ridge National Laboratory, European Spallation Source
#     & Institut Laue - Langevin
# SPDX - License - Identifier: GPL - 3.0 +
"""
Reduction GUI for DNS Instrument at MLZ
"""


class DNSReductionGUIPresenter:
    """
    main gui presenter for dns, presenter is onwed by mainview
    """
    def __init__(self,
                 name=None,
                 view=None,
                 parameter_abo=None,
                 modus=None,
                 parent=None,
                 command_line_reader=None):
        # pylint: disable=unused-argument, too-many-arguments
        self.name = name
        self.view = view
        self.modus = modus
        self.command_line_reader = command_line_reader
        self._parameter_abo = parameter_abo
        self.model = self._parameter_abo
        self._switch_mode('powder_tof')
        # self._switch_mode('simulation')
        # connect signals
        self.view.sig_tab_changed.connect(self._tab_changed)
        self.view.sig_save_as_triggered.connect(self._save_as)
        self.view.sig_save_triggered.connect(self._save)
        self.view.sig_open_triggered.connect(self._load_xml)
        self.view.sig_modus_change.connect(self._switch_mode)
        # self._command_line_launch()
        # self._switch_mode('sc_elastic')
        # self._parameter_abo.observer_dict['paths'].view.set_datapath('C:/mantid_testdata/tof_powder_vanadium')
        # self._parameter_abo.update_from_all_observers()
        # self._parameter_abo._notify_observers()
        # self._parameter_abo.observer_dict['file_selector']._read_all()
        # self._parameter_abo.observer_dict['file_selector']._check_last_scans('')

    def _load_xml(self):
        """Loading of GUI status from XML file"""
        self._parameter_abo.xml_load()

    def _save_as(self):
        """Saving of GUI status as XML file"""
        self._parameter_abo.xml_save_as()

    def _save(self):
        """Saving of GUI status as XML file to known filename"""
        self._parameter_abo.xml_save()

    def _switch_mode(self, modus):
        """
        Switching between differnt data reduction modes
        elastic/TOF, powder/single crystal  and simulation
        """
        self.view.clear_subviews()
        self.view.clear_submenues()
        self.modus.change(modus)
        self._parameter_abo.clear()
        for widget in self.modus.widgets.values():
            self._parameter_abo.register(widget.presenter)
            if widget.view.HAS_TAB:
                self.view.add_subview(widget.view)
            if widget.view.menues:
                self.view.add_submenu(widget.view)
        self._parameter_abo.notify_modus_change()

    def _tab_changed(self, oldtabindex, tabindex):
        oldview = self.view.get_view_for_tabindex(oldtabindex)
        actualview = self.view.get_view_for_tabindex(tabindex)
        for observer in self._parameter_abo.observers:
            if observer.view == oldview:
                self._parameter_abo.update_from_observer(observer)
        for observer in self._parameter_abo.observers:
            if observer.view == actualview:
                self._parameter_abo.notify_focused_tab(observer)
