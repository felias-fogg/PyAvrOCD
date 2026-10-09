# Device description for at90usb1286, generated from Microchip's AT90USB1286.atdf by
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
    'name': 'at90usb1286',
    'architecture': 'avr8',

    # eeprom
    'eeprom_address_byte': 0x0000,
    'eeprom_size_bytes': 0x1000,
    'eeprom_page_size_bytes': 0x08,
    'eeprom_read_size_bytes': 0x01,
    'eeprom_write_size_bytes': 0x01,
    'eeprom_chiperase_effect': ChiperaseEffect.CONDITIONALLY_ERASED_AVR,
    'eeprom_isolated_erase': False,

    # flash
    'flash_address_byte': 0x0000,
    'flash_size_bytes': 0x20000,
    'flash_page_size_bytes': 0x100,
    'flash_read_size_bytes': 0x02,
    'flash_write_size_bytes': 0x100,
    'flash_chiperase_effect': ChiperaseEffect.ALWAYS_ERASED,
    'flash_isolated_erase': False,

    # fuses
    'fuses_address_byte': 0,
    'fuses_size_bytes': 0x0003,
    'fuses_page_size_bytes': 0x01,
    'fuses_read_size_bytes': 0x01,
    'fuses_write_size_bytes': 0x01,
    'fuses_chiperase_effect': ChiperaseEffect.NOT_ERASED,
    'fuses_isolated_erase': False,

    # internal_sram
    'internal_sram_address_byte': 0x0100,
    'internal_sram_size_bytes': 0x2000,
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
    'ocd_rev' : 3,
    'ocd_base' : 0x31,
    'eear_base' : 0x21,
    'eear_size' : 2,
    'eecr_base' : 0x1F,
    'eedr_base' : 0x20,
    'spmcsr_base' : 0x57,
    'osccal_base' : 0x46,
    'ocden_base' : 0x01,
    'ocden_mask' : 0x80,
    'bootrst_base' : 0x01,
    'bootrst_mask' : 0x01,
    'eesave_base' : 0x01,
    'eesave_mask' : 0x08,
    'tcnt0_base' : 0x46,
    'cs0_base' : 0x45,
    'toie0_base' : 0x6E,
    'toie0_mask' : 0x01,
    'masked_registers' : [0x4e, 0x51, 0xce, 0xf1],
    'ronly_registers' : [0x20, 0x23, 0x26, 0x29, 0x2c, 0x2f, 0x35, 0x36, 0x37, 0x38, 0x3b, 0x3c, 0x4d, 0x50, 0x54, 0x60, 0x7a, 0xbc, 0xc8, 0xd9, 0xe6, 0xef, 0xf2, 0xf3],
    'device_id': 0x1E9782,
    'interface': 'ISP+HVPP+JTAG',

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
            'name': 'AT90USB1286',
            'peripherals': {'peripheral': [{'addressBlock': [{'offset': 0x0,
                                                              'size': 0x1,
                                                              'usage': 'registers'},
                                                             {'offset': 0x2B,
                                                              'size': 0x1,
                                                              'usage': 'registers'},
                                                             {'offset': 0x2F,
                                                              'size': 0x1,
                                                              'usage': 'registers'}],
                                            'baseAddress': 0x800050,
                                            'description': 'Analog Comparator',
                                            'name': 'AC',
                                            'registers': {'register': [{'access': 'read-write',
                                                                        'addressOffset': 0x0,
                                                                        'description': 'Analog '
                                                                                       'Comparator '
                                                                                       'Control '
                                                                                       'And '
                                                                                       'Status '
                                                                                       'Register '
                                                                                       '(read-only '
                                                                                       'for '
                                                                                       'debugger)',
                                                                        'fields': {'field': [{'access': 'read-write',
                                                                                              'bitRange': '[1:0]',
                                                                                              'description': 'Analog '
                                                                                                             'Comparator '
                                                                                                             'Interrupt '
                                                                                                             'Mode '
                                                                                                             'Select '
                                                                                                             'bits',
                                                                                              'enumeratedValues': {'enumeratedValue': [{'description': 'Interrupt '
                                                                                                                                                       'on '
                                                                                                                                                       'Toggle',
                                                                                                                                        'name': 'INTERRUPT_ON_TOGGLE',
                                                                                                                                        'value': 0x0},
                                                                                                                                       {'description': 'Reserved',
                                                                                                                                        'name': 'RESERVED',
                                                                                                                                        'value': 0x1},
                                                                                                                                       {'description': 'Interrupt '
                                                                                                                                                       'on '
                                                                                                                                                       'Falling '
                                                                                                                                                       'Edge',
                                                                                                                                        'name': 'INTERRUPT_ON_FALLING_EDGE',
                                                                                                                                        'value': 0x2},
                                                                                                                                       {'description': 'Interrupt '
                                                                                                                                                       'on '
                                                                                                                                                       'Rising '
                                                                                                                                                       'Edge',
                                                                                                                                        'name': 'INTERRUPT_ON_RISING_EDGE',
                                                                                                                                        'value': 0x3}]},
                                                                                              'name': 'ACIS',
                                                                                              'writeConstraint': {'useEnumeratedValues': 0x1}},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[2:2]',
                                                                                              'description': 'Analog '
                                                                                                             'Comparator '
                                                                                                             'Input '
                                                                                                             'Capture '
                                                                                                             'Enable',
                                                                                              'name': 'ACIC'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[3:3]',
                                                                                              'description': 'Analog '
                                                                                                             'Comparator '
                                                                                                             'Interrupt '
                                                                                                             'Enable',
                                                                                              'name': 'ACIE'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[4:4]',
                                                                                              'description': 'Analog '
                                                                                                             'Comparator '
                                                                                                             'Interrupt '
                                                                                                             'Flag',
                                                                                              'name': 'ACI'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[5:5]',
                                                                                              'description': 'Analog '
                                                                                                             'Compare '
                                                                                                             'Output',
                                                                                              'name': 'ACO'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[6:6]',
                                                                                              'description': 'Analog '
                                                                                                             'Comparator '
                                                                                                             'Bandgap '
                                                                                                             'Select',
                                                                                              'name': 'ACBG'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[7:7]',
                                                                                              'description': 'Analog '
                                                                                                             'Comparator '
                                                                                                             'Disable',
                                                                                              'name': 'ACD'}]},
                                                                        'name': 'ACSR',
                                                                        'size': 0x8},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x2B,
                                                                        'description': 'ADC '
                                                                                       'Control '
                                                                                       'and '
                                                                                       'Status '
                                                                                       'Register '
                                                                                       'B',
                                                                        'fields': {'field': [{'access': 'read-write',
                                                                                              'bitRange': '[6:6]',
                                                                                              'description': 'Analog '
                                                                                                             'Comparator '
                                                                                                             'Multiplexer '
                                                                                                             'Enable',
                                                                                              'name': 'ACME'}]},
                                                                        'name': 'ADCSRB',
                                                                        'size': 0x8},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x2F,
                                                                        'description': 'No '
                                                                                       'Description.',
                                                                        'fields': {'field': [{'access': 'read-write',
                                                                                              'bitRange': '[0:0]',
                                                                                              'description': 'AIN0 '
                                                                                                             'Digital '
                                                                                                             'Input '
                                                                                                             'Disable',
                                                                                              'name': 'AIN0D'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[1:1]',
                                                                                              'description': 'AIN1 '
                                                                                                             'Digital '
                                                                                                             'Input '
                                                                                                             'Disable',
                                                                                              'name': 'AIN1D'}]},
                                                                        'name': 'DIDR1',
                                                                        'size': 0x8}]}},
                                           {'addressBlock': [{'offset': 0x0,
                                                              'size': 0x5,
                                                              'usage': 'registers'},
                                                             {'offset': 0x6,
                                                              'size': 0x1,
                                                              'usage': 'registers'}],
                                            'baseAddress': 0x800078,
                                            'description': 'Analog-to-Digital '
                                                           'Converter',
                                            'name': 'ADC',
                                            'registers': {'register': [{'access': 'read-write',
                                                                        'addressOffset': 0x0,
                                                                        'description': 'ADC '
                                                                                       'Data '
                                                                                       'Register  '
                                                                                       'Bytes',
                                                                        'name': 'ADC',
                                                                        'size': 0x10,
                                                                        'writeConstraint': {'range': {'maximum': 0xFFFF,
                                                                                                      'minimum': 0x0}}},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x2,
                                                                        'description': 'The '
                                                                                       'ADC '
                                                                                       'Control '
                                                                                       'and '
                                                                                       'Status '
                                                                                       'register '
                                                                                       '(read-only '
                                                                                       'for '
                                                                                       'debugger)',
                                                                        'fields': {'field': [{'access': 'read-write',
                                                                                              'bitRange': '[2:0]',
                                                                                              'description': 'ADC '
                                                                                                             'Prescaler '
                                                                                                             'Select '
                                                                                                             'Bits',
                                                                                              'enumeratedValues': {'enumeratedValue': [{'description': '2',
                                                                                                                                        'name': '2',
                                                                                                                                        'value': 0x1},
                                                                                                                                       {'description': '4',
                                                                                                                                        'name': '4',
                                                                                                                                        'value': 0x2},
                                                                                                                                       {'description': '8',
                                                                                                                                        'name': '8',
                                                                                                                                        'value': 0x3},
                                                                                                                                       {'description': '16',
                                                                                                                                        'name': '16',
                                                                                                                                        'value': 0x4},
                                                                                                                                       {'description': '32',
                                                                                                                                        'name': '32',
                                                                                                                                        'value': 0x5},
                                                                                                                                       {'description': '64',
                                                                                                                                        'name': '64',
                                                                                                                                        'value': 0x6},
                                                                                                                                       {'description': '128',
                                                                                                                                        'name': '128',
                                                                                                                                        'value': 0x7}]},
                                                                                              'name': 'ADPS',
                                                                                              'writeConstraint': {'useEnumeratedValues': 0x1}},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[3:3]',
                                                                                              'description': 'ADC '
                                                                                                             'Interrupt '
                                                                                                             'Enable',
                                                                                              'name': 'ADIE'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[4:4]',
                                                                                              'description': 'ADC '
                                                                                                             'Interrupt '
                                                                                                             'Flag',
                                                                                              'name': 'ADIF'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[5:5]',
                                                                                              'description': 'ADC '
                                                                                                             'Auto '
                                                                                                             'Trigger '
                                                                                                             'Enable',
                                                                                              'name': 'ADATE'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[6:6]',
                                                                                              'description': 'ADC '
                                                                                                             'Start '
                                                                                                             'Conversion',
                                                                                              'name': 'ADSC'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[7:7]',
                                                                                              'description': 'ADC '
                                                                                                             'Enable',
                                                                                              'name': 'ADEN'}]},
                                                                        'name': 'ADCSRA',
                                                                        'size': 0x8},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x3,
                                                                        'description': 'ADC '
                                                                                       'Control '
                                                                                       'and '
                                                                                       'Status '
                                                                                       'Register '
                                                                                       'B',
                                                                        'fields': {'field': [{'access': 'read-write',
                                                                                              'bitRange': '[2:0]',
                                                                                              'description': 'ADC '
                                                                                                             'Auto '
                                                                                                             'Trigger '
                                                                                                             'Sources',
                                                                                              'enumeratedValues': {'enumeratedValue': [{'description': 'Free '
                                                                                                                                                       'Running '
                                                                                                                                                       'mode',
                                                                                                                                        'name': 'FREE_RUNNING_MODE',
                                                                                                                                        'value': 0x0},
                                                                                                                                       {'description': 'Analog '
                                                                                                                                                       'Comparator',
                                                                                                                                        'name': 'ANALOG_COMPARATOR',
                                                                                                                                        'value': 0x1},
                                                                                                                                       {'description': 'External '
                                                                                                                                                       'Interrupt '
                                                                                                                                                       'Request '
                                                                                                                                                       '0',
                                                                                                                                        'name': 'EXTERNAL_INTERRUPT_REQUEST_0',
                                                                                                                                        'value': 0x2},
                                                                                                                                       {'description': 'Timer/Counter0 '
                                                                                                                                                       'Compare '
                                                                                                                                                       'Match '
                                                                                                                                                       'A',
                                                                                                                                        'name': 'TIMER_COUNTER0_COMPARE_MATCH_A',
                                                                                                                                        'value': 0x3},
                                                                                                                                       {'description': 'Timer/Counter0 '
                                                                                                                                                       'Overflow',
                                                                                                                                        'name': 'TIMER_COUNTER0_OVERFLOW',
                                                                                                                                        'value': 0x4},
                                                                                                                                       {'description': 'Timer/Counter1 '
                                                                                                                                                       'Compare '
                                                                                                                                                       'Match '
                                                                                                                                                       'B',
                                                                                                                                        'name': 'TIMER_COUNTER1_COMPARE_MATCH_B',
                                                                                                                                        'value': 0x5},
                                                                                                                                       {'description': 'Timer/Counter1 '
                                                                                                                                                       'Overflow',
                                                                                                                                        'name': 'TIMER_COUNTER1_OVERFLOW',
                                                                                                                                        'value': 0x6},
                                                                                                                                       {'description': 'Timer/Counter1 '
                                                                                                                                                       'Capture '
                                                                                                                                                       'Event',
                                                                                                                                        'name': 'TIMER_COUNTER1_CAPTURE_EVENT',
                                                                                                                                        'value': 0x7}]},
                                                                                              'name': 'ADTS',
                                                                                              'writeConstraint': {'useEnumeratedValues': 0x1}},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[7:7]',
                                                                                              'description': 'ADC '
                                                                                                             'High '
                                                                                                             'Speed '
                                                                                                             'Mode',
                                                                                              'name': 'ADHSM'}]},
                                                                        'name': 'ADCSRB',
                                                                        'size': 0x8},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x4,
                                                                        'description': 'The '
                                                                                       'ADC '
                                                                                       'multiplexer '
                                                                                       'Selection '
                                                                                       'Register',
                                                                        'fields': {'field': [{'access': 'read-write',
                                                                                              'bitRange': '[4:0]',
                                                                                              'description': 'Analog '
                                                                                                             'Channel '
                                                                                                             'and '
                                                                                                             'Gain '
                                                                                                             'Selection '
                                                                                                             'Bits',
                                                                                              'name': 'MUX',
                                                                                              'writeConstraint': {'range': {'maximum': 0x1F,
                                                                                                                            'minimum': 0x0}}},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[5:5]',
                                                                                              'description': 'Left '
                                                                                                             'Adjust '
                                                                                                             'Result',
                                                                                              'name': 'ADLAR'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[7:6]',
                                                                                              'description': 'Reference '
                                                                                                             'Selection '
                                                                                                             'Bits',
                                                                                              'enumeratedValues': {'enumeratedValue': [{'description': 'AREF, '
                                                                                                                                                       'Internal '
                                                                                                                                                       'Vref '
                                                                                                                                                       'turned '
                                                                                                                                                       'off',
                                                                                                                                        'name': 'AREF_INTERNAL_VREF_TURNED_OFF',
                                                                                                                                        'value': 0x0},
                                                                                                                                       {'description': 'AVCC '
                                                                                                                                                       'with '
                                                                                                                                                       'external '
                                                                                                                                                       'capacitor '
                                                                                                                                                       'at '
                                                                                                                                                       'AREF '
                                                                                                                                                       'pin',
                                                                                                                                        'name': 'AVCC_WITH_EXTERNAL_CAPACITOR_AT_AREF_PIN',
                                                                                                                                        'value': 0x1},
                                                                                                                                       {'description': 'Reserved',
                                                                                                                                        'name': 'RESERVED',
                                                                                                                                        'value': 0x2},
                                                                                                                                       {'description': 'Internal '
                                                                                                                                                       '2.56V '
                                                                                                                                                       'Voltage '
                                                                                                                                                       'Reference '
                                                                                                                                                       'with '
                                                                                                                                                       'external '
                                                                                                                                                       'capacitor '
                                                                                                                                                       'at '
                                                                                                                                                       'AREF '
                                                                                                                                                       'pin',
                                                                                                                                        'name': 'INTERNAL_2_56V_VOLTAGE_REFERENCE_WITH_EXTERNAL_CAPACITOR_AT_AREF_PIN',
                                                                                                                                        'value': 0x3}]},
                                                                                              'name': 'REFS',
                                                                                              'writeConstraint': {'useEnumeratedValues': 0x1}}]},
                                                                        'name': 'ADMUX',
                                                                        'size': 0x8},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x6,
                                                                        'description': 'Digital '
                                                                                       'Input '
                                                                                       'Disable '
                                                                                       'Register '
                                                                                       '1',
                                                                        'fields': {'field': [{'access': 'read-write',
                                                                                              'bitRange': '[0:0]',
                                                                                              'description': 'ADC0 '
                                                                                                             'Digital '
                                                                                                             'input '
                                                                                                             'Disable',
                                                                                              'name': 'ADC0D'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[1:1]',
                                                                                              'description': 'ADC1 '
                                                                                                             'Digital '
                                                                                                             'input '
                                                                                                             'Disable',
                                                                                              'name': 'ADC1D'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[2:2]',
                                                                                              'description': 'ADC2 '
                                                                                                             'Digital '
                                                                                                             'input '
                                                                                                             'Disable',
                                                                                              'name': 'ADC2D'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[3:3]',
                                                                                              'description': 'ADC3 '
                                                                                                             'Digital '
                                                                                                             'input '
                                                                                                             'Disable',
                                                                                              'name': 'ADC3D'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[4:4]',
                                                                                              'description': 'ADC4 '
                                                                                                             'Digital '
                                                                                                             'input '
                                                                                                             'Disable',
                                                                                              'name': 'ADC4D'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[5:5]',
                                                                                              'description': 'ADC5 '
                                                                                                             'Digital '
                                                                                                             'input '
                                                                                                             'Disable',
                                                                                              'name': 'ADC5D'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[6:6]',
                                                                                              'description': 'ADC6 '
                                                                                                             'Digital '
                                                                                                             'input '
                                                                                                             'Disable',
                                                                                              'name': 'ADC6D'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[7:7]',
                                                                                              'description': 'ADC7 '
                                                                                                             'Digital '
                                                                                                             'input '
                                                                                                             'Disable',
                                                                                              'name': 'ADC7D'}]},
                                                                        'name': 'DIDR0',
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
                                                              'usage': 'registers'},
                                                             {'offset': 0xC,
                                                              'size': 0x2,
                                                              'usage': 'registers'},
                                                             {'offset': 0x15,
                                                              'size': 0x3,
                                                              'usage': 'registers'},
                                                             {'offset': 0x1D,
                                                              'size': 0x5,
                                                              'usage': 'registers'},
                                                             {'offset': 0x23,
                                                              'size': 0x1,
                                                              'usage': 'registers'},
                                                             {'offset': 0x26,
                                                              'size': 0x3,
                                                              'usage': 'registers'},
                                                             {'offset': 0x36,
                                                              'size': 0x2,
                                                              'usage': 'registers'}],
                                            'baseAddress': 0x80003E,
                                            'description': 'CPU Registers',
                                            'interrupt': [{'description': 'External '
                                                                          'Pin,Power-on '
                                                                          'Reset,Brown-out '
                                                                          'Reset,Watchdog '
                                                                          'Reset,and '
                                                                          'JTAG '
                                                                          'AVR '
                                                                          'Reset. '
                                                                          'See '
                                                                          'Datasheet.     ',
                                                           'name': 'RESET',
                                                           'value': 0x0},
                                                          {'description': 'External '
                                                                          'Interrupt '
                                                                          'Request '
                                                                          '0',
                                                           'name': 'INT0',
                                                           'value': 0x1},
                                                          {'description': 'External '
                                                                          'Interrupt '
                                                                          'Request '
                                                                          '1',
                                                           'name': 'INT1',
                                                           'value': 0x2},
                                                          {'description': 'External '
                                                                          'Interrupt '
                                                                          'Request '
                                                                          '2',
                                                           'name': 'INT2',
                                                           'value': 0x3},
                                                          {'description': 'External '
                                                                          'Interrupt '
                                                                          'Request '
                                                                          '3',
                                                           'name': 'INT3',
                                                           'value': 0x4},
                                                          {'description': 'External '
                                                                          'Interrupt '
                                                                          'Request '
                                                                          '4',
                                                           'name': 'INT4',
                                                           'value': 0x5},
                                                          {'description': 'External '
                                                                          'Interrupt '
                                                                          'Request '
                                                                          '5',
                                                           'name': 'INT5',
                                                           'value': 0x6},
                                                          {'description': 'External '
                                                                          'Interrupt '
                                                                          'Request '
                                                                          '6',
                                                           'name': 'INT6',
                                                           'value': 0x7},
                                                          {'description': 'External '
                                                                          'Interrupt '
                                                                          'Request '
                                                                          '7',
                                                           'name': 'INT7',
                                                           'value': 0x8},
                                                          {'description': 'Pin '
                                                                          'Change '
                                                                          'Interrupt '
                                                                          'Request '
                                                                          '0',
                                                           'name': 'PCINT0',
                                                           'value': 0x9},
                                                          {'description': 'USB '
                                                                          'General '
                                                                          'Interrupt '
                                                                          'Request',
                                                           'name': 'USB_GEN',
                                                           'value': 0xA},
                                                          {'description': 'USB '
                                                                          'Endpoint/Pipe '
                                                                          'Interrupt '
                                                                          'Communication '
                                                                          'Request',
                                                           'name': 'USB_COM',
                                                           'value': 0xB},
                                                          {'description': 'Watchdog '
                                                                          'Time-out '
                                                                          'Interrupt',
                                                           'name': 'WDT',
                                                           'value': 0xC},
                                                          {'description': 'Timer/Counter2 '
                                                                          'Compare '
                                                                          'Match '
                                                                          'A',
                                                           'name': 'TIMER2_COMPA',
                                                           'value': 0xD},
                                                          {'description': 'Timer/Counter2 '
                                                                          'Compare '
                                                                          'Match '
                                                                          'B',
                                                           'name': 'TIMER2_COMPB',
                                                           'value': 0xE},
                                                          {'description': 'Timer/Counter2 '
                                                                          'Overflow',
                                                           'name': 'TIMER2_OVF',
                                                           'value': 0xF},
                                                          {'description': 'Timer/Counter1 '
                                                                          'Capture '
                                                                          'Event',
                                                           'name': 'TIMER1_CAPT',
                                                           'value': 0x10},
                                                          {'description': 'Timer/Counter1 '
                                                                          'Compare '
                                                                          'Match '
                                                                          'A',
                                                           'name': 'TIMER1_COMPA',
                                                           'value': 0x11},
                                                          {'description': 'Timer/Counter1 '
                                                                          'Compare '
                                                                          'Match '
                                                                          'B',
                                                           'name': 'TIMER1_COMPB',
                                                           'value': 0x12},
                                                          {'description': 'Timer/Counter1 '
                                                                          'Compare '
                                                                          'Match '
                                                                          'C',
                                                           'name': 'TIMER1_COMPC',
                                                           'value': 0x13},
                                                          {'description': 'Timer/Counter1 '
                                                                          'Overflow',
                                                           'name': 'TIMER1_OVF',
                                                           'value': 0x14},
                                                          {'description': 'Timer/Counter0 '
                                                                          'Compare '
                                                                          'Match '
                                                                          'A',
                                                           'name': 'TIMER0_COMPA',
                                                           'value': 0x15},
                                                          {'description': 'Timer/Counter0 '
                                                                          'Compare '
                                                                          'Match '
                                                                          'B',
                                                           'name': 'TIMER0_COMPB',
                                                           'value': 0x16},
                                                          {'description': 'Timer/Counter0 '
                                                                          'Overflow',
                                                           'name': 'TIMER0_OVF',
                                                           'value': 0x17},
                                                          {'description': 'SPI '
                                                                          'Serial '
                                                                          'Transfer '
                                                                          'Complete',
                                                           'name': 'SPI_STC',
                                                           'value': 0x18},
                                                          {'description': 'USART1, '
                                                                          'Rx '
                                                                          'Complete',
                                                           'name': 'USART1_RX',
                                                           'value': 0x19},
                                                          {'description': 'USART1 '
                                                                          'Data '
                                                                          'register '
                                                                          'Empty',
                                                           'name': 'USART1_UDRE',
                                                           'value': 0x1A},
                                                          {'description': 'USART1, '
                                                                          'Tx '
                                                                          'Complete',
                                                           'name': 'USART1_TX',
                                                           'value': 0x1B},
                                                          {'description': 'Analog '
                                                                          'Comparator',
                                                           'name': 'ANALOG_COMP',
                                                           'value': 0x1C},
                                                          {'description': 'ADC '
                                                                          'Conversion '
                                                                          'Complete',
                                                           'name': 'ADC',
                                                           'value': 0x1D},
                                                          {'description': 'EEPROM '
                                                                          'Ready',
                                                           'name': 'EE_READY',
                                                           'value': 0x1E},
                                                          {'description': 'Timer/Counter3 '
                                                                          'Capture '
                                                                          'Event',
                                                           'name': 'TIMER3_CAPT',
                                                           'value': 0x1F},
                                                          {'description': 'Timer/Counter3 '
                                                                          'Compare '
                                                                          'Match '
                                                                          'A',
                                                           'name': 'TIMER3_COMPA',
                                                           'value': 0x20},
                                                          {'description': 'Timer/Counter3 '
                                                                          'Compare '
                                                                          'Match '
                                                                          'B',
                                                           'name': 'TIMER3_COMPB',
                                                           'value': 0x21},
                                                          {'description': 'Timer/Counter3 '
                                                                          'Compare '
                                                                          'Match '
                                                                          'C',
                                                           'name': 'TIMER3_COMPC',
                                                           'value': 0x22},
                                                          {'description': 'Timer/Counter3 '
                                                                          'Overflow',
                                                           'name': 'TIMER3_OVF',
                                                           'value': 0x23},
                                                          {'description': '2-wire '
                                                                          'Serial '
                                                                          'Interface        ',
                                                           'name': 'TWI',
                                                           'value': 0x24},
                                                          {'description': 'Store '
                                                                          'Program '
                                                                          'Memory '
                                                                          'Read',
                                                           'name': 'SPM_READY',
                                                           'value': 0x25}],
                                            'name': 'CPU',
                                            'registers': {'register': [{'access': 'read-write',
                                                                        'addressOffset': 0x23,
                                                                        'description': 'No '
                                                                                       'Description.',
                                                                        'fields': {'field': [{'access': 'read-write',
                                                                                              'bitRange': '[3:0]',
                                                                                              'description': 'No '
                                                                                                             'Description.',
                                                                                              'enumeratedValues': {'enumeratedValue': [{'description': '1',
                                                                                                                                        'name': '1',
                                                                                                                                        'value': 0x0},
                                                                                                                                       {'description': '2',
                                                                                                                                        'name': '2',
                                                                                                                                        'value': 0x1},
                                                                                                                                       {'description': '4',
                                                                                                                                        'name': '4',
                                                                                                                                        'value': 0x2},
                                                                                                                                       {'description': '8',
                                                                                                                                        'name': '8',
                                                                                                                                        'value': 0x3},
                                                                                                                                       {'description': '16',
                                                                                                                                        'name': '16',
                                                                                                                                        'value': 0x4},
                                                                                                                                       {'description': '32',
                                                                                                                                        'name': '32',
                                                                                                                                        'value': 0x5},
                                                                                                                                       {'description': '64',
                                                                                                                                        'name': '64',
                                                                                                                                        'value': 0x6},
                                                                                                                                       {'description': '128',
                                                                                                                                        'name': '128',
                                                                                                                                        'value': 0x7},
                                                                                                                                       {'description': '256',
                                                                                                                                        'name': '256',
                                                                                                                                        'value': 0x8}]},
                                                                                              'name': 'CLKPS',
                                                                                              'writeConstraint': {'useEnumeratedValues': 0x1}},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[7:7]',
                                                                                              'description': 'No '
                                                                                                             'Description.',
                                                                                              'name': 'CLKPCE'}]},
                                                                        'name': 'CLKPR',
                                                                        'size': 0x8},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x1E,
                                                                        'description': 'Extended '
                                                                                       'Indirect '
                                                                                       'Register',
                                                                        'name': 'EIND',
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
                                                                        'fields': {'field': [{'access': 'read-write',
                                                                                              'bitRange': '[0:0]',
                                                                                              'description': 'General '
                                                                                                             'Purpose '
                                                                                                             'IO '
                                                                                                             'Register '
                                                                                                             '0 '
                                                                                                             'bit '
                                                                                                             '0',
                                                                                              'name': 'GPIOR00'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[1:1]',
                                                                                              'description': 'General '
                                                                                                             'Purpose '
                                                                                                             'IO '
                                                                                                             'Register '
                                                                                                             '0 '
                                                                                                             'bit '
                                                                                                             '1',
                                                                                              'name': 'GPIOR01'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[2:2]',
                                                                                              'description': 'General '
                                                                                                             'Purpose '
                                                                                                             'IO '
                                                                                                             'Register '
                                                                                                             '0 '
                                                                                                             'bit '
                                                                                                             '2',
                                                                                              'name': 'GPIOR02'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[3:3]',
                                                                                              'description': 'General '
                                                                                                             'Purpose '
                                                                                                             'IO '
                                                                                                             'Register '
                                                                                                             '0 '
                                                                                                             'bit '
                                                                                                             '3',
                                                                                              'name': 'GPIOR03'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[4:4]',
                                                                                              'description': 'General '
                                                                                                             'Purpose '
                                                                                                             'IO '
                                                                                                             'Register '
                                                                                                             '0 '
                                                                                                             'bit '
                                                                                                             '4',
                                                                                              'name': 'GPIOR04'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[5:5]',
                                                                                              'description': 'General '
                                                                                                             'Purpose '
                                                                                                             'IO '
                                                                                                             'Register '
                                                                                                             '0 '
                                                                                                             'bit '
                                                                                                             '5',
                                                                                              'name': 'GPIOR05'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[6:6]',
                                                                                              'description': 'General '
                                                                                                             'Purpose '
                                                                                                             'IO '
                                                                                                             'Register '
                                                                                                             '0 '
                                                                                                             'bit '
                                                                                                             '6',
                                                                                              'name': 'GPIOR06'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[7:7]',
                                                                                              'description': 'General '
                                                                                                             'Purpose '
                                                                                                             'IO '
                                                                                                             'Register '
                                                                                                             '0 '
                                                                                                             'bit '
                                                                                                             '7',
                                                                                              'name': 'GPIOR07'}]},
                                                                        'name': 'GPIOR0',
                                                                        'size': 0x8},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0xC,
                                                                        'description': 'General '
                                                                                       'Purpose '
                                                                                       'IO '
                                                                                       'Register '
                                                                                       '1',
                                                                        'fields': {'field': [{'access': 'read-write',
                                                                                              'bitRange': '[7:0]',
                                                                                              'description': 'General '
                                                                                                             'Purpose '
                                                                                                             'IO '
                                                                                                             'Register '
                                                                                                             '1 '
                                                                                                             'bis',
                                                                                              'name': 'GPIOR',
                                                                                              'writeConstraint': {'range': {'maximum': 0xFF,
                                                                                                                            'minimum': 0x0}}}]},
                                                                        'name': 'GPIOR1',
                                                                        'size': 0x8},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0xD,
                                                                        'description': 'General '
                                                                                       'Purpose '
                                                                                       'IO '
                                                                                       'Register '
                                                                                       '2',
                                                                        'fields': {'field': [{'access': 'read-write',
                                                                                              'bitRange': '[7:0]',
                                                                                              'description': 'General '
                                                                                                             'Purpose '
                                                                                                             'IO '
                                                                                                             'Register '
                                                                                                             '2 '
                                                                                                             'bis',
                                                                                              'name': 'GPIOR',
                                                                                              'writeConstraint': {'range': {'maximum': 0xFF,
                                                                                                                            'minimum': 0x0}}}]},
                                                                        'name': 'GPIOR2',
                                                                        'size': 0x8},
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
                                                                                                             'Interface '
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
                                                                                              'name': 'BORF'},
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
                                                                        'addressOffset': 0x28,
                                                                        'description': 'Oscillator '
                                                                                       'Calibration '
                                                                                       'Value',
                                                                        'fields': {'field': [{'access': 'read-write',
                                                                                              'bitRange': '[7:0]',
                                                                                              'description': 'Oscillator '
                                                                                                             'Calibration ',
                                                                                              'name': 'OSCCAL',
                                                                                              'writeConstraint': {'range': {'maximum': 0xFF,
                                                                                                                            'minimum': 0x0}}}]},
                                                                        'name': 'OSCCAL',
                                                                        'size': 0x8},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x26,
                                                                        'description': 'Power '
                                                                                       'Reduction '
                                                                                       'Register0',
                                                                        'fields': {'field': [{'access': 'read-write',
                                                                                              'bitRange': '[0:0]',
                                                                                              'description': 'Power '
                                                                                                             'Reduction '
                                                                                                             'ADC',
                                                                                              'name': 'PRADC'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[2:2]',
                                                                                              'description': 'Power '
                                                                                                             'Reduction '
                                                                                                             'Serial '
                                                                                                             'Peripheral '
                                                                                                             'Interface',
                                                                                              'name': 'PRSPI'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[3:3]',
                                                                                              'description': 'Power '
                                                                                                             'Reduction '
                                                                                                             'Timer/Counter1',
                                                                                              'name': 'PRTIM1'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[5:5]',
                                                                                              'description': 'Power '
                                                                                                             'Reduction '
                                                                                                             'Timer/Counter0',
                                                                                              'name': 'PRTIM0'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[6:6]',
                                                                                              'description': 'Power '
                                                                                                             'Reduction '
                                                                                                             'Timer/Counter2',
                                                                                              'name': 'PRTIM2'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[7:7]',
                                                                                              'description': 'Power '
                                                                                                             'Reduction '
                                                                                                             'TWI',
                                                                                              'name': 'PRTWI'}]},
                                                                        'name': 'PRR0',
                                                                        'size': 0x8},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x27,
                                                                        'description': 'Power '
                                                                                       'Reduction '
                                                                                       'Register1',
                                                                        'fields': {'field': [{'access': 'read-write',
                                                                                              'bitRange': '[0:0]',
                                                                                              'description': 'Power '
                                                                                                             'Reduction '
                                                                                                             'USART1',
                                                                                              'name': 'PRUSART1'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[3:3]',
                                                                                              'description': 'Power '
                                                                                                             'Reduction '
                                                                                                             'Timer/Counter3',
                                                                                              'name': 'PRTIM3'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[7:7]',
                                                                                              'description': 'Power '
                                                                                                             'Reduction '
                                                                                                             'USB',
                                                                                              'name': 'PRUSB'}]},
                                                                        'name': 'PRR1',
                                                                        'size': 0x8},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x1D,
                                                                        'description': 'RAM '
                                                                                       'Page '
                                                                                       'Z '
                                                                                       'Select '
                                                                                       'Register',
                                                                        'name': 'RAMPZ',
                                                                        'size': 0x8,
                                                                        'writeConstraint': {'range': {'maximum': 0xFF,
                                                                                                      'minimum': 0x0}}},
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
                                                                        'size': 0x8},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x36,
                                                                        'description': 'External '
                                                                                       'Memory '
                                                                                       'Control '
                                                                                       'Register '
                                                                                       'A',
                                                                        'fields': {'field': [{'access': 'read-write',
                                                                                              'bitRange': '[1:0]',
                                                                                              'description': 'Wait '
                                                                                                             'state '
                                                                                                             'select '
                                                                                                             'bit '
                                                                                                             'lower '
                                                                                                             'page',
                                                                                              'enumeratedValues': {'enumeratedValue': [{'description': 'No '
                                                                                                                                                       'wait-states',
                                                                                                                                        'name': 'NO_WAIT_STATES',
                                                                                                                                        'value': 0x0},
                                                                                                                                       {'description': 'Wait '
                                                                                                                                                       'one '
                                                                                                                                                       'cycle '
                                                                                                                                                       'during '
                                                                                                                                                       'read/write '
                                                                                                                                                       'strobe',
                                                                                                                                        'name': 'WAIT_ONE_CYCLE_DURING_READ_WRITE_STROBE',
                                                                                                                                        'value': 0x1},
                                                                                                                                       {'description': 'Wait '
                                                                                                                                                       'two '
                                                                                                                                                       'cycles '
                                                                                                                                                       'during '
                                                                                                                                                       'read/write '
                                                                                                                                                       'strobe',
                                                                                                                                        'name': 'WAIT_TWO_CYCLES_DURING_READ_WRITE_STROBE',
                                                                                                                                        'value': 0x2},
                                                                                                                                       {'description': 'Wait '
                                                                                                                                                       'two '
                                                                                                                                                       'cycles '
                                                                                                                                                       'during '
                                                                                                                                                       'read/write '
                                                                                                                                                       'and '
                                                                                                                                                       'wait '
                                                                                                                                                       'one '
                                                                                                                                                       'cycle '
                                                                                                                                                       'before '
                                                                                                                                                       'driving '
                                                                                                                                                       'out '
                                                                                                                                                       'new '
                                                                                                                                                       'address',
                                                                                                                                        'name': 'WAIT_TWO_CYCLES_DURING_READ_WRITE_AND_WAIT_ONE_CYCLE_BEFORE_DRIVING_OUT_NEW_ADDRESS',
                                                                                                                                        'value': 0x3}]},
                                                                                              'name': 'SRW0',
                                                                                              'writeConstraint': {'useEnumeratedValues': 0x1}},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[3:2]',
                                                                                              'description': 'Wait '
                                                                                                             'state '
                                                                                                             'select '
                                                                                                             'bit '
                                                                                                             'upper '
                                                                                                             'page',
                                                                                              'enumeratedValues': {'enumeratedValue': [{'description': 'No '
                                                                                                                                                       'wait-states',
                                                                                                                                        'name': 'NO_WAIT_STATES',
                                                                                                                                        'value': 0x0},
                                                                                                                                       {'description': 'Wait '
                                                                                                                                                       'one '
                                                                                                                                                       'cycle '
                                                                                                                                                       'during '
                                                                                                                                                       'read/write '
                                                                                                                                                       'strobe',
                                                                                                                                        'name': 'WAIT_ONE_CYCLE_DURING_READ_WRITE_STROBE',
                                                                                                                                        'value': 0x1},
                                                                                                                                       {'description': 'Wait '
                                                                                                                                                       'two '
                                                                                                                                                       'cycles '
                                                                                                                                                       'during '
                                                                                                                                                       'read/write '
                                                                                                                                                       'strobe',
                                                                                                                                        'name': 'WAIT_TWO_CYCLES_DURING_READ_WRITE_STROBE',
                                                                                                                                        'value': 0x2},
                                                                                                                                       {'description': 'Wait '
                                                                                                                                                       'two '
                                                                                                                                                       'cycles '
                                                                                                                                                       'during '
                                                                                                                                                       'read/write '
                                                                                                                                                       'and '
                                                                                                                                                       'wait '
                                                                                                                                                       'one '
                                                                                                                                                       'cycle '
                                                                                                                                                       'before '
                                                                                                                                                       'driving '
                                                                                                                                                       'out '
                                                                                                                                                       'new '
                                                                                                                                                       'address',
                                                                                                                                        'name': 'WAIT_TWO_CYCLES_DURING_READ_WRITE_AND_WAIT_ONE_CYCLE_BEFORE_DRIVING_OUT_NEW_ADDRESS',
                                                                                                                                        'value': 0x3}]},
                                                                                              'name': 'SRW1',
                                                                                              'writeConstraint': {'useEnumeratedValues': 0x1}},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[6:4]',
                                                                                              'description': 'Wait '
                                                                                                             'state '
                                                                                                             'page '
                                                                                                             'limit',
                                                                                              'enumeratedValues': {'enumeratedValue': [{'description': 'LS '
                                                                                                                                                       '= '
                                                                                                                                                       'N/A, '
                                                                                                                                                       'US '
                                                                                                                                                       '= '
                                                                                                                                                       '0x1100 '
                                                                                                                                                       '- '
                                                                                                                                                       '0xFFFF',
                                                                                                                                        'name': 'LS_N_A_US_0X1100_0XFFFF',
                                                                                                                                        'value': 0x0},
                                                                                                                                       {'description': 'LS '
                                                                                                                                                       '= '
                                                                                                                                                       '0x2100 '
                                                                                                                                                       '- '
                                                                                                                                                       '0x1FFF, '
                                                                                                                                                       'US '
                                                                                                                                                       '= '
                                                                                                                                                       '0x2000 '
                                                                                                                                                       '- '
                                                                                                                                                       '0xFFFF',
                                                                                                                                        'name': 'LS_0X2100_0X1FFF_US_0X2000_0XFFFF',
                                                                                                                                        'value': 0x1},
                                                                                                                                       {'description': 'LS '
                                                                                                                                                       '= '
                                                                                                                                                       '0x2100 '
                                                                                                                                                       '- '
                                                                                                                                                       '0x3FFF, '
                                                                                                                                                       'US '
                                                                                                                                                       '= '
                                                                                                                                                       '0x4000 '
                                                                                                                                                       '- '
                                                                                                                                                       '0xFFFF',
                                                                                                                                        'name': 'LS_0X2100_0X3FFF_US_0X4000_0XFFFF',
                                                                                                                                        'value': 0x2},
                                                                                                                                       {'description': 'LS '
                                                                                                                                                       '= '
                                                                                                                                                       '0x2100 '
                                                                                                                                                       '- '
                                                                                                                                                       '0x5FFF, '
                                                                                                                                                       'US '
                                                                                                                                                       '= '
                                                                                                                                                       '0x6000 '
                                                                                                                                                       '- '
                                                                                                                                                       '0xFFFF',
                                                                                                                                        'name': 'LS_0X2100_0X5FFF_US_0X6000_0XFFFF',
                                                                                                                                        'value': 0x3},
                                                                                                                                       {'description': 'LS '
                                                                                                                                                       '= '
                                                                                                                                                       '0x2100 '
                                                                                                                                                       '- '
                                                                                                                                                       '0x7FFF, '
                                                                                                                                                       'US '
                                                                                                                                                       '= '
                                                                                                                                                       '0x8000 '
                                                                                                                                                       '- '
                                                                                                                                                       '0xFFFF',
                                                                                                                                        'name': 'LS_0X2100_0X7FFF_US_0X8000_0XFFFF',
                                                                                                                                        'value': 0x4},
                                                                                                                                       {'description': 'LS '
                                                                                                                                                       '= '
                                                                                                                                                       '0x2100 '
                                                                                                                                                       '- '
                                                                                                                                                       '0x9FFF, '
                                                                                                                                                       'US '
                                                                                                                                                       '= '
                                                                                                                                                       '0xA000 '
                                                                                                                                                       '- '
                                                                                                                                                       '0xFFFF',
                                                                                                                                        'name': 'LS_0X2100_0X9FFF_US_0XA000_0XFFFF',
                                                                                                                                        'value': 0x5},
                                                                                                                                       {'description': 'LS '
                                                                                                                                                       '= '
                                                                                                                                                       '0x2100 '
                                                                                                                                                       '- '
                                                                                                                                                       '0xBFFF, '
                                                                                                                                                       'US '
                                                                                                                                                       '= '
                                                                                                                                                       '0xC000 '
                                                                                                                                                       '- '
                                                                                                                                                       '0xFFFF',
                                                                                                                                        'name': 'LS_0X2100_0XBFFF_US_0XC000_0XFFFF',
                                                                                                                                        'value': 0x6},
                                                                                                                                       {'description': 'LS '
                                                                                                                                                       '= '
                                                                                                                                                       '0x2100 '
                                                                                                                                                       '- '
                                                                                                                                                       '0xDFFF, '
                                                                                                                                                       'US '
                                                                                                                                                       '= '
                                                                                                                                                       '0xE000 '
                                                                                                                                                       '- '
                                                                                                                                                       '0xFFFF',
                                                                                                                                        'name': 'LS_0X2100_0XDFFF_US_0XE000_0XFFFF',
                                                                                                                                        'value': 0x7}]},
                                                                                              'name': 'SRL',
                                                                                              'writeConstraint': {'useEnumeratedValues': 0x1}},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[7:7]',
                                                                                              'description': 'External '
                                                                                                             'SRAM '
                                                                                                             'Enable',
                                                                                              'name': 'SRE'}]},
                                                                        'name': 'XMCRA',
                                                                        'size': 0x8},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x37,
                                                                        'description': 'External '
                                                                                       'Memory '
                                                                                       'Control '
                                                                                       'Register '
                                                                                       'B',
                                                                        'fields': {'field': [{'access': 'read-write',
                                                                                              'bitRange': '[2:0]',
                                                                                              'description': 'External '
                                                                                                             'Memory '
                                                                                                             'High '
                                                                                                             'Mask',
                                                                                              'enumeratedValues': {'enumeratedValue': [{'description': 'None',
                                                                                                                                        'name': 'NONE',
                                                                                                                                        'value': 0x0},
                                                                                                                                       {'description': 'Px7',
                                                                                                                                        'name': 'PX7',
                                                                                                                                        'value': 0x1},
                                                                                                                                       {'description': 'Px7-Px6',
                                                                                                                                        'name': 'PX7_PX6',
                                                                                                                                        'value': 0x2},
                                                                                                                                       {'description': 'Px7-Px5',
                                                                                                                                        'name': 'PX7_PX5',
                                                                                                                                        'value': 0x3},
                                                                                                                                       {'description': 'Px7-Px4',
                                                                                                                                        'name': 'PX7_PX4',
                                                                                                                                        'value': 0x4},
                                                                                                                                       {'description': 'Px7-Px3',
                                                                                                                                        'name': 'PX7_PX3',
                                                                                                                                        'value': 0x5},
                                                                                                                                       {'description': 'Px7-Px2',
                                                                                                                                        'name': 'PX7_PX2',
                                                                                                                                        'value': 0x6},
                                                                                                                                       {'description': 'Full '
                                                                                                                                                       'Port '
                                                                                                                                                       'X',
                                                                                                                                        'name': 'FULL_PORT_X',
                                                                                                                                        'value': 0x7}]},
                                                                                              'name': 'XMM',
                                                                                              'writeConstraint': {'useEnumeratedValues': 0x1}},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[7:7]',
                                                                                              'description': 'External '
                                                                                                             'Memory '
                                                                                                             'Bus '
                                                                                                             'Keeper '
                                                                                                             'Enable',
                                                                                              'name': 'XMBK'}]},
                                                                        'name': 'XMCRB',
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
                                                                                       'Register '
                                                                                       'Low '
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
                                                              'size': 0x4,
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
                                                                                       'Register '
                                                                                       'A',
                                                                        'fields': {'field': [{'access': 'read-write',
                                                                                              'bitRange': '[1:0]',
                                                                                              'description': 'External '
                                                                                                             'Interrupt '
                                                                                                             'Sense '
                                                                                                             'Control '
                                                                                                             'Bit',
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
                                                                                                             'Bit',
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
                                                                                                             'Bit',
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
                                                                                                             'Bit',
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
                                                                        'addressOffset': 0x2F,
                                                                        'description': 'External '
                                                                                       'Interrupt '
                                                                                       'Control '
                                                                                       'Register '
                                                                                       'B',
                                                                        'fields': {'field': [{'access': 'read-write',
                                                                                              'bitRange': '[1:0]',
                                                                                              'description': 'External '
                                                                                                             'Interrupt '
                                                                                                             '7-4 '
                                                                                                             'Sense '
                                                                                                             'Control '
                                                                                                             'Bit',
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
                                                                                              'name': 'ISC4',
                                                                                              'writeConstraint': {'useEnumeratedValues': 0x1}},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[3:2]',
                                                                                              'description': 'External '
                                                                                                             'Interrupt '
                                                                                                             '7-4 '
                                                                                                             'Sense '
                                                                                                             'Control '
                                                                                                             'Bit',
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
                                                                                              'name': 'ISC5',
                                                                                              'writeConstraint': {'useEnumeratedValues': 0x1}},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[5:4]',
                                                                                              'description': 'External '
                                                                                                             'Interrupt '
                                                                                                             '7-4 '
                                                                                                             'Sense '
                                                                                                             'Control '
                                                                                                             'Bit',
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
                                                                                              'name': 'ISC6',
                                                                                              'writeConstraint': {'useEnumeratedValues': 0x1}},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[7:6]',
                                                                                              'description': 'External '
                                                                                                             'Interrupt '
                                                                                                             '7-4 '
                                                                                                             'Sense '
                                                                                                             'Control '
                                                                                                             'Bit',
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
                                                                                              'name': 'ISC7',
                                                                                              'writeConstraint': {'useEnumeratedValues': 0x1}}]},
                                                                        'name': 'EICRB',
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
                                                                                              'bitRange': '[7:0]',
                                                                                              'description': 'External '
                                                                                                             'Interrupt '
                                                                                                             'Flags',
                                                                                              'name': 'INTF',
                                                                                              'writeConstraint': {'range': {'maximum': 0xFF,
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
                                                                                              'bitRange': '[7:0]',
                                                                                              'description': 'External '
                                                                                                             'Interrupt '
                                                                                                             'Request '
                                                                                                             '7 '
                                                                                                             'Enable',
                                                                                              'name': 'INT',
                                                                                              'writeConstraint': {'range': {'maximum': 0xFF,
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
                                                                                              'bitRange': '[0:0]',
                                                                                              'description': 'Pin '
                                                                                                             'Change '
                                                                                                             'Interrupt '
                                                                                                             'Enable '
                                                                                                             '0',
                                                                                              'name': 'PCIE0'}]},
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
                                                                                              'bitRange': '[0:0]',
                                                                                              'description': 'Pin '
                                                                                                             'Change '
                                                                                                             'Interrupt '
                                                                                                             'Flag '
                                                                                                             '0',
                                                                                              'name': 'PCIF0'}]},
                                                                        'name': 'PCIFR',
                                                                        'size': 0x8},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x30,
                                                                        'description': 'Pin '
                                                                                       'Change '
                                                                                       'Mask '
                                                                                       'Register '
                                                                                       '0',
                                                                        'name': 'PCMSK0',
                                                                        'size': 0x8,
                                                                        'writeConstraint': {'range': {'maximum': 0xFF,
                                                                                                      'minimum': 0x0}}}]}},
                                           {'addressBlock': [{'offset': 0x0,
                                                              'size': 0x1,
                                                              'usage': 'registers'},
                                                             {'offset': 0x3,
                                                              'size': 0x2,
                                                              'usage': 'registers'}],
                                            'baseAddress': 0x800051,
                                            'description': 'JTAG Interface',
                                            'name': 'JTAG',
                                            'registers': {'register': [{'access': 'read-write',
                                                                        'addressOffset': 0x4,
                                                                        'description': 'MCU '
                                                                                       'Control '
                                                                                       'Register',
                                                                        'fields': {'field': [{'access': 'read-write',
                                                                                              'bitRange': '[7:7]',
                                                                                              'description': 'JTAG '
                                                                                                             'Interface '
                                                                                                             'Disable',
                                                                                              'name': 'JTD'}]},
                                                                        'name': 'MCUCR',
                                                                        'size': 0x8},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x3,
                                                                        'description': 'MCU '
                                                                                       'Status '
                                                                                       'Register '
                                                                                       '(read-only '
                                                                                       'for '
                                                                                       'debugger)',
                                                                        'fields': {'field': [{'access': 'read-write',
                                                                                              'bitRange': '[4:4]',
                                                                                              'description': 'JTAG '
                                                                                                             'Reset '
                                                                                                             'Flag',
                                                                                              'name': 'JTRF'}]},
                                                                        'name': 'MCUSR',
                                                                        'size': 0x8},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x0,
                                                                        'description': 'On-Chip '
                                                                                       'Debug '
                                                                                       'Related '
                                                                                       'Register '
                                                                                       'in '
                                                                                       'I/O '
                                                                                       'Memory '
                                                                                       '(write-only '
                                                                                       'for '
                                                                                       'debugger)',
                                                                        'name': 'OCDR',
                                                                        'size': 0x8,
                                                                        'writeConstraint': {'range': {'maximum': 0xFF,
                                                                                                      'minimum': 0x0}}}]}},
                                           {'addressBlock': [{'offset': 0x0,
                                                              'size': 0x1,
                                                              'usage': 'registers'}],
                                            'baseAddress': 0x800049,
                                            'description': 'Phase Locked Loop',
                                            'name': 'PLL',
                                            'registers': {'register': [{'access': 'read-write',
                                                                        'addressOffset': 0x0,
                                                                        'description': 'PLL '
                                                                                       'Status '
                                                                                       'and '
                                                                                       'Control '
                                                                                       'register',
                                                                        'fields': {'field': [{'access': 'read-write',
                                                                                              'bitRange': '[0:0]',
                                                                                              'description': 'PLL '
                                                                                                             'Lock '
                                                                                                             'Status '
                                                                                                             'Bit',
                                                                                              'name': 'PLOCK'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[1:1]',
                                                                                              'description': 'PLL '
                                                                                                             'Enable '
                                                                                                             'Bit',
                                                                                              'name': 'PLLE'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[4:2]',
                                                                                              'description': 'PLL '
                                                                                                             'prescaler '
                                                                                                             'Bits',
                                                                                              'enumeratedValues': {'enumeratedValue': [{'description': 'Clock/4',
                                                                                                                                        'name': 'CLOCK_4',
                                                                                                                                        'value': 0x3},
                                                                                                                                       {'description': 'Clock/8',
                                                                                                                                        'name': 'CLOCK_8',
                                                                                                                                        'value': 0x5}]},
                                                                                              'name': 'PLLP',
                                                                                              'writeConstraint': {'useEnumeratedValues': 0x1}}]},
                                                                        'name': 'PLLCSR',
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
                                                              'size': 0x3,
                                                              'usage': 'registers'}],
                                            'baseAddress': 0x800026,
                                            'description': 'I/O Port',
                                            'name': 'PORTC',
                                            'registers': {'register': [{'access': 'read-write',
                                                                        'addressOffset': 0x1,
                                                                        'description': 'Port '
                                                                                       'C '
                                                                                       'Data '
                                                                                       'Direction '
                                                                                       'Register',
                                                                        'name': 'DDRC',
                                                                        'size': 0x8,
                                                                        'writeConstraint': {'range': {'maximum': 0xFF,
                                                                                                      'minimum': 0x0}}},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x0,
                                                                        'description': 'Port '
                                                                                       'C '
                                                                                       'Input '
                                                                                       'Pins '
                                                                                       '(read-only '
                                                                                       'for '
                                                                                       'debugger)',
                                                                        'name': 'PINC',
                                                                        'size': 0x8,
                                                                        'writeConstraint': {'range': {'maximum': 0xFF,
                                                                                                      'minimum': 0x0}}},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x2,
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
                                                                        'description': 'Port '
                                                                                       'D '
                                                                                       'Data '
                                                                                       'Direction '
                                                                                       'Register',
                                                                        'name': 'DDRD',
                                                                        'size': 0x8,
                                                                        'writeConstraint': {'range': {'maximum': 0xFF,
                                                                                                      'minimum': 0x0}}},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x0,
                                                                        'description': 'Port '
                                                                                       'D '
                                                                                       'Input '
                                                                                       'Pins '
                                                                                       '(read-only '
                                                                                       'for '
                                                                                       'debugger)',
                                                                        'name': 'PIND',
                                                                        'size': 0x8,
                                                                        'writeConstraint': {'range': {'maximum': 0xFF,
                                                                                                      'minimum': 0x0}}},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x2,
                                                                        'description': 'Port '
                                                                                       'D '
                                                                                       'Data '
                                                                                       'Register',
                                                                        'name': 'PORTD',
                                                                        'size': 0x8,
                                                                        'writeConstraint': {'range': {'maximum': 0xFF,
                                                                                                      'minimum': 0x0}}}]}},
                                           {'addressBlock': [{'offset': 0x0,
                                                              'size': 0x3,
                                                              'usage': 'registers'}],
                                            'baseAddress': 0x80002C,
                                            'description': 'I/O Port',
                                            'name': 'PORTE',
                                            'registers': {'register': [{'access': 'read-write',
                                                                        'addressOffset': 0x1,
                                                                        'description': 'Data '
                                                                                       'Direction '
                                                                                       'Register, '
                                                                                       'Port '
                                                                                       'E',
                                                                        'name': 'DDRE',
                                                                        'size': 0x8,
                                                                        'writeConstraint': {'range': {'maximum': 0xFF,
                                                                                                      'minimum': 0x0}}},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x0,
                                                                        'description': 'Input '
                                                                                       'Pins, '
                                                                                       'Port '
                                                                                       'E '
                                                                                       '(read-only '
                                                                                       'for '
                                                                                       'debugger)',
                                                                        'name': 'PINE',
                                                                        'size': 0x8,
                                                                        'writeConstraint': {'range': {'maximum': 0xFF,
                                                                                                      'minimum': 0x0}}},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x2,
                                                                        'description': 'Data '
                                                                                       'Register, '
                                                                                       'Port '
                                                                                       'E',
                                                                        'name': 'PORTE',
                                                                        'size': 0x8,
                                                                        'writeConstraint': {'range': {'maximum': 0xFF,
                                                                                                      'minimum': 0x0}}}]}},
                                           {'addressBlock': [{'offset': 0x0,
                                                              'size': 0x3,
                                                              'usage': 'registers'}],
                                            'baseAddress': 0x80002F,
                                            'description': 'I/O Port',
                                            'name': 'PORTF',
                                            'registers': {'register': [{'access': 'read-write',
                                                                        'addressOffset': 0x1,
                                                                        'description': 'Data '
                                                                                       'Direction '
                                                                                       'Register, '
                                                                                       'Port '
                                                                                       'F',
                                                                        'name': 'DDRF',
                                                                        'size': 0x8,
                                                                        'writeConstraint': {'range': {'maximum': 0xFF,
                                                                                                      'minimum': 0x0}}},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x0,
                                                                        'description': 'Input '
                                                                                       'Pins, '
                                                                                       'Port '
                                                                                       'F '
                                                                                       '(read-only '
                                                                                       'for '
                                                                                       'debugger)',
                                                                        'name': 'PINF',
                                                                        'size': 0x8,
                                                                        'writeConstraint': {'range': {'maximum': 0xFF,
                                                                                                      'minimum': 0x0}}},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x2,
                                                                        'description': 'Data '
                                                                                       'Register, '
                                                                                       'Port '
                                                                                       'F',
                                                                        'name': 'PORTF',
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
                                                              'size': 0x6,
                                                              'usage': 'registers'},
                                                             {'offset': 0x39,
                                                              'size': 0x1,
                                                              'usage': 'registers'}],
                                            'baseAddress': 0x800035,
                                            'description': 'Timer/Counter, '
                                                           '8-bit',
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
                                                                                                             'Reset '
                                                                                                             'Timer/Counter1 '
                                                                                                             'and '
                                                                                                             'Timer/Counter0',
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
                                                                        'addressOffset': 0x12,
                                                                        'description': 'Timer/Counter0 '
                                                                                       'Output '
                                                                                       'Compare '
                                                                                       'Register',
                                                                        'name': 'OCR0A',
                                                                        'size': 0x8,
                                                                        'writeConstraint': {'range': {'maximum': 0xFF,
                                                                                                      'minimum': 0x0}}},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x13,
                                                                        'description': 'Timer/Counter0 '
                                                                                       'Output '
                                                                                       'Compare '
                                                                                       'Register',
                                                                        'name': 'OCR0B',
                                                                        'size': 0x8,
                                                                        'writeConstraint': {'range': {'maximum': 0xFF,
                                                                                                      'minimum': 0x0}}},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0xF,
                                                                        'description': 'Timer/Counter  '
                                                                                       'Control '
                                                                                       'Register '
                                                                                       'A',
                                                                        'fields': {'field': [{'access': 'read-write',
                                                                                              'bitRange': '[1:0]',
                                                                                              'description': 'Waveform '
                                                                                                             'Generation '
                                                                                                             'Mode',
                                                                                              'name': 'WGM0',
                                                                                              'writeConstraint': {'range': {'maximum': 0x3,
                                                                                                                            'minimum': 0x0}}},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[5:4]',
                                                                                              'description': 'Compare '
                                                                                                             'Output '
                                                                                                             'Mode, '
                                                                                                             'Fast '
                                                                                                             'PWm',
                                                                                              'name': 'COM0B',
                                                                                              'writeConstraint': {'range': {'maximum': 0x3,
                                                                                                                            'minimum': 0x0}}},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[7:6]',
                                                                                              'description': 'Compare '
                                                                                                             'Output '
                                                                                                             'Mode, '
                                                                                                             'Phase '
                                                                                                             'Correct '
                                                                                                             'PWM '
                                                                                                             'Mode',
                                                                                              'name': 'COM0A',
                                                                                              'writeConstraint': {'range': {'maximum': 0x3,
                                                                                                                            'minimum': 0x0}}}]},
                                                                        'name': 'TCCR0A',
                                                                        'size': 0x8},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x10,
                                                                        'description': 'Timer/Counter '
                                                                                       'Control '
                                                                                       'Register '
                                                                                       'B',
                                                                        'fields': {'field': [{'access': 'read-write',
                                                                                              'bitRange': '[2:0]',
                                                                                              'description': 'Clock '
                                                                                                             'Select',
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
                                                                                              'description': 'Force '
                                                                                                             'Output '
                                                                                                             'Compare '
                                                                                                             'B',
                                                                                              'name': 'FOC0B'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[7:7]',
                                                                                              'description': 'Force '
                                                                                                             'Output '
                                                                                                             'Compare '
                                                                                                             'A',
                                                                                              'name': 'FOC0A'}]},
                                                                        'name': 'TCCR0B',
                                                                        'size': 0x8},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x11,
                                                                        'description': 'Timer/Counter0',
                                                                        'name': 'TCNT0',
                                                                        'size': 0x8,
                                                                        'writeConstraint': {'range': {'maximum': 0xFF,
                                                                                                      'minimum': 0x0}}},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x0,
                                                                        'description': 'Timer/Counter0 '
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
                                                                                                             '0A',
                                                                                              'name': 'OCF0A'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[2:2]',
                                                                                              'description': 'Timer/Counter0 '
                                                                                                             'Output '
                                                                                                             'Compare '
                                                                                                             'Flag '
                                                                                                             '0B',
                                                                                              'name': 'OCF0B'}]},
                                                                        'name': 'TIFR0',
                                                                        'size': 0x8},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x39,
                                                                        'description': 'Timer/Counter0 '
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
                                                                                                             'Match '
                                                                                                             'A '
                                                                                                             'Interrupt '
                                                                                                             'Enable',
                                                                                              'name': 'OCIE0A'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[2:2]',
                                                                                              'description': 'Timer/Counter0 '
                                                                                                             'Output '
                                                                                                             'Compare '
                                                                                                             'Match '
                                                                                                             'B '
                                                                                                             'Interrupt '
                                                                                                             'Enable',
                                                                                              'name': 'OCIE0B'}]},
                                                                        'name': 'TIMSK0',
                                                                        'size': 0x8}]}},
                                           {'addressBlock': [{'offset': 0x0,
                                                              'size': 0x1,
                                                              'usage': 'registers'},
                                                             {'offset': 0x39,
                                                              'size': 0x1,
                                                              'usage': 'registers'},
                                                             {'offset': 0x4A,
                                                              'size': 0x3,
                                                              'usage': 'registers'},
                                                             {'offset': 0x4E,
                                                              'size': 0xA,
                                                              'usage': 'registers'}],
                                            'baseAddress': 0x800036,
                                            'description': 'Timer/Counter, '
                                                           '16-bit',
                                            'name': 'TC1',
                                            'registers': {'register': [{'access': 'read-write',
                                                                        'addressOffset': 0x50,
                                                                        'description': 'Timer/Counter1 '
                                                                                       'Input '
                                                                                       'Capture '
                                                                                       'Register  '
                                                                                       'Bytes',
                                                                        'name': 'ICR1',
                                                                        'size': 0x10,
                                                                        'writeConstraint': {'range': {'maximum': 0xFFFF,
                                                                                                      'minimum': 0x0}}},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x52,
                                                                        'description': 'Timer/Counter1 '
                                                                                       'Output '
                                                                                       'Compare '
                                                                                       'Register '
                                                                                       'A  '
                                                                                       'Bytes',
                                                                        'name': 'OCR1A',
                                                                        'size': 0x10,
                                                                        'writeConstraint': {'range': {'maximum': 0xFFFF,
                                                                                                      'minimum': 0x0}}},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x54,
                                                                        'description': 'Timer/Counter1 '
                                                                                       'Output '
                                                                                       'Compare '
                                                                                       'Register '
                                                                                       'B  '
                                                                                       'Bytes',
                                                                        'name': 'OCR1B',
                                                                        'size': 0x10,
                                                                        'writeConstraint': {'range': {'maximum': 0xFFFF,
                                                                                                      'minimum': 0x0}}},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x56,
                                                                        'description': 'Timer/Counter1 '
                                                                                       'Output '
                                                                                       'Compare '
                                                                                       'Register '
                                                                                       'C  '
                                                                                       'Bytes',
                                                                        'name': 'OCR1C',
                                                                        'size': 0x10,
                                                                        'writeConstraint': {'range': {'maximum': 0xFFFF,
                                                                                                      'minimum': 0x0}}},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x4A,
                                                                        'description': 'Timer/Counter1 '
                                                                                       'Control '
                                                                                       'Register '
                                                                                       'A',
                                                                        'fields': {'field': [{'access': 'read-write',
                                                                                              'bitRange': '[1:0]',
                                                                                              'description': 'Waveform '
                                                                                                             'Generation '
                                                                                                             'Mode',
                                                                                              'name': 'WGM1',
                                                                                              'writeConstraint': {'range': {'maximum': 0x3,
                                                                                                                            'minimum': 0x0}}},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[3:2]',
                                                                                              'description': 'Compare '
                                                                                                             'Output '
                                                                                                             'Mode '
                                                                                                             '1C, '
                                                                                                             'bits',
                                                                                              'name': 'COM1C',
                                                                                              'writeConstraint': {'range': {'maximum': 0x3,
                                                                                                                            'minimum': 0x0}}},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[5:4]',
                                                                                              'description': 'Compare '
                                                                                                             'Output '
                                                                                                             'Mode '
                                                                                                             '1B, '
                                                                                                             'bits',
                                                                                              'name': 'COM1B',
                                                                                              'writeConstraint': {'range': {'maximum': 0x3,
                                                                                                                            'minimum': 0x0}}},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[7:6]',
                                                                                              'description': 'Compare '
                                                                                                             'Output '
                                                                                                             'Mode '
                                                                                                             '1A, '
                                                                                                             'bits',
                                                                                              'name': 'COM1A',
                                                                                              'writeConstraint': {'range': {'maximum': 0x3,
                                                                                                                            'minimum': 0x0}}}]},
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
                                                                                              'description': 'Prescaler '
                                                                                                             'source '
                                                                                                             'of '
                                                                                                             'Timer/Counter '
                                                                                                             '1',
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
                                                                                              'name': 'CS1',
                                                                                              'writeConstraint': {'useEnumeratedValues': 0x1}},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[4:3]',
                                                                                              'description': 'Waveform '
                                                                                                             'Generation '
                                                                                                             'Mode',
                                                                                              'name': 'WGM1',
                                                                                              'writeConstraint': {'range': {'maximum': 0x3,
                                                                                                                            'minimum': 0x0}}},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[6:6]',
                                                                                              'description': 'Input '
                                                                                                             'Capture '
                                                                                                             '1 '
                                                                                                             'Edge '
                                                                                                             'Select',
                                                                                              'name': 'ICES1'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[7:7]',
                                                                                              'description': 'Input '
                                                                                                             'Capture '
                                                                                                             '1 '
                                                                                                             'Noise '
                                                                                                             'Canceler',
                                                                                              'name': 'ICNC1'}]},
                                                                        'name': 'TCCR1B',
                                                                        'size': 0x8},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x4C,
                                                                        'description': 'Timer/Counter '
                                                                                       '1 '
                                                                                       'Control '
                                                                                       'Register '
                                                                                       'C',
                                                                        'fields': {'field': [{'access': 'read-write',
                                                                                              'bitRange': '[5:5]',
                                                                                              'description': 'Force '
                                                                                                             'Output '
                                                                                                             'Compare '
                                                                                                             '1C',
                                                                                              'name': 'FOC1C'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[6:6]',
                                                                                              'description': 'Force '
                                                                                                             'Output '
                                                                                                             'Compare '
                                                                                                             '1B',
                                                                                              'name': 'FOC1B'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[7:7]',
                                                                                              'description': 'Force '
                                                                                                             'Output '
                                                                                                             'Compare '
                                                                                                             '1A',
                                                                                              'name': 'FOC1A'}]},
                                                                        'name': 'TCCR1C',
                                                                        'size': 0x8},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x4E,
                                                                        'description': 'Timer/Counter1  '
                                                                                       'Bytes',
                                                                        'name': 'TCNT1',
                                                                        'size': 0x10,
                                                                        'writeConstraint': {'range': {'maximum': 0xFFFF,
                                                                                                      'minimum': 0x0}}},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x0,
                                                                        'description': 'Timer/Counter1 '
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
                                                                                              'description': 'Output '
                                                                                                             'Compare '
                                                                                                             'Flag '
                                                                                                             '1A',
                                                                                              'name': 'OCF1A'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[2:2]',
                                                                                              'description': 'Output '
                                                                                                             'Compare '
                                                                                                             'Flag '
                                                                                                             '1B',
                                                                                              'name': 'OCF1B'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[3:3]',
                                                                                              'description': 'Output '
                                                                                                             'Compare '
                                                                                                             'Flag '
                                                                                                             '1C',
                                                                                              'name': 'OCF1C'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[5:5]',
                                                                                              'description': 'Input '
                                                                                                             'Capture '
                                                                                                             'Flag '
                                                                                                             '1',
                                                                                              'name': 'ICF1'}]},
                                                                        'name': 'TIFR1',
                                                                        'size': 0x8},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x39,
                                                                        'description': 'Timer/Counter1 '
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
                                                                                                             'Match '
                                                                                                             'Interrupt '
                                                                                                             'Enable',
                                                                                              'name': 'OCIE1A'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[2:2]',
                                                                                              'description': 'Timer/Counter1 '
                                                                                                             'Output '
                                                                                                             'Compare '
                                                                                                             'B '
                                                                                                             'Match '
                                                                                                             'Interrupt '
                                                                                                             'Enable',
                                                                                              'name': 'OCIE1B'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[3:3]',
                                                                                              'description': 'Timer/Counter1 '
                                                                                                             'Output '
                                                                                                             'Compare '
                                                                                                             'C '
                                                                                                             'Match '
                                                                                                             'Interrupt '
                                                                                                             'Enable',
                                                                                              'name': 'OCIE1C'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[5:5]',
                                                                                              'description': 'Timer/Counter1 '
                                                                                                             'Input '
                                                                                                             'Capture '
                                                                                                             'Interrupt '
                                                                                                             'Enable',
                                                                                              'name': 'ICIE1'}]},
                                                                        'name': 'TIMSK1',
                                                                        'size': 0x8}]}},
                                           {'addressBlock': [{'offset': 0x0,
                                                              'size': 0x1,
                                                              'usage': 'registers'},
                                                             {'offset': 0xC,
                                                              'size': 0x1,
                                                              'usage': 'registers'},
                                                             {'offset': 0x39,
                                                              'size': 0x1,
                                                              'usage': 'registers'},
                                                             {'offset': 0x79,
                                                              'size': 0x5,
                                                              'usage': 'registers'},
                                                             {'offset': 0x7F,
                                                              'size': 0x1,
                                                              'usage': 'registers'}],
                                            'baseAddress': 0x800037,
                                            'description': 'Timer/Counter, '
                                                           '8-bit Async',
                                            'name': 'TC2',
                                            'registers': {'register': [{'access': 'read-write',
                                                                        'addressOffset': 0x7F,
                                                                        'description': 'Asynchronous '
                                                                                       'Status '
                                                                                       'Register',
                                                                        'fields': {'field': [{'access': 'read-write',
                                                                                              'bitRange': '[0:0]',
                                                                                              'description': 'Timer/Counter '
                                                                                                             'Control '
                                                                                                             'Register2 '
                                                                                                             'Update '
                                                                                                             'Busy',
                                                                                              'name': 'TCR2BUB'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[1:1]',
                                                                                              'description': 'Timer/Counter '
                                                                                                             'Control '
                                                                                                             'Register2 '
                                                                                                             'Update '
                                                                                                             'Busy',
                                                                                              'name': 'TCR2AUB'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[2:2]',
                                                                                              'description': 'Output '
                                                                                                             'Compare '
                                                                                                             'Register '
                                                                                                             '2 '
                                                                                                             'Update '
                                                                                                             'Busy',
                                                                                              'name': 'OCR2BUB'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[3:3]',
                                                                                              'description': 'Output '
                                                                                                             'Compare '
                                                                                                             'Register2 '
                                                                                                             'Update '
                                                                                                             'Busy',
                                                                                              'name': 'OCR2AUB'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[4:4]',
                                                                                              'description': 'Timer/Counter2 '
                                                                                                             'Update '
                                                                                                             'Busy',
                                                                                              'name': 'TCN2UB'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[5:5]',
                                                                                              'description': 'Asynchronous '
                                                                                                             'Timer/Counter2',
                                                                                              'name': 'AS2'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[6:6]',
                                                                                              'description': 'Enable '
                                                                                                             'External '
                                                                                                             'Clock '
                                                                                                             'Input',
                                                                                              'name': 'EXCLK'}]},
                                                                        'name': 'ASSR',
                                                                        'size': 0x8},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0xC,
                                                                        'description': 'General '
                                                                                       'Timer '
                                                                                       'Counter '
                                                                                       'Control '
                                                                                       'register',
                                                                        'fields': {'field': [{'access': 'read-write',
                                                                                              'bitRange': '[1:1]',
                                                                                              'description': 'Prescaler '
                                                                                                             'Reset '
                                                                                                             'Timer/Counter2',
                                                                                              'name': 'PSRASY'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[7:7]',
                                                                                              'description': 'Timer/Counter '
                                                                                                             'Synchronization '
                                                                                                             'Mode',
                                                                                              'name': 'TSM'}]},
                                                                        'name': 'GTCCR',
                                                                        'size': 0x8},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x7C,
                                                                        'description': 'Timer/Counter2 '
                                                                                       'Output '
                                                                                       'Compare '
                                                                                       'Register '
                                                                                       'A',
                                                                        'name': 'OCR2A',
                                                                        'size': 0x8,
                                                                        'writeConstraint': {'range': {'maximum': 0xFF,
                                                                                                      'minimum': 0x0}}},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x7D,
                                                                        'description': 'Timer/Counter2 '
                                                                                       'Output '
                                                                                       'Compare '
                                                                                       'Register '
                                                                                       'B',
                                                                        'name': 'OCR2B',
                                                                        'size': 0x8,
                                                                        'writeConstraint': {'range': {'maximum': 0xFF,
                                                                                                      'minimum': 0x0}}},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x79,
                                                                        'description': 'Timer/Counter2 '
                                                                                       'Control '
                                                                                       'Register '
                                                                                       'A',
                                                                        'fields': {'field': [{'access': 'read-write',
                                                                                              'bitRange': '[1:0]',
                                                                                              'description': 'Waveform '
                                                                                                             'Generation '
                                                                                                             'Mode',
                                                                                              'name': 'WGM2',
                                                                                              'writeConstraint': {'range': {'maximum': 0x3,
                                                                                                                            'minimum': 0x0}}},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[5:4]',
                                                                                              'description': 'Compare '
                                                                                                             'Output '
                                                                                                             'Mode '
                                                                                                             'bits',
                                                                                              'name': 'COM2B',
                                                                                              'writeConstraint': {'range': {'maximum': 0x3,
                                                                                                                            'minimum': 0x0}}},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[7:6]',
                                                                                              'description': 'Compare '
                                                                                                             'Output '
                                                                                                             'Mode '
                                                                                                             'bits',
                                                                                              'name': 'COM2A',
                                                                                              'writeConstraint': {'range': {'maximum': 0x3,
                                                                                                                            'minimum': 0x0}}}]},
                                                                        'name': 'TCCR2A',
                                                                        'size': 0x8},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x7A,
                                                                        'description': 'Timer/Counter2 '
                                                                                       'Control '
                                                                                       'Register '
                                                                                       'B',
                                                                        'fields': {'field': [{'access': 'read-write',
                                                                                              'bitRange': '[2:0]',
                                                                                              'description': 'Clock '
                                                                                                             'Select '
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
                                                                                              'name': 'CS2',
                                                                                              'writeConstraint': {'useEnumeratedValues': 0x1}},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[3:3]',
                                                                                              'description': 'Waveform '
                                                                                                             'Generation '
                                                                                                             'Mode',
                                                                                              'name': 'WGM22'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[6:6]',
                                                                                              'description': 'Force '
                                                                                                             'Output '
                                                                                                             'Compare '
                                                                                                             'B',
                                                                                              'name': 'FOC2B'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[7:7]',
                                                                                              'description': 'Force '
                                                                                                             'Output '
                                                                                                             'Compare '
                                                                                                             'A',
                                                                                              'name': 'FOC2A'}]},
                                                                        'name': 'TCCR2B',
                                                                        'size': 0x8},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x7B,
                                                                        'description': 'Timer/Counter2',
                                                                        'name': 'TCNT2',
                                                                        'size': 0x8,
                                                                        'writeConstraint': {'range': {'maximum': 0xFF,
                                                                                                      'minimum': 0x0}}},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x0,
                                                                        'description': 'Timer/Counter '
                                                                                       'Interrupt '
                                                                                       'Flag '
                                                                                       'Register '
                                                                                       '(read-only '
                                                                                       'for '
                                                                                       'debugger)',
                                                                        'fields': {'field': [{'access': 'read-write',
                                                                                              'bitRange': '[0:0]',
                                                                                              'description': 'Timer/Counter2 '
                                                                                                             'Overflow '
                                                                                                             'Flag',
                                                                                              'name': 'TOV2'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[1:1]',
                                                                                              'description': 'Output '
                                                                                                             'Compare '
                                                                                                             'Flag '
                                                                                                             '2A',
                                                                                              'name': 'OCF2A'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[2:2]',
                                                                                              'description': 'Output '
                                                                                                             'Compare '
                                                                                                             'Flag '
                                                                                                             '2B',
                                                                                              'name': 'OCF2B'}]},
                                                                        'name': 'TIFR2',
                                                                        'size': 0x8},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x39,
                                                                        'description': 'Timer/Counter '
                                                                                       'Interrupt '
                                                                                       'Mask '
                                                                                       'register',
                                                                        'fields': {'field': [{'access': 'read-write',
                                                                                              'bitRange': '[0:0]',
                                                                                              'description': 'Timer/Counter2 '
                                                                                                             'Overflow '
                                                                                                             'Interrupt '
                                                                                                             'Enable',
                                                                                              'name': 'TOIE2'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[1:1]',
                                                                                              'description': 'Timer/Counter2 '
                                                                                                             'Output '
                                                                                                             'Compare '
                                                                                                             'Match '
                                                                                                             'A '
                                                                                                             'Interrupt '
                                                                                                             'Enable',
                                                                                              'name': 'OCIE2A'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[2:2]',
                                                                                              'description': 'Timer/Counter2 '
                                                                                                             'Output '
                                                                                                             'Compare '
                                                                                                             'Match '
                                                                                                             'B '
                                                                                                             'Interrupt '
                                                                                                             'Enable',
                                                                                              'name': 'OCIE2B'}]},
                                                                        'name': 'TIMSK2',
                                                                        'size': 0x8}]}},
                                           {'addressBlock': [{'offset': 0x0,
                                                              'size': 0x1,
                                                              'usage': 'registers'},
                                                             {'offset': 0x39,
                                                              'size': 0x1,
                                                              'usage': 'registers'},
                                                             {'offset': 0x58,
                                                              'size': 0x3,
                                                              'usage': 'registers'},
                                                             {'offset': 0x5C,
                                                              'size': 0xA,
                                                              'usage': 'registers'}],
                                            'baseAddress': 0x800038,
                                            'description': 'Timer/Counter, '
                                                           '16-bit',
                                            'name': 'TC3',
                                            'registers': {'register': [{'access': 'read-write',
                                                                        'addressOffset': 0x5E,
                                                                        'description': 'Timer/Counter3 '
                                                                                       'Input '
                                                                                       'Capture '
                                                                                       'Register  '
                                                                                       'Bytes',
                                                                        'name': 'ICR3',
                                                                        'size': 0x10,
                                                                        'writeConstraint': {'range': {'maximum': 0xFFFF,
                                                                                                      'minimum': 0x0}}},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x60,
                                                                        'description': 'Timer/Counter3 '
                                                                                       'Output '
                                                                                       'Compare '
                                                                                       'Register '
                                                                                       'A  '
                                                                                       'Bytes',
                                                                        'name': 'OCR3A',
                                                                        'size': 0x10,
                                                                        'writeConstraint': {'range': {'maximum': 0xFFFF,
                                                                                                      'minimum': 0x0}}},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x62,
                                                                        'description': 'Timer/Counter3 '
                                                                                       'Output '
                                                                                       'Compare '
                                                                                       'Register '
                                                                                       'B  '
                                                                                       'Bytes',
                                                                        'name': 'OCR3B',
                                                                        'size': 0x10,
                                                                        'writeConstraint': {'range': {'maximum': 0xFFFF,
                                                                                                      'minimum': 0x0}}},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x64,
                                                                        'description': 'Timer/Counter3 '
                                                                                       'Output '
                                                                                       'Compare '
                                                                                       'Register '
                                                                                       'B  '
                                                                                       'Bytes',
                                                                        'name': 'OCR3C',
                                                                        'size': 0x10,
                                                                        'writeConstraint': {'range': {'maximum': 0xFFFF,
                                                                                                      'minimum': 0x0}}},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x58,
                                                                        'description': 'Timer/Counter3 '
                                                                                       'Control '
                                                                                       'Register '
                                                                                       'A',
                                                                        'fields': {'field': [{'access': 'read-write',
                                                                                              'bitRange': '[1:0]',
                                                                                              'description': 'Waveform '
                                                                                                             'Generation '
                                                                                                             'Mode',
                                                                                              'name': 'WGM3',
                                                                                              'writeConstraint': {'range': {'maximum': 0x3,
                                                                                                                            'minimum': 0x0}}},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[3:2]',
                                                                                              'description': 'Compare '
                                                                                                             'Output '
                                                                                                             'Mode '
                                                                                                             '3C, '
                                                                                                             'bits',
                                                                                              'name': 'COM3C',
                                                                                              'writeConstraint': {'range': {'maximum': 0x3,
                                                                                                                            'minimum': 0x0}}},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[5:4]',
                                                                                              'description': 'Compare '
                                                                                                             'Output '
                                                                                                             'Mode '
                                                                                                             '3B, '
                                                                                                             'bits',
                                                                                              'name': 'COM3B',
                                                                                              'writeConstraint': {'range': {'maximum': 0x3,
                                                                                                                            'minimum': 0x0}}},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[7:6]',
                                                                                              'description': 'Compare '
                                                                                                             'Output '
                                                                                                             'Mode '
                                                                                                             '1A, '
                                                                                                             'bits',
                                                                                              'name': 'COM3A',
                                                                                              'writeConstraint': {'range': {'maximum': 0x3,
                                                                                                                            'minimum': 0x0}}}]},
                                                                        'name': 'TCCR3A',
                                                                        'size': 0x8},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x59,
                                                                        'description': 'Timer/Counter3 '
                                                                                       'Control '
                                                                                       'Register '
                                                                                       'B',
                                                                        'fields': {'field': [{'access': 'read-write',
                                                                                              'bitRange': '[2:0]',
                                                                                              'description': 'Prescaler '
                                                                                                             'source '
                                                                                                             'of '
                                                                                                             'Timer/Counter '
                                                                                                             '3',
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
                                                                                              'name': 'CS3',
                                                                                              'writeConstraint': {'useEnumeratedValues': 0x1}},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[4:3]',
                                                                                              'description': 'Waveform '
                                                                                                             'Generation '
                                                                                                             'Mode',
                                                                                              'name': 'WGM3',
                                                                                              'writeConstraint': {'range': {'maximum': 0x3,
                                                                                                                            'minimum': 0x0}}},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[6:6]',
                                                                                              'description': 'Input '
                                                                                                             'Capture '
                                                                                                             '3 '
                                                                                                             'Edge '
                                                                                                             'Select',
                                                                                              'name': 'ICES3'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[7:7]',
                                                                                              'description': 'Input '
                                                                                                             'Capture '
                                                                                                             '3 '
                                                                                                             'Noise '
                                                                                                             'Canceler',
                                                                                              'name': 'ICNC3'}]},
                                                                        'name': 'TCCR3B',
                                                                        'size': 0x8},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x5A,
                                                                        'description': 'Timer/Counter '
                                                                                       '3 '
                                                                                       'Control '
                                                                                       'Register '
                                                                                       'C',
                                                                        'fields': {'field': [{'access': 'read-write',
                                                                                              'bitRange': '[5:5]',
                                                                                              'description': 'Force '
                                                                                                             'Output '
                                                                                                             'Compare '
                                                                                                             '3C',
                                                                                              'name': 'FOC3C'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[6:6]',
                                                                                              'description': 'Force '
                                                                                                             'Output '
                                                                                                             'Compare '
                                                                                                             '3B',
                                                                                              'name': 'FOC3B'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[7:7]',
                                                                                              'description': 'Force '
                                                                                                             'Output '
                                                                                                             'Compare '
                                                                                                             '3A',
                                                                                              'name': 'FOC3A'}]},
                                                                        'name': 'TCCR3C',
                                                                        'size': 0x8},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x5C,
                                                                        'description': 'Timer/Counter3  '
                                                                                       'Bytes',
                                                                        'name': 'TCNT3',
                                                                        'size': 0x10,
                                                                        'writeConstraint': {'range': {'maximum': 0xFFFF,
                                                                                                      'minimum': 0x0}}},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x0,
                                                                        'description': 'Timer/Counter3 '
                                                                                       'Interrupt '
                                                                                       'Flag '
                                                                                       'register '
                                                                                       '(read-only '
                                                                                       'for '
                                                                                       'debugger)',
                                                                        'fields': {'field': [{'access': 'read-write',
                                                                                              'bitRange': '[0:0]',
                                                                                              'description': 'Timer/Counter3 '
                                                                                                             'Overflow '
                                                                                                             'Flag',
                                                                                              'name': 'TOV3'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[1:1]',
                                                                                              'description': 'Output '
                                                                                                             'Compare '
                                                                                                             'Flag '
                                                                                                             '3A',
                                                                                              'name': 'OCF3A'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[2:2]',
                                                                                              'description': 'Output '
                                                                                                             'Compare '
                                                                                                             'Flag '
                                                                                                             '3B',
                                                                                              'name': 'OCF3B'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[3:3]',
                                                                                              'description': 'Output '
                                                                                                             'Compare '
                                                                                                             'Flag '
                                                                                                             '3C',
                                                                                              'name': 'OCF3C'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[5:5]',
                                                                                              'description': 'Input '
                                                                                                             'Capture '
                                                                                                             'Flag '
                                                                                                             '3',
                                                                                              'name': 'ICF3'}]},
                                                                        'name': 'TIFR3',
                                                                        'size': 0x8},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x39,
                                                                        'description': 'Timer/Counter3 '
                                                                                       'Interrupt '
                                                                                       'Mask '
                                                                                       'Register',
                                                                        'fields': {'field': [{'access': 'read-write',
                                                                                              'bitRange': '[0:0]',
                                                                                              'description': 'Timer/Counter3 '
                                                                                                             'Overflow '
                                                                                                             'Interrupt '
                                                                                                             'Enable',
                                                                                              'name': 'TOIE3'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[1:1]',
                                                                                              'description': 'Timer/Counter3 '
                                                                                                             'Output '
                                                                                                             'Compare '
                                                                                                             'A '
                                                                                                             'Match '
                                                                                                             'Interrupt '
                                                                                                             'Enable',
                                                                                              'name': 'OCIE3A'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[2:2]',
                                                                                              'description': 'Timer/Counter3 '
                                                                                                             'Output '
                                                                                                             'Compare '
                                                                                                             'B '
                                                                                                             'Match '
                                                                                                             'Interrupt '
                                                                                                             'Enable',
                                                                                              'name': 'OCIE3B'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[3:3]',
                                                                                              'description': 'Timer/Counter3 '
                                                                                                             'Output '
                                                                                                             'Compare '
                                                                                                             'C '
                                                                                                             'Match '
                                                                                                             'Interrupt '
                                                                                                             'Enable',
                                                                                              'name': 'OCIE3C'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[5:5]',
                                                                                              'description': 'Timer/Counter3 '
                                                                                                             'Input '
                                                                                                             'Capture '
                                                                                                             'Interrupt '
                                                                                                             'Enable',
                                                                                              'name': 'ICIE3'}]},
                                                                        'name': 'TIMSK3',
                                                                        'size': 0x8}]}},
                                           {'addressBlock': [{'offset': 0x0,
                                                              'size': 0x6,
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
                                                                                       'Register',
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
                                                              'size': 0x3,
                                                              'usage': 'registers'},
                                                             {'offset': 0x4,
                                                              'size': 0x3,
                                                              'usage': 'registers'}],
                                            'baseAddress': 0x8000C8,
                                            'description': 'USART',
                                            'name': 'USART1',
                                            'registers': {'register': [{'access': 'read-write',
                                                                        'addressOffset': 0x4,
                                                                        'description': 'USART '
                                                                                       'Baud '
                                                                                       'Rate '
                                                                                       'Register  '
                                                                                       'Bytes',
                                                                        'name': 'UBRR1',
                                                                        'size': 0x10,
                                                                        'writeConstraint': {'range': {'maximum': 0xFFFF,
                                                                                                      'minimum': 0x0}}},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x0,
                                                                        'description': 'USART '
                                                                                       'Control '
                                                                                       'and '
                                                                                       'Status '
                                                                                       'Register '
                                                                                       'A '
                                                                                       '(read-only '
                                                                                       'for '
                                                                                       'debugger)',
                                                                        'fields': {'field': [{'access': 'read-write',
                                                                                              'bitRange': '[0:0]',
                                                                                              'description': 'Multi-processor '
                                                                                                             'Communication '
                                                                                                             'Mode',
                                                                                              'name': 'MPCM1'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[1:1]',
                                                                                              'description': 'Double '
                                                                                                             'the '
                                                                                                             'USART '
                                                                                                             'transmission '
                                                                                                             'speed',
                                                                                              'name': 'U2X1'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[2:2]',
                                                                                              'description': 'Parity '
                                                                                                             'Error',
                                                                                              'name': 'UPE1'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[3:3]',
                                                                                              'description': 'Data '
                                                                                                             'overRun',
                                                                                              'name': 'DOR1'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[4:4]',
                                                                                              'description': 'Framing '
                                                                                                             'Error',
                                                                                              'name': 'FE1'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[5:5]',
                                                                                              'description': 'USART '
                                                                                                             'Data '
                                                                                                             'Register '
                                                                                                             'Empty',
                                                                                              'name': 'UDRE1'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[6:6]',
                                                                                              'description': 'USART '
                                                                                                             'Transmit '
                                                                                                             'Complete',
                                                                                              'name': 'TXC1'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[7:7]',
                                                                                              'description': 'USART '
                                                                                                             'Receive '
                                                                                                             'Complete',
                                                                                              'name': 'RXC1'}]},
                                                                        'name': 'UCSR1A',
                                                                        'size': 0x8},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x1,
                                                                        'description': 'USART '
                                                                                       'Control '
                                                                                       'and '
                                                                                       'Status '
                                                                                       'Register '
                                                                                       'B',
                                                                        'fields': {'field': [{'access': 'read-write',
                                                                                              'bitRange': '[0:0]',
                                                                                              'description': 'Transmit '
                                                                                                             'Data '
                                                                                                             'Bit '
                                                                                                             '8',
                                                                                              'name': 'TXB81'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[1:1]',
                                                                                              'description': 'Receive '
                                                                                                             'Data '
                                                                                                             'Bit '
                                                                                                             '8',
                                                                                              'name': 'RXB81'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[2:2]',
                                                                                              'description': 'Character '
                                                                                                             'Size',
                                                                                              'name': 'UCSZ12'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[3:3]',
                                                                                              'description': 'Transmitter '
                                                                                                             'Enable',
                                                                                              'name': 'TXEN1'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[4:4]',
                                                                                              'description': 'Receiver '
                                                                                                             'Enable',
                                                                                              'name': 'RXEN1'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[5:5]',
                                                                                              'description': 'USART '
                                                                                                             'Data '
                                                                                                             'register '
                                                                                                             'Empty '
                                                                                                             'Interrupt '
                                                                                                             'Enable',
                                                                                              'name': 'UDRIE1'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[6:6]',
                                                                                              'description': 'TX '
                                                                                                             'Complete '
                                                                                                             'Interrupt '
                                                                                                             'Enable',
                                                                                              'name': 'TXCIE1'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[7:7]',
                                                                                              'description': 'RX '
                                                                                                             'Complete '
                                                                                                             'Interrupt '
                                                                                                             'Enable',
                                                                                              'name': 'RXCIE1'}]},
                                                                        'name': 'UCSR1B',
                                                                        'size': 0x8},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x2,
                                                                        'description': 'USART '
                                                                                       'Control '
                                                                                       'and '
                                                                                       'Status '
                                                                                       'Register '
                                                                                       'C',
                                                                        'fields': {'field': [{'access': 'read-write',
                                                                                              'bitRange': '[0:0]',
                                                                                              'description': 'Clock '
                                                                                                             'Polarity',
                                                                                              'name': 'UCPOL1'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[2:1]',
                                                                                              'description': 'Character '
                                                                                                             'Size',
                                                                                              'name': 'UCSZ1',
                                                                                              'writeConstraint': {'range': {'maximum': 0x3,
                                                                                                                            'minimum': 0x0}}},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[3:3]',
                                                                                              'description': 'Stop '
                                                                                                             'Bit '
                                                                                                             'Select',
                                                                                              'enumeratedValues': {'enumeratedValue': [{'description': '1-bit',
                                                                                                                                        'name': '1_BIT',
                                                                                                                                        'value': 0x0},
                                                                                                                                       {'description': '2-bit',
                                                                                                                                        'name': '2_BIT',
                                                                                                                                        'value': 0x1}]},
                                                                                              'name': 'USBS1',
                                                                                              'writeConstraint': {'useEnumeratedValues': 0x1}},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[5:4]',
                                                                                              'description': 'Parity '
                                                                                                             'Mode '
                                                                                                             'Bits',
                                                                                              'enumeratedValues': {'enumeratedValue': [{'description': 'Disabled',
                                                                                                                                        'name': 'DISABLED',
                                                                                                                                        'value': 0x0},
                                                                                                                                       {'description': 'Reserved',
                                                                                                                                        'name': 'RESERVED',
                                                                                                                                        'value': 0x1},
                                                                                                                                       {'description': 'Enabled, '
                                                                                                                                                       'Even '
                                                                                                                                                       'Parity',
                                                                                                                                        'name': 'ENABLED_EVEN_PARITY',
                                                                                                                                        'value': 0x2},
                                                                                                                                       {'description': 'Enabled, '
                                                                                                                                                       'Odd '
                                                                                                                                                       'Parity',
                                                                                                                                        'name': 'ENABLED_ODD_PARITY',
                                                                                                                                        'value': 0x3}]},
                                                                                              'name': 'UPM1',
                                                                                              'writeConstraint': {'useEnumeratedValues': 0x1}},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[7:6]',
                                                                                              'description': 'USART '
                                                                                                             'Mode '
                                                                                                             'Select',
                                                                                              'enumeratedValues': {'enumeratedValue': [{'description': 'Asynchronous '
                                                                                                                                                       'USART',
                                                                                                                                        'name': 'ASYNCHRONOUS_USART',
                                                                                                                                        'value': 0x0},
                                                                                                                                       {'description': 'Synchronous '
                                                                                                                                                       'USART',
                                                                                                                                        'name': 'SYNCHRONOUS_USART',
                                                                                                                                        'value': 0x1},
                                                                                                                                       {'description': 'Master '
                                                                                                                                                       'SPI',
                                                                                                                                        'name': 'MASTER_SPI',
                                                                                                                                        'value': 0x3}]},
                                                                                              'name': 'UMSEL1',
                                                                                              'writeConstraint': {'useEnumeratedValues': 0x1}}]},
                                                                        'name': 'UCSR1C',
                                                                        'size': 0x8},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x6,
                                                                        'description': 'USART '
                                                                                       'I/O '
                                                                                       'Data '
                                                                                       'Register '
                                                                                       '(write-only '
                                                                                       'for '
                                                                                       'debugger)',
                                                                        'name': 'UDR1',
                                                                        'size': 0x8,
                                                                        'writeConstraint': {'range': {'maximum': 0xFF,
                                                                                                      'minimum': 0x0}}}]}},
                                           {'addressBlock': [{'offset': 0x0,
                                                              'size': 0x7,
                                                              'usage': 'registers'},
                                                             {'offset': 0x8,
                                                              'size': 0xD,
                                                              'usage': 'registers'}],
                                            'baseAddress': 0x8000E0,
                                            'description': 'USB Device '
                                                           'Registers',
                                            'name': 'USB_DEVICE',
                                            'registers': {'register': [{'access': 'read-write',
                                                                        'addressOffset': 0x3,
                                                                        'description': 'No '
                                                                                       'Description.',
                                                                        'fields': {'field': [{'access': 'read-write',
                                                                                              'bitRange': '[6:0]',
                                                                                              'description': 'No '
                                                                                                             'Description.',
                                                                                              'name': 'UADD',
                                                                                              'writeConstraint': {'range': {'maximum': 0x7F,
                                                                                                                            'minimum': 0x0}}},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[7:7]',
                                                                                              'description': 'No '
                                                                                                             'Description.',
                                                                                              'name': 'ADDEN'}]},
                                                                        'name': 'UDADDR',
                                                                        'size': 0x8},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x0,
                                                                        'description': 'No '
                                                                                       'Description.',
                                                                        'fields': {'field': [{'access': 'read-write',
                                                                                              'bitRange': '[0:0]',
                                                                                              'description': 'No '
                                                                                                             'Description.',
                                                                                              'name': 'DETACH'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[1:1]',
                                                                                              'description': 'No '
                                                                                                             'Description.',
                                                                                              'name': 'RMWKUP'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[2:2]',
                                                                                              'description': 'No '
                                                                                                             'Description.',
                                                                                              'name': 'LSM'}]},
                                                                        'name': 'UDCON',
                                                                        'size': 0x8},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x4,
                                                                        'description': 'No '
                                                                                       'Description.',
                                                                        'name': 'UDFNUM',
                                                                        'size': 0x10,
                                                                        'writeConstraint': {'range': {'maximum': 0xFFFF,
                                                                                                      'minimum': 0x0}}},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x2,
                                                                        'description': 'No '
                                                                                       'Description.',
                                                                        'fields': {'field': [{'access': 'read-write',
                                                                                              'bitRange': '[0:0]',
                                                                                              'description': 'No '
                                                                                                             'Description.',
                                                                                              'name': 'SUSPE'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[2:2]',
                                                                                              'description': 'No '
                                                                                                             'Description.',
                                                                                              'name': 'SOFE'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[3:3]',
                                                                                              'description': 'No '
                                                                                                             'Description.',
                                                                                              'name': 'EORSTE'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[4:4]',
                                                                                              'description': 'No '
                                                                                                             'Description.',
                                                                                              'name': 'WAKEUPE'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[5:5]',
                                                                                              'description': 'No '
                                                                                                             'Description.',
                                                                                              'name': 'EORSME'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[6:6]',
                                                                                              'description': 'No '
                                                                                                             'Description.',
                                                                                              'name': 'UPRSME'}]},
                                                                        'name': 'UDIEN',
                                                                        'size': 0x8},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x1,
                                                                        'description': 'No '
                                                                                       'Description.',
                                                                        'fields': {'field': [{'access': 'read-write',
                                                                                              'bitRange': '[0:0]',
                                                                                              'description': 'No '
                                                                                                             'Description.',
                                                                                              'name': 'SUSPI'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[2:2]',
                                                                                              'description': 'No '
                                                                                                             'Description.',
                                                                                              'name': 'SOFI'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[3:3]',
                                                                                              'description': 'No '
                                                                                                             'Description.',
                                                                                              'name': 'EORSTI'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[4:4]',
                                                                                              'description': 'No '
                                                                                                             'Description.',
                                                                                              'name': 'WAKEUPI'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[5:5]',
                                                                                              'description': 'No '
                                                                                                             'Description.',
                                                                                              'name': 'EORSMI'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[6:6]',
                                                                                              'description': 'No '
                                                                                                             'Description.',
                                                                                              'name': 'UPRSMI'}]},
                                                                        'name': 'UDINT',
                                                                        'size': 0x8},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x6,
                                                                        'description': 'No '
                                                                                       'Description.',
                                                                        'fields': {'field': [{'access': 'read-write',
                                                                                              'bitRange': '[4:4]',
                                                                                              'description': 'No '
                                                                                                             'Description.',
                                                                                              'name': 'FNCERR'}]},
                                                                        'name': 'UDMFN',
                                                                        'size': 0x8},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x13,
                                                                        'description': 'No '
                                                                                       'Description.',
                                                                        'name': 'UEBCHX',
                                                                        'size': 0x8,
                                                                        'writeConstraint': {'range': {'maximum': 0xFF,
                                                                                                      'minimum': 0x0}}},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x12,
                                                                        'description': 'No '
                                                                                       'Description.',
                                                                        'name': 'UEBCLX',
                                                                        'size': 0x8,
                                                                        'writeConstraint': {'range': {'maximum': 0xFF,
                                                                                                      'minimum': 0x0}}},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0xC,
                                                                        'description': 'No '
                                                                                       'Description.',
                                                                        'fields': {'field': [{'access': 'read-write',
                                                                                              'bitRange': '[0:0]',
                                                                                              'description': 'No '
                                                                                                             'Description.',
                                                                                              'name': 'EPDIR'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[7:6]',
                                                                                              'description': 'No '
                                                                                                             'Description.',
                                                                                              'name': 'EPTYPE',
                                                                                              'writeConstraint': {'range': {'maximum': 0x3,
                                                                                                                            'minimum': 0x0}}}]},
                                                                        'name': 'UECFG0X',
                                                                        'size': 0x8},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0xD,
                                                                        'description': 'No '
                                                                                       'Description.',
                                                                        'fields': {'field': [{'access': 'read-write',
                                                                                              'bitRange': '[1:1]',
                                                                                              'description': 'No '
                                                                                                             'Description.',
                                                                                              'name': 'ALLOC'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[3:2]',
                                                                                              'description': 'No '
                                                                                                             'Description.',
                                                                                              'name': 'EPBK',
                                                                                              'writeConstraint': {'range': {'maximum': 0x3,
                                                                                                                            'minimum': 0x0}}},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[6:4]',
                                                                                              'description': 'No '
                                                                                                             'Description.',
                                                                                              'name': 'EPSIZE',
                                                                                              'writeConstraint': {'range': {'maximum': 0x7,
                                                                                                                            'minimum': 0x0}}}]},
                                                                        'name': 'UECFG1X',
                                                                        'size': 0x8},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0xB,
                                                                        'description': 'No '
                                                                                       'Description.',
                                                                        'fields': {'field': [{'access': 'read-write',
                                                                                              'bitRange': '[0:0]',
                                                                                              'description': 'No '
                                                                                                             'Description.',
                                                                                              'name': 'EPEN'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[3:3]',
                                                                                              'description': 'No '
                                                                                                             'Description.',
                                                                                              'name': 'RSTDT'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[4:4]',
                                                                                              'description': 'No '
                                                                                                             'Description.',
                                                                                              'name': 'STALLRQC'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[5:5]',
                                                                                              'description': 'No '
                                                                                                             'Description.',
                                                                                              'name': 'STALLRQ'}]},
                                                                        'name': 'UECONX',
                                                                        'size': 0x8},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x11,
                                                                        'description': 'No '
                                                                                       'Description.',
                                                                        'name': 'UEDATX',
                                                                        'size': 0x8,
                                                                        'writeConstraint': {'range': {'maximum': 0xFF,
                                                                                                      'minimum': 0x0}}},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x10,
                                                                        'description': 'No '
                                                                                       'Description.',
                                                                        'fields': {'field': [{'access': 'read-write',
                                                                                              'bitRange': '[0:0]',
                                                                                              'description': 'No '
                                                                                                             'Description.',
                                                                                              'name': 'TXINE'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[1:1]',
                                                                                              'description': 'No '
                                                                                                             'Description.',
                                                                                              'name': 'STALLEDE'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[2:2]',
                                                                                              'description': 'No '
                                                                                                             'Description.',
                                                                                              'name': 'RXOUTE'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[3:3]',
                                                                                              'description': 'No '
                                                                                                             'Description.',
                                                                                              'name': 'RXSTPE'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[4:4]',
                                                                                              'description': 'No '
                                                                                                             'Description.',
                                                                                              'name': 'NAKOUTE'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[6:6]',
                                                                                              'description': 'No '
                                                                                                             'Description.',
                                                                                              'name': 'NAKINE'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[7:7]',
                                                                                              'description': 'No '
                                                                                                             'Description.',
                                                                                              'name': 'FLERRE'}]},
                                                                        'name': 'UEIENX',
                                                                        'size': 0x8},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x14,
                                                                        'description': 'No '
                                                                                       'Description.',
                                                                        'name': 'UEINT',
                                                                        'size': 0x8,
                                                                        'writeConstraint': {'range': {'maximum': 0xFF,
                                                                                                      'minimum': 0x0}}},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x8,
                                                                        'description': 'No '
                                                                                       'Description.',
                                                                        'fields': {'field': [{'access': 'read-write',
                                                                                              'bitRange': '[0:0]',
                                                                                              'description': 'No '
                                                                                                             'Description.',
                                                                                              'name': 'TXINI'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[1:1]',
                                                                                              'description': 'No '
                                                                                                             'Description.',
                                                                                              'name': 'STALLEDI'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[2:2]',
                                                                                              'description': 'No '
                                                                                                             'Description.',
                                                                                              'name': 'RXOUTI'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[3:3]',
                                                                                              'description': 'No '
                                                                                                             'Description.',
                                                                                              'name': 'RXSTPI'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[4:4]',
                                                                                              'description': 'No '
                                                                                                             'Description.',
                                                                                              'name': 'NAKOUTI'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[5:5]',
                                                                                              'description': 'No '
                                                                                                             'Description.',
                                                                                              'name': 'RWAL'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[6:6]',
                                                                                              'description': 'No '
                                                                                                             'Description.',
                                                                                              'name': 'NAKINI'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[7:7]',
                                                                                              'description': 'No '
                                                                                                             'Description.',
                                                                                              'name': 'FIFOCON'}]},
                                                                        'name': 'UEINTX',
                                                                        'size': 0x8},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x9,
                                                                        'description': 'No '
                                                                                       'Description.',
                                                                        'name': 'UENUM',
                                                                        'size': 0x8,
                                                                        'writeConstraint': {'range': {'maximum': 0xFF,
                                                                                                      'minimum': 0x0}}},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0xA,
                                                                        'description': 'No '
                                                                                       'Description.',
                                                                        'fields': {'field': [{'access': 'read-write',
                                                                                              'bitRange': '[6:0]',
                                                                                              'description': 'No '
                                                                                                             'Description.',
                                                                                              'name': 'EPRST',
                                                                                              'writeConstraint': {'range': {'maximum': 0x7F,
                                                                                                                            'minimum': 0x0}}}]},
                                                                        'name': 'UERST',
                                                                        'size': 0x8},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0xE,
                                                                        'description': 'No '
                                                                                       'Description.',
                                                                        'fields': {'field': [{'access': 'read-write',
                                                                                              'bitRange': '[1:0]',
                                                                                              'description': 'No '
                                                                                                             'Description.',
                                                                                              'name': 'NBUSYBK',
                                                                                              'writeConstraint': {'range': {'maximum': 0x3,
                                                                                                                            'minimum': 0x0}}},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[3:2]',
                                                                                              'description': 'No '
                                                                                                             'Description.',
                                                                                              'name': 'DTSEQ',
                                                                                              'writeConstraint': {'range': {'maximum': 0x3,
                                                                                                                            'minimum': 0x0}}},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[5:5]',
                                                                                              'description': 'No '
                                                                                                             'Description.',
                                                                                              'name': 'UNDERFI'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[6:6]',
                                                                                              'description': 'No '
                                                                                                             'Description.',
                                                                                              'name': 'OVERFI'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[7:7]',
                                                                                              'description': 'No '
                                                                                                             'Description.',
                                                                                              'name': 'CFGOK'}]},
                                                                        'name': 'UESTA0X',
                                                                        'size': 0x8},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0xF,
                                                                        'description': 'No '
                                                                                       'Description.',
                                                                        'fields': {'field': [{'access': 'read-write',
                                                                                              'bitRange': '[1:0]',
                                                                                              'description': 'No '
                                                                                                             'Description.',
                                                                                              'name': 'CURRBK',
                                                                                              'writeConstraint': {'range': {'maximum': 0x3,
                                                                                                                            'minimum': 0x0}}},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[2:2]',
                                                                                              'description': 'No '
                                                                                                             'Description.',
                                                                                              'name': 'CTRLDIR'}]},
                                                                        'name': 'UESTA1X',
                                                                        'size': 0x8}]}},
                                           {'addressBlock': [{'offset': 0x0,
                                                              'size': 0x4,
                                                              'usage': 'registers'}],
                                            'baseAddress': 0x8000D7,
                                            'description': 'USB Controller',
                                            'name': 'USB_GLOBAL',
                                            'registers': {'register': [{'access': 'read-write',
                                                                        'addressOffset': 0x0,
                                                                        'description': 'USB '
                                                                                       'Hardware '
                                                                                       'Configuration '
                                                                                       'Register',
                                                                        'fields': {'field': [{'access': 'read-write',
                                                                                              'bitRange': '[0:0]',
                                                                                              'description': 'No '
                                                                                                             'Description.',
                                                                                              'name': 'UVREGE'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[4:4]',
                                                                                              'description': 'No '
                                                                                                             'Description.',
                                                                                              'name': 'UVCONE'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[6:6]',
                                                                                              'description': 'No '
                                                                                                             'Description.',
                                                                                              'name': 'UIDE'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[7:7]',
                                                                                              'description': 'No '
                                                                                                             'Description.',
                                                                                              'name': 'UIMOD'}]},
                                                                        'name': 'UHWCON',
                                                                        'size': 0x8},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x1,
                                                                        'description': 'USB '
                                                                                       'General '
                                                                                       'Control '
                                                                                       'Register',
                                                                        'fields': {'field': [{'access': 'read-write',
                                                                                              'bitRange': '[0:0]',
                                                                                              'description': 'No '
                                                                                                             'Description.',
                                                                                              'name': 'VBUSTE'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[1:1]',
                                                                                              'description': 'No '
                                                                                                             'Description.',
                                                                                              'name': 'IDTE'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[4:4]',
                                                                                              'description': 'No '
                                                                                                             'Description.',
                                                                                              'name': 'OTGPADE'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[5:5]',
                                                                                              'description': 'No '
                                                                                                             'Description.',
                                                                                              'name': 'FRZCLK'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[6:6]',
                                                                                              'description': 'No '
                                                                                                             'Description.',
                                                                                              'name': 'HOST'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[7:7]',
                                                                                              'description': 'No '
                                                                                                             'Description.',
                                                                                              'name': 'USBE'}]},
                                                                        'name': 'USBCON',
                                                                        'size': 0x8},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x3,
                                                                        'description': 'No '
                                                                                       'Description.',
                                                                        'fields': {'field': [{'access': 'read-write',
                                                                                              'bitRange': '[0:0]',
                                                                                              'description': 'No '
                                                                                                             'Description.',
                                                                                              'name': 'VBUSTI'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[1:1]',
                                                                                              'description': 'No '
                                                                                                             'Description.',
                                                                                              'name': 'IDTI'}]},
                                                                        'name': 'USBINT',
                                                                        'size': 0x8},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x2,
                                                                        'description': 'No '
                                                                                       'Description.',
                                                                        'fields': {'field': [{'access': 'read-write',
                                                                                              'bitRange': '[0:0]',
                                                                                              'description': 'No '
                                                                                                             'Description.',
                                                                                              'name': 'VBUS'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[1:1]',
                                                                                              'description': 'No '
                                                                                                             'Description.',
                                                                                              'name': 'ID'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[3:3]',
                                                                                              'description': 'No '
                                                                                                             'Description.',
                                                                                              'name': 'SPEED'}]},
                                                                        'name': 'USBSTA',
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