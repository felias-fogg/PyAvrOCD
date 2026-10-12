# Device description for atmega406, generated from Microchip's ATmega406.atdf by
# pyavrocd/deviceinfo/harvest.py; the SVD part is added by addsvd.py.
#
# The ATDF and SVD data are Copyright (c) 2026 Microchip Technology Inc. and are
# licensed under the Apache License, Version 2.0. The license text is in
# LICENSE-APACHE-2.0 in the root of this distribution, the notice as it ships
# inside the device packs in extras/atdf/LICENSE.microchip. This file is a
# modified extract of that data: only the fields PyAvrOCD needs, restructured as
# a Python dictionary.
#
# Do not edit by hand. A correction belongs in a patch for the ATDF file, see
# extras/atdf/README.md.

from pymcuprog.deviceinfo.eraseflags import ChiperaseEffect

DEVICE_INFO = {
    'name': 'atmega406',
    'architecture': 'avr8',

    # eeprom
    'eeprom_address_byte': 0x0000,
    'eeprom_size_bytes': 0x0200,
    'eeprom_page_size_bytes': 0x04,
    'eeprom_read_size_bytes': 0x01,
    'eeprom_write_size_bytes': 0x01,
    'eeprom_chiperase_effect': ChiperaseEffect.CONDITIONALLY_ERASED_AVR,
    'eeprom_isolated_erase': True,

    # flash
    'flash_address_byte': 0x0000,
    'flash_size_bytes': 0xa000,
    'flash_page_size_bytes': 0x80,
    'flash_read_size_bytes': 0x02,
    'flash_write_size_bytes': 0x80,
    'flash_chiperase_effect': ChiperaseEffect.ALWAYS_ERASED,
    'flash_isolated_erase': True,

    # fuses
    'fuses_address_byte': 0,
    'fuses_size_bytes': 0x0002,
    'fuses_page_size_bytes': 0x01,
    'fuses_read_size_bytes': 0x01,
    'fuses_write_size_bytes': 0x01,
    'fuses_chiperase_effect': ChiperaseEffect.NOT_ERASED,
    'fuses_isolated_erase': True,

    # internal_sram
    'internal_sram_address_byte': 0x0100,
    'internal_sram_size_bytes': 0x0800,
    'internal_sram_page_size_bytes': 0x01,
    'internal_sram_read_size_bytes': 0x01,
    'internal_sram_write_size_bytes': 0x01,
    'internal_sram_chiperase_effect': ChiperaseEffect.NOT_ERASED,
    'internal_sram_isolated_erase': True,

    # lockbits
    'lockbits_address_byte': 0,
    'lockbits_size_bytes': 0x0001,
    'lockbits_page_size_bytes': 0x01,
    'lockbits_read_size_bytes': 0x01,
    'lockbits_write_size_bytes': 0x01,
    'lockbits_chiperase_effect': ChiperaseEffect.ALWAYS_ERASED,
    'lockbits_isolated_erase': True,

    # signatures
    'signatures_address_byte': 0,
    'signatures_size_bytes': 3,
    'signatures_page_size_bytes': 0x01,
    'signatures_read_size_bytes': 0x01,
    'signatures_write_size_bytes': 0x00,
    'signatures_chiperase_effect': ChiperaseEffect.NOT_ERASED,
    'signatures_isolated_erase': True,

    # Some extra AVR specific fields
    'address_size': '16-bit',
    'prog_clock_khz': 1800,
    # Missing hv_implementation property in ATDF file
    # Defaulting to 1 for devices without UPDI fuse
    'hv_implementation': 1,
    'ocd_rev' : 3,
    'ocd_base' : 0x31,
    'eear_base' : 0x21,
    'eear_size' : 2,
    'eecr_base' : 0x1F,
    'eedr_base' : 0x20,
    'spmcsr_base' : 0x57,
    'osccal_base' : 0x46,
    'ocden_base' : 0x01,
    'ocden_mask' : 0x02,
    'bootrst_base' : 0x00,
    'bootrst_mask' : 0x08,
    'eesave_base' : 0x00,
    'eesave_mask' : 0x40,
    'tcnt0_base' : 0x46,
    'cs0_base' : 0x45,
    'toie0_base' : 0x6E,
    'toie0_mask' : 0x01,
    'masked_registers' : [0x51],
    'ronly_registers' : [0x20, 0x23, 0x35, 0x36, 0x3b, 0x3c, 0x60, 0x62, 0x7a, 0xb9, 0xbc, 0xe0, 0xe1, 0xe2, 0xe3, 0xe5, 0xf2, 0xf8],
    'device_id': 0x1E9507,
    'interface': 'HVPP+JTAG',

    # SVD data
    'svd' : {'device': {'access': 'read-write',
            'addressUnitBits': 0x8,
            'attributes': {'schemaVersion': '1.1'},
            'cpu': {'endian': 'little',
                    'fpuPresent': 0x0,
                    'mpuPresent': 0x0,
                    'name': 'other',
                    'nvicPrioBits': 0x4,
                    'revision': 'r0p0',
                    'vendorSystickConfig': 0x0},
            'description': 'No description available.',
            'name': 'ATmega406',
            'peripherals': {'peripheral': [{'addressBlock': [{'offset': 0x0,
                                                              'size': 0x3,
                                                              'usage': 'registers'},
                                                             {'offset': 0x4,
                                                              'size': 0x1,
                                                              'usage': 'registers'}],
                                            'baseAddress': 0x800078,
                                            'description': 'Analog-to-Digital '
                                                           'Converter',
                                            'name': 'ADC',
                                            'registers': {'register': [{'access': 'read-write',
                                                                        'addressOffset': 0x0,
                                                                        'description': 'VADC '
                                                                                       'Data '
                                                                                       'Register  '
                                                                                       'Bytes',
                                                                        'name': 'VADC',
                                                                        'size': 0x10,
                                                                        'writeConstraint': {'range': {'maximum': 0xFFFF,
                                                                                                      'minimum': 0x0}}},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x2,
                                                                        'description': 'The '
                                                                                       'VADC '
                                                                                       'Control '
                                                                                       'and '
                                                                                       'Status '
                                                                                       'register '
                                                                                       '(read-only '
                                                                                       'for '
                                                                                       'debugger)',
                                                                        'fields': {'field': [{'access': 'read-write',
                                                                                              'bitRange': '[0:0]',
                                                                                              'description': 'VADC '
                                                                                                             'Conversion '
                                                                                                             'Complete '
                                                                                                             'Interrupt '
                                                                                                             'Enable',
                                                                                              'name': 'VADCCIE'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[1:1]',
                                                                                              'description': 'VADC '
                                                                                                             'Conversion '
                                                                                                             'Complete '
                                                                                                             'Interrupt '
                                                                                                             'Flag',
                                                                                              'name': 'VADCCIF'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[2:2]',
                                                                                              'description': 'VADC '
                                                                                                             'Satrt '
                                                                                                             'Conversion',
                                                                                              'name': 'VADSC'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[3:3]',
                                                                                              'description': 'VADC '
                                                                                                             'Enable',
                                                                                              'name': 'VADEN'}]},
                                                                        'name': 'VADCSR',
                                                                        'size': 0x8},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x4,
                                                                        'description': 'The '
                                                                                       'VADC '
                                                                                       'multiplexer '
                                                                                       'Selection '
                                                                                       'Register',
                                                                        'fields': {'field': [{'access': 'read-write',
                                                                                              'bitRange': '[3:0]',
                                                                                              'description': 'Analog '
                                                                                                             'Channel '
                                                                                                             'and '
                                                                                                             'Gain '
                                                                                                             'Selection '
                                                                                                             'Bits',
                                                                                              'name': 'VADMUX',
                                                                                              'writeConstraint': {'range': {'maximum': 0xF,
                                                                                                                            'minimum': 0x0}}}]},
                                                                        'name': 'VADMUX',
                                                                        'size': 0x8}]}},
                                           {'addressBlock': [{'offset': 0x0,
                                                              'size': 0x2,
                                                              'usage': 'registers'}],
                                            'baseAddress': 0x8000D0,
                                            'description': 'Bandgap',
                                            'name': 'BANDGAP',
                                            'registers': {'register': [{'access': 'read-write',
                                                                        'addressOffset': 0x0,
                                                                        'description': 'Bandgap '
                                                                                       'Calibration '
                                                                                       'Register',
                                                                        'fields': {'field': [{'access': 'read-write',
                                                                                              'bitRange': '[5:0]',
                                                                                              'description': 'BG '
                                                                                                             'Calibration '
                                                                                                             'of '
                                                                                                             'PTAT '
                                                                                                             'Current '
                                                                                                             'Bits',
                                                                                              'name': 'BGCC',
                                                                                              'writeConstraint': {'range': {'maximum': 0x3F,
                                                                                                                            'minimum': 0x0}}},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[7:7]',
                                                                                              'description': 'Setting '
                                                                                                             'the '
                                                                                                             'BGD '
                                                                                                             'bit '
                                                                                                             'to '
                                                                                                             'one '
                                                                                                             'will '
                                                                                                             'disable '
                                                                                                             'the '
                                                                                                             'bandgap '
                                                                                                             'voltage '
                                                                                                             'reference. '
                                                                                                             'This '
                                                                                                             'bit '
                                                                                                             'must '
                                                                                                             'be '
                                                                                                             'cleared '
                                                                                                             'before '
                                                                                                             'enabling '
                                                                                                             'CC-ADC '
                                                                                                             'or '
                                                                                                             'V-ADC, '
                                                                                                             'and '
                                                                                                             'must '
                                                                                                             'remain '
                                                                                                             'unset '
                                                                                                             'while '
                                                                                                             'either '
                                                                                                             'ADC '
                                                                                                             'is '
                                                                                                             'enabled.',
                                                                                              'name': 'BGD'}]},
                                                                        'name': 'BGCCR',
                                                                        'size': 0x8},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x1,
                                                                        'description': 'Bandgap '
                                                                                       'Calibration '
                                                                                       'of '
                                                                                       'Resistor '
                                                                                       'Ladder',
                                                                        'name': 'BGCRR',
                                                                        'size': 0x8,
                                                                        'writeConstraint': {'range': {'maximum': 0xFF,
                                                                                                      'minimum': 0x0}}}]}},
                                           {'addressBlock': [{'offset': 0x0,
                                                              'size': 0x7,
                                                              'usage': 'registers'}],
                                            'baseAddress': 0x8000F2,
                                            'description': 'Battery Protection',
                                            'name': 'BATTERY_PROTECTION',
                                            'registers': {'register': [{'access': 'read-write',
                                                                        'addressOffset': 0x5,
                                                                        'description': 'Battery '
                                                                                       'Protection '
                                                                                       'Control '
                                                                                       'Register',
                                                                        'fields': {'field': [{'access': 'read-write',
                                                                                              'bitRange': '[0:0]',
                                                                                              'description': 'No '
                                                                                                             'Description.',
                                                                                              'name': 'CCD'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[1:1]',
                                                                                              'description': 'No '
                                                                                                             'Description.',
                                                                                              'name': 'DCD'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[2:2]',
                                                                                              'description': 'No '
                                                                                                             'Description.',
                                                                                              'name': 'SCD'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[3:3]',
                                                                                              'description': 'No '
                                                                                                             'Description.',
                                                                                              'name': 'DUVD'}]},
                                                                        'name': 'BPCR',
                                                                        'size': 0x8},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x1,
                                                                        'description': 'Battery '
                                                                                       'Protection '
                                                                                       'Deep '
                                                                                       'Under '
                                                                                       'Voltage '
                                                                                       'Register',
                                                                        'fields': {'field': [{'access': 'read-write',
                                                                                              'bitRange': '[3:0]',
                                                                                              'description': 'No '
                                                                                                             'Description.',
                                                                                              'enumeratedValues': {'enumeratedValue': [{'description': '4.71V',
                                                                                                                                        'name': '4_71V',
                                                                                                                                        'value': 0x0},
                                                                                                                                       {'description': '5.03V',
                                                                                                                                        'name': '5_03V',
                                                                                                                                        'value': 0x1},
                                                                                                                                       {'description': '5.34V',
                                                                                                                                        'name': '5_34V',
                                                                                                                                        'value': 0x2},
                                                                                                                                       {'description': '5.66V',
                                                                                                                                        'name': '5_66V',
                                                                                                                                        'value': 0x3},
                                                                                                                                       {'description': '5.97V',
                                                                                                                                        'name': '5_97V',
                                                                                                                                        'value': 0x4},
                                                                                                                                       {'description': '6.29V',
                                                                                                                                        'name': '6_29V',
                                                                                                                                        'value': 0x5},
                                                                                                                                       {'description': '6.60V',
                                                                                                                                        'name': '6_60V',
                                                                                                                                        'value': 0x6},
                                                                                                                                       {'description': '6.91V',
                                                                                                                                        'name': '6_91V',
                                                                                                                                        'value': 0x7},
                                                                                                                                       {'description': '7.23V',
                                                                                                                                        'name': '7_23V',
                                                                                                                                        'value': 0x8},
                                                                                                                                       {'description': '7.54V',
                                                                                                                                        'name': '7_54V',
                                                                                                                                        'value': 0x9},
                                                                                                                                       {'description': '7.86V',
                                                                                                                                        'name': '7_86V',
                                                                                                                                        'value': 0xA},
                                                                                                                                       {'description': '8.17V',
                                                                                                                                        'name': '8_17V',
                                                                                                                                        'value': 0xB},
                                                                                                                                       {'description': '8.49V',
                                                                                                                                        'name': '8_49V',
                                                                                                                                        'value': 0xC},
                                                                                                                                       {'description': '8.80V',
                                                                                                                                        'name': '8_80V',
                                                                                                                                        'value': 0xD},
                                                                                                                                       {'description': '9.11V',
                                                                                                                                        'name': '9_11V',
                                                                                                                                        'value': 0xE},
                                                                                                                                       {'description': '9.43V',
                                                                                                                                        'name': '9_43V',
                                                                                                                                        'value': 0xF}]},
                                                                                              'name': 'DUDL',
                                                                                              'writeConstraint': {'useEnumeratedValues': 0x1}},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[5:4]',
                                                                                              'description': 'No '
                                                                                                             'Description.',
                                                                                              'enumeratedValues': {'enumeratedValue': [{'description': '750ms',
                                                                                                                                        'name': '750MS',
                                                                                                                                        'value': 0x0},
                                                                                                                                       {'description': '1000ms',
                                                                                                                                        'name': '1000MS',
                                                                                                                                        'value': 0x1},
                                                                                                                                       {'description': '1250ms',
                                                                                                                                        'name': '1250MS',
                                                                                                                                        'value': 0x2},
                                                                                                                                       {'description': '1500ms',
                                                                                                                                        'name': '1500MS',
                                                                                                                                        'value': 0x3}]},
                                                                                              'name': 'DUVT',
                                                                                              'writeConstraint': {'useEnumeratedValues': 0x1}}]},
                                                                        'name': 'BPDUV',
                                                                        'size': 0x8},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x0,
                                                                        'description': 'Battery '
                                                                                       'Protection '
                                                                                       'Interrupt '
                                                                                       'Register '
                                                                                       '(read-only '
                                                                                       'for '
                                                                                       'debugger)',
                                                                        'fields': {'field': [{'access': 'read-write',
                                                                                              'bitRange': '[0:0]',
                                                                                              'description': 'No '
                                                                                                             'Description.',
                                                                                              'name': 'SCIE'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[1:1]',
                                                                                              'description': 'No '
                                                                                                             'Description.',
                                                                                              'name': 'DOCIE'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[2:2]',
                                                                                              'description': 'No '
                                                                                                             'Description.',
                                                                                              'name': 'COCIE'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[3:3]',
                                                                                              'description': 'Deep '
                                                                                                             'Under-voltage '
                                                                                                             'Early '
                                                                                                             'Warning '
                                                                                                             'Interrupt '
                                                                                                             'Enable',
                                                                                              'name': 'DUVIE'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[4:4]',
                                                                                              'description': 'No '
                                                                                                             'Description.',
                                                                                              'name': 'SCIF'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[5:5]',
                                                                                              'description': 'No '
                                                                                                             'Description.',
                                                                                              'name': 'DOCIF'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[6:6]',
                                                                                              'description': 'Charge '
                                                                                                             'Over-current '
                                                                                                             'Protection '
                                                                                                             'Activated '
                                                                                                             'Interrupt '
                                                                                                             'Flag',
                                                                                              'name': 'COCIF'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[7:7]',
                                                                                              'description': 'Deep '
                                                                                                             'Under-voltage '
                                                                                                             'Early '
                                                                                                             'Warning '
                                                                                                             'Interrupt '
                                                                                                             'Flag',
                                                                                              'name': 'DUVIF'}]},
                                                                        'name': 'BPIR',
                                                                        'size': 0x8},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x3,
                                                                        'description': 'Battery '
                                                                                       'Protection '
                                                                                       'OverCurrent '
                                                                                       'Detection '
                                                                                       'Level '
                                                                                       'Register',
                                                                        'fields': {'field': [{'access': 'read-write',
                                                                                              'bitRange': '[3:0]',
                                                                                              'description': 'No '
                                                                                                             'Description.',
                                                                                              'enumeratedValues': {'enumeratedValue': [{'description': '0.050V',
                                                                                                                                        'name': '0_050V',
                                                                                                                                        'value': 0x0},
                                                                                                                                       {'description': '0.055V',
                                                                                                                                        'name': '0_055V',
                                                                                                                                        'value': 0x1},
                                                                                                                                       {'description': '0.060V',
                                                                                                                                        'name': '0_060V',
                                                                                                                                        'value': 0x2},
                                                                                                                                       {'description': '0.065V',
                                                                                                                                        'name': '0_065V',
                                                                                                                                        'value': 0x3},
                                                                                                                                       {'description': '0.070V',
                                                                                                                                        'name': '0_070V',
                                                                                                                                        'value': 0x4},
                                                                                                                                       {'description': '0.080V',
                                                                                                                                        'name': '0_080V',
                                                                                                                                        'value': 0x5},
                                                                                                                                       {'description': '0.090V',
                                                                                                                                        'name': '0_090V',
                                                                                                                                        'value': 0x6},
                                                                                                                                       {'description': '0.100V',
                                                                                                                                        'name': '0_100V',
                                                                                                                                        'value': 0x7},
                                                                                                                                       {'description': '0.110V',
                                                                                                                                        'name': '0_110V',
                                                                                                                                        'value': 0x8},
                                                                                                                                       {'description': '0.120V',
                                                                                                                                        'name': '0_120V',
                                                                                                                                        'value': 0x9},
                                                                                                                                       {'description': '0.130V',
                                                                                                                                        'name': '0_130V',
                                                                                                                                        'value': 0xA},
                                                                                                                                       {'description': '0.140V',
                                                                                                                                        'name': '0_140V',
                                                                                                                                        'value': 0xB},
                                                                                                                                       {'description': '0.160V',
                                                                                                                                        'name': '0_160V',
                                                                                                                                        'value': 0xC},
                                                                                                                                       {'description': '0.180V',
                                                                                                                                        'name': '0_180V',
                                                                                                                                        'value': 0xD},
                                                                                                                                       {'description': '0.200V',
                                                                                                                                        'name': '0_200V',
                                                                                                                                        'value': 0xE},
                                                                                                                                       {'description': '0.220V',
                                                                                                                                        'name': '0_220V',
                                                                                                                                        'value': 0xF}]},
                                                                                              'name': 'CCDL',
                                                                                              'writeConstraint': {'useEnumeratedValues': 0x1}},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[7:4]',
                                                                                              'description': 'No '
                                                                                                             'Description.',
                                                                                              'enumeratedValues': {'enumeratedValue': [{'description': '0.050V',
                                                                                                                                        'name': '0_050V',
                                                                                                                                        'value': 0x0},
                                                                                                                                       {'description': '0.055V',
                                                                                                                                        'name': '0_055V',
                                                                                                                                        'value': 0x1},
                                                                                                                                       {'description': '0.060V',
                                                                                                                                        'name': '0_060V',
                                                                                                                                        'value': 0x2},
                                                                                                                                       {'description': '0.065V',
                                                                                                                                        'name': '0_065V',
                                                                                                                                        'value': 0x3},
                                                                                                                                       {'description': '0.070V',
                                                                                                                                        'name': '0_070V',
                                                                                                                                        'value': 0x4},
                                                                                                                                       {'description': '0.080V',
                                                                                                                                        'name': '0_080V',
                                                                                                                                        'value': 0x5},
                                                                                                                                       {'description': '0.090V',
                                                                                                                                        'name': '0_090V',
                                                                                                                                        'value': 0x6},
                                                                                                                                       {'description': '0.100V',
                                                                                                                                        'name': '0_100V',
                                                                                                                                        'value': 0x7},
                                                                                                                                       {'description': '0.110V',
                                                                                                                                        'name': '0_110V',
                                                                                                                                        'value': 0x8},
                                                                                                                                       {'description': '0.120V',
                                                                                                                                        'name': '0_120V',
                                                                                                                                        'value': 0x9},
                                                                                                                                       {'description': '0.130V',
                                                                                                                                        'name': '0_130V',
                                                                                                                                        'value': 0xA},
                                                                                                                                       {'description': '0.140V',
                                                                                                                                        'name': '0_140V',
                                                                                                                                        'value': 0xB},
                                                                                                                                       {'description': '0.160V',
                                                                                                                                        'name': '0_160V',
                                                                                                                                        'value': 0xC},
                                                                                                                                       {'description': '0.180V',
                                                                                                                                        'name': '0_180V',
                                                                                                                                        'value': 0xD},
                                                                                                                                       {'description': '0.200V',
                                                                                                                                        'name': '0_200V',
                                                                                                                                        'value': 0xE},
                                                                                                                                       {'description': '0.220V',
                                                                                                                                        'name': '0_220V',
                                                                                                                                        'value': 0xF}]},
                                                                                              'name': 'DCDL',
                                                                                              'writeConstraint': {'useEnumeratedValues': 0x1}}]},
                                                                        'name': 'BPOCD',
                                                                        'size': 0x8},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x6,
                                                                        'description': 'Battery '
                                                                                       'Protection '
                                                                                       'Parameter '
                                                                                       'Lock '
                                                                                       'Register '
                                                                                       '(read-only '
                                                                                       'for '
                                                                                       'debugger)',
                                                                        'fields': {'field': [{'access': 'read-write',
                                                                                              'bitRange': '[0:0]',
                                                                                              'description': 'Battery '
                                                                                                             'Protection '
                                                                                                             'Parameter '
                                                                                                             'Lock',
                                                                                              'name': 'BPPL'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[1:1]',
                                                                                              'description': 'Battery '
                                                                                                             'Protection '
                                                                                                             'Parameter '
                                                                                                             'Lock '
                                                                                                             'Enable',
                                                                                              'name': 'BPPLE'}]},
                                                                        'name': 'BPPLR',
                                                                        'size': 0x8},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x2,
                                                                        'description': 'Battery '
                                                                                       'Protection '
                                                                                       'Short-Circuit '
                                                                                       'Detection '
                                                                                       'Level '
                                                                                       'Register',
                                                                        'fields': {'field': [{'access': 'read-write',
                                                                                              'bitRange': '[3:0]',
                                                                                              'description': 'No '
                                                                                                             'Description.',
                                                                                              'enumeratedValues': {'enumeratedValue': [{'description': '0.100V',
                                                                                                                                        'name': '0_100V',
                                                                                                                                        'value': 0x0},
                                                                                                                                       {'description': '0.110V',
                                                                                                                                        'name': '0_110V',
                                                                                                                                        'value': 0x1},
                                                                                                                                       {'description': '0.120V',
                                                                                                                                        'name': '0_120V',
                                                                                                                                        'value': 0x2},
                                                                                                                                       {'description': '0.130V',
                                                                                                                                        'name': '0_130V',
                                                                                                                                        'value': 0x3},
                                                                                                                                       {'description': '0.140V',
                                                                                                                                        'name': '0_140V',
                                                                                                                                        'value': 0x4},
                                                                                                                                       {'description': '0.160V',
                                                                                                                                        'name': '0_160V',
                                                                                                                                        'value': 0x5},
                                                                                                                                       {'description': '0.180V',
                                                                                                                                        'name': '0_180V',
                                                                                                                                        'value': 0x6},
                                                                                                                                       {'description': '0.200V',
                                                                                                                                        'name': '0_200V',
                                                                                                                                        'value': 0x7},
                                                                                                                                       {'description': '0.220V',
                                                                                                                                        'name': '0_220V',
                                                                                                                                        'value': 0x8},
                                                                                                                                       {'description': '0.240V',
                                                                                                                                        'name': '0_240V',
                                                                                                                                        'value': 0x9},
                                                                                                                                       {'description': '0.260V',
                                                                                                                                        'name': '0_260V',
                                                                                                                                        'value': 0xA},
                                                                                                                                       {'description': '0.280V',
                                                                                                                                        'name': '0_280V',
                                                                                                                                        'value': 0xB},
                                                                                                                                       {'description': '0.320V',
                                                                                                                                        'name': '0_320V',
                                                                                                                                        'value': 0xC},
                                                                                                                                       {'description': '0.360V',
                                                                                                                                        'name': '0_360V',
                                                                                                                                        'value': 0xD},
                                                                                                                                       {'description': '0.400V',
                                                                                                                                        'name': '0_400V',
                                                                                                                                        'value': 0xE},
                                                                                                                                       {'description': '0.440V',
                                                                                                                                        'name': '0_440V',
                                                                                                                                        'value': 0xF}]},
                                                                                              'name': 'SCDL',
                                                                                              'writeConstraint': {'useEnumeratedValues': 0x1}}]},
                                                                        'name': 'BPSCD',
                                                                        'size': 0x8},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x4,
                                                                        'description': 'Current '
                                                                                       'Battery '
                                                                                       'Protection '
                                                                                       'Timing '
                                                                                       'Register',
                                                                        'fields': {'field': [{'access': 'read-write',
                                                                                              'bitRange': '[3:0]',
                                                                                              'description': 'No '
                                                                                                             'Description.',
                                                                                              'enumeratedValues': {'enumeratedValue': [{'description': '1 '
                                                                                                                                                       'ms',
                                                                                                                                        'name': '1_MS',
                                                                                                                                        'value': 0x0},
                                                                                                                                       {'description': '2 '
                                                                                                                                                       'ms',
                                                                                                                                        'name': '2_MS',
                                                                                                                                        'value': 0x1},
                                                                                                                                       {'description': '4 '
                                                                                                                                                       'ms',
                                                                                                                                        'name': '4_MS',
                                                                                                                                        'value': 0x2},
                                                                                                                                       {'description': '6 '
                                                                                                                                                       'ms',
                                                                                                                                        'name': '6_MS',
                                                                                                                                        'value': 0x3},
                                                                                                                                       {'description': '8 '
                                                                                                                                                       'ms',
                                                                                                                                        'name': '8_MS',
                                                                                                                                        'value': 0x4},
                                                                                                                                       {'description': '10 '
                                                                                                                                                       'ms',
                                                                                                                                        'name': '10_MS',
                                                                                                                                        'value': 0x5},
                                                                                                                                       {'description': '12 '
                                                                                                                                                       'ms',
                                                                                                                                        'name': '12_MS',
                                                                                                                                        'value': 0x6},
                                                                                                                                       {'description': '14 '
                                                                                                                                                       'ms',
                                                                                                                                        'name': '14_MS',
                                                                                                                                        'value': 0x7},
                                                                                                                                       {'description': '16 '
                                                                                                                                                       'ms',
                                                                                                                                        'name': '16_MS',
                                                                                                                                        'value': 0x8},
                                                                                                                                       {'description': '18 '
                                                                                                                                                       'ms',
                                                                                                                                        'name': '18_MS',
                                                                                                                                        'value': 0x9},
                                                                                                                                       {'description': '20 '
                                                                                                                                                       'ms',
                                                                                                                                        'name': '20_MS',
                                                                                                                                        'value': 0xA},
                                                                                                                                       {'description': '22 '
                                                                                                                                                       'ms',
                                                                                                                                        'name': '22_MS',
                                                                                                                                        'value': 0xB},
                                                                                                                                       {'description': '24 '
                                                                                                                                                       'ms',
                                                                                                                                        'name': '24_MS',
                                                                                                                                        'value': 0xC},
                                                                                                                                       {'description': '26 '
                                                                                                                                                       'ms',
                                                                                                                                        'name': '26_MS',
                                                                                                                                        'value': 0xD},
                                                                                                                                       {'description': '28 '
                                                                                                                                                       'ms',
                                                                                                                                        'name': '28_MS',
                                                                                                                                        'value': 0xE},
                                                                                                                                       {'description': '30 '
                                                                                                                                                       'ms',
                                                                                                                                        'name': '30_MS',
                                                                                                                                        'value': 0xF}]},
                                                                                              'name': 'OCPT',
                                                                                              'writeConstraint': {'useEnumeratedValues': 0x1}},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[7:4]',
                                                                                              'description': 'No '
                                                                                                             'Description.',
                                                                                              'enumeratedValues': {'enumeratedValue': [{'description': '61 '
                                                                                                                                                       'us',
                                                                                                                                        'name': '61_US',
                                                                                                                                        'value': 0x0},
                                                                                                                                       {'description': '122 '
                                                                                                                                                       'us',
                                                                                                                                        'name': '122_US',
                                                                                                                                        'value': 0x1},
                                                                                                                                       {'description': '183 '
                                                                                                                                                       'us',
                                                                                                                                        'name': '183_US',
                                                                                                                                        'value': 0x2},
                                                                                                                                       {'description': '244 '
                                                                                                                                                       'us',
                                                                                                                                        'name': '244_US',
                                                                                                                                        'value': 0x3},
                                                                                                                                       {'description': '305 '
                                                                                                                                                       'us',
                                                                                                                                        'name': '305_US',
                                                                                                                                        'value': 0x4},
                                                                                                                                       {'description': '366 '
                                                                                                                                                       'us',
                                                                                                                                        'name': '366_US',
                                                                                                                                        'value': 0x5},
                                                                                                                                       {'description': '427 '
                                                                                                                                                       'us',
                                                                                                                                        'name': '427_US',
                                                                                                                                        'value': 0x6},
                                                                                                                                       {'description': '488 '
                                                                                                                                                       'us',
                                                                                                                                        'name': '488_US',
                                                                                                                                        'value': 0x7},
                                                                                                                                       {'description': '610 '
                                                                                                                                                       'us',
                                                                                                                                        'name': '610_US',
                                                                                                                                        'value': 0x8},
                                                                                                                                       {'description': '732 '
                                                                                                                                                       'us',
                                                                                                                                        'name': '732_US',
                                                                                                                                        'value': 0x9},
                                                                                                                                       {'description': '854 '
                                                                                                                                                       'us',
                                                                                                                                        'name': '854_US',
                                                                                                                                        'value': 0xA},
                                                                                                                                       {'description': '976 '
                                                                                                                                                       'us',
                                                                                                                                        'name': '976_US',
                                                                                                                                        'value': 0xB},
                                                                                                                                       {'description': '1098 '
                                                                                                                                                       'us',
                                                                                                                                        'name': '1098_US',
                                                                                                                                        'value': 0xC},
                                                                                                                                       {'description': '1220 '
                                                                                                                                                       'us',
                                                                                                                                        'name': '1220_US',
                                                                                                                                        'value': 0xD},
                                                                                                                                       {'description': '1342 '
                                                                                                                                                       'us',
                                                                                                                                        'name': '1342_US',
                                                                                                                                        'value': 0xE},
                                                                                                                                       {'description': '1464 '
                                                                                                                                                       'us',
                                                                                                                                        'name': '1464_US',
                                                                                                                                        'value': 0xF}]},
                                                                                              'name': 'SCPT',
                                                                                              'writeConstraint': {'useEnumeratedValues': 0x1}}]},
                                                                        'name': 'CBPTR',
                                                                        'size': 0x8}]}},
                                           {'addressBlock': [{'offset': 0x0,
                                                              'size': 0x1,
                                                              'usage': 'registers'}],
                                            'baseAddress': 0x800057,
                                            'description': 'Bootloader',
                                            'name': 'BOOT_LOAD',
                                            'registers': {'register': [{'access': 'read-write',
                                                                        'addressOffset': 0x0,
                                                                        'description': 'Store '
                                                                                       'Program '
                                                                                       'Memory '
                                                                                       'Control '
                                                                                       'Register',
                                                                        'fields': {'field': [{'access': 'read-write',
                                                                                              'bitRange': '[0:0]',
                                                                                              'description': 'Store '
                                                                                                             'Program '
                                                                                                             'Memory '
                                                                                                             'Enable',
                                                                                              'name': 'SPMEN'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[1:1]',
                                                                                              'description': 'Page '
                                                                                                             'Erase',
                                                                                              'name': 'PGERS'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[2:2]',
                                                                                              'description': 'Page '
                                                                                                             'Write',
                                                                                              'name': 'PGWRT'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[3:3]',
                                                                                              'description': 'Boot '
                                                                                                             'Lock '
                                                                                                             'Bit '
                                                                                                             'Set',
                                                                                              'name': 'BLBSET'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[4:4]',
                                                                                              'description': 'Read '
                                                                                                             'While '
                                                                                                             'Write '
                                                                                                             'section '
                                                                                                             'read '
                                                                                                             'enable',
                                                                                              'name': 'RWWSRE'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[5:5]',
                                                                                              'description': 'Signature '
                                                                                                             'Row '
                                                                                                             'Read',
                                                                                              'name': 'SIGRD'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[6:6]',
                                                                                              'description': 'Read '
                                                                                                             'While '
                                                                                                             'Write '
                                                                                                             'Section '
                                                                                                             'Busy',
                                                                                              'name': 'RWWSB'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[7:7]',
                                                                                              'description': 'SPM '
                                                                                                             'Interrupt '
                                                                                                             'Enable',
                                                                                              'name': 'SPMIE'}]},
                                                                        'name': 'SPMCSR',
                                                                        'size': 0x8}]}},
                                           {'addressBlock': [{'offset': 0x0,
                                                              'size': 0x1,
                                                              'usage': 'registers'}],
                                            'baseAddress': 0x8000F1,
                                            'description': 'Cell Balancing',
                                            'name': 'CELL_BALANCING',
                                            'registers': {'register': [{'access': 'read-write',
                                                                        'addressOffset': 0x0,
                                                                        'description': 'Cell '
                                                                                       'Balancing '
                                                                                       'Control '
                                                                                       'Register',
                                                                        'fields': {'field': [{'access': 'read-write',
                                                                                              'bitRange': '[3:0]',
                                                                                              'description': 'Cell '
                                                                                                             'Balancing '
                                                                                                             'Enables',
                                                                                              'name': 'CBE',
                                                                                              'writeConstraint': {'range': {'maximum': 0xF,
                                                                                                                            'minimum': 0x0}}}]},
                                                                        'name': 'CBCR',
                                                                        'size': 0x8}]}},
                                           {'addressBlock': [{'offset': 0x0,
                                                              'size': 0xA,
                                                              'usage': 'registers'}],
                                            'baseAddress': 0x8000E0,
                                            'description': 'Coulomb Counter',
                                            'name': 'COULOMB_COUNTER',
                                            'registers': {'register': [{'access': 'read-write',
                                                                        'addressOffset': 0x0,
                                                                        'description': 'ADC '
                                                                                       'Accumulate '
                                                                                       'Current '
                                                                                       '(read-only '
                                                                                       'for '
                                                                                       'debugger)',
                                                                        'name': 'CADAC0',
                                                                        'size': 0x8,
                                                                        'writeConstraint': {'range': {'maximum': 0xFF,
                                                                                                      'minimum': 0x0}}},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x1,
                                                                        'description': 'ADC '
                                                                                       'Accumulate '
                                                                                       'Current '
                                                                                       '(read-only '
                                                                                       'for '
                                                                                       'debugger)',
                                                                        'name': 'CADAC1',
                                                                        'size': 0x8,
                                                                        'writeConstraint': {'range': {'maximum': 0xFF,
                                                                                                      'minimum': 0x0}}},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x2,
                                                                        'description': 'ADC '
                                                                                       'Accumulate '
                                                                                       'Current '
                                                                                       '(read-only '
                                                                                       'for '
                                                                                       'debugger)',
                                                                        'name': 'CADAC2',
                                                                        'size': 0x8,
                                                                        'writeConstraint': {'range': {'maximum': 0xFF,
                                                                                                      'minimum': 0x0}}},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x3,
                                                                        'description': 'ADC '
                                                                                       'Accumulate '
                                                                                       'Current '
                                                                                       '(read-only '
                                                                                       'for '
                                                                                       'debugger)',
                                                                        'name': 'CADAC3',
                                                                        'size': 0x8,
                                                                        'writeConstraint': {'range': {'maximum': 0xFF,
                                                                                                      'minimum': 0x0}}},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x4,
                                                                        'description': 'CC-ADC '
                                                                                       'Control '
                                                                                       'and '
                                                                                       'Status '
                                                                                       'Register '
                                                                                       'A',
                                                                        'fields': {'field': [{'access': 'read-write',
                                                                                              'bitRange': '[0:0]',
                                                                                              'description': 'When '
                                                                                                             'the '
                                                                                                             'CADSE '
                                                                                                             'bit '
                                                                                                             'is '
                                                                                                             'written '
                                                                                                             'to '
                                                                                                             'one, '
                                                                                                             'the '
                                                                                                             'ongoing '
                                                                                                             'CC-ADC '
                                                                                                             'conversion '
                                                                                                             'is '
                                                                                                             'aborted, '
                                                                                                             'and '
                                                                                                             'the '
                                                                                                             'CC-ADC '
                                                                                                             'enters '
                                                                                                             'Regular '
                                                                                                             'Current '
                                                                                                             'detection '
                                                                                                             'mode.',
                                                                                              'name': 'CADSE'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[2:1]',
                                                                                              'description': 'The '
                                                                                                             'CADSI '
                                                                                                             'bits '
                                                                                                             'determine '
                                                                                                             'the '
                                                                                                             'current '
                                                                                                             'sampling '
                                                                                                             'interval '
                                                                                                             'for '
                                                                                                             'the '
                                                                                                             'Regular '
                                                                                                             'Current '
                                                                                                             'detection '
                                                                                                             'in '
                                                                                                             'Power-down '
                                                                                                             'mode. '
                                                                                                             'The '
                                                                                                             'actual '
                                                                                                             'settings '
                                                                                                             'remain '
                                                                                                             'to '
                                                                                                             'be '
                                                                                                             'determined.',
                                                                                              'enumeratedValues': {'enumeratedValue': [{'description': '125ms',
                                                                                                                                        'name': '125MS',
                                                                                                                                        'value': 0x0},
                                                                                                                                       {'description': '250ms',
                                                                                                                                        'name': '250MS',
                                                                                                                                        'value': 0x1},
                                                                                                                                       {'description': '500ms',
                                                                                                                                        'name': '500MS',
                                                                                                                                        'value': 0x2},
                                                                                                                                       {'description': '1000ms',
                                                                                                                                        'name': '1000MS',
                                                                                                                                        'value': 0x3}]},
                                                                                              'name': 'CADSI',
                                                                                              'writeConstraint': {'useEnumeratedValues': 0x1}},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[4:3]',
                                                                                              'description': 'CC_ADC '
                                                                                                             'Accumulate '
                                                                                                             'Current '
                                                                                                             'Select '
                                                                                                             'Bits',
                                                                                              'enumeratedValues': {'enumeratedValue': [{'description': '125ms',
                                                                                                                                        'name': '125MS',
                                                                                                                                        'value': 0x0},
                                                                                                                                       {'description': '250ms',
                                                                                                                                        'name': '250MS',
                                                                                                                                        'value': 0x1},
                                                                                                                                       {'description': '500ms',
                                                                                                                                        'name': '500MS',
                                                                                                                                        'value': 0x2},
                                                                                                                                       {'description': '1000ms',
                                                                                                                                        'name': '1000MS',
                                                                                                                                        'value': 0x3}]},
                                                                                              'name': 'CADAS',
                                                                                              'writeConstraint': {'useEnumeratedValues': 0x1}},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[5:5]',
                                                                                              'description': 'CC_ADC '
                                                                                                             'Update '
                                                                                                             'Busy',
                                                                                              'name': 'CADUB'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[7:7]',
                                                                                              'description': 'When '
                                                                                                             'the '
                                                                                                             'CADEN '
                                                                                                             'bit '
                                                                                                             'is '
                                                                                                             'cleared '
                                                                                                             '(zero), '
                                                                                                             'the '
                                                                                                             'CC-ADC '
                                                                                                             'is '
                                                                                                             'disabled. '
                                                                                                             'When '
                                                                                                             'the '
                                                                                                             'CADEN '
                                                                                                             'bit '
                                                                                                             'is '
                                                                                                             'set '
                                                                                                             '(one), '
                                                                                                             'the '
                                                                                                             'CC-ADC '
                                                                                                             'will '
                                                                                                             'continuously '
                                                                                                             'measure '
                                                                                                             'the '
                                                                                                             'voltage '
                                                                                                             'drop '
                                                                                                             'over '
                                                                                                             'the '
                                                                                                             'external '
                                                                                                             'sense '
                                                                                                             'resistor '
                                                                                                             'RSENSE. '
                                                                                                             'In '
                                                                                                             'Power-down, '
                                                                                                             'only '
                                                                                                             'the '
                                                                                                             'Regular '
                                                                                                             'Current '
                                                                                                             'detection '
                                                                                                             'is '
                                                                                                             'active. '
                                                                                                             'In '
                                                                                                             'Power-off, '
                                                                                                             'the '
                                                                                                             'CC-ADC '
                                                                                                             'is '
                                                                                                             'always '
                                                                                                             'disabled.',
                                                                                              'name': 'CADEN'}]},
                                                                        'name': 'CADCSRA',
                                                                        'size': 0x8},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x5,
                                                                        'description': 'CC-ADC '
                                                                                       'Control '
                                                                                       'and '
                                                                                       'Status '
                                                                                       'Register '
                                                                                       'B '
                                                                                       '(read-only '
                                                                                       'for '
                                                                                       'debugger)',
                                                                        'fields': {'field': [{'access': 'read-write',
                                                                                              'bitRange': '[0:0]',
                                                                                              'description': 'CC-ADC '
                                                                                                             'Instantaneous '
                                                                                                             'Current '
                                                                                                             'Interrupt '
                                                                                                             'Flag',
                                                                                              'name': 'CADICIF'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[1:1]',
                                                                                              'description': 'CC-ADC '
                                                                                                             'Accumulate '
                                                                                                             'Current '
                                                                                                             'Interrupt '
                                                                                                             'Flag',
                                                                                              'name': 'CADRCIF'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[2:2]',
                                                                                              'description': 'CC-ADC '
                                                                                                             'Accumulate '
                                                                                                             'Current '
                                                                                                             'Interrupt '
                                                                                                             'Flag',
                                                                                              'name': 'CADACIF'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[4:4]',
                                                                                              'description': 'CAD '
                                                                                                             'Instantaneous '
                                                                                                             'Current '
                                                                                                             'Interrupt '
                                                                                                             'Enable',
                                                                                              'name': 'CADICIE'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[5:5]',
                                                                                              'description': 'Regular '
                                                                                                             'Current '
                                                                                                             'Interrupt '
                                                                                                             'Enable',
                                                                                              'name': 'CADRCIE'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[6:6]',
                                                                                              'description': 'No '
                                                                                                             'Description.',
                                                                                              'name': 'CADACIE'}]},
                                                                        'name': 'CADCSRB',
                                                                        'size': 0x8},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x8,
                                                                        'description': 'CC-ADC '
                                                                                       'Instantaneous '
                                                                                       'Current',
                                                                        'name': 'CADIC',
                                                                        'size': 0x10,
                                                                        'writeConstraint': {'range': {'maximum': 0xFFFF,
                                                                                                      'minimum': 0x0}}},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x6,
                                                                        'description': 'CC-ADC '
                                                                                       'Regular '
                                                                                       'Charge '
                                                                                       'Current',
                                                                        'name': 'CADRCC',
                                                                        'size': 0x8,
                                                                        'writeConstraint': {'range': {'maximum': 0xFF,
                                                                                                      'minimum': 0x0}}},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x7,
                                                                        'description': 'CC-ADC '
                                                                                       'Regular '
                                                                                       'Discharge '
                                                                                       'Current',
                                                                        'name': 'CADRDC',
                                                                        'size': 0x8,
                                                                        'writeConstraint': {'range': {'maximum': 0xFF,
                                                                                                      'minimum': 0x0}}}]}},
                                           {'addressBlock': [{'offset': 0x0,
                                                              'size': 0x1,
                                                              'usage': 'registers'},
                                                             {'offset': 0xC,
                                                              'size': 0x2,
                                                              'usage': 'registers'},
                                                             {'offset': 0x15,
                                                              'size': 0x3,
                                                              'usage': 'registers'},
                                                             {'offset': 0x1F,
                                                              'size': 0x3,
                                                              'usage': 'registers'},
                                                             {'offset': 0x26,
                                                              'size': 0x1,
                                                              'usage': 'registers'},
                                                             {'offset': 0x28,
                                                              'size': 0x1,
                                                              'usage': 'registers'},
                                                             {'offset': 0x40,
                                                              'size': 0x1,
                                                              'usage': 'registers'},
                                                             {'offset': 0x82,
                                                              'size': 0x1,
                                                              'usage': 'registers'}],
                                            'baseAddress': 0x80003E,
                                            'description': 'CPU Registers',
                                            'interrupt': [{'description': 'External '
                                                                          'Pin, '
                                                                          'Power-on '
                                                                          'Reset, '
                                                                          'Brown-out '
                                                                          'Reset '
                                                                          'and '
                                                                          'Watchdog '
                                                                          'Reset',
                                                           'name': 'RESET',
                                                           'value': 0x0},
                                                          {'description': 'Battery '
                                                                          'Protection '
                                                                          'Interrupt',
                                                           'name': 'BPINT',
                                                           'value': 0x1},
                                                          {'description': 'External '
                                                                          'Interrupt '
                                                                          'Request '
                                                                          '0',
                                                           'name': 'INT0',
                                                           'value': 0x2},
                                                          {'description': 'External '
                                                                          'Interrupt '
                                                                          'Request '
                                                                          '1',
                                                           'name': 'INT1',
                                                           'value': 0x3},
                                                          {'description': 'External '
                                                                          'Interrupt '
                                                                          'Request '
                                                                          '2',
                                                           'name': 'INT2',
                                                           'value': 0x4},
                                                          {'description': 'External '
                                                                          'Interrupt '
                                                                          'Request '
                                                                          '3',
                                                           'name': 'INT3',
                                                           'value': 0x5},
                                                          {'description': 'Pin '
                                                                          'Change '
                                                                          'Interrupt '
                                                                          '0',
                                                           'name': 'PCINT0',
                                                           'value': 0x6},
                                                          {'description': 'Pin '
                                                                          'Change '
                                                                          'Interrupt '
                                                                          '1',
                                                           'name': 'PCINT1',
                                                           'value': 0x7},
                                                          {'description': 'Watchdog '
                                                                          'Timeout '
                                                                          'Interrupt',
                                                           'name': 'WDT',
                                                           'value': 0x8},
                                                          {'description': 'Wakeup '
                                                                          'timer '
                                                                          'overflow',
                                                           'name': 'WAKE_UP',
                                                           'value': 0x9},
                                                          {'description': 'Timer/Counter '
                                                                          '1 '
                                                                          'Compare '
                                                                          'Match',
                                                           'name': 'TIM1_COMP',
                                                           'value': 0xA},
                                                          {'description': 'Timer/Counter '
                                                                          '1 '
                                                                          'Overflow',
                                                           'name': 'TIM1_OVF',
                                                           'value': 0xB},
                                                          {'description': 'Timer/Counter0 '
                                                                          'Compare '
                                                                          'A '
                                                                          'Match',
                                                           'name': 'TIM0_COMPA',
                                                           'value': 0xC},
                                                          {'description': 'Timer/Counter0 '
                                                                          'Compare '
                                                                          'B '
                                                                          'Match',
                                                           'name': 'TIM0_COMPB',
                                                           'value': 0xD},
                                                          {'description': 'Timer/Counter0 '
                                                                          'Overflow',
                                                           'name': 'TIM0_OVF',
                                                           'value': 0xE},
                                                          {'description': 'Two-Wire '
                                                                          'Bus '
                                                                          'Connect/Disconnect',
                                                           'name': 'TWI_BUS_CD',
                                                           'value': 0xF},
                                                          {'description': 'Two-Wire '
                                                                          'Serial '
                                                                          'Interface',
                                                           'name': 'TWI',
                                                           'value': 0x10},
                                                          {'description': 'Voltage '
                                                                          'ADC '
                                                                          'Conversion '
                                                                          'Complete',
                                                           'name': 'VADC',
                                                           'value': 0x11},
                                                          {'description': 'Coulomb '
                                                                          'Counter '
                                                                          'ADC '
                                                                          'Conversion '
                                                                          'Complete',
                                                           'name': 'CCADC_CONV',
                                                           'value': 0x12},
                                                          {'description': 'Coloumb '
                                                                          'Counter '
                                                                          'ADC '
                                                                          'Regular '
                                                                          'Current',
                                                           'name': 'CCADC_REG_CUR',
                                                           'value': 0x13},
                                                          {'description': 'Coloumb '
                                                                          'Counter '
                                                                          'ADC '
                                                                          'Accumulator',
                                                           'name': 'CCADC_ACC',
                                                           'value': 0x14},
                                                          {'description': 'EEPROM '
                                                                          'Ready',
                                                           'name': 'EE_READY',
                                                           'value': 0x15},
                                                          {'description': 'Store '
                                                                          'Program '
                                                                          'Memory '
                                                                          'Ready',
                                                           'name': 'SPM_READY',
                                                           'value': 0x16}],
                                            'name': 'CPU',
                                            'registers': {'register': [{'access': 'read-write',
                                                                        'addressOffset': 0x82,
                                                                        'description': 'Clock '
                                                                                       'Control '
                                                                                       'and '
                                                                                       'Status '
                                                                                       'Register',
                                                                        'fields': {'field': [{'access': 'read-write',
                                                                                              'bitRange': '[0:0]',
                                                                                              'description': 'Asynchronous '
                                                                                                             'Clock '
                                                                                                             'Select',
                                                                                              'name': 'ACS'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[1:1]',
                                                                                              'description': '32 '
                                                                                                             'kHz '
                                                                                                             'Crystal '
                                                                                                             'Oscillator '
                                                                                                             'Enable',
                                                                                              'name': 'XOE'}]},
                                                                        'name': 'CCSR',
                                                                        'size': 0x8},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x40,
                                                                        'description': 'Digital '
                                                                                       'Input '
                                                                                       'Disable '
                                                                                       'Register',
                                                                        'name': 'DIDR0',
                                                                        'size': 0x8,
                                                                        'writeConstraint': {'range': {'maximum': 0xFF,
                                                                                                      'minimum': 0x0}}},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x28,
                                                                        'description': 'Fast '
                                                                                       'Oscillator '
                                                                                       'Calibration '
                                                                                       'Value',
                                                                        'name': 'FOSCCAL',
                                                                        'size': 0x8,
                                                                        'writeConstraint': {'range': {'maximum': 0xFF,
                                                                                                      'minimum': 0x0}}},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x0,
                                                                        'description': 'General '
                                                                                       'Purpose '
                                                                                       'IO '
                                                                                       'Register '
                                                                                       '0',
                                                                        'name': 'GPIOR0',
                                                                        'size': 0x8,
                                                                        'writeConstraint': {'range': {'maximum': 0xFF,
                                                                                                      'minimum': 0x0}}},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0xC,
                                                                        'description': 'General '
                                                                                       'Purpose '
                                                                                       'IO '
                                                                                       'Register '
                                                                                       '1',
                                                                        'name': 'GPIOR1',
                                                                        'size': 0x8,
                                                                        'writeConstraint': {'range': {'maximum': 0xFF,
                                                                                                      'minimum': 0x0}}},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0xD,
                                                                        'description': 'General '
                                                                                       'Purpose '
                                                                                       'IO '
                                                                                       'Register '
                                                                                       '2',
                                                                        'name': 'GPIOR2',
                                                                        'size': 0x8,
                                                                        'writeConstraint': {'range': {'maximum': 0xFF,
                                                                                                      'minimum': 0x0}}},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x17,
                                                                        'description': 'MCU '
                                                                                       'Control '
                                                                                       'Register',
                                                                        'fields': {'field': [{'access': 'read-write',
                                                                                              'bitRange': '[0:0]',
                                                                                              'description': 'Interrupt '
                                                                                                             'Vector '
                                                                                                             'Change '
                                                                                                             'Enable',
                                                                                              'name': 'IVCE'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[1:1]',
                                                                                              'description': 'Interrupt '
                                                                                                             'Vector '
                                                                                                             'Select',
                                                                                              'name': 'IVSEL'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[4:4]',
                                                                                              'description': 'Pull-up '
                                                                                                             'disable',
                                                                                              'name': 'PUD'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[7:7]',
                                                                                              'description': 'JTAG '
                                                                                                             'Disable',
                                                                                              'name': 'JTD'}]},
                                                                        'name': 'MCUCR',
                                                                        'size': 0x8},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x16,
                                                                        'description': 'MCU '
                                                                                       'Status '
                                                                                       'Register',
                                                                        'fields': {'field': [{'access': 'read-write',
                                                                                              'bitRange': '[0:0]',
                                                                                              'description': 'Power-on '
                                                                                                             'reset '
                                                                                                             'flag',
                                                                                              'name': 'PORF'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[1:1]',
                                                                                              'description': 'External '
                                                                                                             'Reset '
                                                                                                             'Flag',
                                                                                              'name': 'EXTRF'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[2:2]',
                                                                                              'description': 'Brown-out '
                                                                                                             'Reset '
                                                                                                             'Flag',
                                                                                              'name': 'BODRF'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[3:3]',
                                                                                              'description': 'Watchdog '
                                                                                                             'Reset '
                                                                                                             'Flag',
                                                                                              'name': 'WDRF'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[4:4]',
                                                                                              'description': 'JTAG '
                                                                                                             'Reset '
                                                                                                             'Flag',
                                                                                              'name': 'JTRF'}]},
                                                                        'name': 'MCUSR',
                                                                        'size': 0x8},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x26,
                                                                        'description': 'Power '
                                                                                       'Reduction '
                                                                                       'Register '
                                                                                       '0',
                                                                        'fields': {'field': [{'access': 'read-write',
                                                                                              'bitRange': '[0:0]',
                                                                                              'description': 'Power '
                                                                                                             'Reduction '
                                                                                                             'V-ADC',
                                                                                              'name': 'PRVADC'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[1:1]',
                                                                                              'description': 'Power '
                                                                                                             'Reduction '
                                                                                                             'Timer/Counter0',
                                                                                              'name': 'PRTIM0'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[2:2]',
                                                                                              'description': 'Power '
                                                                                                             'Reduction '
                                                                                                             'Timer/Counter1',
                                                                                              'name': 'PRTIM1'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[3:3]',
                                                                                              'description': 'Power '
                                                                                                             'Reduction '
                                                                                                             'TWI',
                                                                                              'name': 'PRTWI'}]},
                                                                        'name': 'PRR0',
                                                                        'size': 0x8},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x15,
                                                                        'description': 'Sleep '
                                                                                       'Mode '
                                                                                       'Control '
                                                                                       'Register',
                                                                        'fields': {'field': [{'access': 'read-write',
                                                                                              'bitRange': '[0:0]',
                                                                                              'description': 'Sleep '
                                                                                                             'Enable',
                                                                                              'name': 'SE'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[3:1]',
                                                                                              'description': 'Sleep '
                                                                                                             'Mode '
                                                                                                             'Select '
                                                                                                             'bits',
                                                                                              'enumeratedValues': {'enumeratedValue': [{'description': 'Idle',
                                                                                                                                        'name': 'IDLE',
                                                                                                                                        'value': 0x0},
                                                                                                                                       {'description': 'ADC '
                                                                                                                                                       'Noise '
                                                                                                                                                       'Reduction '
                                                                                                                                                       '(If '
                                                                                                                                                       'Available)',
                                                                                                                                        'name': 'ADC',
                                                                                                                                        'value': 0x1},
                                                                                                                                       {'description': 'Power '
                                                                                                                                                       'Down',
                                                                                                                                        'name': 'PDOWN',
                                                                                                                                        'value': 0x2},
                                                                                                                                       {'description': 'Power '
                                                                                                                                                       'Save',
                                                                                                                                        'name': 'PSAVE',
                                                                                                                                        'value': 0x3},
                                                                                                                                       {'description': 'Power '
                                                                                                                                                       'Off',
                                                                                                                                        'name': 'POFF',
                                                                                                                                        'value': 0x4},
                                                                                                                                       {'description': 'Reserved',
                                                                                                                                        'name': 'VAL_0x05',
                                                                                                                                        'value': 0x5},
                                                                                                                                       {'description': 'Reserved',
                                                                                                                                        'name': 'VAL_0x06',
                                                                                                                                        'value': 0x6},
                                                                                                                                       {'description': 'Reserved',
                                                                                                                                        'name': 'VAL_0x07',
                                                                                                                                        'value': 0x7}]},
                                                                                              'name': 'SM',
                                                                                              'writeConstraint': {'useEnumeratedValues': 0x1}}]},
                                                                        'name': 'SMCR',
                                                                        'size': 0x8},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x1F,
                                                                        'description': 'Stack '
                                                                                       'Pointer ',
                                                                        'name': 'SP',
                                                                        'size': 0x10,
                                                                        'writeConstraint': {'range': {'maximum': 0xFFFF,
                                                                                                      'minimum': 0x0}}},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x21,
                                                                        'description': 'Status '
                                                                                       'Register',
                                                                        'fields': {'field': [{'access': 'read-write',
                                                                                              'bitRange': '[0:0]',
                                                                                              'description': 'Carry '
                                                                                                             'Flag',
                                                                                              'name': 'C'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[1:1]',
                                                                                              'description': 'Zero '
                                                                                                             'Flag',
                                                                                              'name': 'Z'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[2:2]',
                                                                                              'description': 'Negative '
                                                                                                             'Flag',
                                                                                              'name': 'N'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[3:3]',
                                                                                              'description': "Two's "
                                                                                                             'Complement '
                                                                                                             'Overflow '
                                                                                                             'Flag',
                                                                                              'name': 'V'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[4:4]',
                                                                                              'description': 'Sign '
                                                                                                             'Bit',
                                                                                              'name': 'S'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[5:5]',
                                                                                              'description': 'Half '
                                                                                                             'Carry '
                                                                                                             'Flag',
                                                                                              'name': 'H'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[6:6]',
                                                                                              'description': 'Bit '
                                                                                                             'Copy '
                                                                                                             'Storage',
                                                                                              'name': 'T'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[7:7]',
                                                                                              'description': 'Global '
                                                                                                             'Interrupt '
                                                                                                             'Enable',
                                                                                              'name': 'I'}]},
                                                                        'name': 'SREG',
                                                                        'size': 0x8}]}},
                                           {'addressBlock': [{'offset': 0x0,
                                                              'size': 0x4,
                                                              'usage': 'registers'}],
                                            'baseAddress': 0x80003F,
                                            'description': 'EEPROM',
                                            'name': 'EEPROM',
                                            'registers': {'register': [{'access': 'read-write',
                                                                        'addressOffset': 0x2,
                                                                        'description': 'EEPROM '
                                                                                       'Address '
                                                                                       'Register  '
                                                                                       'Bytes',
                                                                        'name': 'EEAR',
                                                                        'size': 0x10,
                                                                        'writeConstraint': {'range': {'maximum': 0xFFFF,
                                                                                                      'minimum': 0x0}}},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x0,
                                                                        'description': 'EEPROM '
                                                                                       'Control '
                                                                                       'Register',
                                                                        'fields': {'field': [{'access': 'read-write',
                                                                                              'bitRange': '[0:0]',
                                                                                              'description': 'EEPROM '
                                                                                                             'Read '
                                                                                                             'Enable',
                                                                                              'name': 'EERE'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[1:1]',
                                                                                              'description': 'EEPROM '
                                                                                                             'Programming '
                                                                                                             'Enable',
                                                                                              'name': 'EEPE'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[2:2]',
                                                                                              'description': 'EEPROM '
                                                                                                             'Master '
                                                                                                             'Programming '
                                                                                                             'Enable',
                                                                                              'name': 'EEMPE'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[3:3]',
                                                                                              'description': 'EEPROM '
                                                                                                             'Ready '
                                                                                                             'Interrupt '
                                                                                                             'Enable',
                                                                                              'name': 'EERIE'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[5:4]',
                                                                                              'description': 'EEPROM '
                                                                                                             'Programming '
                                                                                                             'Mode '
                                                                                                             'Bits',
                                                                                              'enumeratedValues': {'enumeratedValue': [{'description': 'Erase '
                                                                                                                                                       'and '
                                                                                                                                                       'Write '
                                                                                                                                                       'in '
                                                                                                                                                       'one '
                                                                                                                                                       'operation',
                                                                                                                                        'name': 'ERASE_AND_WRITE_IN_ONE_OPERATION',
                                                                                                                                        'value': 0x0},
                                                                                                                                       {'description': 'Erase '
                                                                                                                                                       'Only',
                                                                                                                                        'name': 'ERASE_ONLY',
                                                                                                                                        'value': 0x1},
                                                                                                                                       {'description': 'Write '
                                                                                                                                                       'Only',
                                                                                                                                        'name': 'WRITE_ONLY',
                                                                                                                                        'value': 0x2}]},
                                                                                              'name': 'EEPM',
                                                                                              'writeConstraint': {'useEnumeratedValues': 0x1}}]},
                                                                        'name': 'EECR',
                                                                        'size': 0x8},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x1,
                                                                        'description': 'EEPROM '
                                                                                       'Data '
                                                                                       'Register',
                                                                        'name': 'EEDR',
                                                                        'size': 0x8,
                                                                        'writeConstraint': {'range': {'maximum': 0xFF,
                                                                                                      'minimum': 0x0}}}]}},
                                           {'addressBlock': [{'offset': 0x0,
                                                              'size': 0x3,
                                                              'usage': 'registers'},
                                                             {'offset': 0x2D,
                                                              'size': 0x2,
                                                              'usage': 'registers'},
                                                             {'offset': 0x30,
                                                              'size': 0x2,
                                                              'usage': 'registers'}],
                                            'baseAddress': 0x80003B,
                                            'description': 'External '
                                                           'Interrupts',
                                            'name': 'EXINT',
                                            'registers': {'register': [{'access': 'read-write',
                                                                        'addressOffset': 0x2E,
                                                                        'description': 'External '
                                                                                       'Interrupt '
                                                                                       'Control '
                                                                                       'Register',
                                                                        'fields': {'field': [{'access': 'read-write',
                                                                                              'bitRange': '[1:0]',
                                                                                              'description': 'External '
                                                                                                             'Interrupt '
                                                                                                             'Sense '
                                                                                                             'Control '
                                                                                                             '0 '
                                                                                                             'Bits',
                                                                                              'enumeratedValues': {'enumeratedValue': [{'description': 'Low '
                                                                                                                                                       'Level '
                                                                                                                                                       'of '
                                                                                                                                                       'INTX',
                                                                                                                                        'name': 'LOW_LEVEL_OF_INTX',
                                                                                                                                        'value': 0x0},
                                                                                                                                       {'description': 'Any '
                                                                                                                                                       'Logical '
                                                                                                                                                       'Change '
                                                                                                                                                       'of '
                                                                                                                                                       'INTX',
                                                                                                                                        'name': 'ANY_LOGICAL_CHANGE_OF_INTX',
                                                                                                                                        'value': 0x1},
                                                                                                                                       {'description': 'Falling '
                                                                                                                                                       'Edge '
                                                                                                                                                       'of '
                                                                                                                                                       'INTX',
                                                                                                                                        'name': 'FALLING_EDGE_OF_INTX',
                                                                                                                                        'value': 0x2},
                                                                                                                                       {'description': 'Rising '
                                                                                                                                                       'Edge '
                                                                                                                                                       'of '
                                                                                                                                                       'INTX',
                                                                                                                                        'name': 'RISING_EDGE_OF_INTX',
                                                                                                                                        'value': 0x3}]},
                                                                                              'name': 'ISC0',
                                                                                              'writeConstraint': {'useEnumeratedValues': 0x1}},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[3:2]',
                                                                                              'description': 'External '
                                                                                                             'Interrupt '
                                                                                                             'Sense '
                                                                                                             'Control '
                                                                                                             '1 '
                                                                                                             'Bits',
                                                                                              'enumeratedValues': {'enumeratedValue': [{'description': 'Low '
                                                                                                                                                       'Level '
                                                                                                                                                       'of '
                                                                                                                                                       'INTX',
                                                                                                                                        'name': 'LOW_LEVEL_OF_INTX',
                                                                                                                                        'value': 0x0},
                                                                                                                                       {'description': 'Any '
                                                                                                                                                       'Logical '
                                                                                                                                                       'Change '
                                                                                                                                                       'of '
                                                                                                                                                       'INTX',
                                                                                                                                        'name': 'ANY_LOGICAL_CHANGE_OF_INTX',
                                                                                                                                        'value': 0x1},
                                                                                                                                       {'description': 'Falling '
                                                                                                                                                       'Edge '
                                                                                                                                                       'of '
                                                                                                                                                       'INTX',
                                                                                                                                        'name': 'FALLING_EDGE_OF_INTX',
                                                                                                                                        'value': 0x2},
                                                                                                                                       {'description': 'Rising '
                                                                                                                                                       'Edge '
                                                                                                                                                       'of '
                                                                                                                                                       'INTX',
                                                                                                                                        'name': 'RISING_EDGE_OF_INTX',
                                                                                                                                        'value': 0x3}]},
                                                                                              'name': 'ISC1',
                                                                                              'writeConstraint': {'useEnumeratedValues': 0x1}},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[5:4]',
                                                                                              'description': 'External '
                                                                                                             'Interrupt '
                                                                                                             'Sense '
                                                                                                             'Control '
                                                                                                             '2 '
                                                                                                             'Bits',
                                                                                              'enumeratedValues': {'enumeratedValue': [{'description': 'Low '
                                                                                                                                                       'Level '
                                                                                                                                                       'of '
                                                                                                                                                       'INTX',
                                                                                                                                        'name': 'LOW_LEVEL_OF_INTX',
                                                                                                                                        'value': 0x0},
                                                                                                                                       {'description': 'Any '
                                                                                                                                                       'Logical '
                                                                                                                                                       'Change '
                                                                                                                                                       'of '
                                                                                                                                                       'INTX',
                                                                                                                                        'name': 'ANY_LOGICAL_CHANGE_OF_INTX',
                                                                                                                                        'value': 0x1},
                                                                                                                                       {'description': 'Falling '
                                                                                                                                                       'Edge '
                                                                                                                                                       'of '
                                                                                                                                                       'INTX',
                                                                                                                                        'name': 'FALLING_EDGE_OF_INTX',
                                                                                                                                        'value': 0x2},
                                                                                                                                       {'description': 'Rising '
                                                                                                                                                       'Edge '
                                                                                                                                                       'of '
                                                                                                                                                       'INTX',
                                                                                                                                        'name': 'RISING_EDGE_OF_INTX',
                                                                                                                                        'value': 0x3}]},
                                                                                              'name': 'ISC2',
                                                                                              'writeConstraint': {'useEnumeratedValues': 0x1}},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[7:6]',
                                                                                              'description': 'External '
                                                                                                             'Interrupt '
                                                                                                             'Sense '
                                                                                                             'Control '
                                                                                                             '3 '
                                                                                                             'Bits',
                                                                                              'enumeratedValues': {'enumeratedValue': [{'description': 'Low '
                                                                                                                                                       'Level '
                                                                                                                                                       'of '
                                                                                                                                                       'INTX',
                                                                                                                                        'name': 'LOW_LEVEL_OF_INTX',
                                                                                                                                        'value': 0x0},
                                                                                                                                       {'description': 'Any '
                                                                                                                                                       'Logical '
                                                                                                                                                       'Change '
                                                                                                                                                       'of '
                                                                                                                                                       'INTX',
                                                                                                                                        'name': 'ANY_LOGICAL_CHANGE_OF_INTX',
                                                                                                                                        'value': 0x1},
                                                                                                                                       {'description': 'Falling '
                                                                                                                                                       'Edge '
                                                                                                                                                       'of '
                                                                                                                                                       'INTX',
                                                                                                                                        'name': 'FALLING_EDGE_OF_INTX',
                                                                                                                                        'value': 0x2},
                                                                                                                                       {'description': 'Rising '
                                                                                                                                                       'Edge '
                                                                                                                                                       'of '
                                                                                                                                                       'INTX',
                                                                                                                                        'name': 'RISING_EDGE_OF_INTX',
                                                                                                                                        'value': 0x3}]},
                                                                                              'name': 'ISC3',
                                                                                              'writeConstraint': {'useEnumeratedValues': 0x1}}]},
                                                                        'name': 'EICRA',
                                                                        'size': 0x8},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x1,
                                                                        'description': 'External '
                                                                                       'Interrupt '
                                                                                       'Flag '
                                                                                       'Register '
                                                                                       '(read-only '
                                                                                       'for '
                                                                                       'debugger)',
                                                                        'fields': {'field': [{'access': 'read-write',
                                                                                              'bitRange': '[3:0]',
                                                                                              'description': 'External '
                                                                                                             'Interrupt '
                                                                                                             'Flags',
                                                                                              'name': 'INTF',
                                                                                              'writeConstraint': {'range': {'maximum': 0xF,
                                                                                                                            'minimum': 0x0}}}]},
                                                                        'name': 'EIFR',
                                                                        'size': 0x8},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x2,
                                                                        'description': 'External '
                                                                                       'Interrupt '
                                                                                       'Mask '
                                                                                       'Register',
                                                                        'fields': {'field': [{'access': 'read-write',
                                                                                              'bitRange': '[3:0]',
                                                                                              'description': 'External '
                                                                                                             'Interrupt '
                                                                                                             'Request '
                                                                                                             '1 '
                                                                                                             'Enable',
                                                                                              'name': 'INT',
                                                                                              'writeConstraint': {'range': {'maximum': 0xF,
                                                                                                                            'minimum': 0x0}}}]},
                                                                        'name': 'EIMSK',
                                                                        'size': 0x8},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x2D,
                                                                        'description': 'Pin '
                                                                                       'Change '
                                                                                       'Interrupt '
                                                                                       'Control '
                                                                                       'Register',
                                                                        'fields': {'field': [{'access': 'read-write',
                                                                                              'bitRange': '[1:0]',
                                                                                              'description': 'Pin '
                                                                                                             'Change '
                                                                                                             'Interrupt '
                                                                                                             'Enables',
                                                                                              'name': 'PCIE',
                                                                                              'writeConstraint': {'range': {'maximum': 0x3,
                                                                                                                            'minimum': 0x0}}}]},
                                                                        'name': 'PCICR',
                                                                        'size': 0x8},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x0,
                                                                        'description': 'Pin '
                                                                                       'Change '
                                                                                       'Interrupt '
                                                                                       'Flag '
                                                                                       'Register '
                                                                                       '(read-only '
                                                                                       'for '
                                                                                       'debugger)',
                                                                        'fields': {'field': [{'access': 'read-write',
                                                                                              'bitRange': '[1:0]',
                                                                                              'description': 'Pin '
                                                                                                             'Change '
                                                                                                             'Interrupt '
                                                                                                             'Flags',
                                                                                              'name': 'PCIF',
                                                                                              'writeConstraint': {'range': {'maximum': 0x3,
                                                                                                                            'minimum': 0x0}}}]},
                                                                        'name': 'PCIFR',
                                                                        'size': 0x8},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x30,
                                                                        'description': 'Pin '
                                                                                       'Change '
                                                                                       'Enable '
                                                                                       'Mask '
                                                                                       'Register '
                                                                                       '0',
                                                                        'name': 'PCMSK0',
                                                                        'size': 0x8,
                                                                        'writeConstraint': {'range': {'maximum': 0xFF,
                                                                                                      'minimum': 0x0}}},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x31,
                                                                        'description': 'Pin '
                                                                                       'Change '
                                                                                       'Enable '
                                                                                       'Mask '
                                                                                       'Register '
                                                                                       '1',
                                                                        'name': 'PCMSK1',
                                                                        'size': 0x8,
                                                                        'writeConstraint': {'range': {'maximum': 0xFF,
                                                                                                      'minimum': 0x0}}}]}},
                                           {'addressBlock': [{'offset': 0x0,
                                                              'size': 0x1,
                                                              'usage': 'registers'}],
                                            'baseAddress': 0x8000F0,
                                            'description': 'FET Control',
                                            'name': 'FET',
                                            'registers': {'register': [{'access': 'read-write',
                                                                        'addressOffset': 0x0,
                                                                        'description': 'No '
                                                                                       'Description.',
                                                                        'fields': {'field': [{'access': 'read-write',
                                                                                              'bitRange': '[0:0]',
                                                                                              'description': 'Precharge '
                                                                                                             'FET '
                                                                                                             'disable',
                                                                                              'name': 'PFD'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[1:1]',
                                                                                              'description': 'Charge '
                                                                                                             'FET '
                                                                                                             'Enable',
                                                                                              'name': 'CFE'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[2:2]',
                                                                                              'description': 'Discharge '
                                                                                                             'FET '
                                                                                                             'Enable',
                                                                                              'name': 'DFE'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[3:3]',
                                                                                              'description': 'Current '
                                                                                                             'Protection '
                                                                                                             'Status',
                                                                                              'name': 'CPS'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[4:4]',
                                                                                              'description': 'Pulse '
                                                                                                             'Width '
                                                                                                             'Modulation '
                                                                                                             'Modulation '
                                                                                                             'of '
                                                                                                             'OPC '
                                                                                                             'output',
                                                                                              'name': 'PWMOPC'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[5:5]',
                                                                                              'description': 'Pulse '
                                                                                                             'Width '
                                                                                                             'Modulation '
                                                                                                             'of '
                                                                                                             'OC '
                                                                                                             'output',
                                                                                              'name': 'PWMOC'}]},
                                                                        'name': 'FCSR',
                                                                        'size': 0x8}]}},
                                           {'addressBlock': [{'offset': 0x0,
                                                              'size': 0x3,
                                                              'usage': 'registers'}],
                                            'baseAddress': 0x800020,
                                            'description': 'I/O Port',
                                            'name': 'PORTA',
                                            'registers': {'register': [{'access': 'read-write',
                                                                        'addressOffset': 0x1,
                                                                        'description': 'Port '
                                                                                       'A '
                                                                                       'Data '
                                                                                       'Direction '
                                                                                       'Register',
                                                                        'name': 'DDRA',
                                                                        'size': 0x8,
                                                                        'writeConstraint': {'range': {'maximum': 0xFF,
                                                                                                      'minimum': 0x0}}},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x0,
                                                                        'description': 'Port '
                                                                                       'A '
                                                                                       'Input '
                                                                                       'Pins '
                                                                                       '(read-only '
                                                                                       'for '
                                                                                       'debugger)',
                                                                        'name': 'PINA',
                                                                        'size': 0x8,
                                                                        'writeConstraint': {'range': {'maximum': 0xFF,
                                                                                                      'minimum': 0x0}}},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x2,
                                                                        'description': 'Port '
                                                                                       'A '
                                                                                       'Data '
                                                                                       'Register',
                                                                        'name': 'PORTA',
                                                                        'size': 0x8,
                                                                        'writeConstraint': {'range': {'maximum': 0xFF,
                                                                                                      'minimum': 0x0}}}]}},
                                           {'addressBlock': [{'offset': 0x0,
                                                              'size': 0x3,
                                                              'usage': 'registers'}],
                                            'baseAddress': 0x800023,
                                            'description': 'I/O Port',
                                            'name': 'PORTB',
                                            'registers': {'register': [{'access': 'read-write',
                                                                        'addressOffset': 0x1,
                                                                        'description': 'Port '
                                                                                       'B '
                                                                                       'Data '
                                                                                       'Direction '
                                                                                       'Register',
                                                                        'name': 'DDRB',
                                                                        'size': 0x8,
                                                                        'writeConstraint': {'range': {'maximum': 0xFF,
                                                                                                      'minimum': 0x0}}},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x0,
                                                                        'description': 'Port '
                                                                                       'B '
                                                                                       'Input '
                                                                                       'Pins '
                                                                                       '(read-only '
                                                                                       'for '
                                                                                       'debugger)',
                                                                        'name': 'PINB',
                                                                        'size': 0x8,
                                                                        'writeConstraint': {'range': {'maximum': 0xFF,
                                                                                                      'minimum': 0x0}}},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x2,
                                                                        'description': 'Port '
                                                                                       'B '
                                                                                       'Data '
                                                                                       'Register',
                                                                        'name': 'PORTB',
                                                                        'size': 0x8,
                                                                        'writeConstraint': {'range': {'maximum': 0xFF,
                                                                                                      'minimum': 0x0}}}]}},
                                           {'addressBlock': [{'offset': 0x0,
                                                              'size': 0x1,
                                                              'usage': 'registers'}],
                                            'baseAddress': 0x800028,
                                            'description': 'I/O Port',
                                            'name': 'PORTC',
                                            'registers': {'register': [{'access': 'read-write',
                                                                        'addressOffset': 0x0,
                                                                        'description': 'Port '
                                                                                       'C '
                                                                                       'Data '
                                                                                       'Register',
                                                                        'name': 'PORTC',
                                                                        'size': 0x8,
                                                                        'writeConstraint': {'range': {'maximum': 0xFF,
                                                                                                      'minimum': 0x0}}}]}},
                                           {'addressBlock': [{'offset': 0x0,
                                                              'size': 0x3,
                                                              'usage': 'registers'}],
                                            'baseAddress': 0x800029,
                                            'description': 'I/O Port',
                                            'name': 'PORTD',
                                            'registers': {'register': [{'access': 'read-write',
                                                                        'addressOffset': 0x1,
                                                                        'description': 'Data '
                                                                                       'Direction '
                                                                                       'Register, '
                                                                                       'Port '
                                                                                       'D',
                                                                        'name': 'DDRD',
                                                                        'size': 0x8,
                                                                        'writeConstraint': {'range': {'maximum': 0xFF,
                                                                                                      'minimum': 0x0}}},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x0,
                                                                        'description': 'Input '
                                                                                       'Pins, '
                                                                                       'Port '
                                                                                       'D',
                                                                        'name': 'PIND',
                                                                        'size': 0x8,
                                                                        'writeConstraint': {'range': {'maximum': 0xFF,
                                                                                                      'minimum': 0x0}}},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x2,
                                                                        'description': 'Data '
                                                                                       'Register, '
                                                                                       'Port '
                                                                                       'D',
                                                                        'name': 'PORTD',
                                                                        'size': 0x8,
                                                                        'writeConstraint': {'range': {'maximum': 0xFF,
                                                                                                      'minimum': 0x0}}}]}},
                                           {'addressBlock': [{'offset': 0x0,
                                                              'size': 0x1,
                                                              'usage': 'registers'},
                                                             {'offset': 0xF,
                                                              'size': 0x5,
                                                              'usage': 'registers'},
                                                             {'offset': 0x39,
                                                              'size': 0x1,
                                                              'usage': 'registers'}],
                                            'baseAddress': 0x800035,
                                            'description': 'Timer/Counter, '
                                                           '8-bit',
                                            'name': 'TC0',
                                            'registers': {'register': [{'access': 'read-write',
                                                                        'addressOffset': 0x12,
                                                                        'description': 'Output '
                                                                                       'compare '
                                                                                       'Register '
                                                                                       'A',
                                                                        'fields': {'field': [{'access': 'read-write',
                                                                                              'bitRange': '[7:0]',
                                                                                              'description': 'No '
                                                                                                             'Description.',
                                                                                              'name': 'OCR0A',
                                                                                              'writeConstraint': {'range': {'maximum': 0xFF,
                                                                                                                            'minimum': 0x0}}}]},
                                                                        'name': 'OCR0A',
                                                                        'size': 0x8},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x13,
                                                                        'description': 'Output '
                                                                                       'compare '
                                                                                       'Register '
                                                                                       'B',
                                                                        'fields': {'field': [{'access': 'read-write',
                                                                                              'bitRange': '[7:0]',
                                                                                              'description': 'No '
                                                                                                             'Description.',
                                                                                              'name': 'OCR0B',
                                                                                              'writeConstraint': {'range': {'maximum': 0xFF,
                                                                                                                            'minimum': 0x0}}}]},
                                                                        'name': 'OCR0B',
                                                                        'size': 0x8},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0xF,
                                                                        'description': 'Timer/Counter0 '
                                                                                       'Control '
                                                                                       'Register',
                                                                        'fields': {'field': [{'access': 'read-write',
                                                                                              'bitRange': '[1:0]',
                                                                                              'description': 'Clock '
                                                                                                             'Select0 '
                                                                                                             'bits',
                                                                                              'name': 'WGM0',
                                                                                              'writeConstraint': {'range': {'maximum': 0x3,
                                                                                                                            'minimum': 0x0}}},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[5:4]',
                                                                                              'description': 'No '
                                                                                                             'Description.',
                                                                                              'name': 'COM0B',
                                                                                              'writeConstraint': {'range': {'maximum': 0x3,
                                                                                                                            'minimum': 0x0}}},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[7:6]',
                                                                                              'description': 'Force '
                                                                                                             'Output '
                                                                                                             'Compare',
                                                                                              'name': 'COM0A',
                                                                                              'writeConstraint': {'range': {'maximum': 0x3,
                                                                                                                            'minimum': 0x0}}}]},
                                                                        'name': 'TCCR0A',
                                                                        'size': 0x8},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x10,
                                                                        'description': 'Timer/Counter0 '
                                                                                       'Control '
                                                                                       'Register',
                                                                        'fields': {'field': [{'access': 'read-write',
                                                                                              'bitRange': '[2:0]',
                                                                                              'description': 'Clock '
                                                                                                             'Select0 '
                                                                                                             'bits',
                                                                                              'enumeratedValues': {'enumeratedValue': [{'description': 'No '
                                                                                                                                                       'Clock '
                                                                                                                                                       'Source '
                                                                                                                                                       '(Stopped)',
                                                                                                                                        'name': 'NO_CLOCK_SOURCE_STOPPED',
                                                                                                                                        'value': 0x0},
                                                                                                                                       {'description': 'Running, '
                                                                                                                                                       'No '
                                                                                                                                                       'Prescaling',
                                                                                                                                        'name': 'RUNNING_NO_PRESCALING',
                                                                                                                                        'value': 0x1},
                                                                                                                                       {'description': 'Running, '
                                                                                                                                                       'CLK/8',
                                                                                                                                        'name': 'RUNNING_CLK_8',
                                                                                                                                        'value': 0x2},
                                                                                                                                       {'description': 'Running, '
                                                                                                                                                       'CLK/64',
                                                                                                                                        'name': 'RUNNING_CLK_64',
                                                                                                                                        'value': 0x3},
                                                                                                                                       {'description': 'Running, '
                                                                                                                                                       'CLK/256',
                                                                                                                                        'name': 'RUNNING_CLK_256',
                                                                                                                                        'value': 0x4},
                                                                                                                                       {'description': 'Running, '
                                                                                                                                                       'CLK/1024',
                                                                                                                                        'name': 'RUNNING_CLK_1024',
                                                                                                                                        'value': 0x5},
                                                                                                                                       {'description': 'Running, '
                                                                                                                                                       'ExtClk '
                                                                                                                                                       'Tn '
                                                                                                                                                       'Falling '
                                                                                                                                                       'Edge',
                                                                                                                                        'name': 'RUNNING_EXTCLK_TN_FALLING_EDGE',
                                                                                                                                        'value': 0x6},
                                                                                                                                       {'description': 'Running, '
                                                                                                                                                       'ExtClk '
                                                                                                                                                       'Tn '
                                                                                                                                                       'Rising '
                                                                                                                                                       'Edge',
                                                                                                                                        'name': 'RUNNING_EXTCLK_TN_RISING_EDGE',
                                                                                                                                        'value': 0x7}]},
                                                                                              'name': 'CS0',
                                                                                              'writeConstraint': {'useEnumeratedValues': 0x1}},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[3:3]',
                                                                                              'description': 'No '
                                                                                                             'Description.',
                                                                                              'name': 'WGM02'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[6:6]',
                                                                                              'description': 'Waveform '
                                                                                                             'Generation '
                                                                                                             'Mode',
                                                                                              'name': 'FOC0B'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[7:7]',
                                                                                              'description': 'Force '
                                                                                                             'Output '
                                                                                                             'Compare',
                                                                                              'name': 'FOC0A'}]},
                                                                        'name': 'TCCR0B',
                                                                        'size': 0x8},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x11,
                                                                        'description': 'Timer '
                                                                                       'Counter '
                                                                                       '0',
                                                                        'name': 'TCNT0',
                                                                        'size': 0x8,
                                                                        'writeConstraint': {'range': {'maximum': 0xFF,
                                                                                                      'minimum': 0x0}}},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x0,
                                                                        'description': 'Timer/Counter '
                                                                                       'Interrupt '
                                                                                       'Flag '
                                                                                       'register '
                                                                                       '(read-only '
                                                                                       'for '
                                                                                       'debugger)',
                                                                        'fields': {'field': [{'access': 'read-write',
                                                                                              'bitRange': '[0:0]',
                                                                                              'description': 'Overflow '
                                                                                                             'Flag',
                                                                                              'name': 'TOV0'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[1:1]',
                                                                                              'description': 'Output '
                                                                                                             'Compare '
                                                                                                             'Flag',
                                                                                              'name': 'OCF0A'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[2:2]',
                                                                                              'description': 'Output '
                                                                                                             'Compare '
                                                                                                             'Flag',
                                                                                              'name': 'OCF0B'}]},
                                                                        'name': 'TIFR0',
                                                                        'size': 0x8},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x39,
                                                                        'description': 'Timer/Counter '
                                                                                       'Interrupt '
                                                                                       'Mask '
                                                                                       'Register',
                                                                        'fields': {'field': [{'access': 'read-write',
                                                                                              'bitRange': '[0:0]',
                                                                                              'description': 'Overflow '
                                                                                                             'Interrupt '
                                                                                                             'Enable',
                                                                                              'name': 'TOIE0'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[1:1]',
                                                                                              'description': 'Output '
                                                                                                             'Compare '
                                                                                                             'Interrupt '
                                                                                                             'Enable',
                                                                                              'name': 'OCIE0A'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[2:2]',
                                                                                              'description': 'Output '
                                                                                                             'Compare '
                                                                                                             'Interrupt '
                                                                                                             'Enable',
                                                                                              'name': 'OCIE0B'}]},
                                                                        'name': 'TIMSK0',
                                                                        'size': 0x8}]}},
                                           {'addressBlock': [{'offset': 0x0,
                                                              'size': 0x1,
                                                              'usage': 'registers'},
                                                             {'offset': 0xD,
                                                              'size': 0x1,
                                                              'usage': 'registers'},
                                                             {'offset': 0x39,
                                                              'size': 0x1,
                                                              'usage': 'registers'},
                                                             {'offset': 0x4B,
                                                              'size': 0x1,
                                                              'usage': 'registers'},
                                                             {'offset': 0x4E,
                                                              'size': 0x2,
                                                              'usage': 'registers'},
                                                             {'offset': 0x52,
                                                              'size': 0x2,
                                                              'usage': 'registers'}],
                                            'baseAddress': 0x800036,
                                            'description': 'Timer/Counter, '
                                                           '16-bit',
                                            'name': 'TC1',
                                            'registers': {'register': [{'access': 'read-write',
                                                                        'addressOffset': 0xD,
                                                                        'description': 'General '
                                                                                       'Timer/Counter '
                                                                                       'Control '
                                                                                       'Register',
                                                                        'fields': {'field': [{'access': 'read-write',
                                                                                              'bitRange': '[0:0]',
                                                                                              'description': 'Prescaler '
                                                                                                             'Reset',
                                                                                              'name': 'PSRSYNC'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[7:7]',
                                                                                              'description': 'Timer/Counter '
                                                                                                             'Synchronization '
                                                                                                             'Mode',
                                                                                              'name': 'TSM'}]},
                                                                        'name': 'GTCCR',
                                                                        'size': 0x8},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x53,
                                                                        'description': 'Output '
                                                                                       'Compare '
                                                                                       'Register '
                                                                                       '1A '
                                                                                       'High '
                                                                                       'byte',
                                                                        'name': 'OCR1AH',
                                                                        'size': 0x8,
                                                                        'writeConstraint': {'range': {'maximum': 0xFF,
                                                                                                      'minimum': 0x0}}},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x52,
                                                                        'description': 'Output '
                                                                                       'Compare '
                                                                                       'Register '
                                                                                       '1A '
                                                                                       'Low '
                                                                                       'byte',
                                                                        'name': 'OCR1AL',
                                                                        'size': 0x8,
                                                                        'writeConstraint': {'range': {'maximum': 0xFF,
                                                                                                      'minimum': 0x0}}},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x4B,
                                                                        'description': 'Timer/Counter1 '
                                                                                       'Control '
                                                                                       'Register '
                                                                                       'B',
                                                                        'fields': {'field': [{'access': 'read-write',
                                                                                              'bitRange': '[2:0]',
                                                                                              'description': 'Clock '
                                                                                                             'Select1 '
                                                                                                             'bits',
                                                                                              'enumeratedValues': {'enumeratedValue': [{'description': 'No '
                                                                                                                                                       'Clock '
                                                                                                                                                       'Source '
                                                                                                                                                       '(Stopped)',
                                                                                                                                        'name': 'NO_CLOCK_SOURCE_STOPPED',
                                                                                                                                        'value': 0x0},
                                                                                                                                       {'description': 'Running, '
                                                                                                                                                       'No '
                                                                                                                                                       'Prescaling',
                                                                                                                                        'name': 'RUNNING_NO_PRESCALING',
                                                                                                                                        'value': 0x1},
                                                                                                                                       {'description': 'Running, '
                                                                                                                                                       'CLK/8',
                                                                                                                                        'name': 'RUNNING_CLK_8',
                                                                                                                                        'value': 0x2},
                                                                                                                                       {'description': 'Running, '
                                                                                                                                                       'CLK/32',
                                                                                                                                        'name': 'RUNNING_CLK_32',
                                                                                                                                        'value': 0x3},
                                                                                                                                       {'description': 'Running, '
                                                                                                                                                       'CLK/64',
                                                                                                                                        'name': 'RUNNING_CLK_64',
                                                                                                                                        'value': 0x4},
                                                                                                                                       {'description': 'Running, '
                                                                                                                                                       'CLK/128',
                                                                                                                                        'name': 'RUNNING_CLK_128',
                                                                                                                                        'value': 0x5},
                                                                                                                                       {'description': 'Running, '
                                                                                                                                                       'CLK/256',
                                                                                                                                        'name': 'RUNNING_CLK_256',
                                                                                                                                        'value': 0x6},
                                                                                                                                       {'description': 'Running, '
                                                                                                                                                       'CLK/1024',
                                                                                                                                        'name': 'RUNNING_CLK_1024',
                                                                                                                                        'value': 0x7}]},
                                                                                              'name': 'CS1',
                                                                                              'writeConstraint': {'useEnumeratedValues': 0x1}},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[3:3]',
                                                                                              'description': 'Clear '
                                                                                                             'Timer/Counter '
                                                                                                             'on '
                                                                                                             'Compare '
                                                                                                             'Match',
                                                                                              'name': 'CTC1'}]},
                                                                        'name': 'TCCR1B',
                                                                        'size': 0x8},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x4E,
                                                                        'description': 'Timer '
                                                                                       'Counter '
                                                                                       '1  '
                                                                                       'Bytes',
                                                                        'name': 'TCNT1',
                                                                        'size': 0x10,
                                                                        'writeConstraint': {'range': {'maximum': 0xFFFF,
                                                                                                      'minimum': 0x0}}},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x0,
                                                                        'description': 'Timer/Counter '
                                                                                       'Interrupt '
                                                                                       'Flag '
                                                                                       'register '
                                                                                       '(read-only '
                                                                                       'for '
                                                                                       'debugger)',
                                                                        'fields': {'field': [{'access': 'read-write',
                                                                                              'bitRange': '[0:0]',
                                                                                              'description': 'Timer/Counter1 '
                                                                                                             'Overflow '
                                                                                                             'Flag',
                                                                                              'name': 'TOV1'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[1:1]',
                                                                                              'description': 'Timer/Counter1 '
                                                                                                             'Output '
                                                                                                             'Compare '
                                                                                                             'Flag '
                                                                                                             'A',
                                                                                              'name': 'OCF1A'}]},
                                                                        'name': 'TIFR1',
                                                                        'size': 0x8},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x39,
                                                                        'description': 'Timer/Counter '
                                                                                       'Interrupt '
                                                                                       'Mask '
                                                                                       'Register',
                                                                        'fields': {'field': [{'access': 'read-write',
                                                                                              'bitRange': '[0:0]',
                                                                                              'description': 'Timer/Counter1 '
                                                                                                             'Overflow '
                                                                                                             'Interrupt '
                                                                                                             'Enable',
                                                                                              'name': 'TOIE1'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[1:1]',
                                                                                              'description': 'Timer/Counter1 '
                                                                                                             'Output '
                                                                                                             'Compare '
                                                                                                             'Interrupt '
                                                                                                             'Enable',
                                                                                              'name': 'OCIE1A'}]},
                                                                        'name': 'TIMSK1',
                                                                        'size': 0x8}]}},
                                           {'addressBlock': [{'offset': 0x0,
                                                              'size': 0x7,
                                                              'usage': 'registers'}],
                                            'baseAddress': 0x8000B8,
                                            'description': 'Two Wire Serial '
                                                           'Interface',
                                            'name': 'TWI',
                                            'registers': {'register': [{'access': 'read-write',
                                                                        'addressOffset': 0x5,
                                                                        'description': 'TWI '
                                                                                       '(Slave) '
                                                                                       'Address '
                                                                                       'Mask '
                                                                                       'Register',
                                                                        'fields': {'field': [{'access': 'read-write',
                                                                                              'bitRange': '[7:1]',
                                                                                              'description': 'No '
                                                                                                             'Description.',
                                                                                              'name': 'TWAM',
                                                                                              'writeConstraint': {'range': {'maximum': 0x7F,
                                                                                                                            'minimum': 0x0}}}]},
                                                                        'name': 'TWAMR',
                                                                        'size': 0x8},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x2,
                                                                        'description': 'TWI '
                                                                                       '(Slave) '
                                                                                       'Address '
                                                                                       'register',
                                                                        'fields': {'field': [{'access': 'read-write',
                                                                                              'bitRange': '[0:0]',
                                                                                              'description': 'TWI '
                                                                                                             'General '
                                                                                                             'Call '
                                                                                                             'Recognition '
                                                                                                             'Enable '
                                                                                                             'Bit',
                                                                                              'name': 'TWGCE'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[7:1]',
                                                                                              'description': 'TWI '
                                                                                                             '(Slave) '
                                                                                                             'Address '
                                                                                                             'register '
                                                                                                             'Bits',
                                                                                              'name': 'TWA',
                                                                                              'writeConstraint': {'range': {'maximum': 0x7F,
                                                                                                                            'minimum': 0x0}}}]},
                                                                        'name': 'TWAR',
                                                                        'size': 0x8},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x6,
                                                                        'description': 'TWI '
                                                                                       'Bus '
                                                                                       'Control '
                                                                                       'and '
                                                                                       'Status '
                                                                                       'Register',
                                                                        'fields': {'field': [{'access': 'read-write',
                                                                                              'bitRange': '[0:0]',
                                                                                              'description': 'TWI '
                                                                                                             'Bus '
                                                                                                             'Connect/Disconnect '
                                                                                                             'Interrupt '
                                                                                                             'Polarity',
                                                                                              'name': 'TWBCIP'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[2:1]',
                                                                                              'description': 'TWI '
                                                                                                             'Bus '
                                                                                                             'Disconnect '
                                                                                                             'Time-out '
                                                                                                             'Period',
                                                                                              'enumeratedValues': {'enumeratedValue': [{'description': '250ms',
                                                                                                                                        'name': '250MS',
                                                                                                                                        'value': 0x0},
                                                                                                                                       {'description': '500ms',
                                                                                                                                        'name': '500MS',
                                                                                                                                        'value': 0x1},
                                                                                                                                       {'description': '1000ms',
                                                                                                                                        'name': '1000MS',
                                                                                                                                        'value': 0x2},
                                                                                                                                       {'description': '2000ms',
                                                                                                                                        'name': '2000MS',
                                                                                                                                        'value': 0x3}]},
                                                                                              'name': 'TWBDT',
                                                                                              'writeConstraint': {'useEnumeratedValues': 0x1}},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[6:6]',
                                                                                              'description': 'TWI '
                                                                                                             'Bus '
                                                                                                             'Connect/Disconnect '
                                                                                                             'Interrupt '
                                                                                                             'Enable',
                                                                                              'name': 'TWBCIE'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[7:7]',
                                                                                              'description': 'TWI '
                                                                                                             'Bus '
                                                                                                             'Connect/Disconnect '
                                                                                                             'Interrupt '
                                                                                                             'Flag',
                                                                                              'name': 'TWBCIF'}]},
                                                                        'name': 'TWBCSR',
                                                                        'size': 0x8},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x0,
                                                                        'description': 'TWI '
                                                                                       'Bit '
                                                                                       'Rate '
                                                                                       'register',
                                                                        'name': 'TWBR',
                                                                        'size': 0x8,
                                                                        'writeConstraint': {'range': {'maximum': 0xFF,
                                                                                                      'minimum': 0x0}}},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x4,
                                                                        'description': 'TWI '
                                                                                       'Control '
                                                                                       'Register '
                                                                                       '(read-only '
                                                                                       'for '
                                                                                       'debugger)',
                                                                        'fields': {'field': [{'access': 'read-write',
                                                                                              'bitRange': '[0:0]',
                                                                                              'description': 'TWI '
                                                                                                             'Interrupt '
                                                                                                             'Enable',
                                                                                              'name': 'TWIE'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[2:2]',
                                                                                              'description': 'TWI '
                                                                                                             'Enable '
                                                                                                             'Bit',
                                                                                              'name': 'TWEN'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[3:3]',
                                                                                              'description': 'TWI '
                                                                                                             'Write '
                                                                                                             'Collision '
                                                                                                             'Flag',
                                                                                              'name': 'TWWC'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[4:4]',
                                                                                              'description': 'TWI '
                                                                                                             'Stop '
                                                                                                             'Condition '
                                                                                                             'Bit',
                                                                                              'name': 'TWSTO'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[5:5]',
                                                                                              'description': 'TWI '
                                                                                                             'Start '
                                                                                                             'Condition '
                                                                                                             'Bit',
                                                                                              'name': 'TWSTA'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[6:6]',
                                                                                              'description': 'TWI '
                                                                                                             'Enable '
                                                                                                             'Acknowledge '
                                                                                                             'Bit',
                                                                                              'name': 'TWEA'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[7:7]',
                                                                                              'description': 'TWI '
                                                                                                             'Interrupt '
                                                                                                             'Flag',
                                                                                              'name': 'TWINT'}]},
                                                                        'name': 'TWCR',
                                                                        'size': 0x8},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x3,
                                                                        'description': 'TWI '
                                                                                       'Data '
                                                                                       'register',
                                                                        'name': 'TWDR',
                                                                        'size': 0x8,
                                                                        'writeConstraint': {'range': {'maximum': 0xFF,
                                                                                                      'minimum': 0x0}}},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x1,
                                                                        'description': 'TWI '
                                                                                       'Status '
                                                                                       'Register '
                                                                                       '(read-only '
                                                                                       'for '
                                                                                       'debugger)',
                                                                        'fields': {'field': [{'access': 'read-write',
                                                                                              'bitRange': '[1:0]',
                                                                                              'description': 'TWI '
                                                                                                             'Prescaler',
                                                                                              'enumeratedValues': {'enumeratedValue': [{'description': '1',
                                                                                                                                        'name': '1',
                                                                                                                                        'value': 0x0},
                                                                                                                                       {'description': '4',
                                                                                                                                        'name': '4',
                                                                                                                                        'value': 0x1},
                                                                                                                                       {'description': '16',
                                                                                                                                        'name': '16',
                                                                                                                                        'value': 0x2},
                                                                                                                                       {'description': '64',
                                                                                                                                        'name': '64',
                                                                                                                                        'value': 0x3}]},
                                                                                              'name': 'TWPS',
                                                                                              'writeConstraint': {'useEnumeratedValues': 0x1}},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[7:3]',
                                                                                              'description': 'TWI '
                                                                                                             'Status',
                                                                                              'name': 'TWS',
                                                                                              'writeConstraint': {'range': {'maximum': 0x1F,
                                                                                                                            'minimum': 0x0}}}]},
                                                                        'name': 'TWSR',
                                                                        'size': 0x8}]}},
                                           {'addressBlock': [{'offset': 0x0,
                                                              'size': 0x1,
                                                              'usage': 'registers'}],
                                            'baseAddress': 0x800062,
                                            'description': 'Wakeup Timer',
                                            'name': 'WAKEUP_TIMER',
                                            'registers': {'register': [{'access': 'read-write',
                                                                        'addressOffset': 0x0,
                                                                        'description': 'Wake-up '
                                                                                       'Timer '
                                                                                       'Control '
                                                                                       'Register '
                                                                                       '(read-only '
                                                                                       'for '
                                                                                       'debugger)',
                                                                        'fields': {'field': [{'access': 'read-write',
                                                                                              'bitRange': '[2:0]',
                                                                                              'description': 'Wake-up '
                                                                                                             'Timer '
                                                                                                             'Prescaler '
                                                                                                             'Bits',
                                                                                              'enumeratedValues': {'enumeratedValue': [{'description': '4K(Slow '
                                                                                                                                                       'RC) '
                                                                                                                                                       '/ '
                                                                                                                                                       '1K '
                                                                                                                                                       '(32kHz)',
                                                                                                                                        'name': '4K_SLOW_RC_1K_32KHZ',
                                                                                                                                        'value': 0x0},
                                                                                                                                       {'description': '8K(Slow '
                                                                                                                                                       'RC) '
                                                                                                                                                       '/ '
                                                                                                                                                       '2K '
                                                                                                                                                       '(32kHz)',
                                                                                                                                        'name': '8K_SLOW_RC_2K_32KHZ',
                                                                                                                                        'value': 0x1},
                                                                                                                                       {'description': '16K(Slow '
                                                                                                                                                       'RC) '
                                                                                                                                                       '/ '
                                                                                                                                                       '4K '
                                                                                                                                                       '(32kHz)',
                                                                                                                                        'name': '16K_SLOW_RC_4K_32KHZ',
                                                                                                                                        'value': 0x2},
                                                                                                                                       {'description': '32K(Slow '
                                                                                                                                                       'RC) '
                                                                                                                                                       '/ '
                                                                                                                                                       '8K '
                                                                                                                                                       '(32kHz)',
                                                                                                                                        'name': '32K_SLOW_RC_8K_32KHZ',
                                                                                                                                        'value': 0x3},
                                                                                                                                       {'description': '64K(Slow '
                                                                                                                                                       'RC) '
                                                                                                                                                       '/ '
                                                                                                                                                       '16K '
                                                                                                                                                       '(32kHz)',
                                                                                                                                        'name': '64K_SLOW_RC_16K_32KHZ',
                                                                                                                                        'value': 0x4},
                                                                                                                                       {'description': '128K(Slow '
                                                                                                                                                       'RC) '
                                                                                                                                                       '/ '
                                                                                                                                                       '32K '
                                                                                                                                                       '(32kHz)',
                                                                                                                                        'name': '128K_SLOW_RC_32K_32KHZ',
                                                                                                                                        'value': 0x5},
                                                                                                                                       {'description': '256K(Slow '
                                                                                                                                                       'RC) '
                                                                                                                                                       '/ '
                                                                                                                                                       '64K '
                                                                                                                                                       '(32kHz)',
                                                                                                                                        'name': '256K_SLOW_RC_64K_32KHZ',
                                                                                                                                        'value': 0x6},
                                                                                                                                       {'description': '512K(Slow '
                                                                                                                                                       'RC) '
                                                                                                                                                       '/ '
                                                                                                                                                       '128K '
                                                                                                                                                       '(32kHz)',
                                                                                                                                        'name': '512K_SLOW_RC_128K_32KHZ',
                                                                                                                                        'value': 0x7}]},
                                                                                              'name': 'WUTP',
                                                                                              'writeConstraint': {'useEnumeratedValues': 0x1}},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[3:3]',
                                                                                              'description': 'Wake-up '
                                                                                                             'Timer '
                                                                                                             'Enable',
                                                                                              'name': 'WUTE'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[4:4]',
                                                                                              'description': 'Wake-up '
                                                                                                             'Timer '
                                                                                                             'Reset',
                                                                                              'name': 'WUTR'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[5:5]',
                                                                                              'description': 'Wake-up '
                                                                                                             'timer '
                                                                                                             'Calibration '
                                                                                                             'Flag',
                                                                                              'name': 'WUTCF'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[6:6]',
                                                                                              'description': 'Wake-up '
                                                                                                             'Timer '
                                                                                                             'Interrupt '
                                                                                                             'Enable',
                                                                                              'name': 'WUTIE'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[7:7]',
                                                                                              'description': 'Wake-up '
                                                                                                             'Timer '
                                                                                                             'Interrupt '
                                                                                                             'Flag',
                                                                                              'name': 'WUTIF'}]},
                                                                        'name': 'WUTCSR',
                                                                        'size': 0x8}]}},
                                           {'addressBlock': [{'offset': 0x0,
                                                              'size': 0x1,
                                                              'usage': 'registers'}],
                                            'baseAddress': 0x800060,
                                            'description': 'Watchdog Timer',
                                            'name': 'WDT',
                                            'registers': {'register': [{'access': 'read-write',
                                                                        'addressOffset': 0x0,
                                                                        'description': 'Watchdog '
                                                                                       'Timer '
                                                                                       'Control '
                                                                                       'Register '
                                                                                       '(read-only '
                                                                                       'for '
                                                                                       'debugger)',
                                                                        'fields': {'field': [{'access': 'read-write',
                                                                                              'bitRange': '[5:0]',
                                                                                              'description': 'Watchdog '
                                                                                                             'Timer '
                                                                                                             'Prescaler '
                                                                                                             'Bits',
                                                                                              'enumeratedValues': {'enumeratedValue': [{'description': 'Oscillator '
                                                                                                                                                       'Cycles '
                                                                                                                                                       '2K',
                                                                                                                                        'name': 'OSCILLATOR_CYCLES_2K',
                                                                                                                                        'value': 0x0},
                                                                                                                                       {'description': 'Oscillator '
                                                                                                                                                       'Cycles '
                                                                                                                                                       '4K',
                                                                                                                                        'name': 'OSCILLATOR_CYCLES_4K',
                                                                                                                                        'value': 0x1},
                                                                                                                                       {'description': 'Oscillator '
                                                                                                                                                       'Cycles '
                                                                                                                                                       '8K',
                                                                                                                                        'name': 'OSCILLATOR_CYCLES_8K',
                                                                                                                                        'value': 0x2},
                                                                                                                                       {'description': 'Oscillator '
                                                                                                                                                       'Cycles '
                                                                                                                                                       '16K',
                                                                                                                                        'name': 'OSCILLATOR_CYCLES_16K',
                                                                                                                                        'value': 0x3},
                                                                                                                                       {'description': 'Oscillator '
                                                                                                                                                       'Cycles '
                                                                                                                                                       '32K',
                                                                                                                                        'name': 'OSCILLATOR_CYCLES_32K',
                                                                                                                                        'value': 0x4},
                                                                                                                                       {'description': 'Oscillator '
                                                                                                                                                       'Cycles '
                                                                                                                                                       '64K',
                                                                                                                                        'name': 'OSCILLATOR_CYCLES_64K',
                                                                                                                                        'value': 0x5},
                                                                                                                                       {'description': 'Oscillator '
                                                                                                                                                       'Cycles '
                                                                                                                                                       '128K',
                                                                                                                                        'name': 'OSCILLATOR_CYCLES_128K',
                                                                                                                                        'value': 0x6},
                                                                                                                                       {'description': 'Oscillator '
                                                                                                                                                       'Cycles '
                                                                                                                                                       '256K',
                                                                                                                                        'name': 'OSCILLATOR_CYCLES_256K',
                                                                                                                                        'value': 0x7}]},
                                                                                              'name': 'WDP',
                                                                                              'writeConstraint': {'useEnumeratedValues': 0x1}},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[3:3]',
                                                                                              'description': 'Watch '
                                                                                                             'Dog '
                                                                                                             'Enable',
                                                                                              'name': 'WDE'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[4:4]',
                                                                                              'description': 'Watchdog '
                                                                                                             'Change '
                                                                                                             'Enable',
                                                                                              'name': 'WDCE'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[6:6]',
                                                                                              'description': 'Watchdog '
                                                                                                             'Timeout '
                                                                                                             'Interrupt '
                                                                                                             'Enable',
                                                                                              'name': 'WDIE'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[7:7]',
                                                                                              'description': 'Watchdog '
                                                                                                             'Timeout '
                                                                                                             'Interrupt '
                                                                                                             'Flag',
                                                                                              'name': 'WDIF'}]},
                                                                        'name': 'WDTCSR',
                                                                        'size': 0x8}]}}]},
            'resetMask': 0xFF,
            'resetValue': 0x0,
            'size': 0x8,
            'version': '1.0',
            'width': 0x8}}
}