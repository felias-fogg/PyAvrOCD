# Device description for attiny87, generated from Microchip's ATtiny87.atdf by
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
    'name': 'attiny87',
    'architecture': 'avr8',

    # eeprom
    'eeprom_address_byte': 0x0000,
    'eeprom_size_bytes': 0x0200,
    'eeprom_page_size_bytes': 0x04,
    'eeprom_read_size_bytes': 0x01,
    'eeprom_write_size_bytes': 0x01,
    'eeprom_chiperase_effect': ChiperaseEffect.CONDITIONALLY_ERASED_AVR,
    'eeprom_isolated_erase': False,

    # flash
    'flash_address_byte': 0x0000,
    'flash_size_bytes': 0x2000,
    'flash_page_size_bytes': 0x80,
    'flash_read_size_bytes': 0x02,
    'flash_write_size_bytes': 0x80,
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
    'internal_sram_size_bytes': 0x0200,
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
    'dwen_mask' : 0x40,
    'eesave_base' : 0x01,
    'eesave_mask' : 0x08,
    'tcnt0_base' : 0x47,
    'cs0_base' : 0x46,
    'toie0_base' : 0x6E,
    'toie0_mask' : 0x01,
    'masked_registers' : [0x4e, 0x51, 0xd2],
    'ronly_registers' : [0x20, 0x23, 0x35, 0x36, 0x3b, 0x3c, 0x4d, 0x50, 0x60, 0x61, 0x66, 0x7a, 0xb9, 0xbb, 0xcb],
    'device_id': 0x1E9387,
    'interface': 'ISP+HVPP+debugWIRE',

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
            'name': 'ATtiny87',
            'peripherals': {'peripheral': [{'addressBlock': [{'offset': 0x0,
                                                              'size': 0x1,
                                                              'usage': 'registers'},
                                                             {'offset': 0x2B,
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
                                                                                                             'Internal '
                                                                                                             'Reference '
                                                                                                             'Select',
                                                                                              'name': 'ACIRS'},
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
                                                                        'description': 'Analog '
                                                                                       'Comparator '
                                                                                       '& '
                                                                                       'ADC '
                                                                                       'Control '
                                                                                       'and '
                                                                                       'Status '
                                                                                       'Register '
                                                                                       'B '
                                                                                       '(Shared '
                                                                                       'with '
                                                                                       'AD_CONVERTER '
                                                                                       'IO_MODULE)',
                                                                        'fields': {'field': [{'access': 'read-write',
                                                                                              'bitRange': '[5:4]',
                                                                                              'description': 'Analog '
                                                                                                             'Comparator '
                                                                                                             'Internal '
                                                                                                             'Voltage '
                                                                                                             'Reference '
                                                                                                             'Select '
                                                                                                             'Bits',
                                                                                              'name': 'ACIR',
                                                                                              'writeConstraint': {'range': {'maximum': 0x3,
                                                                                                                            'minimum': 0x0}}},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[6:6]',
                                                                                              'description': 'Analog '
                                                                                                             'Comparator '
                                                                                                             'Multiplexer '
                                                                                                             'Enable',
                                                                                              'name': 'ACME'}]},
                                                                        'name': 'ADCSRB',
                                                                        'size': 0x8}]}},
                                           {'addressBlock': [{'offset': 0x0,
                                                              'size': 0x6,
                                                              'usage': 'registers'},
                                                             {'offset': 0x7,
                                                              'size': 0x2,
                                                              'usage': 'registers'}],
                                            'baseAddress': 0x800077,
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
                                                                                       'register '
                                                                                       'A '
                                                                                       '(read-only '
                                                                                       'for '
                                                                                       'debugger)',
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
                                                                                              'description': 'ADC  '
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
                                                                        'addressOffset': 0x4,
                                                                        'description': 'The '
                                                                                       'ADC '
                                                                                       'Control '
                                                                                       'and '
                                                                                       'Status '
                                                                                       'register '
                                                                                       'B '
                                                                                       '(Shared '
                                                                                       'with '
                                                                                       'ANALOG_COMPARATOR '
                                                                                       'IO_MODULE)',
                                                                        'fields': {'field': [{'access': 'read-write',
                                                                                              'bitRange': '[2:0]',
                                                                                              'description': 'ADC '
                                                                                                             'Auto '
                                                                                                             'Trigger '
                                                                                                             'Source '
                                                                                                             'bits',
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
                                                                                                                                       {'description': 'Timer/Counter1 '
                                                                                                                                                       'Compare '
                                                                                                                                                       'Match '
                                                                                                                                                       'A',
                                                                                                                                        'name': 'TIMER_COUNTER1_COMPARE_MATCH_A',
                                                                                                                                        'value': 0x3},
                                                                                                                                       {'description': 'Timer/Counter1 '
                                                                                                                                                       'Overflow',
                                                                                                                                        'name': 'TIMER_COUNTER1_OVERFLOW',
                                                                                                                                        'value': 0x4},
                                                                                                                                       {'description': 'Timer/Counter1 '
                                                                                                                                                       'Compare '
                                                                                                                                                       'Match '
                                                                                                                                                       'B',
                                                                                                                                        'name': 'TIMER_COUNTER1_COMPARE_MATCH_B',
                                                                                                                                        'value': 0x5},
                                                                                                                                       {'description': 'Timer/Counter1 '
                                                                                                                                                       'Capture '
                                                                                                                                                       'Event',
                                                                                                                                        'name': 'TIMER_COUNTER1_CAPTURE_EVENT',
                                                                                                                                        'value': 0x6},
                                                                                                                                       {'description': 'Watchdog '
                                                                                                                                                       'Interrupt '
                                                                                                                                                       'Request',
                                                                                                                                        'name': 'WATCHDOG_INTERRUPT_REQUEST',
                                                                                                                                        'value': 0x7}]},
                                                                                              'name': 'ADTS',
                                                                                              'writeConstraint': {'useEnumeratedValues': 0x1}},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[7:7]',
                                                                                              'description': 'Bipolar '
                                                                                                             'Input '
                                                                                                             'Mode',
                                                                                              'name': 'BIN'}]},
                                                                        'name': 'ADCSRB',
                                                                        'size': 0x8},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x5,
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
                                                                                              'enumeratedValues': {'enumeratedValue': [{'description': 'If '
                                                                                                                                                       'AREFEN==0 '
                                                                                                                                                       'then '
                                                                                                                                                       'Internal '
                                                                                                                                                       '1.1V '
                                                                                                                                                       'as '
                                                                                                                                                       'Voltage '
                                                                                                                                                       'Reference '
                                                                                                                                                       'without '
                                                                                                                                                       'external '
                                                                                                                                                       'capacitor. '
                                                                                                                                                       'If '
                                                                                                                                                       'AREFEN==1 '
                                                                                                                                                       'then '
                                                                                                                                                       'Internal '
                                                                                                                                                       '1.1V '
                                                                                                                                                       'as '
                                                                                                                                                       'Voltage '
                                                                                                                                                       'Reference '
                                                                                                                                                       'with '
                                                                                                                                                       'external '
                                                                                                                                                       'capacitor '
                                                                                                                                                       'at '
                                                                                                                                                       'AREF '
                                                                                                                                                       'pin.',
                                                                                                                                        'name': 'IF_AREFEN_0_THEN_INTERNAL_1_1V_AS_VOLTAGE_REFERENCE_WITHOUT_EXTERNAL_CAPACITOR_IF_AREFEN_1_THEN_INTERNAL_1_1V_AS_VOLTAGE_REFERENCE_WITH_EXTERNAL_CAPACITOR_AT_AREF_PIN',
                                                                                                                                        'value': 0x1},
                                                                                                                                       {'description': 'If '
                                                                                                                                                       'AREFEN==0 '
                                                                                                                                                       'then '
                                                                                                                                                       'Internal '
                                                                                                                                                       'AVCC '
                                                                                                                                                       'as '
                                                                                                                                                       'Voltage '
                                                                                                                                                       'Reference. '
                                                                                                                                                       'If '
                                                                                                                                                       'AREFEN==1 '
                                                                                                                                                       'then '
                                                                                                                                                       'AREF '
                                                                                                                                                       'pin '
                                                                                                                                                       'as '
                                                                                                                                                       'Voltage '
                                                                                                                                                       'Reference.  ',
                                                                                                                                        'name': 'IF_AREFEN_0_THEN_INTERNAL_AVCC_AS_VOLTAGE_REFERENCE_IF_AREFEN_1_THEN_AREF_PIN_AS_VOLTAGE_REFERENCE',
                                                                                                                                        'value': 0x2},
                                                                                                                                       {'description': 'If '
                                                                                                                                                       'AREFEN==0 '
                                                                                                                                                       'then '
                                                                                                                                                       'Internal '
                                                                                                                                                       '2.56V '
                                                                                                                                                       'as '
                                                                                                                                                       'Voltage '
                                                                                                                                                       'Reference '
                                                                                                                                                       'without '
                                                                                                                                                       'external '
                                                                                                                                                       'capacitor. '
                                                                                                                                                       'If '
                                                                                                                                                       'AREFEN==1 '
                                                                                                                                                       'then '
                                                                                                                                                       'Internal '
                                                                                                                                                       '2.56V '
                                                                                                                                                       'as '
                                                                                                                                                       'Voltage '
                                                                                                                                                       'Reference '
                                                                                                                                                       'with '
                                                                                                                                                       'external '
                                                                                                                                                       'capacitor '
                                                                                                                                                       'at '
                                                                                                                                                       'AREF '
                                                                                                                                                       'pin.',
                                                                                                                                        'name': 'IF_AREFEN_0_THEN_INTERNAL_2_56V_AS_VOLTAGE_REFERENCE_WITHOUT_EXTERNAL_CAPACITOR_IF_AREFEN_1_THEN_INTERNAL_2_56V_AS_VOLTAGE_REFERENCE_WITH_EXTERNAL_CAPACITOR_AT_AREF_PIN',
                                                                                                                                        'value': 0x3}]},
                                                                                              'name': 'REFS',
                                                                                              'writeConstraint': {'useEnumeratedValues': 0x1}}]},
                                                                        'name': 'ADMUX',
                                                                        'size': 0x8},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x0,
                                                                        'description': 'Analog '
                                                                                       'Miscellaneous '
                                                                                       'Control '
                                                                                       'Register '
                                                                                       '(Shared '
                                                                                       'with '
                                                                                       'CURRENT_SOURCE '
                                                                                       'IO_MODULE)',
                                                                        'fields': {'field': [{'access': 'read-write',
                                                                                              'bitRange': '[1:1]',
                                                                                              'description': 'Internal '
                                                                                                             'Voltage '
                                                                                                             'Reference '
                                                                                                             'Output '
                                                                                                             'Enable',
                                                                                              'name': 'XREFEN'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[2:2]',
                                                                                              'description': 'External '
                                                                                                             'Voltage '
                                                                                                             'Reference '
                                                                                                             'Input '
                                                                                                             'Enable',
                                                                                              'name': 'AREFEN'}]},
                                                                        'name': 'AMISCR',
                                                                        'size': 0x8},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x7,
                                                                        'description': 'Digital '
                                                                                       'Input '
                                                                                       'Disable '
                                                                                       'Register '
                                                                                       '0',
                                                                        'fields': {'field': [{'access': 'read-write',
                                                                                              'bitRange': '[0:0]',
                                                                                              'description': 'No '
                                                                                                             'Description.',
                                                                                              'name': 'ADC0D'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[1:1]',
                                                                                              'description': 'No '
                                                                                                             'Description.',
                                                                                              'name': 'ADC1D'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[2:2]',
                                                                                              'description': 'No '
                                                                                                             'Description.',
                                                                                              'name': 'ADC2D'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[3:3]',
                                                                                              'description': 'No '
                                                                                                             'Description.',
                                                                                              'name': 'ADC3D'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[4:4]',
                                                                                              'description': 'No '
                                                                                                             'Description.',
                                                                                              'name': 'ADC4D'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[5:5]',
                                                                                              'description': 'No '
                                                                                                             'Description.',
                                                                                              'name': 'ADC5D'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[6:6]',
                                                                                              'description': 'No '
                                                                                                             'Description.',
                                                                                              'name': 'ADC6D'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[7:7]',
                                                                                              'description': 'No '
                                                                                                             'Description.',
                                                                                              'name': 'ADC7D'}]},
                                                                        'name': 'DIDR0',
                                                                        'size': 0x8},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x8,
                                                                        'description': 'Digital '
                                                                                       'Input '
                                                                                       'Disable '
                                                                                       'Register '
                                                                                       '1',
                                                                        'fields': {'field': [{'access': 'read-write',
                                                                                              'bitRange': '[4:4]',
                                                                                              'description': 'No '
                                                                                                             'Description.',
                                                                                              'name': 'ADC8D'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[5:5]',
                                                                                              'description': 'No '
                                                                                                             'Description.',
                                                                                              'name': 'ADC9D'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[6:6]',
                                                                                              'description': 'No '
                                                                                                             'Description.',
                                                                                              'name': 'ADC10D'}]},
                                                                        'name': 'DIDR1',
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
                                                                                              'description': 'Read '
                                                                                                             'Fuse '
                                                                                                             'and '
                                                                                                             'Lock '
                                                                                                             'Bits',
                                                                                              'name': 'RFLB'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[4:4]',
                                                                                              'description': 'Clear '
                                                                                                             'Temporary '
                                                                                                             'Page '
                                                                                                             'Buffer',
                                                                                              'name': 'CTPB'},
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
                                                                                              'name': 'RWWSB'}]},
                                                                        'name': 'SPMCSR',
                                                                        'size': 0x8}]}},
                                           {'addressBlock': [{'offset': 0x0,
                                                              'size': 0x1,
                                                              'usage': 'registers'},
                                                             {'offset': 0xC,
                                                              'size': 0x1,
                                                              'usage': 'registers'},
                                                             {'offset': 0x18,
                                                              'size': 0x2,
                                                              'usage': 'registers'},
                                                             {'offset': 0x1F,
                                                              'size': 0x1,
                                                              'usage': 'registers'},
                                                             {'offset': 0x21,
                                                              'size': 0x3,
                                                              'usage': 'registers'},
                                                             {'offset': 0x2B,
                                                              'size': 0x3,
                                                              'usage': 'registers'},
                                                             {'offset': 0x2F,
                                                              'size': 0x4,
                                                              'usage': 'registers'},
                                                             {'offset': 0x34,
                                                              'size': 0x1,
                                                              'usage': 'registers'}],
                                            'baseAddress': 0x800032,
                                            'description': 'CPU Registers',
                                            'interrupt': [{'description': 'External '
                                                                          'Reset, '
                                                                          'Power-on '
                                                                          'Reset '
                                                                          'and '
                                                                          'Watchdog '
                                                                          'Reset',
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
                                                          {'description': 'Pin '
                                                                          'Change '
                                                                          'Interrupt '
                                                                          'Request '
                                                                          '0',
                                                           'name': 'PCINT0',
                                                           'value': 0x3},
                                                          {'description': 'Pin '
                                                                          'Change '
                                                                          'Interrupt '
                                                                          'Request '
                                                                          '1',
                                                           'name': 'PCINT1',
                                                           'value': 0x4},
                                                          {'description': 'Watchdog '
                                                                          'Time-Out '
                                                                          'Interrupt',
                                                           'name': 'WDT',
                                                           'value': 0x5},
                                                          {'description': 'Timer/Counter1 '
                                                                          'Capture '
                                                                          'Event',
                                                           'name': 'TIMER1_CAPT',
                                                           'value': 0x6},
                                                          {'description': 'Timer/Counter1 '
                                                                          'Compare '
                                                                          'Match '
                                                                          '1A',
                                                           'name': 'TIMER1_COMPA',
                                                           'value': 0x7},
                                                          {'description': 'Timer/Counter1 '
                                                                          'Compare '
                                                                          'Match '
                                                                          '1B',
                                                           'name': 'TIMER1_COMPB',
                                                           'value': 0x8},
                                                          {'description': 'Timer/Counter1 '
                                                                          'Overflow',
                                                           'name': 'TIMER1_OVF',
                                                           'value': 0x9},
                                                          {'description': 'Timer/Counter0 '
                                                                          'Compare '
                                                                          'Match '
                                                                          '0A',
                                                           'name': 'TIMER0_COMPA',
                                                           'value': 0xA},
                                                          {'description': 'Timer/Counter0 '
                                                                          'Overflow',
                                                           'name': 'TIMER0_OVF',
                                                           'value': 0xB},
                                                          {'description': 'LIN '
                                                                          'Transfer '
                                                                          'Complete',
                                                           'name': 'LIN_TC',
                                                           'value': 0xC},
                                                          {'description': 'LIN '
                                                                          'Error',
                                                           'name': 'LIN_ERR',
                                                           'value': 0xD},
                                                          {'description': 'SPI '
                                                                          'Serial '
                                                                          'Transfer '
                                                                          'Complete',
                                                           'name': 'SPI_STC',
                                                           'value': 0xE},
                                                          {'description': 'ADC '
                                                                          'Conversion '
                                                                          'Complete',
                                                           'name': 'ADC',
                                                           'value': 0xF},
                                                          {'description': 'EEPROM '
                                                                          'Ready',
                                                           'name': 'EE_RDY',
                                                           'value': 0x10},
                                                          {'description': 'Analog '
                                                                          'Comparator',
                                                           'name': 'ANA_COMP',
                                                           'value': 0x11},
                                                          {'description': 'USI '
                                                                          'Start '
                                                                          'Condition '
                                                                          'Detection',
                                                           'name': 'USI_START',
                                                           'value': 0x12},
                                                          {'description': 'USI '
                                                                          'Counter '
                                                                          'Overflow',
                                                           'name': 'USI_OVF',
                                                           'value': 0x13}],
                                            'name': 'CPU',
                                            'registers': {'register': [{'access': 'read-write',
                                                                        'addressOffset': 0x30,
                                                                        'description': 'Clock '
                                                                                       'Control '
                                                                                       '& '
                                                                                       'Status '
                                                                                       'Register',
                                                                        'fields': {'field': [{'access': 'read-write',
                                                                                              'bitRange': '[3:0]',
                                                                                              'description': 'Clock '
                                                                                                             'Control '
                                                                                                             'bits',
                                                                                              'enumeratedValues': {'enumeratedValue': [{'description': 'No '
                                                                                                                                                       'Command',
                                                                                                                                        'name': 'NO_COMMAND',
                                                                                                                                        'value': 0x0},
                                                                                                                                       {'description': 'Disable '
                                                                                                                                                       'Clock '
                                                                                                                                                       'Source',
                                                                                                                                        'name': 'DISABLE_CLOCK_SOURCE',
                                                                                                                                        'value': 0x1},
                                                                                                                                       {'description': 'Enable '
                                                                                                                                                       'Clock '
                                                                                                                                                       'Source',
                                                                                                                                        'name': 'ENABLE_CLOCK_SOURCE',
                                                                                                                                        'value': 0x2},
                                                                                                                                       {'description': 'Request '
                                                                                                                                                       'for '
                                                                                                                                                       'Clock '
                                                                                                                                                       'Availability',
                                                                                                                                        'name': 'REQUEST_FOR_CLOCK_AVAILABILITY',
                                                                                                                                        'value': 0x3},
                                                                                                                                       {'description': 'Clock '
                                                                                                                                                       'Source '
                                                                                                                                                       'Switch',
                                                                                                                                        'name': 'CLOCK_SOURCE_SWITCH',
                                                                                                                                        'value': 0x4},
                                                                                                                                       {'description': 'Recovery '
                                                                                                                                                       'System '
                                                                                                                                                       'Clock '
                                                                                                                                                       'Source '
                                                                                                                                                       'Code',
                                                                                                                                        'name': 'RECOVERY_SYSTEM_CLOCK_SOURCE_CODE',
                                                                                                                                        'value': 0x5},
                                                                                                                                       {'description': 'Enable '
                                                                                                                                                       'Watchdog '
                                                                                                                                                       'in '
                                                                                                                                                       'Automatic '
                                                                                                                                                       'Reload '
                                                                                                                                                       'Mode',
                                                                                                                                        'name': 'ENABLE_WATCHDOG_IN_AUTOMATIC_RELOAD_MODE',
                                                                                                                                        'value': 0x6},
                                                                                                                                       {'description': 'CKOUT '
                                                                                                                                                       'Command',
                                                                                                                                        'name': 'CKOUT_COMMAND',
                                                                                                                                        'value': 0x7},
                                                                                                                                       {'description': 'From '
                                                                                                                                                       '0x08 '
                                                                                                                                                       'up '
                                                                                                                                                       'to '
                                                                                                                                                       '0x0F: '
                                                                                                                                                       'No '
                                                                                                                                                       'command',
                                                                                                                                        'name': 'FROM_0X08_UP_TO_0X0F_NO_COMMAND',
                                                                                                                                        'value': 0x8}]},
                                                                                              'name': 'CLKC',
                                                                                              'writeConstraint': {'useEnumeratedValues': 0x1}},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[4:4]',
                                                                                              'description': 'Clock '
                                                                                                             'Ready '
                                                                                                             'Flag',
                                                                                              'name': 'CLKRDY'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[7:7]',
                                                                                              'description': 'Clock '
                                                                                                             'Control '
                                                                                                             'Change '
                                                                                                             'Enable',
                                                                                              'name': 'CLKCCE'}]},
                                                                        'name': 'CLKCSR',
                                                                        'size': 0x8},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x2F,
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
                                                                        'addressOffset': 0x31,
                                                                        'description': 'Clock '
                                                                                       'Selection '
                                                                                       'Register',
                                                                        'fields': {'field': [{'access': 'read-write',
                                                                                              'bitRange': '[3:0]',
                                                                                              'description': 'Clock '
                                                                                                             'Source '
                                                                                                             'Select '
                                                                                                             'bit '
                                                                                                             '3 '
                                                                                                             '- '
                                                                                                             'CKSEL3 '
                                                                                                             'fuse '
                                                                                                             'substitution',
                                                                                              'name': 'CSEL',
                                                                                              'writeConstraint': {'range': {'maximum': 0xF,
                                                                                                                            'minimum': 0x0}}},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[5:4]',
                                                                                              'description': 'Clock '
                                                                                                             'Start-up '
                                                                                                             'Time '
                                                                                                             'bit '
                                                                                                             '1 '
                                                                                                             '- '
                                                                                                             'SUT1 '
                                                                                                             'fuse '
                                                                                                             'substitution',
                                                                                              'name': 'CSUT',
                                                                                              'writeConstraint': {'range': {'maximum': 0x3,
                                                                                                                            'minimum': 0x0}}},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[6:6]',
                                                                                              'description': 'Clock '
                                                                                                             'Out '
                                                                                                             '- '
                                                                                                             'CKOUT '
                                                                                                             'fuse '
                                                                                                             'substitution',
                                                                                              'name': 'COUT'}]},
                                                                        'name': 'CLKSELR',
                                                                        'size': 0x8},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x1F,
                                                                        'description': 'DebugWire '
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
                                                                        'addressOffset': 0xC,
                                                                        'description': 'General '
                                                                                       'purpose '
                                                                                       'register '
                                                                                       '0',
                                                                        'name': 'GPIOR0',
                                                                        'size': 0x8,
                                                                        'writeConstraint': {'range': {'maximum': 0xFF,
                                                                                                      'minimum': 0x0}}},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x18,
                                                                        'description': 'General '
                                                                                       'Purpose '
                                                                                       'register '
                                                                                       '1',
                                                                        'name': 'GPIOR1',
                                                                        'size': 0x8,
                                                                        'writeConstraint': {'range': {'maximum': 0xFF,
                                                                                                      'minimum': 0x0}}},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x19,
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
                                                                        'addressOffset': 0x23,
                                                                        'description': 'MCU '
                                                                                       'Control '
                                                                                       'Register',
                                                                        'fields': {'field': [{'access': 'read-write',
                                                                                              'bitRange': '[4:4]',
                                                                                              'description': 'Pull-up '
                                                                                                             'Disable',
                                                                                              'name': 'PUD'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[5:5]',
                                                                                              'description': 'BOD '
                                                                                                             'Sleep '
                                                                                                             'Enable',
                                                                                              'name': 'BODSE'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[6:6]',
                                                                                              'description': 'BOD '
                                                                                                             'Sleep',
                                                                                              'name': 'BODS'}]},
                                                                        'name': 'MCUCR',
                                                                        'size': 0x8},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x22,
                                                                        'description': 'MCU '
                                                                                       'Status '
                                                                                       'register',
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
                                                                        'addressOffset': 0x34,
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
                                                                        'addressOffset': 0x0,
                                                                        'description': 'Port '
                                                                                       'Control '
                                                                                       'Register',
                                                                        'fields': {'field': [{'access': 'read-write',
                                                                                              'bitRange': '[0:0]',
                                                                                              'description': 'No '
                                                                                                             'Description.',
                                                                                              'name': 'PUDA'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[1:1]',
                                                                                              'description': 'No '
                                                                                                             'Description.',
                                                                                              'name': 'PUDB'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[4:4]',
                                                                                              'description': 'No '
                                                                                                             'Description.',
                                                                                              'name': 'BBMA'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[5:5]',
                                                                                              'description': 'No '
                                                                                                             'Description.',
                                                                                              'name': 'BBMB'}]},
                                                                        'name': 'PORTCR',
                                                                        'size': 0x8},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x32,
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
                                                                                              'name': 'PRTIM1'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[4:4]',
                                                                                              'description': 'Power '
                                                                                                             'Reduction '
                                                                                                             'SPI',
                                                                                              'name': 'PRSPI'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[5:5]',
                                                                                              'description': 'Power '
                                                                                                             'Reduction '
                                                                                                             'LINUART',
                                                                                              'name': 'PRLIN'}]},
                                                                        'name': 'PRR',
                                                                        'size': 0x8},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x21,
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
                                                                                              'bitRange': '[2:1]',
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
                                                                                              'writeConstraint': {'useEnumeratedValues': 0x1}}]},
                                                                        'name': 'SMCR',
                                                                        'size': 0x8},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x2B,
                                                                        'description': 'Stack '
                                                                                       'Pointer  '
                                                                                       'Bytes',
                                                                        'name': 'SP',
                                                                        'size': 0x10,
                                                                        'writeConstraint': {'range': {'maximum': 0xFFFF,
                                                                                                      'minimum': 0x0}}},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x2D,
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
                                                              'size': 0x1,
                                                              'usage': 'registers'}],
                                            'baseAddress': 0x800077,
                                            'description': 'Current Source',
                                            'name': 'CURRENT_SOURCE',
                                            'registers': {'register': [{'access': 'read-write',
                                                                        'addressOffset': 0x0,
                                                                        'description': 'Analog '
                                                                                       'Miscellaneous '
                                                                                       'Control '
                                                                                       'Register '
                                                                                       '(Shared '
                                                                                       'with '
                                                                                       'AD_CONVERTER '
                                                                                       'IO_MODULE)',
                                                                        'fields': {'field': [{'access': 'read-write',
                                                                                              'bitRange': '[0:0]',
                                                                                              'description': 'Current '
                                                                                                             'Source '
                                                                                                             'Enable',
                                                                                              'name': 'ISRCEN'}]},
                                                                        'name': 'AMISCR',
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
                                                                                              'name': 'ISC1',
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
                                                                                              'bitRange': '[1:0]',
                                                                                              'description': 'External '
                                                                                                             'Interrupt '
                                                                                                             'Flags',
                                                                                              'name': 'INTF',
                                                                                              'writeConstraint': {'range': {'maximum': 0x3,
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
                                                                                              'bitRange': '[1:0]',
                                                                                              'description': 'External '
                                                                                                             'Interrupt '
                                                                                                             'Request '
                                                                                                             '1 '
                                                                                                             'Enable',
                                                                                              'name': 'INT',
                                                                                              'writeConstraint': {'range': {'maximum': 0x3,
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
                                                                                                             'Enable  '
                                                                                                             'on '
                                                                                                             'any '
                                                                                                             'PCINT14..8 '
                                                                                                             'pin',
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
                                                                                       'Mask '
                                                                                       'Register '
                                                                                       '0',
                                                                        'fields': {'field': [{'access': 'read-write',
                                                                                              'bitRange': '[7:0]',
                                                                                              'description': 'Pin '
                                                                                                             'Change '
                                                                                                             'Enable '
                                                                                                             'Masks',
                                                                                              'name': 'PCINT',
                                                                                              'writeConstraint': {'range': {'maximum': 0xFF,
                                                                                                                            'minimum': 0x0}}}]},
                                                                        'name': 'PCMSK0',
                                                                        'size': 0x8},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x31,
                                                                        'description': 'Pin '
                                                                                       'Change '
                                                                                       'Mask '
                                                                                       'Register '
                                                                                       '1',
                                                                        'fields': {'field': [{'access': 'read-write',
                                                                                              'bitRange': '[7:0]',
                                                                                              'description': 'Pin '
                                                                                                             'Change '
                                                                                                             'Enable '
                                                                                                             'Masks',
                                                                                              'name': 'PCINT',
                                                                                              'writeConstraint': {'range': {'maximum': 0xFF,
                                                                                                                            'minimum': 0x0}}}]},
                                                                        'name': 'PCMSK1',
                                                                        'size': 0x8}]}},
                                           {'addressBlock': [{'offset': 0x0,
                                                              'size': 0xB,
                                                              'usage': 'registers'}],
                                            'baseAddress': 0x8000C8,
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
                                                              'size': 0x1,
                                                              'usage': 'registers'},
                                                             {'offset': 0x10,
                                                              'size': 0x4,
                                                              'usage': 'registers'},
                                                             {'offset': 0x39,
                                                              'size': 0x1,
                                                              'usage': 'registers'},
                                                             {'offset': 0x81,
                                                              'size': 0x1,
                                                              'usage': 'registers'}],
                                            'baseAddress': 0x800035,
                                            'description': 'Timer/Counter, '
                                                           '8-bit Async',
                                            'name': 'TC0',
                                            'registers': {'register': [{'access': 'read-write',
                                                                        'addressOffset': 0x81,
                                                                        'description': 'Asynchronous '
                                                                                       'Status '
                                                                                       'Register',
                                                                        'fields': {'field': [{'access': 'read-write',
                                                                                              'bitRange': '[0:0]',
                                                                                              'description': 'Timer/Counter0 '
                                                                                                             'Control '
                                                                                                             'Register '
                                                                                                             'B '
                                                                                                             'Update '
                                                                                                             'Busy',
                                                                                              'name': 'TCR0BUB'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[1:1]',
                                                                                              'description': 'Timer/Counter0 '
                                                                                                             'Control '
                                                                                                             'Register '
                                                                                                             'A '
                                                                                                             'Update '
                                                                                                             'Busy',
                                                                                              'name': 'TCR0AUB'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[3:3]',
                                                                                              'description': 'Output '
                                                                                                             'Compare '
                                                                                                             'Register '
                                                                                                             '0A  '
                                                                                                             'Update '
                                                                                                             'Busy',
                                                                                              'name': 'OCR0AUB'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[4:4]',
                                                                                              'description': 'Timer/Counter0 '
                                                                                                             'Update '
                                                                                                             'Busy',
                                                                                              'name': 'TCN0UB'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[5:5]',
                                                                                              'description': 'Asynchronous '
                                                                                                             'Timer/Counter0',
                                                                                              'name': 'AS0'},
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
                                                                        'addressOffset': 0xE,
                                                                        'description': 'General '
                                                                                       'Timer '
                                                                                       'Counter '
                                                                                       'Control '
                                                                                       'register',
                                                                        'fields': {'field': [{'access': 'read-write',
                                                                                              'bitRange': '[0:0]',
                                                                                              'description': 'Prescaler '
                                                                                                             'Reset '
                                                                                                             'Synchronous '
                                                                                                             '16-bit '
                                                                                                             'Timer/Counter1',
                                                                                              'name': 'PSR1'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[1:1]',
                                                                                              'description': 'Prescaler '
                                                                                                             'Reset '
                                                                                                             'Asynchronous '
                                                                                                             '8-bit '
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
                                                                        'addressOffset': 0x13,
                                                                        'description': 'Timer/Counter0 '
                                                                                       'Output '
                                                                                       'Compare '
                                                                                       'Register '
                                                                                       'A',
                                                                        'name': 'OCR0A',
                                                                        'size': 0x8,
                                                                        'writeConstraint': {'range': {'maximum': 0xFF,
                                                                                                      'minimum': 0x0}}},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x10,
                                                                        'description': 'Timer/Counter0 '
                                                                                       'Control '
                                                                                       'Register '
                                                                                       'A',
                                                                        'fields': {'field': [{'access': 'read-write',
                                                                                              'bitRange': '[1:0]',
                                                                                              'description': 'Waveform '
                                                                                                             'Generation '
                                                                                                             'Mode '
                                                                                                             'bits',
                                                                                              'name': 'WGM0',
                                                                                              'writeConstraint': {'range': {'maximum': 0x3,
                                                                                                                            'minimum': 0x0}}},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[7:6]',
                                                                                              'description': 'Compare '
                                                                                                             'Output '
                                                                                                             'Mode '
                                                                                                             'bits',
                                                                                              'name': 'COM0A',
                                                                                              'writeConstraint': {'range': {'maximum': 0x3,
                                                                                                                            'minimum': 0x0}}}]},
                                                                        'name': 'TCCR0A',
                                                                        'size': 0x8},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x11,
                                                                        'description': 'Timer/Counter0 '
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
                                                                                              'name': 'CS0',
                                                                                              'writeConstraint': {'useEnumeratedValues': 0x1}},
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
                                                                        'addressOffset': 0x12,
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
                                                                                       'Register '
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
                                                                                              'description': 'Output '
                                                                                                             'Compare '
                                                                                                             'Flag '
                                                                                                             '0A',
                                                                                              'name': 'OCF0A'}]},
                                                                        'name': 'TIFR0',
                                                                        'size': 0x8},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x39,
                                                                        'description': 'Timer/Counter0 '
                                                                                       'Interrupt '
                                                                                       'Mask '
                                                                                       'register',
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
                                                                                              'name': 'OCIE0A'}]},
                                                                        'name': 'TIMSK0',
                                                                        'size': 0x8}]}},
                                           {'addressBlock': [{'offset': 0x0,
                                                              'size': 0x1,
                                                              'usage': 'registers'},
                                                             {'offset': 0x39,
                                                              'size': 0x1,
                                                              'usage': 'registers'},
                                                             {'offset': 0x4A,
                                                              'size': 0xC,
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
                                                                        'addressOffset': 0x4A,
                                                                        'description': 'Timer/Counter1 '
                                                                                       'Control '
                                                                                       'Register '
                                                                                       'A',
                                                                        'fields': {'field': [{'access': 'read-write',
                                                                                              'bitRange': '[1:0]',
                                                                                              'description': 'Pulse '
                                                                                                             'Width '
                                                                                                             'Modulator '
                                                                                                             'Select '
                                                                                                             'Bits',
                                                                                              'name': 'WGM1',
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
                                                                                              'description': 'Timer/Counter1 '
                                                                                                             'Clock '
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
                                                                                                             'Mode '
                                                                                                             'Bits',
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
                                                                        'description': 'Timer/Counter1 '
                                                                                       'Control '
                                                                                       'Register '
                                                                                       'C',
                                                                        'fields': {'field': [{'access': 'read-write',
                                                                                              'bitRange': '[6:6]',
                                                                                              'description': 'Timer/Counter1 '
                                                                                                             'Force '
                                                                                                             'Output '
                                                                                                             'Compare '
                                                                                                             'for '
                                                                                                             'Channel '
                                                                                                             'B',
                                                                                              'name': 'FOC1B'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[7:7]',
                                                                                              'description': 'Timer/Counter1 '
                                                                                                             'Force '
                                                                                                             'Output '
                                                                                                             'Compare '
                                                                                                             'for '
                                                                                                             'Channel '
                                                                                                             'A',
                                                                                              'name': 'FOC1A'}]},
                                                                        'name': 'TCCR1C',
                                                                        'size': 0x8},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x4D,
                                                                        'description': 'Timer/Counter1 '
                                                                                       'Control '
                                                                                       'Register '
                                                                                       'D',
                                                                        'fields': {'field': [{'access': 'read-write',
                                                                                              'bitRange': '[0:0]',
                                                                                              'description': 'Timer/Counter1 '
                                                                                                             'Output '
                                                                                                             'Compare '
                                                                                                             'U-pin '
                                                                                                             'Enable '
                                                                                                             'for '
                                                                                                             'Channel '
                                                                                                             'A',
                                                                                              'name': 'OC1AU'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[1:1]',
                                                                                              'description': 'Timer/Counter1 '
                                                                                                             'Output '
                                                                                                             'Compare '
                                                                                                             'V-pin '
                                                                                                             'Enable '
                                                                                                             'for '
                                                                                                             'Channel '
                                                                                                             'A',
                                                                                              'name': 'OC1AV'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[2:2]',
                                                                                              'description': 'Timer/Counter1 '
                                                                                                             'Output '
                                                                                                             'Compare '
                                                                                                             'W-pin '
                                                                                                             'Enable '
                                                                                                             'for '
                                                                                                             'Channel '
                                                                                                             'A',
                                                                                              'name': 'OC1AW'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[3:3]',
                                                                                              'description': 'Timer/Counter1 '
                                                                                                             'Output '
                                                                                                             'Compare '
                                                                                                             'X-pin '
                                                                                                             'Enable '
                                                                                                             'for '
                                                                                                             'Channel '
                                                                                                             'A',
                                                                                              'name': 'OC1AX'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[4:4]',
                                                                                              'description': 'Timer/Counter1 '
                                                                                                             'Output '
                                                                                                             'Compare '
                                                                                                             'U-pin '
                                                                                                             'Enable '
                                                                                                             'for '
                                                                                                             'Channel '
                                                                                                             'B',
                                                                                              'name': 'OC1BU'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[5:5]',
                                                                                              'description': 'Timer/Counter1 '
                                                                                                             'Output '
                                                                                                             'Compare '
                                                                                                             'V-pin '
                                                                                                             'Enable '
                                                                                                             'for '
                                                                                                             'Channel '
                                                                                                             'B',
                                                                                              'name': 'OC1BV'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[6:6]',
                                                                                              'description': 'Timer/Counter1 '
                                                                                                             'Output '
                                                                                                             'Compare '
                                                                                                             'W-pin '
                                                                                                             'Enable '
                                                                                                             'for '
                                                                                                             'Channel '
                                                                                                             'B',
                                                                                              'name': 'OC1BW'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[7:7]',
                                                                                              'description': 'Timer/Counter1 '
                                                                                                             'Output '
                                                                                                             'Compare '
                                                                                                             'X-pin '
                                                                                                             'Enable '
                                                                                                             'for '
                                                                                                             'Channel '
                                                                                                             'B',
                                                                                              'name': 'OC1BX'}]},
                                                                        'name': 'TCCR1D',
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
                                                                                              'description': 'Timer/Counter1 '
                                                                                                             'Output '
                                                                                                             'Compare '
                                                                                                             'A '
                                                                                                             'Match '
                                                                                                             'Flag',
                                                                                              'name': 'OCF1A'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[2:2]',
                                                                                              'description': 'Timer/Counter1 '
                                                                                                             'Output '
                                                                                                             'Compare '
                                                                                                             'B '
                                                                                                             'Match '
                                                                                                             'Flag',
                                                                                              'name': 'OCF1B'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[5:5]',
                                                                                              'description': 'Timer/Counter1 '
                                                                                                             'Input '
                                                                                                             'Capture '
                                                                                                             'Flag',
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
                                                              'size': 0x5,
                                                              'usage': 'registers'}],
                                            'baseAddress': 0x8000B8,
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
                                                                        'addressOffset': 0x4,
                                                                        'description': 'USI '
                                                                                       'Pin '
                                                                                       'Position',
                                                                        'name': 'USIPP',
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
                                                                        'name': 'WDTCR',
                                                                        'size': 0x8}]}}]},
            'resetMask': 0xFF,
            'resetValue': 0x0,
            'size': 0x8,
            'version': '1.0',
            'width': 0x8}}
}