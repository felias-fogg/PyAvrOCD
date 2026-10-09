# Device description for attiny25, generated from Microchip's ATtiny25.atdf by
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
    'name': 'attiny25',
    'architecture': 'avr8',

    # eeprom
    'eeprom_address_byte': 0x0000,
    'eeprom_size_bytes': 0x0080,
    'eeprom_page_size_bytes': 0x04,
    'eeprom_read_size_bytes': 0x01,
    'eeprom_write_size_bytes': 0x01,
    'eeprom_chiperase_effect': ChiperaseEffect.CONDITIONALLY_ERASED_AVR,
    'eeprom_isolated_erase': False,

    # flash
    'flash_address_byte': 0x0000,
    'flash_size_bytes': 0x0800,
    'flash_page_size_bytes': 0x20,
    'flash_read_size_bytes': 0x02,
    'flash_write_size_bytes': 0x20,
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
    'internal_sram_address_byte': 0x0060,
    'internal_sram_size_bytes': 0x0080,
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
    'ocd_base' : 0x22,
    'eear_base' : 0x1E,
    'eear_size' : 2,
    'eecr_base' : 0x1C,
    'eedr_base' : 0x1D,
    'spmcsr_base' : 0x57,
    'osccal_base' : 0x31,
    'dwen_base' : 0x01,
    'dwen_mask' : 0x40,
    'eesave_base' : 0x01,
    'eesave_mask' : 0x08,
    'tcnt0_base' : 0x52,
    'cs0_base' : 0x53,
    'toie0_base' : 0x59,
    'toie0_mask' : 0x02,
    'masked_registers' : [0x42],
    'ronly_registers' : [0x28, 0x2e, 0x30, 0x36, 0x41, 0x46, 0x4f, 0x51, 0x54, 0x57, 0x5a],
    'device_id': 0x1E9108,
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
            'name': 'ATtiny25',
            'peripherals': {'peripheral': [{'addressBlock': [{'offset': 0x0,
                                                              'size': 0x1,
                                                              'usage': 'registers'},
                                                             {'offset': 0x5,
                                                              'size': 0x1,
                                                              'usage': 'registers'},
                                                             {'offset': 0x11,
                                                              'size': 0x1,
                                                              'usage': 'registers'}],
                                            'baseAddress': 0x800023,
                                            'description': 'Analog Comparator',
                                            'name': 'AC',
                                            'registers': {'register': [{'access': 'read-write',
                                                                        'addressOffset': 0x5,
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
                                                                        'addressOffset': 0x0,
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
                                                                        'addressOffset': 0x11,
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
                                                                        'name': 'DIDR0',
                                                                        'size': 0x8}]}},
                                           {'addressBlock': [{'offset': 0x0,
                                                              'size': 0x5,
                                                              'usage': 'registers'},
                                                             {'offset': 0x11,
                                                              'size': 0x1,
                                                              'usage': 'registers'}],
                                            'baseAddress': 0x800023,
                                            'description': 'Analog-to-Digital '
                                                           'Converter',
                                            'name': 'ADC',
                                            'registers': {'register': [{'access': 'read-write',
                                                                        'addressOffset': 0x1,
                                                                        'description': 'ADC '
                                                                                       'Data '
                                                                                       'Register  '
                                                                                       'Bytes',
                                                                        'name': 'ADC',
                                                                        'size': 0x10,
                                                                        'writeConstraint': {'range': {'maximum': 0xFFFF,
                                                                                                      'minimum': 0x0}}},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x3,
                                                                        'description': 'The '
                                                                                       'ADC '
                                                                                       'Control '
                                                                                       'and '
                                                                                       'Status '
                                                                                       'register',
                                                                        'fields': {'field': [{'access': 'read-write',
                                                                                              'bitRange': '[2:0]',
                                                                                              'description': 'ADC  '
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
                                                                        'addressOffset': 0x0,
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
                                                                                              'bitRange': '[5:5]',
                                                                                              'description': 'Input '
                                                                                                             'Polarity '
                                                                                                             'Mode',
                                                                                              'name': 'IPR'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[7:7]',
                                                                                              'description': 'Bipolar '
                                                                                                             'Input '
                                                                                                             'Mode',
                                                                                              'name': 'BIN'}]},
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
                                                                                              'bitRange': '[3:0]',
                                                                                              'description': 'Analog '
                                                                                                             'Channel '
                                                                                                             'and '
                                                                                                             'Gain '
                                                                                                             'Selection '
                                                                                                             'Bits',
                                                                                              'name': 'MUX',
                                                                                              'writeConstraint': {'range': {'maximum': 0xF,
                                                                                                                            'minimum': 0x0}}},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[4:4]',
                                                                                              'description': 'Reference '
                                                                                                             'Selection '
                                                                                                             'Bit '
                                                                                                             '2',
                                                                                              'name': 'REFS2'},
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
                                                                                              'name': 'REFS',
                                                                                              'writeConstraint': {'range': {'maximum': 0x3,
                                                                                                                            'minimum': 0x0}}}]},
                                                                        'name': 'ADMUX',
                                                                        'size': 0x8},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x11,
                                                                        'description': 'Digital '
                                                                                       'Input '
                                                                                       'Disable '
                                                                                       'Register '
                                                                                       '0',
                                                                        'fields': {'field': [{'access': 'read-write',
                                                                                              'bitRange': '[2:2]',
                                                                                              'description': 'ADC1 '
                                                                                                             'Digital '
                                                                                                             'input '
                                                                                                             'Disable',
                                                                                              'name': 'ADC1D'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[3:3]',
                                                                                              'description': 'ADC3 '
                                                                                                             'Digital '
                                                                                                             'input '
                                                                                                             'Disable',
                                                                                              'name': 'ADC3D'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[4:4]',
                                                                                              'description': 'ADC2 '
                                                                                                             'Digital '
                                                                                                             'input '
                                                                                                             'Disable',
                                                                                              'name': 'ADC2D'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[5:5]',
                                                                                              'description': 'ADC0 '
                                                                                                             'Digital '
                                                                                                             'input '
                                                                                                             'Disable',
                                                                                              'name': 'ADC0D'}]},
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
                                                                                       'Register '
                                                                                       '(read-only '
                                                                                       'for '
                                                                                       'debugger)',
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
                                                                                              'description': 'Read '
                                                                                                             'fuse '
                                                                                                             'and '
                                                                                                             'lock '
                                                                                                             'bits',
                                                                                              'name': 'RFLB'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[4:4]',
                                                                                              'description': 'Clear '
                                                                                                             'temporary '
                                                                                                             'page '
                                                                                                             'buffer',
                                                                                              'name': 'CTPB'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[5:5]',
                                                                                              'description': 'Read '
                                                                                                             'Device '
                                                                                                             'Signature '
                                                                                                             'Imprint '
                                                                                                             'Table',
                                                                                              'name': 'RSIG'}]},
                                                                        'name': 'SPMCSR',
                                                                        'size': 0x8}]}},
                                           {'addressBlock': [{'offset': 0x0,
                                                              'size': 0x3,
                                                              'usage': 'registers'},
                                                             {'offset': 0xF,
                                                              'size': 0x1,
                                                              'usage': 'registers'},
                                                             {'offset': 0x11,
                                                              'size': 0x1,
                                                              'usage': 'registers'},
                                                             {'offset': 0x15,
                                                              'size': 0x2,
                                                              'usage': 'registers'},
                                                             {'offset': 0x20,
                                                              'size': 0x1,
                                                              'usage': 'registers'},
                                                             {'offset': 0x23,
                                                              'size': 0x2,
                                                              'usage': 'registers'},
                                                             {'offset': 0x2C,
                                                              'size': 0x1,
                                                              'usage': 'registers'},
                                                             {'offset': 0x2E,
                                                              'size': 0x1,
                                                              'usage': 'registers'}],
                                            'baseAddress': 0x800031,
                                            'description': 'CPU Registers',
                                            'interrupt': [{'description': 'External '
                                                                          'Pin, '
                                                                          'Power-on '
                                                                          'Reset, '
                                                                          'Brown-out '
                                                                          'Reset,Watchdog '
                                                                          'Reset',
                                                           'name': 'RESET',
                                                           'value': 0x0},
                                                          {'description': 'External '
                                                                          'Interrupt '
                                                                          '0',
                                                           'name': 'INT0',
                                                           'value': 0x1},
                                                          {'description': 'Pin '
                                                                          'change '
                                                                          'Interrupt '
                                                                          'Request '
                                                                          '0',
                                                           'name': 'PCINT0',
                                                           'value': 0x2},
                                                          {'description': 'Timer/Counter1 '
                                                                          'Compare '
                                                                          'Match '
                                                                          '1A',
                                                           'name': 'TIMER1_COMPA',
                                                           'value': 0x3},
                                                          {'description': 'Timer/Counter1 '
                                                                          'Overflow',
                                                           'name': 'TIMER1_OVF',
                                                           'value': 0x4},
                                                          {'description': 'Timer/Counter0 '
                                                                          'Overflow',
                                                           'name': 'TIMER0_OVF',
                                                           'value': 0x5},
                                                          {'description': 'EEPROM '
                                                                          'Ready',
                                                           'name': 'EE_RDY',
                                                           'value': 0x6},
                                                          {'description': 'Analog '
                                                                          'comparator',
                                                           'name': 'ANA_COMP',
                                                           'value': 0x7},
                                                          {'description': 'ADC '
                                                                          'Conversion '
                                                                          'ready',
                                                           'name': 'ADC',
                                                           'value': 0x8},
                                                          {'description': 'Timer/Counter1 '
                                                                          'Compare '
                                                                          'Match '
                                                                          'B',
                                                           'name': 'TIMER1_COMPB',
                                                           'value': 0x9},
                                                          {'description': 'Timer/Counter0 '
                                                                          'Compare '
                                                                          'Match '
                                                                          'A',
                                                           'name': 'TIMER0_COMPA',
                                                           'value': 0xA},
                                                          {'description': 'Timer/Counter0 '
                                                                          'Compare '
                                                                          'Match '
                                                                          'B',
                                                           'name': 'TIMER0_COMPB',
                                                           'value': 0xB},
                                                          {'description': 'Watchdog '
                                                                          'Time-out',
                                                           'name': 'WDT',
                                                           'value': 0xC},
                                                          {'description': 'USI '
                                                                          'START',
                                                           'name': 'USI_START',
                                                           'value': 0xD},
                                                          {'description': 'USI '
                                                                          'Overflow',
                                                           'name': 'USI_OVF',
                                                           'value': 0xE}],
                                            'name': 'CPU',
                                            'registers': {'register': [{'access': 'read-write',
                                                                        'addressOffset': 0x15,
                                                                        'description': 'Clock '
                                                                                       'Prescale '
                                                                                       'Register '
                                                                                       '(read-only '
                                                                                       'for '
                                                                                       'debugger)',
                                                                        'fields': {'field': [{'access': 'read-write',
                                                                                              'bitRange': '[3:0]',
                                                                                              'description': 'Clock '
                                                                                                             'Prescaler '
                                                                                                             'Select '
                                                                                                             'Bits',
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
                                                                                              'description': 'Clock '
                                                                                                             'Prescaler '
                                                                                                             'Change '
                                                                                                             'Enable',
                                                                                              'name': 'CLKPCE'}]},
                                                                        'name': 'CLKPR',
                                                                        'size': 0x8},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x11,
                                                                        'description': 'debugWire '
                                                                                       'data '
                                                                                       'register '
                                                                                       '(write-only '
                                                                                       'for '
                                                                                       'debugger)',
                                                                        'name': 'DWDR',
                                                                        'size': 0x8,
                                                                        'writeConstraint': {'range': {'maximum': 0xFF,
                                                                                                      'minimum': 0x0}}},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x0,
                                                                        'description': 'General '
                                                                                       'purpose '
                                                                                       'register '
                                                                                       '0',
                                                                        'name': 'GPIOR0',
                                                                        'size': 0x8,
                                                                        'writeConstraint': {'range': {'maximum': 0xFF,
                                                                                                      'minimum': 0x0}}},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x1,
                                                                        'description': 'General '
                                                                                       'Purpose '
                                                                                       'register '
                                                                                       '1',
                                                                        'name': 'GPIOR1',
                                                                        'size': 0x8,
                                                                        'writeConstraint': {'range': {'maximum': 0xFF,
                                                                                                      'minimum': 0x0}}},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x2,
                                                                        'description': 'General '
                                                                                       'Purpose '
                                                                                       'IO '
                                                                                       'register '
                                                                                       '2',
                                                                        'name': 'GPIOR2',
                                                                        'size': 0x8,
                                                                        'writeConstraint': {'range': {'maximum': 0xFF,
                                                                                                      'minimum': 0x0}}},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x24,
                                                                        'description': 'MCU '
                                                                                       'Control '
                                                                                       'Register',
                                                                        'fields': {'field': [{'access': 'read-write',
                                                                                              'bitRange': '[1:0]',
                                                                                              'description': 'Interrupt '
                                                                                                             'Sense '
                                                                                                             'Control '
                                                                                                             '0 '
                                                                                                             'bits',
                                                                                              'enumeratedValues': {'enumeratedValue': [{'description': 'Low '
                                                                                                                                                       'Level '
                                                                                                                                                       'of '
                                                                                                                                                       'INTX',
                                                                                                                                        'name': 'LOW_LEVEL_OF_INTX',
                                                                                                                                        'value': 0x0},
                                                                                                                                       {'description': 'Any '
                                                                                                                                                       'Logical '
                                                                                                                                                       'Change '
                                                                                                                                                       'in '
                                                                                                                                                       'INTX',
                                                                                                                                        'name': 'ANY_LOGICAL_CHANGE_IN_INTX',
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
                                                                                              'bitRange': '[4:3]',
                                                                                              'description': 'Sleep '
                                                                                                             'Mode '
                                                                                                             'Select '
                                                                                                             'Bits',
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
                                                                                                                                       {'description': 'Reserved',
                                                                                                                                        'name': 'VAL_0x03',
                                                                                                                                        'value': 0x3}]},
                                                                                              'name': 'SM',
                                                                                              'writeConstraint': {'useEnumeratedValues': 0x1}},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[5:5]',
                                                                                              'description': 'Sleep '
                                                                                                             'Enable',
                                                                                              'name': 'SE'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[6:6]',
                                                                                              'description': 'Pull-up '
                                                                                                             'Disable',
                                                                                              'name': 'PUD'}]},
                                                                        'name': 'MCUCR',
                                                                        'size': 0x8},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x23,
                                                                        'description': 'MCU '
                                                                                       'Status '
                                                                                       'register '
                                                                                       '(read-only '
                                                                                       'for '
                                                                                       'debugger)',
                                                                        'fields': {'field': [{'access': 'read-write',
                                                                                              'bitRange': '[0:0]',
                                                                                              'description': 'Power-On '
                                                                                                             'Reset '
                                                                                                             'Flag',
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
                                                                                              'name': 'WDRF'}]},
                                                                        'name': 'MCUSR',
                                                                        'size': 0x8},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x20,
                                                                        'description': 'Oscillator '
                                                                                       'Calibration '
                                                                                       'Register '
                                                                                       '(read-only '
                                                                                       'for '
                                                                                       'debugger)',
                                                                        'fields': {'field': [{'access': 'read-write',
                                                                                              'bitRange': '[7:0]',
                                                                                              'description': 'Oscillator '
                                                                                                             'Calibration',
                                                                                              'name': 'OSCCAL',
                                                                                              'writeConstraint': {'range': {'maximum': 0xFF,
                                                                                                                            'minimum': 0x0}}}]},
                                                                        'name': 'OSCCAL',
                                                                        'size': 0x8},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x16,
                                                                        'description': 'PLL '
                                                                                       'Control '
                                                                                       'and '
                                                                                       'status '
                                                                                       'register',
                                                                        'fields': {'field': [{'access': 'read-write',
                                                                                              'bitRange': '[0:0]',
                                                                                              'description': 'PLL '
                                                                                                             'Lock '
                                                                                                             'detector',
                                                                                              'name': 'PLOCK'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[1:1]',
                                                                                              'description': 'PLL '
                                                                                                             'Enable',
                                                                                              'name': 'PLLE'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[2:2]',
                                                                                              'description': 'PCK '
                                                                                                             'Enable',
                                                                                              'name': 'PCKE'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[7:7]',
                                                                                              'description': 'Low '
                                                                                                             'speed '
                                                                                                             'mode',
                                                                                              'name': 'LSM'}]},
                                                                        'name': 'PLLCSR',
                                                                        'size': 0x8},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0xF,
                                                                        'description': 'Power '
                                                                                       'Reduction '
                                                                                       'Register',
                                                                        'fields': {'field': [{'access': 'read-write',
                                                                                              'bitRange': '[0:0]',
                                                                                              'description': 'Power '
                                                                                                             'Reduction '
                                                                                                             'ADC',
                                                                                              'name': 'PRADC'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[1:1]',
                                                                                              'description': 'Power '
                                                                                                             'Reduction '
                                                                                                             'USI',
                                                                                              'name': 'PRUSI'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[2:2]',
                                                                                              'description': 'Power '
                                                                                                             'Reduction '
                                                                                                             'Timer/Counter0',
                                                                                              'name': 'PRTIM0'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[3:3]',
                                                                                              'description': 'Power '
                                                                                                             'Reduction '
                                                                                                             'Timer/Counter1',
                                                                                              'name': 'PRTIM1'}]},
                                                                        'name': 'PRR',
                                                                        'size': 0x8},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x2C,
                                                                        'description': 'Stack '
                                                                                       'Pointer '
                                                                                       'Low '
                                                                                       'Byte',
                                                                        'name': 'SPL',
                                                                        'size': 0x8,
                                                                        'writeConstraint': {'range': {'maximum': 0xFF,
                                                                                                      'minimum': 0x0}}},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x2E,
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
                                            'baseAddress': 0x80003C,
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
                                                              'size': 0x1,
                                                              'usage': 'registers'},
                                                             {'offset': 0x20,
                                                              'size': 0x1,
                                                              'usage': 'registers'},
                                                             {'offset': 0x25,
                                                              'size': 0x2,
                                                              'usage': 'registers'}],
                                            'baseAddress': 0x800035,
                                            'description': 'External '
                                                           'Interrupts',
                                            'name': 'EXINT',
                                            'registers': {'register': [{'access': 'read-write',
                                                                        'addressOffset': 0x25,
                                                                        'description': 'General '
                                                                                       'Interrupt '
                                                                                       'Flag '
                                                                                       'register '
                                                                                       '(read-only '
                                                                                       'for '
                                                                                       'debugger)',
                                                                        'fields': {'field': [{'access': 'read-write',
                                                                                              'bitRange': '[5:5]',
                                                                                              'description': 'Pin '
                                                                                                             'Change '
                                                                                                             'Interrupt '
                                                                                                             'Flag',
                                                                                              'name': 'PCIF'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[6:6]',
                                                                                              'description': 'External '
                                                                                                             'Interrupt '
                                                                                                             'Flag '
                                                                                                             '0',
                                                                                              'name': 'INTF0'}]},
                                                                        'name': 'GIFR',
                                                                        'size': 0x8},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x26,
                                                                        'description': 'General '
                                                                                       'Interrupt '
                                                                                       'Mask '
                                                                                       'Register',
                                                                        'fields': {'field': [{'access': 'read-write',
                                                                                              'bitRange': '[5:5]',
                                                                                              'description': 'Pin '
                                                                                                             'Change '
                                                                                                             'Interrupt '
                                                                                                             'Enable',
                                                                                              'name': 'PCIE'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[6:6]',
                                                                                              'description': 'External '
                                                                                                             'Interrupt '
                                                                                                             'Request '
                                                                                                             '0 '
                                                                                                             'Enable',
                                                                                              'name': 'INT0'}]},
                                                                        'name': 'GIMSK',
                                                                        'size': 0x8},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x20,
                                                                        'description': 'MCU '
                                                                                       'Control '
                                                                                       'Register',
                                                                        'fields': {'field': [{'access': 'read-write',
                                                                                              'bitRange': '[0:0]',
                                                                                              'description': 'Interrupt '
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
                                                                                                                                                       'on '
                                                                                                                                                       'INTX',
                                                                                                                                        'name': 'ANY_LOGICAL_CHANGE_ON_INTX',
                                                                                                                                        'value': 0x1}]},
                                                                                              'name': 'ISC00',
                                                                                              'writeConstraint': {'useEnumeratedValues': 0x1}},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[1:1]',
                                                                                              'description': 'Interrupt '
                                                                                                             'Sense '
                                                                                                             'Control '
                                                                                                             '0 '
                                                                                                             'Bit '
                                                                                                             '1',
                                                                                              'name': 'ISC01'}]},
                                                                        'name': 'MCUCR',
                                                                        'size': 0x8},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x0,
                                                                        'description': 'Pin '
                                                                                       'Change '
                                                                                       'Enable '
                                                                                       'Mask',
                                                                        'name': 'PCMSK',
                                                                        'size': 0x8,
                                                                        'writeConstraint': {'range': {'maximum': 0xFF,
                                                                                                      'minimum': 0x0}}}]}},
                                           {'addressBlock': [{'offset': 0x0,
                                                              'size': 0x3,
                                                              'usage': 'registers'}],
                                            'baseAddress': 0x800036,
                                            'description': 'I/O Port',
                                            'name': 'PORTB',
                                            'registers': {'register': [{'access': 'read-write',
                                                                        'addressOffset': 0x1,
                                                                        'description': 'Data '
                                                                                       'Direction '
                                                                                       'Register, '
                                                                                       'Port '
                                                                                       'B',
                                                                        'fields': {'field': [{'access': 'read-write',
                                                                                              'bitRange': '[0:0]',
                                                                                              'description': 'Pin '
                                                                                                             'B0',
                                                                                              'name': 'PB0'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[1:1]',
                                                                                              'description': 'Pin '
                                                                                                             'B1',
                                                                                              'name': 'PB1'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[2:2]',
                                                                                              'description': 'Pin '
                                                                                                             'B2',
                                                                                              'name': 'PB2'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[3:3]',
                                                                                              'description': 'Pin '
                                                                                                             'B3',
                                                                                              'name': 'PB3'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[4:4]',
                                                                                              'description': 'Pin '
                                                                                                             'B4',
                                                                                              'name': 'PB4'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[5:5]',
                                                                                              'description': 'Pin '
                                                                                                             'B5',
                                                                                              'name': 'PB5'}]},
                                                                        'name': 'DDRB',
                                                                        'size': 0x8},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x0,
                                                                        'description': 'Input '
                                                                                       'Pins, '
                                                                                       'Port '
                                                                                       'B '
                                                                                       '(read-only '
                                                                                       'for '
                                                                                       'debugger)',
                                                                        'fields': {'field': [{'access': 'read-write',
                                                                                              'bitRange': '[0:0]',
                                                                                              'description': 'Pin '
                                                                                                             'B0',
                                                                                              'name': 'PB0'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[1:1]',
                                                                                              'description': 'Pin '
                                                                                                             'B1',
                                                                                              'name': 'PB1'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[2:2]',
                                                                                              'description': 'Pin '
                                                                                                             'B2',
                                                                                              'name': 'PB2'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[3:3]',
                                                                                              'description': 'Pin '
                                                                                                             'B3',
                                                                                              'name': 'PB3'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[4:4]',
                                                                                              'description': 'Pin '
                                                                                                             'B4',
                                                                                              'name': 'PB4'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[5:5]',
                                                                                              'description': 'Pin '
                                                                                                             'B5',
                                                                                              'name': 'PB5'}]},
                                                                        'name': 'PINB',
                                                                        'size': 0x8},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x2,
                                                                        'description': 'Data '
                                                                                       'Register, '
                                                                                       'Port '
                                                                                       'B',
                                                                        'fields': {'field': [{'access': 'read-write',
                                                                                              'bitRange': '[0:0]',
                                                                                              'description': 'Pin '
                                                                                                             'B0',
                                                                                              'name': 'PB0'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[1:1]',
                                                                                              'description': 'Pin '
                                                                                                             'B1',
                                                                                              'name': 'PB1'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[2:2]',
                                                                                              'description': 'Pin '
                                                                                                             'B2',
                                                                                              'name': 'PB2'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[3:3]',
                                                                                              'description': 'Pin '
                                                                                                             'B3',
                                                                                              'name': 'PB3'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[4:4]',
                                                                                              'description': 'Pin '
                                                                                                             'B4',
                                                                                              'name': 'PB4'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[5:5]',
                                                                                              'description': 'Pin '
                                                                                                             'B5',
                                                                                              'name': 'PB5'}]},
                                                                        'name': 'PORTB',
                                                                        'size': 0x8}]}},
                                           {'addressBlock': [{'offset': 0x0,
                                                              'size': 0x3,
                                                              'usage': 'registers'},
                                                             {'offset': 0x4,
                                                              'size': 0x1,
                                                              'usage': 'registers'},
                                                             {'offset': 0xA,
                                                              'size': 0x2,
                                                              'usage': 'registers'},
                                                             {'offset': 0x10,
                                                              'size': 0x2,
                                                              'usage': 'registers'}],
                                            'baseAddress': 0x800048,
                                            'description': 'Timer/Counter, '
                                                           '8-bit',
                                            'name': 'TC0',
                                            'registers': {'register': [{'access': 'read-write',
                                                                        'addressOffset': 0x4,
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
                                                                                              'name': 'PSR0'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[7:7]',
                                                                                              'description': 'Timer/Counter '
                                                                                                             'Synchronization '
                                                                                                             'Mode',
                                                                                              'name': 'TSM'}]},
                                                                        'name': 'GTCCR',
                                                                        'size': 0x8},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x1,
                                                                        'description': 'Timer/Counter0 '
                                                                                       'Output '
                                                                                       'Compare '
                                                                                       'Register',
                                                                        'name': 'OCR0A',
                                                                        'size': 0x8,
                                                                        'writeConstraint': {'range': {'maximum': 0xFF,
                                                                                                      'minimum': 0x0}}},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x0,
                                                                        'description': 'Timer/Counter0 '
                                                                                       'Output '
                                                                                       'Compare '
                                                                                       'Register',
                                                                        'name': 'OCR0B',
                                                                        'size': 0x8,
                                                                        'writeConstraint': {'range': {'maximum': 0xFF,
                                                                                                      'minimum': 0x0}}},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x2,
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
                                                                        'addressOffset': 0xB,
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
                                                                        'addressOffset': 0xA,
                                                                        'description': 'Timer/Counter0',
                                                                        'name': 'TCNT0',
                                                                        'size': 0x8,
                                                                        'writeConstraint': {'range': {'maximum': 0xFF,
                                                                                                      'minimum': 0x0}}},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x10,
                                                                        'description': 'Timer/Counter0 '
                                                                                       'Interrupt '
                                                                                       'Flag '
                                                                                       'register',
                                                                        'fields': {'field': [{'access': 'read-write',
                                                                                              'bitRange': '[1:1]',
                                                                                              'description': 'Timer/Counter0 '
                                                                                                             'Overflow '
                                                                                                             'Flag',
                                                                                              'name': 'TOV0'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[3:3]',
                                                                                              'description': 'Timer/Counter0 '
                                                                                                             'Output '
                                                                                                             'Compare '
                                                                                                             'Flag '
                                                                                                             '0B',
                                                                                              'name': 'OCF0B'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[4:4]',
                                                                                              'description': 'Timer/Counter0 '
                                                                                                             'Output '
                                                                                                             'Compare '
                                                                                                             'Flag '
                                                                                                             '0A',
                                                                                              'name': 'OCF0A'}]},
                                                                        'name': 'TIFR',
                                                                        'size': 0x8},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x11,
                                                                        'description': 'Timer/Counter '
                                                                                       'Interrupt '
                                                                                       'Mask '
                                                                                       'Register',
                                                                        'fields': {'field': [{'access': 'read-write',
                                                                                              'bitRange': '[1:1]',
                                                                                              'description': 'Timer/Counter0 '
                                                                                                             'Overflow '
                                                                                                             'Interrupt '
                                                                                                             'Enable',
                                                                                              'name': 'TOIE0'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[3:3]',
                                                                                              'description': 'Timer/Counter0 '
                                                                                                             'Output '
                                                                                                             'Compare '
                                                                                                             'Match '
                                                                                                             'B '
                                                                                                             'Interrupt '
                                                                                                             'Enable',
                                                                                              'name': 'OCIE0B'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[4:4]',
                                                                                              'description': 'Timer/Counter0 '
                                                                                                             'Output '
                                                                                                             'Compare '
                                                                                                             'Match '
                                                                                                             'A '
                                                                                                             'Interrupt '
                                                                                                             'Enable',
                                                                                              'name': 'OCIE0A'}]},
                                                                        'name': 'TIMSK',
                                                                        'size': 0x8}]}},
                                           {'addressBlock': [{'offset': 0x0,
                                                              'size': 0x3,
                                                              'usage': 'registers'},
                                                             {'offset': 0x8,
                                                              'size': 0x6,
                                                              'usage': 'registers'},
                                                             {'offset': 0x15,
                                                              'size': 0x2,
                                                              'usage': 'registers'}],
                                            'baseAddress': 0x800043,
                                            'description': 'Timer/Counter, '
                                                           '8-bit',
                                            'name': 'TC1',
                                            'registers': {'register': [{'access': 'read-write',
                                                                        'addressOffset': 0x2,
                                                                        'description': 'Dead '
                                                                                       'time '
                                                                                       'value '
                                                                                       'register',
                                                                        'fields': {'field': [{'access': 'read-write',
                                                                                              'bitRange': '[3:0]',
                                                                                              'description': 'No '
                                                                                                             'Description.',
                                                                                              'name': 'DTVL',
                                                                                              'writeConstraint': {'range': {'maximum': 0xF,
                                                                                                                            'minimum': 0x0}}},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[7:4]',
                                                                                              'description': 'No '
                                                                                                             'Description.',
                                                                                              'name': 'DTVH',
                                                                                              'writeConstraint': {'range': {'maximum': 0xF,
                                                                                                                            'minimum': 0x0}}}]},
                                                                        'name': 'DT1A',
                                                                        'size': 0x8},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x1,
                                                                        'description': 'Dead '
                                                                                       'time '
                                                                                       'value '
                                                                                       'B',
                                                                        'fields': {'field': [{'access': 'read-write',
                                                                                              'bitRange': '[3:0]',
                                                                                              'description': 'No '
                                                                                                             'Description.',
                                                                                              'name': 'DTVL',
                                                                                              'writeConstraint': {'range': {'maximum': 0xF,
                                                                                                                            'minimum': 0x0}}},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[7:4]',
                                                                                              'description': 'No '
                                                                                                             'Description.',
                                                                                              'name': 'DTVH',
                                                                                              'writeConstraint': {'range': {'maximum': 0xF,
                                                                                                                            'minimum': 0x0}}}]},
                                                                        'name': 'DT1B',
                                                                        'size': 0x8},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x0,
                                                                        'description': 'Dead '
                                                                                       'time '
                                                                                       'prescaler '
                                                                                       'register',
                                                                        'fields': {'field': [{'access': 'read-write',
                                                                                              'bitRange': '[1:0]',
                                                                                              'description': 'No '
                                                                                                             'Description.',
                                                                                              'name': 'DTPS',
                                                                                              'writeConstraint': {'range': {'maximum': 0x3,
                                                                                                                            'minimum': 0x0}}}]},
                                                                        'name': 'DTPS',
                                                                        'size': 0x8},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x9,
                                                                        'description': 'Timer '
                                                                                       'counter '
                                                                                       'control '
                                                                                       'register',
                                                                        'fields': {'field': [{'access': 'read-write',
                                                                                              'bitRange': '[1:1]',
                                                                                              'description': 'Prescaler '
                                                                                                             'Reset '
                                                                                                             'Timer/Counter1',
                                                                                              'name': 'PSR1'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[2:2]',
                                                                                              'description': 'Force '
                                                                                                             'Output '
                                                                                                             'Compare '
                                                                                                             '1A',
                                                                                              'name': 'FOC1A'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[3:3]',
                                                                                              'description': 'Force '
                                                                                                             'Output '
                                                                                                             'Compare '
                                                                                                             'Match '
                                                                                                             '1B',
                                                                                              'name': 'FOC1B'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[5:4]',
                                                                                              'description': 'Comparator '
                                                                                                             'B '
                                                                                                             'Output '
                                                                                                             'Mode',
                                                                                              'name': 'COM1B',
                                                                                              'writeConstraint': {'range': {'maximum': 0x3,
                                                                                                                            'minimum': 0x0}}},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[6:6]',
                                                                                              'description': 'Pulse '
                                                                                                             'Width '
                                                                                                             'Modulator '
                                                                                                             'B '
                                                                                                             'Enable',
                                                                                              'name': 'PWM1B'}]},
                                                                        'name': 'GTCCR',
                                                                        'size': 0x8},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0xB,
                                                                        'description': 'Output '
                                                                                       'Compare '
                                                                                       'Register',
                                                                        'name': 'OCR1A',
                                                                        'size': 0x8,
                                                                        'writeConstraint': {'range': {'maximum': 0xFF,
                                                                                                      'minimum': 0x0}}},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x8,
                                                                        'description': 'Output '
                                                                                       'Compare '
                                                                                       'Register',
                                                                        'name': 'OCR1B',
                                                                        'size': 0x8,
                                                                        'writeConstraint': {'range': {'maximum': 0xFF,
                                                                                                      'minimum': 0x0}}},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0xA,
                                                                        'description': 'Output '
                                                                                       'compare '
                                                                                       'register',
                                                                        'name': 'OCR1C',
                                                                        'size': 0x8,
                                                                        'writeConstraint': {'range': {'maximum': 0xFF,
                                                                                                      'minimum': 0x0}}},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0xD,
                                                                        'description': 'Timer/Counter '
                                                                                       'Control '
                                                                                       'Register',
                                                                        'fields': {'field': [{'access': 'read-write',
                                                                                              'bitRange': '[3:0]',
                                                                                              'description': 'Clock '
                                                                                                             'Select '
                                                                                                             'Bits',
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
                                                                                                                                                       'CLK/2',
                                                                                                                                        'name': 'RUNNING_CLK_2',
                                                                                                                                        'value': 0x2},
                                                                                                                                       {'description': 'Running, '
                                                                                                                                                       'CLK/4',
                                                                                                                                        'name': 'RUNNING_CLK_4',
                                                                                                                                        'value': 0x3},
                                                                                                                                       {'description': 'Running, '
                                                                                                                                                       'CLK/8',
                                                                                                                                        'name': 'RUNNING_CLK_8',
                                                                                                                                        'value': 0x4},
                                                                                                                                       {'description': 'Running, '
                                                                                                                                                       'CLK/16',
                                                                                                                                        'name': 'RUNNING_CLK_16',
                                                                                                                                        'value': 0x5},
                                                                                                                                       {'description': 'Running, '
                                                                                                                                                       'CLK/32',
                                                                                                                                        'name': 'RUNNING_CLK_32',
                                                                                                                                        'value': 0x6},
                                                                                                                                       {'description': 'Running, '
                                                                                                                                                       'CLK/64',
                                                                                                                                        'name': 'RUNNING_CLK_64',
                                                                                                                                        'value': 0x7},
                                                                                                                                       {'description': 'Running, '
                                                                                                                                                       'CLK/128',
                                                                                                                                        'name': 'RUNNING_CLK_128',
                                                                                                                                        'value': 0x8},
                                                                                                                                       {'description': 'Running, '
                                                                                                                                                       'CLK/256',
                                                                                                                                        'name': 'RUNNING_CLK_256',
                                                                                                                                        'value': 0x9},
                                                                                                                                       {'description': 'Running, '
                                                                                                                                                       'CLK/512',
                                                                                                                                        'name': 'RUNNING_CLK_512',
                                                                                                                                        'value': 0xA},
                                                                                                                                       {'description': 'Running, '
                                                                                                                                                       'CLK/1024',
                                                                                                                                        'name': 'RUNNING_CLK_1024',
                                                                                                                                        'value': 0xB},
                                                                                                                                       {'description': 'Running, '
                                                                                                                                                       'CLK/2048',
                                                                                                                                        'name': 'RUNNING_CLK_2048',
                                                                                                                                        'value': 0xC},
                                                                                                                                       {'description': 'Running, '
                                                                                                                                                       'CLK/4096',
                                                                                                                                        'name': 'RUNNING_CLK_4096',
                                                                                                                                        'value': 0xD},
                                                                                                                                       {'description': 'Running, '
                                                                                                                                                       'CLK/8192',
                                                                                                                                        'name': 'RUNNING_CLK_8192',
                                                                                                                                        'value': 0xE},
                                                                                                                                       {'description': 'Running, '
                                                                                                                                                       'CLK/16384',
                                                                                                                                        'name': 'RUNNING_CLK_16384',
                                                                                                                                        'value': 0xF}]},
                                                                                              'name': 'CS1',
                                                                                              'writeConstraint': {'useEnumeratedValues': 0x1}},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[5:4]',
                                                                                              'description': 'Compare '
                                                                                                             'Output '
                                                                                                             'Mode, '
                                                                                                             'Bits',
                                                                                              'enumeratedValues': {'enumeratedValue': [{'description': 'Disconnected '
                                                                                                                                                       'from '
                                                                                                                                                       'OCn/PWMn',
                                                                                                                                        'name': 'DISCONNECTED_FROM_OCN_PWMN',
                                                                                                                                        'value': 0x0},
                                                                                                                                       {'description': 'Toggle '
                                                                                                                                                       'OCn/PWMn '
                                                                                                                                                       'output '
                                                                                                                                                       'line',
                                                                                                                                        'name': 'TOGGLE_OCN_PWMN_OUTPUT_LINE',
                                                                                                                                        'value': 0x1},
                                                                                                                                       {'description': 'Clear '
                                                                                                                                                       'OCn/PWMn '
                                                                                                                                                       'output '
                                                                                                                                                       'line',
                                                                                                                                        'name': 'CLEAR_OCN_PWMN_OUTPUT_LINE',
                                                                                                                                        'value': 0x2},
                                                                                                                                       {'description': 'set '
                                                                                                                                                       'OCn/PWMn '
                                                                                                                                                       'output '
                                                                                                                                                       'line',
                                                                                                                                        'name': 'SET_OCN_PWMN_OUTPUT_LINE',
                                                                                                                                        'value': 0x3}]},
                                                                                              'name': 'COM1A',
                                                                                              'writeConstraint': {'useEnumeratedValues': 0x1}},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[6:6]',
                                                                                              'description': 'Pulse '
                                                                                                             'Width '
                                                                                                             'Modulator '
                                                                                                             'Enable',
                                                                                              'name': 'PWM1A'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[7:7]',
                                                                                              'description': 'Clear '
                                                                                                             'Timer/Counter '
                                                                                                             'on '
                                                                                                             'Compare '
                                                                                                             'Match',
                                                                                              'name': 'CTC1'}]},
                                                                        'name': 'TCCR1',
                                                                        'size': 0x8},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0xC,
                                                                        'description': 'Timer/Counter '
                                                                                       'Register '
                                                                                       '(read-only '
                                                                                       'for '
                                                                                       'debugger)',
                                                                        'name': 'TCNT1',
                                                                        'size': 0x8,
                                                                        'writeConstraint': {'range': {'maximum': 0xFF,
                                                                                                      'minimum': 0x0}}},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x15,
                                                                        'description': 'Timer/Counter '
                                                                                       'Interrupt '
                                                                                       'Flag '
                                                                                       'Register',
                                                                        'fields': {'field': [{'access': 'read-write',
                                                                                              'bitRange': '[2:2]',
                                                                                              'description': 'Timer/Counter1 '
                                                                                                             'Overflow '
                                                                                                             'Flag',
                                                                                              'name': 'TOV1'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[5:5]',
                                                                                              'description': 'Timer/Counter1 '
                                                                                                             'Output '
                                                                                                             'Compare '
                                                                                                             'Flag '
                                                                                                             '1B',
                                                                                              'name': 'OCF1B'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[6:6]',
                                                                                              'description': 'Timer/Counter1 '
                                                                                                             'Output '
                                                                                                             'Compare '
                                                                                                             'Flag '
                                                                                                             '1A',
                                                                                              'name': 'OCF1A'}]},
                                                                        'name': 'TIFR',
                                                                        'size': 0x8},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x16,
                                                                        'description': 'Timer/Counter '
                                                                                       'Interrupt '
                                                                                       'Mask '
                                                                                       'Register',
                                                                        'fields': {'field': [{'access': 'read-write',
                                                                                              'bitRange': '[2:2]',
                                                                                              'description': 'Timer/Counter1 '
                                                                                                             'Overflow '
                                                                                                             'Interrupt '
                                                                                                             'Enable',
                                                                                              'name': 'TOIE1'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[5:5]',
                                                                                              'description': 'OCIE1A: '
                                                                                                             'Timer/Counter1 '
                                                                                                             'Output '
                                                                                                             'Compare '
                                                                                                             'B '
                                                                                                             'Interrupt '
                                                                                                             'Enable',
                                                                                              'name': 'OCIE1B'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[6:6]',
                                                                                              'description': 'OCIE1A: '
                                                                                                             'Timer/Counter1 '
                                                                                                             'Output '
                                                                                                             'Compare '
                                                                                                             'Interrupt '
                                                                                                             'Enable',
                                                                                              'name': 'OCIE1A'}]},
                                                                        'name': 'TIMSK',
                                                                        'size': 0x8}]}},
                                           {'addressBlock': [{'offset': 0x0,
                                                              'size': 0x4,
                                                              'usage': 'registers'}],
                                            'baseAddress': 0x80002D,
                                            'description': 'Universal Serial '
                                                           'Interface',
                                            'name': 'USI',
                                            'registers': {'register': [{'access': 'read-write',
                                                                        'addressOffset': 0x3,
                                                                        'description': 'USI '
                                                                                       'Buffer '
                                                                                       'Register '
                                                                                       '(read-only '
                                                                                       'for '
                                                                                       'debugger)',
                                                                        'name': 'USIBR',
                                                                        'size': 0x8,
                                                                        'writeConstraint': {'range': {'maximum': 0xFF,
                                                                                                      'minimum': 0x0}}},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x0,
                                                                        'description': 'USI '
                                                                                       'Control '
                                                                                       'Register',
                                                                        'fields': {'field': [{'access': 'read-write',
                                                                                              'bitRange': '[0:0]',
                                                                                              'description': 'Toggle '
                                                                                                             'Clock '
                                                                                                             'Port '
                                                                                                             'Pin',
                                                                                              'name': 'USITC'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[1:1]',
                                                                                              'description': 'Clock '
                                                                                                             'Strobe',
                                                                                              'name': 'USICLK'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[3:2]',
                                                                                              'description': 'USI '
                                                                                                             'Clock '
                                                                                                             'Source '
                                                                                                             'Select '
                                                                                                             'Bits',
                                                                                              'name': 'USICS',
                                                                                              'writeConstraint': {'range': {'maximum': 0x3,
                                                                                                                            'minimum': 0x0}}},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[5:4]',
                                                                                              'description': 'USI '
                                                                                                             'Wire '
                                                                                                             'Mode '
                                                                                                             'Bits',
                                                                                              'enumeratedValues': {'enumeratedValue': [{'description': 'Normal '
                                                                                                                                                       'Operation',
                                                                                                                                        'name': 'NORMAL_OPERATION',
                                                                                                                                        'value': 0x0},
                                                                                                                                       {'description': 'Three-Wire '
                                                                                                                                                       'Mode',
                                                                                                                                        'name': 'THREE_WIRE_MODE',
                                                                                                                                        'value': 0x1},
                                                                                                                                       {'description': 'Two-Wire '
                                                                                                                                                       'Mode',
                                                                                                                                        'name': 'TWO_WIRE_MODE',
                                                                                                                                        'value': 0x2},
                                                                                                                                       {'description': 'Two-Wire '
                                                                                                                                                       'Mode '
                                                                                                                                                       'Held '
                                                                                                                                                       'Low',
                                                                                                                                        'name': 'TWO_WIRE_MODE_HELD_LOW',
                                                                                                                                        'value': 0x3}]},
                                                                                              'name': 'USIWM',
                                                                                              'writeConstraint': {'useEnumeratedValues': 0x1}},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[6:6]',
                                                                                              'description': 'Counter '
                                                                                                             'Overflow '
                                                                                                             'Interrupt '
                                                                                                             'Enable',
                                                                                              'name': 'USIOIE'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[7:7]',
                                                                                              'description': 'Start '
                                                                                                             'Condition '
                                                                                                             'Interrupt '
                                                                                                             'Enable',
                                                                                              'name': 'USISIE'}]},
                                                                        'name': 'USICR',
                                                                        'size': 0x8},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x2,
                                                                        'description': 'USI '
                                                                                       'Data '
                                                                                       'Register',
                                                                        'name': 'USIDR',
                                                                        'size': 0x8,
                                                                        'writeConstraint': {'range': {'maximum': 0xFF,
                                                                                                      'minimum': 0x0}}},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x1,
                                                                        'description': 'USI '
                                                                                       'Status '
                                                                                       'Register '
                                                                                       '(read-only '
                                                                                       'for '
                                                                                       'debugger)',
                                                                        'fields': {'field': [{'access': 'read-write',
                                                                                              'bitRange': '[3:0]',
                                                                                              'description': 'USI '
                                                                                                             'Counter '
                                                                                                             'Value '
                                                                                                             'Bits',
                                                                                              'name': 'USICNT',
                                                                                              'writeConstraint': {'range': {'maximum': 0xF,
                                                                                                                            'minimum': 0x0}}},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[4:4]',
                                                                                              'description': 'Data '
                                                                                                             'Output '
                                                                                                             'Collision',
                                                                                              'name': 'USIDC'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[5:5]',
                                                                                              'description': 'Stop '
                                                                                                             'Condition '
                                                                                                             'Flag',
                                                                                              'name': 'USIPF'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[6:6]',
                                                                                              'description': 'Counter '
                                                                                                             'Overflow '
                                                                                                             'Interrupt '
                                                                                                             'Flag',
                                                                                              'name': 'USIOIF'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[7:7]',
                                                                                              'description': 'Start '
                                                                                                             'Condition '
                                                                                                             'Interrupt '
                                                                                                             'Flag',
                                                                                              'name': 'USISIF'}]},
                                                                        'name': 'USISR',
                                                                        'size': 0x8}]}},
                                           {'addressBlock': [{'offset': 0x0,
                                                              'size': 0x1,
                                                              'usage': 'registers'}],
                                            'baseAddress': 0x800041,
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
                                                                        'name': 'WDTCR',
                                                                        'size': 0x8}]}}]},
            'resetMask': 0xFF,
            'resetValue': 0x0,
            'size': 0x8,
            'version': '1.0',
            'width': 0x8}}
}