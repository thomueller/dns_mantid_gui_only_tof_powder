# Mantid Repository : https://github.com/mantidproject/mantid
#
# Copyright &copy; 2019 ISIS Rutherford Appleton Laboratory UKRI,

#     NScD Oak Ridge National Laboratory, European Spallation Source
#     & Institut Laue - Langevin
# SPDX - License - Identifier: GPL - 3.0 +
"""
GUI for reduction of elastic and TOF data at the DNS instrumentat MLZ
"""
# pylint: disable=invalid-name
import os
import sys
print(sys.path.pop(0))

from mantidqt.gui_helper import get_qapplication
from qtpy import QtGui, QtWidgets\


from mantidqtinterfaces.DNSReduction.main_widget import DNSReductionGuiWidget

app, within_mantid = get_qapplication()

reducer_widget = DNSReductionGuiWidget(name='DNS-Reduction')
view = reducer_widget.view
view.setWindowTitle('DNS Reduction GUI- Powder TOF')
screenShape = QtWidgets.QDesktopWidget().screenGeometry()
view.resize(int(screenShape.width()*0.6), int(screenShape.height()*0.6))
appdir = os.path.dirname(__file__)
app.setWindowIcon(QtGui.QIcon('{}/DNSReduction/dns_icon.png'.format(appdir)))

#my_font = QtGui.QFont("Sans Serif", 16)
#HBBB GGGGGGGG HHHHHHHHHHHHHHHBview.setFont(my_font)
view.show()

if not within_mantid:
    sys.exit(app.exec_())

