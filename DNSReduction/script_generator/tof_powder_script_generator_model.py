# Mantid Repository : https://github.com/mantidproject/mantid
#
# Copyright &copy; 2021 ISIS Rutherford Appleton Laboratory UKRI,
#     NScD Oak Ridge National Laboratory, European Spallation Source
#     & Institut Laue - Langevin
# SPDX - License - Identifier: GPL - 3.0 +
"""
DNS script generator for TOF powder data
"""

from mantidqtinterfaces.DNSReduction.data_structures.dns_tof_powder_dataset \
    import DNSTofDataset
from mantidqtinterfaces.DNSReduction.script_generator.\
    common_script_generator_model import \
    DNSScriptGeneratorModel


class DNSTofPowderScriptGeneratorModel(DNSScriptGeneratorModel):
    # pylint: disable=too-many-instance-attributes
    # having the options as instance attribues, is much better readable
    # none of them are public
    def __init__(self, parent):
        super().__init__(parent)
        self._script = None
        self._nb_banks = 0
        self._nb_vana_banks = 0
        self._nb_empty_banks = 0
        self._tof_opt = None
        self._vana_cor = None
        self._bg_cor = None
        self._standard_data = None
        self._sample_data = None

    def _validate_tof_options(self):
        return not (self._tof_opt['dEstep'] == 0 or self._tof_opt['qstep'] == 0
                    or self._tof_opt['qmax'] <= self._tof_opt['qmin']
                    or self._tof_opt['dEmax'] <= self._tof_opt['dEmin'])

    def _validate_nb_empty_banks(self):
        return not (self._nb_empty_banks == 0 and self._tof_opt['corrections']
                    and (self._tof_opt['substract_vana_back']
                         or self._tof_opt['substract_sample_back']))

    def _validate_nb_vana_banks(self):
        return not (self._nb_vana_banks == 0 and self._tof_opt['corrections']
                    and self._tof_opt['det_efficency'])

    def _check_vana_cor(self):
        return (self._tof_opt['corrections'] and self._tof_opt['det_efficency']
                and self._nb_vana_banks > 0)

    def _check_bg_cor(self):
        return self._tof_opt['corrections'] and self._nb_empty_banks > 0

    def _error_in_input(self):
        if not self._validate_tof_options():
            return 'Bin sizes make no sense.'
        if not self._validate_nb_vana_banks():
            return ('No vanadium files selected, but'
                    'Vanadium correction option choosen.')
        if not self._validate_nb_empty_banks():
            return ('No Background files selected, but background'
                    ' substraction option choosen.')
        return ''

    def _get_vanastring(self):
        if self._vana_cor:
            return ("\n          'vana_temperature' : "
                    "{},".format(self._tof_opt['vanadium_temperature']))
        return ''

    def _get_backstring(self):
        if self._bg_cor:
            return ("\n          'ecVanaFactor'     : "
                    "{},".format(self._tof_opt['vana_back_factor']))
        return ''

    def _get_backtofstring(self):
        if self._bg_cor:
            return ("\n          'ecSampleFactor'   : "
                    "{},".format(self._tof_opt['sample_back_factor']))
        return ''

    def _get_parameter_lines(self):
        backstring = self._get_backstring()
        vanastring = self._get_vanastring()
        backtofstring = self._get_backtofstring()
        return [
            "params = {{ 'e_channel'        : {}, "
            "\n          'wavelength'       : {},"
            "\n          'delete_raw'       : {},"
            "{}{}{} }}".format(self._tof_opt['epp_channel'],
                               self._tof_opt['wavelength'],
                               self._tof_opt['delete_raw'], vanastring,
                               backstring, backtofstring), ''
        ]

    def _get_binning_lines(self):
        return [
            "bins = {{'qmin' : {:7.3f}, 'qmax' : {:7.3f}, 'qstep' : {:7.3f},"
            "\n        'dEmin': {:7.3f}, 'dEmax': {:7.3f}, 'dEstep': {:7.3f}"
            "}}".format(self._tof_opt['qmin'], self._tof_opt['qmax'],
                        self._tof_opt['qstep'], self._tof_opt['dEmin'],
                        self._tof_opt['dEmax'], self._tof_opt['dEstep']), ''
        ]

    @staticmethod
    def _get_header_lines():
        lines = [
            "import numpy as np",
            "from mantid.simpleapi import MonitorEfficiencyCorUser,"
            " FindEPP, mtd",
            "from mantid.simpleapi import ComputeCalibrationCoefVan, Divide,"
            "CorrectTOF",
            "from mantid.simpleapi import SaveAscii, SaveNexus, MaskDetectors",
            "from mantidqtinterfaces.DNSReduction.scripts.dnstof import "
            "convert_to_d_e, get_sqw, "
            "load_data", ''
        ]
        return lines

    def _get_sample_data_lines(self):
        return ['sample_data = {}'.format(self._sample_data.format_dataset())]

    def _get_standard_data_lines(self):
        if self._tof_opt['corrections']:
            return [
                'standard_data = {}'
                ''.format(self._standard_data.format_dataset())
            ]
        return ['']

    def _get_load_data_lines(self):
        lines = [
            'load_data(sample_data["{}"], "raw_data1", params)'
            ''.format(self._sample_data.get_sample_filename())
        ]
        if self._bg_cor:
            lines += [
                'load_data(standard_data["{}"], "raw_ec", params)'
                ''.format(self._standard_data.get_empty_filename())
            ]
        if self._vana_cor:
            lines += [
                'load_data(standard_data["{}"], "raw_vanadium", params)'
                ''.format(self._standard_data.get_vana_filename())
            ]
        lines += ['']
        return lines

    def _get_normation_lines(self):
        if self._tof_opt['norm_monitor']:
            return [
                '# normalize', 'data1 = MonitorEfficiencyCorUser("raw_data1")'
            ]
        return ['data1 = mtd["raw_data1"]']

    def _get_substract_empty_lines(self):
        lines = []
        if self._bg_cor:
            lines = ['', 'ec =  MonitorEfficiencyCorUser("raw_ec")']
            if self._nb_empty_banks != self._nb_banks:
                lines += ['# only one empty can bank', 'ec = ec[0]']
            if self._tof_opt['substract_sample_back']:
                lines += [
                    "# subtract empty can",
                    "data1 = data1 - ec* params['ecSampleFactor']", ''
                ]
        return lines

    def _get_vana_ec_subst_lines(self):
        if self._tof_opt['substract_vana_back'] and self._bg_cor:
            if self._tof_opt['vana_back_factor'] != 1:
                return ["vanadium = vanadium - ec * params['ecVanaFactor']"]
            return ["vanadium = vanadium - ec"]
        return ['']

    def _get_only_one_vana_lines(self):
        if self._nb_vana_banks != self._nb_banks:
            return [
                '# only one vandium bank position', 'vanadium = vanadium[0]',
                ''
            ]
        return []

    @staticmethod
    def _get_epp_and_coef_lines():
        return [
            "# detector efficciency correction: compute coefficients",
            "epptable = FindEPP(vanadium)",
            "coefs = ComputeCalibrationCoefVan(vanadium, epptable,"
            " Temperature=params['vana_temperature'])"
        ]

    def _get_corr_epp_lines(self):
        if self._tof_opt['correct_elastic_peak_position']:
            return [
                '', '# correct TOF to get EPP at 0 meV',
                'data1 = CorrectTOF(data1, epptable)', ''
            ]
        return []

    def _get_bad_detec_lines(self):
        if self._nb_vana_banks > 1 or self._nb_vana_banks == self._nb_banks:
            return [
                'badDetectors = np.where(np.array(coefs[0]'
                '.extractY()).flatten() <= 0)[0]'
            ]
        return [
            'badDetectors = np.where(np.array(coefs.extractY())'
            '.flatten() <= 0)[0]'
        ]

    def _get_mask_detec_lines(self):
        if self._tof_opt['mask_bad_detectors']:
            lines = ['# get list of bad detectors']
            lines += self._get_bad_detec_lines()
            lines += [
                'print("Following detectors will be masked: ",'
                'badDetectors)',
                'MaskDetectors(data1, DetectorList=badDetectors)', ''
            ]
            return lines
        return ['']

    @staticmethod
    def _get_det_eff_cor_lines():
        return [
            '# apply detector efficiency correction',
            'data1 = Divide(data1, coefs)'
        ]

    def _get_vana_lines(self):
        if self._vana_cor:
            lines = ['vanadium =  MonitorEfficiencyCorUser("raw_vanadium")']
            lines += self._get_vana_ec_subst_lines()
            lines += self._get_only_one_vana_lines()
            lines += self._get_epp_and_coef_lines()
            lines += self._get_mask_detec_lines()
            lines += self._get_det_eff_cor_lines()
            lines += self._get_corr_epp_lines()
            return lines
        return ['']

    @staticmethod
    def _get_energy_print_lines():
        return [
            "# get Ei", "Ei = data1[0].getRun().getLogData('Ei').value",
            "print ('Incident Energy is {} meV'.format(Ei))", ""
        ]

    @staticmethod
    def _get_sqw_lines():
        return [
            "# get S(q,w)", "convert_to_d_e('data1', Ei)", "",
            "# merge al detector positions together",
            "get_sqw('data1_dE_S', 'data1', bins)"
        ]

    def _get_save_lines(self, paths):
        lines = []
        sascii, nexus = self._check_if_to_save(paths)
        if sascii:
            lines += [
                "SaveAscii('data1_dE_S', '{}/data1_dE_S.csv', "
                "WriteSpectrumID=False)".format(paths["export_dir"])
            ]
        if nexus:
            lines += [
                "SaveNexus('data1_dE_S', '{}/data1_dE_S.csv', )"
                "".format(paths["export_dir"])
            ]
        return lines

    @staticmethod
    def _check_if_to_save(paths):
        sascii = (paths["ascii"] and paths["export"]
                  and bool(paths["export_dir"]))
        nexus = (paths["nexus"] and paths["export"]
                 and bool(paths["export_dir"]))
        return [sascii, nexus]

    def _setup_sample_data(self, paths, fselector):
        self._sample_data = DNSTofDataset(data=fselector['full_data'],
                                          path=paths['data_dir'],
                                          issample=True)
        self._nb_banks = self._sample_data.get_nb_sample_banks()

    def _setup_standard_data(self, paths, fselector):
        if self._tof_opt['corrections']:
            self._standard_data = DNSTofDataset(
                data=fselector['standard_data'],
                path=paths['standards_dir'],
                issample=False)
            self._nb_vana_banks = self._standard_data.get_nb_vana_banks()
            self._nb_empty_banks = self._standard_data.get_nb_empty_banks()
        else:
            self._nb_vana_banks = 0
            self._nb_empty_banks = 0

    def script_maker(self, options, paths, fselector=None):  # noqa: C901
        self._tof_opt = options
        self._script = []

        self._setup_sample_data(paths, fselector)
        self._setup_standard_data(paths, fselector)
        self._check_if_to_save(paths)
        # if to do correction
        self._vana_cor = self._check_vana_cor()
        self._bg_cor = self._check_bg_cor()
        # validate if input binning makes sense, otherwise return
        # error = self._error_in_input()
        # print(self._error_in_input())
        # if error:
        #    return ['']  # todo add error raising

        # startin wrting script
        self._add_lines_to_script(self._get_header_lines())
        self._add_lines_to_script(self._get_sample_data_lines())
        self._add_lines_to_script(self._get_standard_data_lines())
        self._add_lines_to_script(self._get_parameter_lines())
        self._add_lines_to_script(self._get_binning_lines())
        self._add_lines_to_script(self._get_load_data_lines())
        self._add_lines_to_script(self._get_normation_lines())
        self._add_lines_to_script(self._get_substract_empty_lines())
        self._add_lines_to_script(self._get_vana_lines())
        self._add_lines_to_script(self._get_energy_print_lines())
        self._add_lines_to_script(self._get_sqw_lines())
        self._add_lines_to_script(self._get_save_lines(paths))
        return self._script
