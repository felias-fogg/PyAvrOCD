# Device description for atmega64hve2, generated from Microchip's ATmega64HVE2.atdf by
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
    'name': 'atmega64hve2',
    'architecture': 'avr8',

    # eeprom
    'eeprom_address_byte': 0x0000,
    'eeprom_size_bytes': 0x0400,
    'eeprom_page_size_bytes': 0x04,
    'eeprom_read_size_bytes': 0x01,
    'eeprom_write_size_bytes': 0x01,
    'eeprom_chiperase_effect': ChiperaseEffect.CONDITIONALLY_ERASED_AVR,
    'eeprom_isolated_erase': False,

    # flash
    'flash_address_byte': 0x0000,
    'flash_size_bytes': 0x10000,
    'flash_page_size_bytes': 0x80,
    'flash_read_size_bytes': 0x02,
    'flash_write_size_bytes': 0x80,
    'flash_chiperase_effect': ChiperaseEffect.ALWAYS_ERASED,
    'flash_isolated_erase': False,

    # fuses
    'fuses_address_byte': 0,
    'fuses_size_bytes': 0x0002,
    'fuses_page_size_bytes': 0x01,
    'fuses_read_size_bytes': 0x01,
    'fuses_write_size_bytes': 0x01,
    'fuses_chiperase_effect': ChiperaseEffect.NOT_ERASED,
    'fuses_isolated_erase': False,

    # internal_sram
    'internal_sram_address_byte': 0x0100,
    'internal_sram_size_bytes': 0x1000,
    'internal_sram_page_size_bytes': 0x01,
    'internal_sram_read_size_bytes': 0x01,
    'internal_sram_write_size_bytes': 0x01,
    'internal_sram_chiperase_effect': ChiperaseEffect.NOT_ERASED,
    'internal_sram_isolated_erase': False,

    # lockbits
    'lockbits_address_byte': 0,
    'lockbits_size_bytes': 0x0001,
    'lockbits_page_size_bytes': 0x01,
    'lockbits_read_size_bytes': 0x01,
    'lockbits_write_size_bytes': 0x01,
    'lockbits_chiperase_effect': ChiperaseEffect.ALWAYS_ERASED,
    'lockbits_isolated_erase': False,

    # signatures
    'signatures_address_byte': 0,
    'signatures_size_bytes': 3,
    'signatures_page_size_bytes': 0x01,
    'signatures_read_size_bytes': 0x01,
    'signatures_write_size_bytes': 0x00,
    'signatures_chiperase_effect': ChiperaseEffect.NOT_ERASED,
    'signatures_isolated_erase': False,

    # Some extra AVR specific fields
    'address_size': '16-bit',
    'ocd_rev' : 1,
    'ocd_base' : 0x31,
    'eear_base' : 0x21,
    'eear_size' : 2,
    'eecr_base' : 0x1F,
    'eedr_base' : 0x20,
    'spmcsr_base' : 0x57,
    'osccal_base' : 0x46,
    'dwen_base' : 0x01,
    'dwen_mask' : 0x08,
    'bootrst_base' : 0x01,
    'bootrst_mask' : 0x01,
    'eesave_base' : 0x00,
    'eesave_mask' : 0x40,
    'tcnt0_base' : 0x46,
    'cs0_base' : 0x45,
    'toie0_base' : 0x6E,
    'toie0_mask' : 0x01,
    'masked_registers' : [0x4e, 0x51, 0xca],
    'ronly_registers' : [0x20, 0x23, 0x35, 0x36, 0x3b, 0x3c, 0x4d, 0x54, 0x60, 0x61, 0x62, 0xc3],
    'device_id': 0x1E9610,
    'interface': 'ISP+HVSP+debugWIRE',

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
            'name': 'ATmega64HVE2',
            'peripherals': {'peripheral': [{'addressBlock': [{'offset': 0x0,
                                                              'size': 0x17,
                                                              'usage': 'registers'}],
                                            'baseAddress': 0x8000E0,
                                            'description': 'Analog-to-Digital '
                                                           'Converter',
                                            'name': 'ADC',
                                            'registers': {'register': [{'access': 'read-write',
                                                                        'addressOffset': 0x2,
                                                                        'description': 'ADC '
                                                                                       'Control '
                                                                                       'Register '
                                                                                       'A',
                                                                        'fields': {'field': [{'access': 'read-write',
                                                                                              'bitRange': '[0:0]',
                                                                                              'description': 'Sampling '
                                                                                                             'Clock '
                                                                                                             'Select',
                                                                                              'enumeratedValues': {'enumeratedValue': [{'description': 'PLL '
                                                                                                                                                       '(512kHz '
                                                                                                                                                       'output) '
                                                                                                                                                       'as '
                                                                                                                                                       'sampling '
                                                                                                                                                       'clock',
                                                                                                                                        'name': 'PLL_512KHZ_OUTPUT_AS_SAMPLING_CLOCK',
                                                                                                                                        'value': 0x0},
                                                                                                                                       {'description': 'Slow '
                                                                                                                                                       'RC '
                                                                                                                                                       'Oscillator '
                                                                                                                                                       'as '
                                                                                                                                                       'sampling '
                                                                                                                                                       'clock',
                                                                                                                                        'name': 'SLOW_RC_OSCILLATOR_AS_SAMPLING_CLOCK',
                                                                                                                                        'value': 0x1}]},
                                                                                              'name': 'CKSEL',
                                                                                              'writeConstraint': {'useEnumeratedValues': 0x1}},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[2:1]',
                                                                                              'description': 'C-ADC '
                                                                                                             'Chopper '
                                                                                                             'Mode '
                                                                                                             'Select',
                                                                                              'enumeratedValues': {'enumeratedValue': [{'description': 'Chopping '
                                                                                                                                                       'Disabled',
                                                                                                                                        'name': 'CHOPPING_DISABLED',
                                                                                                                                        'value': 0x0},
                                                                                                                                       {'description': 'Automatic '
                                                                                                                                                       'Fast '
                                                                                                                                                       'Chopping',
                                                                                                                                        'name': 'AUTOMATIC_FAST_CHOPPING',
                                                                                                                                        'value': 0x1},
                                                                                                                                       {'description': 'Automatic '
                                                                                                                                                       'Slow '
                                                                                                                                                       'Chopping',
                                                                                                                                        'name': 'AUTOMATIC_SLOW_CHOPPING',
                                                                                                                                        'value': 0x2},
                                                                                                                                       {'description': 'Software '
                                                                                                                                                       'Polarity '
                                                                                                                                                       'Control',
                                                                                                                                        'name': 'SOFTWARE_POLARITY_CONTROL',
                                                                                                                                        'value': 0x3}]},
                                                                                              'name': 'ADCMS',
                                                                                              'writeConstraint': {'useEnumeratedValues': 0x1}},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[3:3]',
                                                                                              'description': 'ADC '
                                                                                                             'Polarity '
                                                                                                             'Select',
                                                                                              'name': 'ADPSEL'}]},
                                                                        'name': 'ADCRA',
                                                                        'size': 0x8},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x3,
                                                                        'description': 'ADC '
                                                                                       'Control '
                                                                                       'Register '
                                                                                       'B',
                                                                        'fields': {'field': [{'access': 'read-write',
                                                                                              'bitRange': '[2:0]',
                                                                                              'description': 'Accumulated '
                                                                                                             'Decimation '
                                                                                                             'Ratio '
                                                                                                             'Select',
                                                                                              'enumeratedValues': {'enumeratedValue': [{'description': '512',
                                                                                                                                        'name': '512',
                                                                                                                                        'value': 0x0},
                                                                                                                                       {'description': '256',
                                                                                                                                        'name': '256',
                                                                                                                                        'value': 0x1},
                                                                                                                                       {'description': '128',
                                                                                                                                        'name': '128',
                                                                                                                                        'value': 0x2},
                                                                                                                                       {'description': '64',
                                                                                                                                        'name': '64',
                                                                                                                                        'value': 0x3},
                                                                                                                                       {'description': '32',
                                                                                                                                        'name': '32',
                                                                                                                                        'value': 0x4},
                                                                                                                                       {'description': '16',
                                                                                                                                        'name': '16',
                                                                                                                                        'value': 0x5},
                                                                                                                                       {'description': '8',
                                                                                                                                        'name': '8',
                                                                                                                                        'value': 0x6},
                                                                                                                                       {'description': '4',
                                                                                                                                        'name': '4',
                                                                                                                                        'value': 0x7}]},
                                                                                              'name': 'ADADES',
                                                                                              'writeConstraint': {'useEnumeratedValues': 0x1}},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[4:3]',
                                                                                              'description': 'Instantaneous '
                                                                                                             'Decimation '
                                                                                                             'Ratio '
                                                                                                             'Select',
                                                                                              'enumeratedValues': {'enumeratedValue': [{'description': '512',
                                                                                                                                        'name': '512',
                                                                                                                                        'value': 0x0},
                                                                                                                                       {'description': '256',
                                                                                                                                        'name': '256',
                                                                                                                                        'value': 0x1},
                                                                                                                                       {'description': '128',
                                                                                                                                        'name': '128',
                                                                                                                                        'value': 0x2},
                                                                                                                                       {'description': '64',
                                                                                                                                        'name': '64',
                                                                                                                                        'value': 0x3}]},
                                                                                              'name': 'ADIDES',
                                                                                              'writeConstraint': {'useEnumeratedValues': 0x1}}]},
                                                                        'name': 'ADCRB',
                                                                        'size': 0x8},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x4,
                                                                        'description': 'ADC '
                                                                                       'Control '
                                                                                       'Register '
                                                                                       'B',
                                                                        'fields': {'field': [{'access': 'read-write',
                                                                                              'bitRange': '[3:0]',
                                                                                              'description': 'C-ADC '
                                                                                                             'Regular '
                                                                                                             'Current '
                                                                                                             'Count '
                                                                                                             'Threshold',
                                                                                              'enumeratedValues': {'enumeratedValue': [{'description': '1',
                                                                                                                                        'name': '1',
                                                                                                                                        'value': 0x0},
                                                                                                                                       {'description': '2',
                                                                                                                                        'name': '2',
                                                                                                                                        'value': 0x1},
                                                                                                                                       {'description': '3',
                                                                                                                                        'name': '3',
                                                                                                                                        'value': 0x2},
                                                                                                                                       {'description': '4',
                                                                                                                                        'name': '4',
                                                                                                                                        'value': 0x3},
                                                                                                                                       {'description': '5',
                                                                                                                                        'name': '5',
                                                                                                                                        'value': 0x4},
                                                                                                                                       {'description': '6',
                                                                                                                                        'name': '6',
                                                                                                                                        'value': 0x5},
                                                                                                                                       {'description': '7',
                                                                                                                                        'name': '7',
                                                                                                                                        'value': 0x6},
                                                                                                                                       {'description': '8',
                                                                                                                                        'name': '8',
                                                                                                                                        'value': 0x7},
                                                                                                                                       {'description': '9',
                                                                                                                                        'name': '9',
                                                                                                                                        'value': 0x8},
                                                                                                                                       {'description': '10',
                                                                                                                                        'name': '10',
                                                                                                                                        'value': 0x9},
                                                                                                                                       {'description': '11',
                                                                                                                                        'name': '11',
                                                                                                                                        'value': 0xA},
                                                                                                                                       {'description': '12',
                                                                                                                                        'name': '12',
                                                                                                                                        'value': 0xB},
                                                                                                                                       {'description': '13',
                                                                                                                                        'name': '13',
                                                                                                                                        'value': 0xC},
                                                                                                                                       {'description': '14',
                                                                                                                                        'name': '14',
                                                                                                                                        'value': 0xD},
                                                                                                                                       {'description': '15',
                                                                                                                                        'name': '15',
                                                                                                                                        'value': 0xE},
                                                                                                                                       {'description': '16',
                                                                                                                                        'name': '16',
                                                                                                                                        'value': 0xF}]},
                                                                                              'name': 'CADRCT',
                                                                                              'writeConstraint': {'useEnumeratedValues': 0x1}},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[5:4]',
                                                                                              'description': 'C-ADC '
                                                                                                             'Regular '
                                                                                                             'Current '
                                                                                                             'Comparator '
                                                                                                             'Mode',
                                                                                              'enumeratedValues': {'enumeratedValue': [{'description': 'Comparator '
                                                                                                                                                       'Disabled',
                                                                                                                                        'name': 'COMPARATOR_DISABLED',
                                                                                                                                        'value': 0x0},
                                                                                                                                       {'description': 'Comparator '
                                                                                                                                                       'Enabled. '
                                                                                                                                                       'Regular '
                                                                                                                                                       'Current '
                                                                                                                                                       'Counter '
                                                                                                                                                       'counts '
                                                                                                                                                       'up '
                                                                                                                                                       'if '
                                                                                                                                                       'Accumulated '
                                                                                                                                                       'Current '
                                                                                                                                                       'is '
                                                                                                                                                       'above '
                                                                                                                                                       'threshold '
                                                                                                                                                       'and '
                                                                                                                                                       'is '
                                                                                                                                                       'reset '
                                                                                                                                                       'if '
                                                                                                                                                       'Accumulated '
                                                                                                                                                       'Current '
                                                                                                                                                       'is '
                                                                                                                                                       'below '
                                                                                                                                                       'threshold.',
                                                                                                                                        'name': 'COMPARATOR_ENABLED_REGULAR_CURRENT_COUNTER_COUNTS_UP_IF_ACCUMULATED_CURRENT_IS_ABOVE_THRESHOLD_AND_IS_RESET_IF_ACCUMULATED_CURRENT_IS_BELOW_THRESHOLD',
                                                                                                                                        'value': 0x1},
                                                                                                                                       {'description': 'Comparator '
                                                                                                                                                       'Enabled. '
                                                                                                                                                       'Regular '
                                                                                                                                                       'Current '
                                                                                                                                                       'Counter '
                                                                                                                                                       'counts '
                                                                                                                                                       'up '
                                                                                                                                                       'if '
                                                                                                                                                       'Accumulated '
                                                                                                                                                       'Current '
                                                                                                                                                       'is '
                                                                                                                                                       'above '
                                                                                                                                                       'threshold '
                                                                                                                                                       'and '
                                                                                                                                                       'down '
                                                                                                                                                       'if '
                                                                                                                                                       'Accumulated '
                                                                                                                                                       'Current '
                                                                                                                                                       'is '
                                                                                                                                                       'below '
                                                                                                                                                       'threshold.',
                                                                                                                                        'name': 'COMPARATOR_ENABLED_REGULAR_CURRENT_COUNTER_COUNTS_UP_IF_ACCUMULATED_CURRENT_IS_ABOVE_THRESHOLD_AND_DOWN_IF_ACCUMULATED_CURRENT_IS_BELOW_THRESHOLD',
                                                                                                                                        'value': 0x2},
                                                                                                                                       {'description': 'Reserved',
                                                                                                                                        'name': 'RESERVED',
                                                                                                                                        'value': 0x3}]},
                                                                                              'name': 'CADRCM',
                                                                                              'writeConstraint': {'useEnumeratedValues': 0x1}},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[7:7]',
                                                                                              'description': 'C-ADC '
                                                                                                             'Enable',
                                                                                              'name': 'CADEN'}]},
                                                                        'name': 'ADCRC',
                                                                        'size': 0x8},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x5,
                                                                        'description': 'ADC '
                                                                                       'Control '
                                                                                       'Register '
                                                                                       'D',
                                                                        'fields': {'field': [{'access': 'read-write',
                                                                                              'bitRange': '[0:0]',
                                                                                              'description': 'C-ADC '
                                                                                                             'Diagnostics '
                                                                                                             'Channel '
                                                                                                             'Select',
                                                                                              'name': 'CADDSEL'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[2:1]',
                                                                                              'description': 'C-ADC '
                                                                                                             'Pin '
                                                                                                             'Diagnostics '
                                                                                                             'Mode',
                                                                                              'enumeratedValues': {'enumeratedValue': [{'description': 'No '
                                                                                                                                                       'current '
                                                                                                                                                       'source '
                                                                                                                                                       'is '
                                                                                                                                                       'enabled',
                                                                                                                                        'name': 'NO_CURRENT_SOURCE_IS_ENABLED',
                                                                                                                                        'value': 0x0},
                                                                                                                                       {'description': 'Current '
                                                                                                                                                       'source '
                                                                                                                                                       'on '
                                                                                                                                                       'PI '
                                                                                                                                                       'pin '
                                                                                                                                                       'enabled',
                                                                                                                                        'name': 'CURRENT_SOURCE_ON_PI_PIN_ENABLED',
                                                                                                                                        'value': 0x1},
                                                                                                                                       {'description': 'Current '
                                                                                                                                                       'source '
                                                                                                                                                       'on '
                                                                                                                                                       'NI '
                                                                                                                                                       'pin '
                                                                                                                                                       'enabled',
                                                                                                                                        'name': 'CURRENT_SOURCE_ON_NI_PIN_ENABLED',
                                                                                                                                        'value': 0x2},
                                                                                                                                       {'description': 'Current '
                                                                                                                                                       'source '
                                                                                                                                                       'on '
                                                                                                                                                       'both '
                                                                                                                                                       'PI/NI '
                                                                                                                                                       'pins '
                                                                                                                                                       'enabled',
                                                                                                                                        'name': 'CURRENT_SOURCE_ON_BOTH_PI_NI_PINS_ENABLED',
                                                                                                                                        'value': 0x3}]},
                                                                                              'name': 'CADPDM',
                                                                                              'writeConstraint': {'useEnumeratedValues': 0x1}},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[5:3]',
                                                                                              'description': 'C-ADC '
                                                                                                             'Gain',
                                                                                              'enumeratedValues': {'enumeratedValue': [{'description': '4x',
                                                                                                                                        'name': '4X',
                                                                                                                                        'value': 0x0},
                                                                                                                                       {'description': '8x',
                                                                                                                                        'name': '8X',
                                                                                                                                        'value': 0x1},
                                                                                                                                       {'description': '16x',
                                                                                                                                        'name': '16X',
                                                                                                                                        'value': 0x2},
                                                                                                                                       {'description': '32x',
                                                                                                                                        'name': '32X',
                                                                                                                                        'value': 0x3},
                                                                                                                                       {'description': '64x',
                                                                                                                                        'name': '64X',
                                                                                                                                        'value': 0x4},
                                                                                                                                       {'description': '128x',
                                                                                                                                        'name': '128X',
                                                                                                                                        'value': 0x5},
                                                                                                                                       {'description': '256x',
                                                                                                                                        'name': '256X',
                                                                                                                                        'value': 0x6},
                                                                                                                                       {'description': 'Reserved',
                                                                                                                                        'name': 'RESERVED',
                                                                                                                                        'value': 0x7}]},
                                                                                              'name': 'CADG',
                                                                                              'writeConstraint': {'useEnumeratedValues': 0x1}}]},
                                                                        'name': 'ADCRD',
                                                                        'size': 0x8},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x6,
                                                                        'description': 'ADC '
                                                                                       'Control '
                                                                                       'Register '
                                                                                       'E',
                                                                        'fields': {'field': [{'access': 'read-write',
                                                                                              'bitRange': '[2:0]',
                                                                                              'description': 'V-ADC '
                                                                                                             'Channel '
                                                                                                             'Select',
                                                                                              'enumeratedValues': {'enumeratedValue': [{'description': 'PV '
                                                                                                                                                       '- '
                                                                                                                                                       'NV',
                                                                                                                                        'name': 'PV_NV',
                                                                                                                                        'value': 0x0},
                                                                                                                                       {'description': 'ADC0 '
                                                                                                                                                       '- '
                                                                                                                                                       'SGND',
                                                                                                                                        'name': 'ADC0_SGND',
                                                                                                                                        'value': 0x1},
                                                                                                                                       {'description': 'ADC1 '
                                                                                                                                                       '- '
                                                                                                                                                       'SGND',
                                                                                                                                        'name': 'ADC1_SGND',
                                                                                                                                        'value': 0x2},
                                                                                                                                       {'description': 'VTEMP '
                                                                                                                                                       '- '
                                                                                                                                                       'GND',
                                                                                                                                        'name': 'VTEMP_GND',
                                                                                                                                        'value': 0x3},
                                                                                                                                       {'description': 'DIAGNOSIS '
                                                                                                                                                       '- '
                                                                                                                                                       'GND '
                                                                                                                                                       '(VREF/TBD)',
                                                                                                                                        'name': 'DIAGNOSIS_GND_VREF_TBD',
                                                                                                                                        'value': 0x4},
                                                                                                                                       {'description': 'Reserved',
                                                                                                                                        'name': 'RESERVED',
                                                                                                                                        'value': 0x7}]},
                                                                                              'name': 'VADMUX',
                                                                                              'writeConstraint': {'useEnumeratedValues': 0x1}},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[4:3]',
                                                                                              'description': 'V-ADC '
                                                                                                             'Pin '
                                                                                                             'Diagnostics '
                                                                                                             'Mode',
                                                                                              'enumeratedValues': {'enumeratedValue': [{'description': 'No '
                                                                                                                                                       'current '
                                                                                                                                                       'source '
                                                                                                                                                       'is '
                                                                                                                                                       'enabled',
                                                                                                                                        'name': 'NO_CURRENT_SOURCE_IS_ENABLED',
                                                                                                                                        'value': 0x0},
                                                                                                                                       {'description': 'Current '
                                                                                                                                                       'source '
                                                                                                                                                       'on '
                                                                                                                                                       'PV '
                                                                                                                                                       'pin '
                                                                                                                                                       'enabled',
                                                                                                                                        'name': 'CURRENT_SOURCE_ON_PV_PIN_ENABLED',
                                                                                                                                        'value': 0x1},
                                                                                                                                       {'description': 'Current '
                                                                                                                                                       'source '
                                                                                                                                                       'on '
                                                                                                                                                       'NV '
                                                                                                                                                       'pin '
                                                                                                                                                       'enabled',
                                                                                                                                        'name': 'CURRENT_SOURCE_ON_NV_PIN_ENABLED',
                                                                                                                                        'value': 0x2},
                                                                                                                                       {'description': 'Current '
                                                                                                                                                       'source '
                                                                                                                                                       'on '
                                                                                                                                                       'both '
                                                                                                                                                       'PV/NV '
                                                                                                                                                       'pins '
                                                                                                                                                       'enabled',
                                                                                                                                        'name': 'CURRENT_SOURCE_ON_BOTH_PV_NV_PINS_ENABLED',
                                                                                                                                        'value': 0x3}]},
                                                                                              'name': 'VADPDM',
                                                                                              'writeConstraint': {'useEnumeratedValues': 0x1}},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[5:5]',
                                                                                              'description': 'V-ADC '
                                                                                                             'Reference '
                                                                                                             'Select',
                                                                                              'enumeratedValues': {'enumeratedValue': [{'description': 'VREF '
                                                                                                                                                       'as '
                                                                                                                                                       'reference',
                                                                                                                                        'name': 'VREF_AS_REFERENCE',
                                                                                                                                        'value': 0x0},
                                                                                                                                       {'description': 'AVDD/3 '
                                                                                                                                                       'as '
                                                                                                                                                       'reference '
                                                                                                                                                       '(for '
                                                                                                                                                       'diagnosis '
                                                                                                                                                       'purpose)',
                                                                                                                                        'name': 'AVDD_3_AS_REFERENCE_FOR_DIAGNOSIS_PURPOSE',
                                                                                                                                        'value': 0x1}]},
                                                                                              'name': 'VADREFS',
                                                                                              'writeConstraint': {'useEnumeratedValues': 0x1}},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[7:7]',
                                                                                              'description': 'V-ADC '
                                                                                                             'Enable',
                                                                                              'name': 'VADEN'}]},
                                                                        'name': 'ADCRE',
                                                                        'size': 0x8},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x7,
                                                                        'description': 'ADC '
                                                                                       'Interrupt '
                                                                                       'Flag '
                                                                                       'Register',
                                                                        'fields': {'field': [{'access': 'read-write',
                                                                                              'bitRange': '[0:0]',
                                                                                              'description': 'C-ADC '
                                                                                                             'Instantaneous '
                                                                                                             'Current '
                                                                                                             'Interrupt '
                                                                                                             'Flag',
                                                                                              'name': 'CADICIF'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[1:1]',
                                                                                              'description': 'C-ADC '
                                                                                                             'Accumulated '
                                                                                                             'Current '
                                                                                                             'Interrupt '
                                                                                                             'Flag',
                                                                                              'name': 'CADACIF'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[2:2]',
                                                                                              'description': 'C-ADC '
                                                                                                             'Regulator '
                                                                                                             'Current '
                                                                                                             'Interrupt '
                                                                                                             'Flag',
                                                                                              'name': 'CADRCIF'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[4:4]',
                                                                                              'description': 'V-DAC '
                                                                                                             'Instantaneous '
                                                                                                             'Voltage '
                                                                                                             'Interrupt '
                                                                                                             'Flag',
                                                                                              'name': 'VADICIF'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[5:5]',
                                                                                              'description': 'V-ADC '
                                                                                                             'Accumulated '
                                                                                                             'Voltage '
                                                                                                             'Interrupt '
                                                                                                             'Flag',
                                                                                              'name': 'VADACIF'}]},
                                                                        'name': 'ADIFR',
                                                                        'size': 0x8},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x8,
                                                                        'description': 'ADC '
                                                                                       'Interrupt '
                                                                                       'Mask '
                                                                                       'Register',
                                                                        'fields': {'field': [{'access': 'read-write',
                                                                                              'bitRange': '[0:0]',
                                                                                              'description': 'C-ADC '
                                                                                                             'Instantaneous '
                                                                                                             'Current '
                                                                                                             'Interrupt '
                                                                                                             'Enable',
                                                                                              'name': 'CADICIE'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[1:1]',
                                                                                              'description': 'C-ADC '
                                                                                                             'Accumulated '
                                                                                                             'Current '
                                                                                                             'Interrupt '
                                                                                                             'Enable',
                                                                                              'name': 'CADACIE'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[2:2]',
                                                                                              'description': 'C-ADC '
                                                                                                             'Regulator '
                                                                                                             'Current '
                                                                                                             'Interrupt '
                                                                                                             'Enable',
                                                                                              'name': 'CADRCIE'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[4:4]',
                                                                                              'description': 'V-DAC '
                                                                                                             'Instantaneous '
                                                                                                             'Voltage '
                                                                                                             'Interrupt '
                                                                                                             'Enable',
                                                                                              'name': 'VADICIE'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[5:5]',
                                                                                              'description': 'V-ADC '
                                                                                                             'Accumulated '
                                                                                                             'Voltage '
                                                                                                             'Interrupt '
                                                                                                             'Enable',
                                                                                              'name': 'VADACIE'}]},
                                                                        'name': 'ADIMR',
                                                                        'size': 0x8},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x0,
                                                                        'description': 'ADC '
                                                                                       'Synchronization '
                                                                                       'Control '
                                                                                       'and '
                                                                                       'Status '
                                                                                       'Register',
                                                                        'fields': {'field': [{'access': 'read-write',
                                                                                              'bitRange': '[1:0]',
                                                                                              'description': 'Synchronization '
                                                                                                             'Command',
                                                                                              'enumeratedValues': {'enumeratedValue': [{'description': 'Reserved',
                                                                                                                                        'name': 'RESERVED',
                                                                                                                                        'value': 0x0},
                                                                                                                                       {'description': 'Reset '
                                                                                                                                                       'and '
                                                                                                                                                       'Synchronize',
                                                                                                                                        'name': 'RESET_AND_SYNCHRONIZE',
                                                                                                                                        'value': 0x1},
                                                                                                                                       {'description': 'Synchronize '
                                                                                                                                                       'on '
                                                                                                                                                       'next '
                                                                                                                                                       'Instantaneous '
                                                                                                                                                       'Conversion',
                                                                                                                                        'name': 'SYNCHRONIZE_ON_NEXT_INSTANTANEOUS_CONVERSION',
                                                                                                                                        'value': 0x2},
                                                                                                                                       {'description': 'Synchronize '
                                                                                                                                                       'on '
                                                                                                                                                       'next '
                                                                                                                                                       'Accumulated '
                                                                                                                                                       'Conversion',
                                                                                                                                        'name': 'SYNCHRONIZE_ON_NEXT_ACCUMULATED_CONVERSION',
                                                                                                                                        'value': 0x3}]},
                                                                                              'name': 'SCMD',
                                                                                              'writeConstraint': {'useEnumeratedValues': 0x1}},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[2:2]',
                                                                                              'description': 'Synchronization '
                                                                                                             'Busy',
                                                                                              'name': 'SBSY'}]},
                                                                        'name': 'ADSCSRA',
                                                                        'size': 0x8},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x1,
                                                                        'description': 'ADC '
                                                                                       'Synchronization '
                                                                                       'Control '
                                                                                       'and '
                                                                                       'Status '
                                                                                       'Register',
                                                                        'fields': {'field': [{'access': 'read-write',
                                                                                              'bitRange': '[0:0]',
                                                                                              'description': 'CADIC '
                                                                                                             'Data '
                                                                                                             'Read '
                                                                                                             'Out '
                                                                                                             'Busy',
                                                                                              'name': 'CADICRB'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[1:1]',
                                                                                              'description': 'CADAC '
                                                                                                             'Data '
                                                                                                             'Read '
                                                                                                             'Out '
                                                                                                             'Busy',
                                                                                              'name': 'CADACRB'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[2:2]',
                                                                                              'description': 'C-ADC '
                                                                                                             'Instantaneous '
                                                                                                             'Conversion '
                                                                                                             'Polarity '
                                                                                                             'Status',
                                                                                              'name': 'CADICPS'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[4:4]',
                                                                                              'description': 'VADIC '
                                                                                                             'Data '
                                                                                                             'Read '
                                                                                                             'Out '
                                                                                                             'Busy',
                                                                                              'name': 'VADICRB'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[5:5]',
                                                                                              'description': 'VADAC '
                                                                                                             'Data '
                                                                                                             'Read '
                                                                                                             'Out '
                                                                                                             'Busy',
                                                                                              'name': 'VADACRB'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[6:6]',
                                                                                              'description': 'V-ADC '
                                                                                                             'Instantaneous '
                                                                                                             'Conversion '
                                                                                                             'Polarity '
                                                                                                             'Status',
                                                                                              'name': 'VADICPS'}]},
                                                                        'name': 'ADSCSRB',
                                                                        'size': 0x8},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0xD,
                                                                        'description': 'C-ADC '
                                                                                       'Accumulated '
                                                                                       'Conversion '
                                                                                       'Result',
                                                                        'name': 'CADAC0',
                                                                        'size': 0x8,
                                                                        'writeConstraint': {'range': {'maximum': 0xFF,
                                                                                                      'minimum': 0x0}}},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0xE,
                                                                        'description': 'C-ADC '
                                                                                       'Accumulated '
                                                                                       'Conversion '
                                                                                       'Result',
                                                                        'name': 'CADAC1',
                                                                        'size': 0x8,
                                                                        'writeConstraint': {'range': {'maximum': 0xFF,
                                                                                                      'minimum': 0x0}}},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0xF,
                                                                        'description': 'C-ADC '
                                                                                       'Accumulated '
                                                                                       'Conversion '
                                                                                       'Result',
                                                                        'name': 'CADAC2',
                                                                        'size': 0x8,
                                                                        'writeConstraint': {'range': {'maximum': 0xFF,
                                                                                                      'minimum': 0x0}}},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x10,
                                                                        'description': 'C-ADC '
                                                                                       'Accumulated '
                                                                                       'Conversion '
                                                                                       'Result',
                                                                        'name': 'CADAC3',
                                                                        'size': 0x8,
                                                                        'writeConstraint': {'range': {'maximum': 0xFF,
                                                                                                      'minimum': 0x0}}},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0xB,
                                                                        'description': 'C-ADC '
                                                                                       'Instantaneous '
                                                                                       'Conversion '
                                                                                       'Result',
                                                                        'name': 'CADIC',
                                                                        'size': 0x10,
                                                                        'writeConstraint': {'range': {'maximum': 0xFFFF,
                                                                                                      'minimum': 0x0}}},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x9,
                                                                        'description': 'CC-ADC '
                                                                                       'Regulator '
                                                                                       'Current '
                                                                                       'Comparator '
                                                                                       'Threshold '
                                                                                       'Level',
                                                                        'name': 'CADRCL',
                                                                        'size': 0x10,
                                                                        'writeConstraint': {'range': {'maximum': 0xFFFF,
                                                                                                      'minimum': 0x0}}},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x13,
                                                                        'description': 'V-ADC '
                                                                                       'Accumulated '
                                                                                       'Conversion '
                                                                                       'Result',
                                                                        'name': 'VADAC0',
                                                                        'size': 0x8,
                                                                        'writeConstraint': {'range': {'maximum': 0xFF,
                                                                                                      'minimum': 0x0}}},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x14,
                                                                        'description': 'V-ADC '
                                                                                       'Accumulated '
                                                                                       'Conversion '
                                                                                       'Result',
                                                                        'name': 'VADAC1',
                                                                        'size': 0x8,
                                                                        'writeConstraint': {'range': {'maximum': 0xFF,
                                                                                                      'minimum': 0x0}}},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x15,
                                                                        'description': 'V-ADC '
                                                                                       'Accumulated '
                                                                                       'Conversion '
                                                                                       'Result',
                                                                        'name': 'VADAC2',
                                                                        'size': 0x8,
                                                                        'writeConstraint': {'range': {'maximum': 0xFF,
                                                                                                      'minimum': 0x0}}},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x16,
                                                                        'description': 'V-ADC '
                                                                                       'Accumulated '
                                                                                       'Conversion '
                                                                                       'Result',
                                                                        'name': 'VADAC3',
                                                                        'size': 0x8,
                                                                        'writeConstraint': {'range': {'maximum': 0xFF,
                                                                                                      'minimum': 0x0}}},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x11,
                                                                        'description': 'V-ADC '
                                                                                       'Instantaneous '
                                                                                       'Conversion '
                                                                                       'Result',
                                                                        'name': 'VADIC',
                                                                        'size': 0x10,
                                                                        'writeConstraint': {'range': {'maximum': 0xFFFF,
                                                                                                      'minimum': 0x0}}}]}},
                                           {'addressBlock': [{'offset': 0x0,
                                                              'size': 0x4,
                                                              'usage': 'registers'}],
                                            'baseAddress': 0x8000D1,
                                            'description': 'Bandgap',
                                            'name': 'BANDGAP',
                                            'registers': {'register': [{'access': 'read-write',
                                                                        'addressOffset': 0x2,
                                                                        'description': 'Band '
                                                                                       'Gap '
                                                                                       'Calibration '
                                                                                       'Register '
                                                                                       'A',
                                                                        'fields': {'field': [{'access': 'read-write',
                                                                                              'bitRange': '[7:0]',
                                                                                              'description': 'Band '
                                                                                                             'Gap '
                                                                                                             'Calibration '
                                                                                                             'Nominal',
                                                                                              'name': 'BGCN',
                                                                                              'writeConstraint': {'range': {'maximum': 0xFF,
                                                                                                                            'minimum': 0x0}}}]},
                                                                        'name': 'BGCRA',
                                                                        'size': 0x8},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x1,
                                                                        'description': 'Band '
                                                                                       'Gap '
                                                                                       'Calibration '
                                                                                       'Register '
                                                                                       'B',
                                                                        'fields': {'field': [{'access': 'read-write',
                                                                                              'bitRange': '[7:0]',
                                                                                              'description': 'Band '
                                                                                                             'Gap '
                                                                                                             'Calibration '
                                                                                                             'Linear',
                                                                                              'name': 'BGCL',
                                                                                              'writeConstraint': {'range': {'maximum': 0xFF,
                                                                                                                            'minimum': 0x0}}}]},
                                                                        'name': 'BGCRB',
                                                                        'size': 0x8},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x0,
                                                                        'description': 'Bandgap '
                                                                                       'Control '
                                                                                       'and '
                                                                                       'Status '
                                                                                       'Register '
                                                                                       'A',
                                                                        'fields': {'field': [{'access': 'read-write',
                                                                                              'bitRange': '[2:0]',
                                                                                              'description': 'Band '
                                                                                                             'Gap '
                                                                                                             'Sample '
                                                                                                             'Configuration',
                                                                                              'name': 'BGSC',
                                                                                              'writeConstraint': {'range': {'maximum': 0x7,
                                                                                                                            'minimum': 0x0}}}]},
                                                                        'name': 'BGCSRA',
                                                                        'size': 0x8},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x3,
                                                                        'description': 'Band '
                                                                                       'Gap '
                                                                                       'Lock '
                                                                                       'Register',
                                                                        'fields': {'field': [{'access': 'read-write',
                                                                                              'bitRange': '[0:0]',
                                                                                              'description': 'Band '
                                                                                                             'Gap '
                                                                                                             'Lock',
                                                                                              'name': 'BGPL'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[1:1]',
                                                                                              'description': 'Band '
                                                                                                             'Gap '
                                                                                                             'Lock '
                                                                                                             'Enable',
                                                                                              'name': 'BGPLE'}]},
                                                                        'name': 'BGLR',
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
                                                                                       'and '
                                                                                       'Status '
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
                                                                                              'description': 'Lock '
                                                                                                             'Bit '
                                                                                                             'Set',
                                                                                              'name': 'LBSET'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[4:4]',
                                                                                              'description': 'Read-While-Write '
                                                                                                             'Section '
                                                                                                             'Read '
                                                                                                             'Enable',
                                                                                              'name': 'RWWSRE'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[5:5]',
                                                                                              'description': 'Signature '
                                                                                                             'Row '
                                                                                                             'Read',
                                                                                              'name': 'SIGRD'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[6:6]',
                                                                                              'description': 'Read-While-Write '
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
                                                             {'offset': 0x23,
                                                              'size': 0x1,
                                                              'usage': 'registers'},
                                                             {'offset': 0x26,
                                                              'size': 0x1,
                                                              'usage': 'registers'},
                                                             {'offset': 0x28,
                                                              'size': 0x2,
                                                              'usage': 'registers'},
                                                             {'offset': 0x40,
                                                              'size': 0x1,
                                                              'usage': 'registers'},
                                                             {'offset': 0x9A,
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
                                                          {'description': 'External '
                                                                          'Interrupt '
                                                                          '0',
                                                           'name': 'INT0',
                                                           'value': 0x1},
                                                          {'description': 'Pin '
                                                                          'Change '
                                                                          'Interrupt '
                                                                          '0',
                                                           'name': 'PCINT0',
                                                           'value': 0x2},
                                                          {'description': 'Pin '
                                                                          'Change '
                                                                          'Interrupt '
                                                                          '1',
                                                           'name': 'PCINT1',
                                                           'value': 0x3},
                                                          {'description': 'Watchdog '
                                                                          'Timeout '
                                                                          'Interrupt',
                                                           'name': 'WDT',
                                                           'value': 0x4},
                                                          {'description': 'Wakeup '
                                                                          'Timer '
                                                                          'Overflow',
                                                           'name': 'WAKEUP',
                                                           'value': 0x5},
                                                          {'description': 'Timer '
                                                                          '1 '
                                                                          'Input '
                                                                          'capture',
                                                           'name': 'TIMER1_IC',
                                                           'value': 0x6},
                                                          {'description': 'Timer '
                                                                          '1 '
                                                                          'Compare '
                                                                          'Match '
                                                                          'A',
                                                           'name': 'TIMER1_COMPA',
                                                           'value': 0x7},
                                                          {'description': 'Timer '
                                                                          '1 '
                                                                          'Compare '
                                                                          'Match '
                                                                          'B',
                                                           'name': 'TIMER1_COMPB',
                                                           'value': 0x8},
                                                          {'description': 'Timer '
                                                                          '1 '
                                                                          'overflow',
                                                           'name': 'TIMER1_OVF',
                                                           'value': 0x9},
                                                          {'description': 'Timer '
                                                                          '0 '
                                                                          'Input '
                                                                          'Capture',
                                                           'name': 'TIMER0_IC',
                                                           'value': 0xA},
                                                          {'description': 'Timer '
                                                                          '0 '
                                                                          'Compare '
                                                                          'Match '
                                                                          'A',
                                                           'name': 'TIMER0_COMPA',
                                                           'value': 0xB},
                                                          {'description': 'Timer '
                                                                          '0 '
                                                                          'Compare '
                                                                          'Match '
                                                                          'B',
                                                           'name': 'TIMER0_COMPB',
                                                           'value': 0xC},
                                                          {'description': 'Timer '
                                                                          '0 '
                                                                          'Overflow',
                                                           'name': 'TIMER0_OVF',
                                                           'value': 0xD},
                                                          {'description': 'LIN '
                                                                          'Status '
                                                                          'Interrupt',
                                                           'name': 'LIN_STATUS',
                                                           'value': 0xE},
                                                          {'description': 'LIN '
                                                                          'Error '
                                                                          'Interrupt',
                                                           'name': 'LIN_ERROR',
                                                           'value': 0xF},
                                                          {'description': 'SPI '
                                                                          'Serial '
                                                                          'transfer '
                                                                          'complete',
                                                           'name': 'SPI_STC',
                                                           'value': 0x10},
                                                          {'description': 'Voltage '
                                                                          'ADC '
                                                                          'Instantaneous '
                                                                          'Conversion '
                                                                          'Complete',
                                                           'name': 'VADC_CONV',
                                                           'value': 0x11},
                                                          {'description': 'Voltage '
                                                                          'ADC '
                                                                          'Accumulated '
                                                                          'Conversion '
                                                                          'Complete',
                                                           'name': 'VADC_ACC',
                                                           'value': 0x12},
                                                          {'description': 'C-ADC '
                                                                          'Instantaneous '
                                                                          'Conversion '
                                                                          'Complete',
                                                           'name': 'CADC_CONV',
                                                           'value': 0x13},
                                                          {'description': 'C-ADC '
                                                                          'Regular '
                                                                          'Current',
                                                           'name': 'CADC_REG_CUR',
                                                           'value': 0x14},
                                                          {'description': 'C-ADC '
                                                                          'Accumulated '
                                                                          'Conversion '
                                                                          'Complete',
                                                           'name': 'CADC_ACC',
                                                           'value': 0x15},
                                                          {'description': 'EEPROM '
                                                                          'Ready',
                                                           'name': 'EE_READY',
                                                           'value': 0x16},
                                                          {'description': 'SPM '
                                                                          'Ready',
                                                           'name': 'SPM',
                                                           'value': 0x17},
                                                          {'description': 'PLL '
                                                                          'Lock '
                                                                          'Change '
                                                                          'Interrupt',
                                                           'name': 'PLL',
                                                           'value': 0x18}],
                                            'name': 'CPU',
                                            'registers': {'register': [{'access': 'read-write',
                                                                        'addressOffset': 0x23,
                                                                        'description': 'Clock '
                                                                                       'Prescale '
                                                                                       'Register '
                                                                                       '(read-only '
                                                                                       'for '
                                                                                       'debugger)',
                                                                        'fields': {'field': [{'access': 'read-write',
                                                                                              'bitRange': '[1:0]',
                                                                                              'description': 'Clock '
                                                                                                             'Prescaler '
                                                                                                             'Select '
                                                                                                             'Bits',
                                                                                              'name': 'CLKPS',
                                                                                              'writeConstraint': {'range': {'maximum': 0x3,
                                                                                                                            'minimum': 0x0}}},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[7:7]',
                                                                                              'description': 'Clock '
                                                                                                             'Prescaler '
                                                                                                             'Change '
                                                                                                             'Enable',
                                                                                              'name': 'CLKPCE'}]},
                                                                        'name': 'CLKPR',
                                                                        'size': 0x8},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x40,
                                                                        'description': 'Digital '
                                                                                       'Input '
                                                                                       'Disable '
                                                                                       'Register',
                                                                        'fields': {'field': [{'access': 'read-write',
                                                                                              'bitRange': '[0:0]',
                                                                                              'description': 'When '
                                                                                                             'this '
                                                                                                             'bit '
                                                                                                             'is '
                                                                                                             'written '
                                                                                                             'logic '
                                                                                                             'one, '
                                                                                                             'the '
                                                                                                             'digital '
                                                                                                             'input '
                                                                                                             'buffer '
                                                                                                             'of '
                                                                                                             'the '
                                                                                                             'corresponding '
                                                                                                             'V_ADC '
                                                                                                             'pin '
                                                                                                             'is '
                                                                                                             'disabled.',
                                                                                              'name': 'PA0DID'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[1:1]',
                                                                                              'description': 'When '
                                                                                                             'this '
                                                                                                             'bit '
                                                                                                             'is '
                                                                                                             'written '
                                                                                                             'logic '
                                                                                                             'one, '
                                                                                                             'the '
                                                                                                             'digital '
                                                                                                             'input '
                                                                                                             'buffer '
                                                                                                             'of '
                                                                                                             'the '
                                                                                                             'corresponding '
                                                                                                             'V_ADC '
                                                                                                             'pin '
                                                                                                             'is '
                                                                                                             'disabled.',
                                                                                              'name': 'PA1DID'}]},
                                                                        'name': 'DIDR0',
                                                                        'size': 0x8},
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
                                                                                              'bitRange': '[5:5]',
                                                                                              'description': 'Clock '
                                                                                                             'Output '
                                                                                                             'Enable',
                                                                                              'name': 'CKOE'}]},
                                                                        'name': 'MCUCR',
                                                                        'size': 0x8},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x16,
                                                                        'description': 'MCU '
                                                                                       'Status '
                                                                                       'Register '
                                                                                       '(read-only '
                                                                                       'for '
                                                                                       'debugger)',
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
                                                                                              'description': 'OCD '
                                                                                                             'Reset '
                                                                                                             'Flag',
                                                                                              'name': 'OCDRF'}]},
                                                                        'name': 'MCUSR',
                                                                        'size': 0x8},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x9A,
                                                                        'description': 'PLL '
                                                                                       'Control '
                                                                                       'and '
                                                                                       'Status '
                                                                                       'Register',
                                                                        'fields': {'field': [{'access': 'read-write',
                                                                                              'bitRange': '[0:0]',
                                                                                              'description': 'PLL '
                                                                                                             'Lock '
                                                                                                             'Change '
                                                                                                             'Interrupt '
                                                                                                             'Enable',
                                                                                              'name': 'PLLCIE'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[1:1]',
                                                                                              'description': 'PLL '
                                                                                                             'Lock '
                                                                                                             'Change '
                                                                                                             'Interrupt '
                                                                                                             'Flag',
                                                                                              'name': 'PLLCIF'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[4:4]',
                                                                                              'description': 'PLL '
                                                                                                             'Lock',
                                                                                              'name': 'LOCK'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[5:5]',
                                                                                              'description': 'PLL '
                                                                                                             'Software '
                                                                                                             'Enable',
                                                                                              'name': 'SWEN'}]},
                                                                        'name': 'PLLCSR',
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
                                                                                                             'Timer/Counter0',
                                                                                              'name': 'PRTIM0'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[1:1]',
                                                                                              'description': 'Power '
                                                                                                             'Reduction '
                                                                                                             'Timer/Counter1',
                                                                                              'name': 'PRTIM1'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[2:2]',
                                                                                              'description': 'Power '
                                                                                                             'reduction '
                                                                                                             'SPI',
                                                                                              'name': 'PRSPI'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[3:3]',
                                                                                              'description': 'Power '
                                                                                                             'Reduction '
                                                                                                             'LIN '
                                                                                                             'UART '
                                                                                                             'Interface',
                                                                                              'name': 'PRLIN'}]},
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
                                                                                                                                       {'description': 'ADC',
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
                                                                                                                                       {'description': 'Reserved',
                                                                                                                                        'name': 'VAL_0x04',
                                                                                                                                        'value': 0x4},
                                                                                                                                       {'description': 'Reserved',
                                                                                                                                        'name': 'VAL_0x05',
                                                                                                                                        'value': 0x5},
                                                                                                                                       {'description': 'Standby',
                                                                                                                                        'name': 'STDBY',
                                                                                                                                        'value': 0x6},
                                                                                                                                       {'description': 'Extended '
                                                                                                                                                       'Standby',
                                                                                                                                        'name': 'ESTDBY',
                                                                                                                                        'value': 0x7}]},
                                                                                              'name': 'SM',
                                                                                              'writeConstraint': {'useEnumeratedValues': 0x1}}]},
                                                                        'name': 'SMCR',
                                                                        'size': 0x8},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x28,
                                                                        'description': 'Slow '
                                                                                       'Oscillator '
                                                                                       'Calibration '
                                                                                       'Register '
                                                                                       'A',
                                                                        'name': 'SOSCCALA',
                                                                        'size': 0x8,
                                                                        'writeConstraint': {'range': {'maximum': 0xFF,
                                                                                                      'minimum': 0x0}}},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x29,
                                                                        'description': 'Oscillator '
                                                                                       'Calibration '
                                                                                       'Register '
                                                                                       'B',
                                                                        'name': 'SOSCCALB',
                                                                        'size': 0x8,
                                                                        'writeConstraint': {'range': {'maximum': 0xFF,
                                                                                                      'minimum': 0x0}}},
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
                                                                                       'Read/Write '
                                                                                       'Access',
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
                                                                                                             'Write '
                                                                                                             'Enable',
                                                                                              'name': 'EEPE'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[2:2]',
                                                                                              'description': 'EEPROM '
                                                                                                             'Master '
                                                                                                             'Write '
                                                                                                             'Enable',
                                                                                              'name': 'EEMPE'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[3:3]',
                                                                                              'description': 'EEProm '
                                                                                                             'Ready '
                                                                                                             'Interrupt '
                                                                                                             'Enable',
                                                                                              'name': 'EERIE'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[5:4]',
                                                                                              'description': 'No '
                                                                                                             'Description.',
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
                                                                                              'bitRange': '[0:0]',
                                                                                              'description': 'External '
                                                                                                             'Interrupt '
                                                                                                             'Sense '
                                                                                                             'Control '
                                                                                                             '0 '
                                                                                                             'Bit '
                                                                                                             '0',
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
                                                                                                                                        'value': 0x1}]},
                                                                                              'name': 'ISC00',
                                                                                              'writeConstraint': {'useEnumeratedValues': 0x1}},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[1:1]',
                                                                                              'description': 'External '
                                                                                                             'Interrupt '
                                                                                                             'Sense '
                                                                                                             'Control '
                                                                                                             '0 '
                                                                                                             'Bit '
                                                                                                             '1',
                                                                                              'name': 'ISC01'}]},
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
                                                                                              'bitRange': '[0:0]',
                                                                                              'description': 'External '
                                                                                                             'Interrupt '
                                                                                                             'Flag '
                                                                                                             '0',
                                                                                              'name': 'INTF0'}]},
                                                                        'name': 'EIFR',
                                                                        'size': 0x8},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x2,
                                                                        'description': 'External '
                                                                                       'Interrupt '
                                                                                       'Mask '
                                                                                       'Register',
                                                                        'fields': {'field': [{'access': 'read-write',
                                                                                              'bitRange': '[0:0]',
                                                                                              'description': 'External '
                                                                                                             'Interrupt '
                                                                                                             'Request '
                                                                                                             '0 '
                                                                                                             'Enable',
                                                                                              'name': 'INT0'}]},
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
                                                              'size': 0xB,
                                                              'usage': 'registers'}],
                                            'baseAddress': 0x8000C0,
                                            'description': 'Local Interconnect '
                                                           'Network',
                                            'name': 'LINUART',
                                            'registers': {'register': [{'access': 'read-write',
                                                                        'addressOffset': 0x6,
                                                                        'description': 'LIN '
                                                                                       'Baud '
                                                                                       'Rate '
                                                                                       'High '
                                                                                       'Register',
                                                                        'fields': {'field': [{'access': 'read-write',
                                                                                              'bitRange': '[3:0]',
                                                                                              'description': 'No '
                                                                                                             'Description.',
                                                                                              'name': 'LDIV',
                                                                                              'writeConstraint': {'range': {'maximum': 0xF,
                                                                                                                            'minimum': 0x0}}}]},
                                                                        'name': 'LINBRRH',
                                                                        'size': 0x8},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x5,
                                                                        'description': 'LIN '
                                                                                       'Baud '
                                                                                       'Rate '
                                                                                       'Low '
                                                                                       'Register',
                                                                        'fields': {'field': [{'access': 'read-write',
                                                                                              'bitRange': '[7:0]',
                                                                                              'description': 'No '
                                                                                                             'Description.',
                                                                                              'name': 'LDIV',
                                                                                              'writeConstraint': {'range': {'maximum': 0xFF,
                                                                                                                            'minimum': 0x0}}}]},
                                                                        'name': 'LINBRRL',
                                                                        'size': 0x8},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x4,
                                                                        'description': 'LIN '
                                                                                       'Bit '
                                                                                       'Timing '
                                                                                       'Register',
                                                                        'fields': {'field': [{'access': 'read-write',
                                                                                              'bitRange': '[5:0]',
                                                                                              'description': 'LIN '
                                                                                                             'Bit '
                                                                                                             'Timing '
                                                                                                             'bits',
                                                                                              'name': 'LBT',
                                                                                              'writeConstraint': {'range': {'maximum': 0x3F,
                                                                                                                            'minimum': 0x0}}},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[7:7]',
                                                                                              'description': 'Disable '
                                                                                                             'Bit '
                                                                                                             'Timing '
                                                                                                             'Resynchronization',
                                                                                              'name': 'LDISR'}]},
                                                                        'name': 'LINBTR',
                                                                        'size': 0x8},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x0,
                                                                        'description': 'LIN '
                                                                                       'Control '
                                                                                       'Register',
                                                                        'fields': {'field': [{'access': 'read-write',
                                                                                              'bitRange': '[2:0]',
                                                                                              'description': 'LIN '
                                                                                                             'Command '
                                                                                                             'and '
                                                                                                             'Mode '
                                                                                                             'bits',
                                                                                              'name': 'LCMD',
                                                                                              'writeConstraint': {'range': {'maximum': 0x7,
                                                                                                                            'minimum': 0x0}}},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[3:3]',
                                                                                              'description': 'LIN '
                                                                                                             'or '
                                                                                                             'UART '
                                                                                                             'Enable',
                                                                                              'name': 'LENA'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[5:4]',
                                                                                              'description': 'LIN '
                                                                                                             'Configuration '
                                                                                                             'bits',
                                                                                              'name': 'LCONF',
                                                                                              'writeConstraint': {'range': {'maximum': 0x3,
                                                                                                                            'minimum': 0x0}}},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[6:6]',
                                                                                              'description': 'LIN '
                                                                                                             'Standard',
                                                                                              'name': 'LIN13'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[7:7]',
                                                                                              'description': 'Software '
                                                                                                             'Reset',
                                                                                              'name': 'LSWRES'}]},
                                                                        'name': 'LINCR',
                                                                        'size': 0x8},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0xA,
                                                                        'description': 'LIN '
                                                                                       'Data '
                                                                                       'Register '
                                                                                       '(write-only '
                                                                                       'for '
                                                                                       'debugger)',
                                                                        'fields': {'field': [{'access': 'read-write',
                                                                                              'bitRange': '[7:0]',
                                                                                              'description': 'No '
                                                                                                             'Description.',
                                                                                              'name': 'LDATA',
                                                                                              'writeConstraint': {'range': {'maximum': 0xFF,
                                                                                                                            'minimum': 0x0}}}]},
                                                                        'name': 'LINDAT',
                                                                        'size': 0x8},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x7,
                                                                        'description': 'LIN '
                                                                                       'Data '
                                                                                       'Length '
                                                                                       'Register',
                                                                        'fields': {'field': [{'access': 'read-write',
                                                                                              'bitRange': '[3:0]',
                                                                                              'description': 'LIN '
                                                                                                             'Receive '
                                                                                                             'Data '
                                                                                                             'Length '
                                                                                                             'bits',
                                                                                              'name': 'LRXDL',
                                                                                              'writeConstraint': {'range': {'maximum': 0xF,
                                                                                                                            'minimum': 0x0}}},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[7:4]',
                                                                                              'description': 'LIN '
                                                                                                             'Transmit '
                                                                                                             'Data '
                                                                                                             'Length '
                                                                                                             'bits',
                                                                                              'name': 'LTXDL',
                                                                                              'writeConstraint': {'range': {'maximum': 0xF,
                                                                                                                            'minimum': 0x0}}}]},
                                                                        'name': 'LINDLR',
                                                                        'size': 0x8},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x2,
                                                                        'description': 'LIN '
                                                                                       'Enable '
                                                                                       'Interrupt '
                                                                                       'Register',
                                                                        'fields': {'field': [{'access': 'read-write',
                                                                                              'bitRange': '[0:0]',
                                                                                              'description': 'Enable '
                                                                                                             'Receive '
                                                                                                             'Performed '
                                                                                                             'Interrupt',
                                                                                              'name': 'LENRXOK'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[1:1]',
                                                                                              'description': 'Enable '
                                                                                                             'Transmit '
                                                                                                             'Performed '
                                                                                                             'Interrupt',
                                                                                              'name': 'LENTXOK'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[2:2]',
                                                                                              'description': 'Enable '
                                                                                                             'Identifier '
                                                                                                             'Interrupt',
                                                                                              'name': 'LENIDOK'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[3:3]',
                                                                                              'description': 'Enable '
                                                                                                             'Error '
                                                                                                             'Interrupt',
                                                                                              'name': 'LENERR'}]},
                                                                        'name': 'LINENIR',
                                                                        'size': 0x8},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x3,
                                                                        'description': 'LIN '
                                                                                       'Error '
                                                                                       'Register '
                                                                                       '(read-only '
                                                                                       'for '
                                                                                       'debugger)',
                                                                        'fields': {'field': [{'access': 'read-write',
                                                                                              'bitRange': '[0:0]',
                                                                                              'description': 'Bit '
                                                                                                             'Error '
                                                                                                             'Flag',
                                                                                              'name': 'LBERR'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[1:1]',
                                                                                              'description': 'Checksum '
                                                                                                             'Error '
                                                                                                             'Flag',
                                                                                              'name': 'LCERR'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[2:2]',
                                                                                              'description': 'Parity '
                                                                                                             'Error '
                                                                                                             'Flag',
                                                                                              'name': 'LPERR'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[3:3]',
                                                                                              'description': 'Synchronization '
                                                                                                             'Error '
                                                                                                             'Flag',
                                                                                              'name': 'LSERR'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[4:4]',
                                                                                              'description': 'Framing '
                                                                                                             'Error '
                                                                                                             'Flag',
                                                                                              'name': 'LFERR'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[5:5]',
                                                                                              'description': 'Overrun '
                                                                                                             'Error '
                                                                                                             'Flag',
                                                                                              'name': 'LOVERR'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[6:6]',
                                                                                              'description': 'Frame '
                                                                                                             'Time '
                                                                                                             'Out '
                                                                                                             'Error '
                                                                                                             'Flag',
                                                                                              'name': 'LTOERR'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[7:7]',
                                                                                              'description': 'Abort '
                                                                                                             'Flag',
                                                                                              'name': 'LABORT'}]},
                                                                        'name': 'LINERR',
                                                                        'size': 0x8},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x8,
                                                                        'description': 'LIN '
                                                                                       'Identifier '
                                                                                       'Register',
                                                                        'fields': {'field': [{'access': 'read-write',
                                                                                              'bitRange': '[5:0]',
                                                                                              'description': 'Identifier '
                                                                                                             'bit '
                                                                                                             '5 '
                                                                                                             'or '
                                                                                                             'Data '
                                                                                                             'Length '
                                                                                                             'bits',
                                                                                              'name': 'LID',
                                                                                              'writeConstraint': {'range': {'maximum': 0x3F,
                                                                                                                            'minimum': 0x0}}},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[7:6]',
                                                                                              'description': 'Parity '
                                                                                                             'bits',
                                                                                              'name': 'LP',
                                                                                              'writeConstraint': {'range': {'maximum': 0x3,
                                                                                                                            'minimum': 0x0}}}]},
                                                                        'name': 'LINIDR',
                                                                        'size': 0x8},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x9,
                                                                        'description': 'LIN '
                                                                                       'Data '
                                                                                       'Buffer '
                                                                                       'Selection '
                                                                                       'Register',
                                                                        'fields': {'field': [{'access': 'read-write',
                                                                                              'bitRange': '[2:0]',
                                                                                              'description': 'FIFO '
                                                                                                             'LIN '
                                                                                                             'Data '
                                                                                                             'Buffer '
                                                                                                             'Index '
                                                                                                             'bits',
                                                                                              'name': 'LINDX',
                                                                                              'writeConstraint': {'range': {'maximum': 0x7,
                                                                                                                            'minimum': 0x0}}},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[3:3]',
                                                                                              'description': 'Auto '
                                                                                                             'Increment '
                                                                                                             'of '
                                                                                                             'Data '
                                                                                                             'Buffer '
                                                                                                             'Index '
                                                                                                             '(Active '
                                                                                                             'Low)',
                                                                                              'name': 'LAINC'}]},
                                                                        'name': 'LINSEL',
                                                                        'size': 0x8},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x1,
                                                                        'description': 'LIN '
                                                                                       'Status '
                                                                                       'and '
                                                                                       'Interrupt '
                                                                                       'Register',
                                                                        'fields': {'field': [{'access': 'read-write',
                                                                                              'bitRange': '[0:0]',
                                                                                              'description': 'Receive '
                                                                                                             'Performed '
                                                                                                             'Interrupt',
                                                                                              'name': 'LRXOK'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[1:1]',
                                                                                              'description': 'Transmit '
                                                                                                             'Performed '
                                                                                                             'Interrupt',
                                                                                              'name': 'LTXOK'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[2:2]',
                                                                                              'description': 'Identifier '
                                                                                                             'Interrupt',
                                                                                              'name': 'LIDOK'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[3:3]',
                                                                                              'description': 'Error '
                                                                                                             'Interrupt',
                                                                                              'name': 'LERR'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[4:4]',
                                                                                              'description': 'Busy '
                                                                                                             'Signal',
                                                                                              'name': 'LBUSY'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[7:5]',
                                                                                              'description': 'Identifier '
                                                                                                             'Status '
                                                                                                             'bits',
                                                                                              'name': 'LIDST',
                                                                                              'writeConstraint': {'range': {'maximum': 0x7,
                                                                                                                            'minimum': 0x0}}}]},
                                                                        'name': 'LINSIR',
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
                                                              'usage': 'registers'},
                                                             {'offset': 0xB9,
                                                              'size': 0x1,
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
                                                                        'addressOffset': 0xB9,
                                                                        'description': 'Port '
                                                                                       'B '
                                                                                       'Override',
                                                                        'fields': {'field': [{'access': 'read-write',
                                                                                              'bitRange': '[0:0]',
                                                                                              'description': 'Port '
                                                                                                             'B '
                                                                                                             'Override '
                                                                                                             'Enable '
                                                                                                             '0',
                                                                                              'name': 'PBOE0'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[3:3]',
                                                                                              'description': 'Port '
                                                                                                             'B '
                                                                                                             'Override '
                                                                                                             'Enable '
                                                                                                             '3',
                                                                                              'name': 'PBOE3'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[7:7]',
                                                                                              'description': 'Port '
                                                                                                             'B '
                                                                                                             'Override '
                                                                                                             'Change '
                                                                                                             'Enable',
                                                                                              'name': 'PBOVCE'}]},
                                                                        'name': 'PBOV',
                                                                        'size': 0x8},
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
                                                              'size': 0x3,
                                                              'usage': 'registers'}],
                                            'baseAddress': 0x80004C,
                                            'description': 'Serial Peripheral '
                                                           'Interface',
                                            'name': 'SPI',
                                            'registers': {'register': [{'access': 'read-write',
                                                                        'addressOffset': 0x0,
                                                                        'description': 'SPI '
                                                                                       'Control '
                                                                                       'Register',
                                                                        'fields': {'field': [{'access': 'read-write',
                                                                                              'bitRange': '[1:0]',
                                                                                              'description': 'SPI '
                                                                                                             'Clock '
                                                                                                             'Rate '
                                                                                                             'Selects',
                                                                                              'enumeratedValues': {'enumeratedValue': [{'description': 'fosc/4',
                                                                                                                                        'name': 'FOSC_4',
                                                                                                                                        'value': 0x0},
                                                                                                                                       {'description': 'fosc/16',
                                                                                                                                        'name': 'FOSC_16',
                                                                                                                                        'value': 0x1},
                                                                                                                                       {'description': 'fosc/128',
                                                                                                                                        'name': 'FOSC_128',
                                                                                                                                        'value': 0x3}]},
                                                                                              'name': 'SPR',
                                                                                              'writeConstraint': {'useEnumeratedValues': 0x1}},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[2:2]',
                                                                                              'description': 'Clock '
                                                                                                             'Phase',
                                                                                              'name': 'CPHA'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[3:3]',
                                                                                              'description': 'Clock '
                                                                                                             'polarity',
                                                                                              'name': 'CPOL'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[4:4]',
                                                                                              'description': 'Master/Slave '
                                                                                                             'Select',
                                                                                              'name': 'MSTR'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[5:5]',
                                                                                              'description': 'Data '
                                                                                                             'Order',
                                                                                              'name': 'DORD'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[6:6]',
                                                                                              'description': 'SPI '
                                                                                                             'Enable',
                                                                                              'name': 'SPE'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[7:7]',
                                                                                              'description': 'SPI '
                                                                                                             'Interrupt '
                                                                                                             'Enable',
                                                                                              'name': 'SPIE'}]},
                                                                        'name': 'SPCR',
                                                                        'size': 0x8},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x2,
                                                                        'description': 'SPI '
                                                                                       'Data '
                                                                                       'Register '
                                                                                       '(write-only '
                                                                                       'for '
                                                                                       'debugger)',
                                                                        'name': 'SPDR',
                                                                        'size': 0x8,
                                                                        'writeConstraint': {'range': {'maximum': 0xFF,
                                                                                                      'minimum': 0x0}}},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x1,
                                                                        'description': 'SPI '
                                                                                       'Status '
                                                                                       'Register '
                                                                                       '(read-only '
                                                                                       'for '
                                                                                       'debugger)',
                                                                        'fields': {'field': [{'access': 'read-write',
                                                                                              'bitRange': '[0:0]',
                                                                                              'description': 'Double '
                                                                                                             'SPI '
                                                                                                             'Speed '
                                                                                                             'Bit',
                                                                                              'name': 'SPI2X'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[6:6]',
                                                                                              'description': 'Write '
                                                                                                             'Collision '
                                                                                                             'Flag',
                                                                                              'name': 'WCOL'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[7:7]',
                                                                                              'description': 'SPI '
                                                                                                             'Interrupt '
                                                                                                             'Flag',
                                                                                              'name': 'SPIF'}]},
                                                                        'name': 'SPSR',
                                                                        'size': 0x8}]}},
                                           {'addressBlock': [{'offset': 0x0,
                                                              'size': 0x1,
                                                              'usage': 'registers'},
                                                             {'offset': 0xE,
                                                              'size': 0x7,
                                                              'usage': 'registers'},
                                                             {'offset': 0x39,
                                                              'size': 0x1,
                                                              'usage': 'registers'}],
                                            'baseAddress': 0x800035,
                                            'description': 'Timer/Counter, '
                                                           '16-bit',
                                            'name': 'TC0',
                                            'registers': {'register': [{'access': 'read-write',
                                                                        'addressOffset': 0xE,
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
                                                                        'addressOffset': 0x13,
                                                                        'description': 'Output '
                                                                                       'Compare '
                                                                                       'Register '
                                                                                       '0A',
                                                                        'name': 'OCR0A',
                                                                        'size': 0x8,
                                                                        'writeConstraint': {'range': {'maximum': 0xFF,
                                                                                                      'minimum': 0x0}}},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x14,
                                                                        'description': 'Output '
                                                                                       'Compare '
                                                                                       'Register '
                                                                                       'B',
                                                                        'name': 'OCR0B',
                                                                        'size': 0x8,
                                                                        'writeConstraint': {'range': {'maximum': 0xFF,
                                                                                                      'minimum': 0x0}}},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0xF,
                                                                        'description': 'Timer/Counter '
                                                                                       '0 '
                                                                                       'Control '
                                                                                       'Register '
                                                                                       'A',
                                                                        'fields': {'field': [{'access': 'read-write',
                                                                                              'bitRange': '[0:0]',
                                                                                              'description': 'Waveform '
                                                                                                             'Generation '
                                                                                                             'Mode',
                                                                                              'name': 'WGM00'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[3:3]',
                                                                                              'description': 'Input '
                                                                                                             'Capture '
                                                                                                             'Select',
                                                                                              'name': 'ICS0'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[4:4]',
                                                                                              'description': 'Input '
                                                                                                             'Capture '
                                                                                                             'Edge '
                                                                                                             'Select',
                                                                                              'name': 'ICES0'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[5:5]',
                                                                                              'description': 'Input '
                                                                                                             'Capture '
                                                                                                             'Noise '
                                                                                                             'Canceler',
                                                                                              'name': 'ICNC0'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[6:6]',
                                                                                              'description': 'Input '
                                                                                                             'Capture '
                                                                                                             'Mode '
                                                                                                             'Enable',
                                                                                              'name': 'ICEN0'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[7:7]',
                                                                                              'description': 'Timer/Counter '
                                                                                                             'Width',
                                                                                              'name': 'TCW0'}]},
                                                                        'name': 'TCCR0A',
                                                                        'size': 0x8},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x10,
                                                                        'description': 'Timer/Counter0 '
                                                                                       'Control '
                                                                                       'Register '
                                                                                       'B',
                                                                        'fields': {'field': [{'access': 'read-write',
                                                                                              'bitRange': '[0:0]',
                                                                                              'description': 'Clock '
                                                                                                             'Select0 '
                                                                                                             'bit '
                                                                                                             '0',
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
                                                                                                                                        'value': 0x1}]},
                                                                                              'name': 'CS00',
                                                                                              'writeConstraint': {'useEnumeratedValues': 0x1}},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[1:1]',
                                                                                              'description': 'Clock '
                                                                                                             'Select0 '
                                                                                                             'bit '
                                                                                                             '1',
                                                                                              'name': 'CS01'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[2:2]',
                                                                                              'description': 'Clock '
                                                                                                             'Select0 '
                                                                                                             'bit '
                                                                                                             '2',
                                                                                              'name': 'CS02'}]},
                                                                        'name': 'TCCR0B',
                                                                        'size': 0x8},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x11,
                                                                        'description': 'Timer '
                                                                                       'Counter '
                                                                                       '0  '
                                                                                       'Bytes',
                                                                        'name': 'TCNT0',
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
                                                                                              'description': 'Timer/Counter0 '
                                                                                                             'Overflow '
                                                                                                             'Flag',
                                                                                              'name': 'TOV0'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[1:1]',
                                                                                              'description': 'Timer/Counter0 '
                                                                                                             'Output '
                                                                                                             'Compare '
                                                                                                             'Flag '
                                                                                                             'A',
                                                                                              'name': 'OCF0A'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[2:2]',
                                                                                              'description': 'Timer/Counter0 '
                                                                                                             'Output '
                                                                                                             'Compare '
                                                                                                             'Flag '
                                                                                                             'B',
                                                                                              'name': 'OCF0B'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[3:3]',
                                                                                              'description': 'Timer/Counter '
                                                                                                             '0 '
                                                                                                             'Input '
                                                                                                             'Capture '
                                                                                                             'Flag',
                                                                                              'name': 'ICF0'}]},
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
                                                                                              'description': 'Timer/Counter0 '
                                                                                                             'Overflow '
                                                                                                             'Interrupt '
                                                                                                             'Enable',
                                                                                              'name': 'TOIE0'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[1:1]',
                                                                                              'description': 'Timer/Counter0 '
                                                                                                             'Output '
                                                                                                             'Compare '
                                                                                                             'A '
                                                                                                             'Interrupt '
                                                                                                             'Enable',
                                                                                              'name': 'OCIE0A'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[2:2]',
                                                                                              'description': 'Timer/Counter0 '
                                                                                                             'Output '
                                                                                                             'Compare '
                                                                                                             'B '
                                                                                                             'Interrupt '
                                                                                                             'Enable',
                                                                                              'name': 'OCIE0B'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[3:3]',
                                                                                              'description': 'Timer/Counter '
                                                                                                             'n '
                                                                                                             'Input '
                                                                                                             'Capture '
                                                                                                             'Interrupt '
                                                                                                             'Enable',
                                                                                              'name': 'ICIE0'}]},
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
                                                             {'offset': 0x4A,
                                                              'size': 0x2,
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
                                                                        'addressOffset': 0x52,
                                                                        'description': 'Output '
                                                                                       'Compare '
                                                                                       'Register '
                                                                                       '1A',
                                                                        'name': 'OCR1A',
                                                                        'size': 0x8,
                                                                        'writeConstraint': {'range': {'maximum': 0xFF,
                                                                                                      'minimum': 0x0}}},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x53,
                                                                        'description': 'Output '
                                                                                       'Compare '
                                                                                       'Register '
                                                                                       'B',
                                                                        'name': 'OCR1B',
                                                                        'size': 0x8,
                                                                        'writeConstraint': {'range': {'maximum': 0xFF,
                                                                                                      'minimum': 0x0}}},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x4A,
                                                                        'description': 'Timer/Counter '
                                                                                       '1 '
                                                                                       'Control '
                                                                                       'Register '
                                                                                       'A',
                                                                        'fields': {'field': [{'access': 'read-write',
                                                                                              'bitRange': '[0:0]',
                                                                                              'description': 'Waveform '
                                                                                                             'Generation '
                                                                                                             'Mode',
                                                                                              'name': 'WGM10'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[3:3]',
                                                                                              'description': 'Input '
                                                                                                             'Capture '
                                                                                                             'Select',
                                                                                              'name': 'ICS1'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[4:4]',
                                                                                              'description': 'Input '
                                                                                                             'Capture '
                                                                                                             'Edge '
                                                                                                             'Select',
                                                                                              'name': 'ICES1'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[5:5]',
                                                                                              'description': 'Input '
                                                                                                             'Capture '
                                                                                                             'Noise '
                                                                                                             'Canceler',
                                                                                              'name': 'ICNC1'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[6:6]',
                                                                                              'description': 'Input '
                                                                                                             'Capture '
                                                                                                             'Mode '
                                                                                                             'Enable',
                                                                                              'name': 'ICEN1'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[7:7]',
                                                                                              'description': 'Timer/Counter '
                                                                                                             'Width',
                                                                                              'name': 'TCW1'}]},
                                                                        'name': 'TCCR1A',
                                                                        'size': 0x8},
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
                                                                                                             'bis',
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
                                                                                              'name': 'CS',
                                                                                              'writeConstraint': {'useEnumeratedValues': 0x1}}]},
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
                                                                                              'name': 'OCF1A'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[2:2]',
                                                                                              'description': 'Timer/Counter1 '
                                                                                                             'Output '
                                                                                                             'Compare '
                                                                                                             'Flag '
                                                                                                             'B',
                                                                                              'name': 'OCF1B'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[3:3]',
                                                                                              'description': 'Timer/Counter '
                                                                                                             '1 '
                                                                                                             'Input '
                                                                                                             'Capture '
                                                                                                             'Flag',
                                                                                              'name': 'ICF1'}]},
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
                                                                                                             'A '
                                                                                                             'Interrupt '
                                                                                                             'Enable',
                                                                                              'name': 'OCIE1A'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[2:2]',
                                                                                              'description': 'Timer/Counter1 '
                                                                                                             'Output '
                                                                                                             'Compare '
                                                                                                             'B '
                                                                                                             'Interrupt '
                                                                                                             'Enable',
                                                                                              'name': 'OCIE1B'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[3:3]',
                                                                                              'description': 'Timer/Counter '
                                                                                                             'n '
                                                                                                             'Input '
                                                                                                             'Capture '
                                                                                                             'Interrupt '
                                                                                                             'Enable',
                                                                                              'name': 'ICIE1'}]},
                                                                        'name': 'TIMSK1',
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
                                                                                       'and '
                                                                                       'Status '
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
                                                                                              'name': 'WUTP',
                                                                                              'writeConstraint': {'range': {'maximum': 0x7,
                                                                                                                            'minimum': 0x0}}},
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
                                                              'usage': 'registers'},
                                                             {'offset': 0x3,
                                                              'size': 0x1,
                                                              'usage': 'registers'}],
                                            'baseAddress': 0x800060,
                                            'description': 'Watchdog Timer',
                                            'name': 'WDT',
                                            'registers': {'register': [{'access': 'read-write',
                                                                        'addressOffset': 0x3,
                                                                        'description': 'Watchdog '
                                                                                       'Timer '
                                                                                       'Configuration '
                                                                                       'Lock '
                                                                                       'Register',
                                                                        'fields': {'field': [{'access': 'read-write',
                                                                                              'bitRange': '[0:0]',
                                                                                              'description': 'Watchdog '
                                                                                                             'Timer '
                                                                                                             'Configuration '
                                                                                                             'Lock '
                                                                                                             'Enable',
                                                                                              'name': 'WDCLE'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[2:1]',
                                                                                              'description': 'Watchdog '
                                                                                                             'Timer '
                                                                                                             'Configuration '
                                                                                                             'Lock '
                                                                                                             'bits',
                                                                                              'name': 'WDCL',
                                                                                              'writeConstraint': {'range': {'maximum': 0x3,
                                                                                                                            'minimum': 0x0}}}]},
                                                                        'name': 'WDTCLR',
                                                                        'size': 0x8},
                                                                       {'access': 'read-write',
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