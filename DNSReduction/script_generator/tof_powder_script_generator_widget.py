# Mantid Repository : https://github.com/mantidproject/mantid
#
# Copyright &copy; 2021 ISIS Rutherford Appleton Laboratory UKRI,
#     NScD Oak Ridge National Laboratory, European Spallation Source
#     & Institut Laue - Langevin
# SPDX - License - Identifier: GPL - 3.0 +
"""
DNS Powder Script generator Widget widget
"""
# yapf: disable
from mantidqtinterfaces.DNSReduction.data_structures.dns_widget import \
    DNSWidget
from mantidqtinterfaces.DNSReduction.script_generator.\
    common_script_generator_view import DNSScriptGeneratorView
from mantidqtinterfaces.DNSReduction.script_generator.\
    tof_powder_script_generator_model import DNSTofPowderScriptGeneratorModel
from mantidqtinterfaces.DNSReduction.script_generator.\
    tof_powder_script_generator_presenter import \
    DNSTofPowderScriptGeneratorPresenter
# yapf: enable


class DNSTofPowderScriptGeneratorWidget(DNSWidget):
    def __init__(self, name, parent):
        super().__init__(name, parent)
        self.view = DNSScriptGeneratorView(parent=parent.view)
        self.model = DNSTofPowderScriptGeneratorModel(parent=self)
        self.presenter = DNSTofPowderScriptGeneratorPresenter(parent=self,
                                                              view=self.view,
                                                              model=self.model,
                                                              name=name)
