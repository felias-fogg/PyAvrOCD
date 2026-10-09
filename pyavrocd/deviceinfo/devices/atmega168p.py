# Device description for atmega168p, generated from Microchip's ATmega168P.atdf by
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
    'name': 'atmega168p',
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
    'flash_size_bytes': 0x4000,
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
    'internal_sram_size_bytes': 0x0400,
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
    'bootrst_base' : 0x02,
    'bootrst_mask' : 0x01,
    'eesave_base' : 0x01,
    'eesave_mask' : 0x08,
    'tcnt0_base' : 0x46,
    'cs0_base' : 0x45,
    'toie0_base' : 0x6E,
    'toie0_mask' : 0x01,
    'masked_registers' : [0x4e, 0x51, 0x82, 0xc6],
    'ronly_registers' : [0x23, 0x26, 0x29, 0x35, 0x36, 0x37, 0x3b, 0x3c, 0x4d, 0x50, 0x60, 0x61, 0x64, 0x66, 0x7a, 0xbc, 0xc0],
    'device_id': 0x1E940B,
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
            'name': 'ATmega168P',
            'peripherals': {'peripheral': [{'addressBlock': [{'offset': 0x0,
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
                                                                        'addressOffset': 0x2F,
                                                                        'description': 'Digital '
                                                                                       'Input '
                                                                                       'Disable '
                                                                                       'Register '
                                                                                       '1',
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
                                                                        'addressOffset': 0x3,
                                                                        'description': 'The '
                                                                                       'ADC '
                                                                                       'Control '
                                                                                       'and '
                                                                                       'Status '
                                                                                       'register '
                                                                                       'B',
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
                                                                                              'bitRange': '[6:6]',
                                                                                              'description': 'No '
                                                                                                             'Description.',
                                                                                              'name': 'ACME'}]},
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
                                                                                                             'Selection '
                                                                                                             'Bits',
                                                                                              'enumeratedValues': {'enumeratedValue': [{'description': 'ADC '
                                                                                                                                                       'Single '
                                                                                                                                                       'Ended '
                                                                                                                                                       'Input '
                                                                                                                                                       'pin '
                                                                                                                                                       '0',
                                                                                                                                        'name': 'ADC0',
                                                                                                                                        'value': 0x0},
                                                                                                                                       {'description': 'ADC '
                                                                                                                                                       'Single '
                                                                                                                                                       'Ended '
                                                                                                                                                       'Input '
                                                                                                                                                       'pin '
                                                                                                                                                       '1',
                                                                                                                                        'name': 'ADC1',
                                                                                                                                        'value': 0x1},
                                                                                                                                       {'description': 'ADC '
                                                                                                                                                       'Single '
                                                                                                                                                       'Ended '
                                                                                                                                                       'Input '
                                                                                                                                                       'pin '
                                                                                                                                                       '2',
                                                                                                                                        'name': 'ADC2',
                                                                                                                                        'value': 0x2},
                                                                                                                                       {'description': 'ADC '
                                                                                                                                                       'Single '
                                                                                                                                                       'Ended '
                                                                                                                                                       'Input '
                                                                                                                                                       'pin '
                                                                                                                                                       '3',
                                                                                                                                        'name': 'ADC3',
                                                                                                                                        'value': 0x3},
                                                                                                                                       {'description': 'ADC '
                                                                                                                                                       'Single '
                                                                                                                                                       'Ended '
                                                                                                                                                       'Input '
                                                                                                                                                       'pin '
                                                                                                                                                       '4',
                                                                                                                                        'name': 'ADC4',
                                                                                                                                        'value': 0x4},
                                                                                                                                       {'description': 'ADC '
                                                                                                                                                       'Single '
                                                                                                                                                       'Ended '
                                                                                                                                                       'Input '
                                                                                                                                                       'pin '
                                                                                                                                                       '5',
                                                                                                                                        'name': 'ADC5',
                                                                                                                                        'value': 0x5},
                                                                                                                                       {'description': 'ADC '
                                                                                                                                                       'Single '
                                                                                                                                                       'Ended '
                                                                                                                                                       'Input '
                                                                                                                                                       'pin '
                                                                                                                                                       '6',
                                                                                                                                        'name': 'ADC6',
                                                                                                                                        'value': 0x6},
                                                                                                                                       {'description': 'ADC '
                                                                                                                                                       'Single '
                                                                                                                                                       'Ended '
                                                                                                                                                       'Input '
                                                                                                                                                       'pin '
                                                                                                                                                       '7',
                                                                                                                                        'name': 'ADC7',
                                                                                                                                        'value': 0x7},
                                                                                                                                       {'description': 'Temperature '
                                                                                                                                                       'sensor',
                                                                                                                                        'name': 'TEMPSENS',
                                                                                                                                        'value': 0x8},
                                                                                                                                       {'description': 'Internal '
                                                                                                                                                       'Reference '
                                                                                                                                                       '(VBG)',
                                                                                                                                        'name': 'ADC_VBG',
                                                                                                                                        'value': 0xE},
                                                                                                                                       {'description': '0V '
                                                                                                                                                       '(GND)',
                                                                                                                                        'name': 'ADC_GND',
                                                                                                                                        'value': 0xF}]},
                                                                                              'name': 'MUX',
                                                                                              'writeConstraint': {'useEnumeratedValues': 0x1}},
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
                                                                                                                                                       '1.1V '
                                                                                                                                                       'Voltage '
                                                                                                                                                       'Reference '
                                                                                                                                                       'with '
                                                                                                                                                       'external '
                                                                                                                                                       'capacitor '
                                                                                                                                                       'at '
                                                                                                                                                       'AREF '
                                                                                                                                                       'pin',
                                                                                                                                        'name': 'INTERNAL_1_1V_VOLTAGE_REFERENCE_WITH_EXTERNAL_CAPACITOR_AT_AREF_PIN',
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
                                                                                       'Register',
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
                                                                                              'name': 'ADC5D'}]},
                                                                        'name': 'DIDR0',
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
                                                             {'offset': 0x19,
                                                              'size': 0x1,
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
                                                                          '0',
                                                           'name': 'PCINT1',
                                                           'value': 0x4},
                                                          {'description': 'Pin '
                                                                          'Change '
                                                                          'Interrupt '
                                                                          'Request '
                                                                          '1',
                                                           'name': 'PCINT2',
                                                           'value': 0x5},
                                                          {'description': 'Watchdog '
                                                                          'Time-out '
                                                                          'Interrupt',
                                                           'name': 'WDT',
                                                           'value': 0x6},
                                                          {'description': 'Timer/Counter2 '
                                                                          'Compare '
                                                                          'Match '
                                                                          'A',
                                                           'name': 'TIMER2_COMPA',
                                                           'value': 0x7},
                                                          {'description': 'Timer/Counter2 '
                                                                          'Compare '
                                                                          'Match '
                                                                          'A',
                                                           'name': 'TIMER2_COMPB',
                                                           'value': 0x8},
                                                          {'description': 'Timer/Counter2 '
                                                                          'Overflow',
                                                           'name': 'TIMER2_OVF',
                                                           'value': 0x9},
                                                          {'description': 'Timer/Counter1 '
                                                                          'Capture '
                                                                          'Event',
                                                           'name': 'TIMER1_CAPT',
                                                           'value': 0xA},
                                                          {'description': 'Timer/Counter1 '
                                                                          'Compare '
                                                                          'Match '
                                                                          'A',
                                                           'name': 'TIMER1_COMPA',
                                                           'value': 0xB},
                                                          {'description': 'Timer/Counter1 '
                                                                          'Compare '
                                                                          'Match '
                                                                          'B',
                                                           'name': 'TIMER1_COMPB',
                                                           'value': 0xC},
                                                          {'description': 'Timer/Counter1 '
                                                                          'Overflow',
                                                           'name': 'TIMER1_OVF',
                                                           'value': 0xD},
                                                          {'description': 'TimerCounter0 '
                                                                          'Compare '
                                                                          'Match '
                                                                          'A',
                                                           'name': 'TIMER0_COMPA',
                                                           'value': 0xE},
                                                          {'description': 'TimerCounter0 '
                                                                          'Compare '
                                                                          'Match '
                                                                          'B',
                                                           'name': 'TIMER0_COMPB',
                                                           'value': 0xF},
                                                          {'description': 'Timer/Counter0 '
                                                                          'Overflow',
                                                           'name': 'TIMER0_OVF',
                                                           'value': 0x10},
                                                          {'description': 'SPI '
                                                                          'Serial '
                                                                          'Transfer '
                                                                          'Complete',
                                                           'name': 'SPI_STC',
                                                           'value': 0x11},
                                                          {'description': 'USART '
                                                                          'Rx '
                                                                          'Complete',
                                                           'name': 'USART_RX',
                                                           'value': 0x12},
                                                          {'description': 'USART, '
                                                                          'Data '
                                                                          'Register '
                                                                          'Empty',
                                                           'name': 'USART_UDRE',
                                                           'value': 0x13},
                                                          {'description': 'USART '
                                                                          'Tx '
                                                                          'Complete',
                                                           'name': 'USART_TX',
                                                           'value': 0x14},
                                                          {'description': 'ADC '
                                                                          'Conversion '
                                                                          'Complete',
                                                           'name': 'ADC',
                                                           'value': 0x15},
                                                          {'description': 'EEPROM '
                                                                          'Ready',
                                                           'name': 'EE_READY',
                                                           'value': 0x16},
                                                          {'description': 'Analog '
                                                                          'Comparator',
                                                           'name': 'ANALOG_COMP',
                                                           'value': 0x17},
                                                          {'description': 'Two-wire '
                                                                          'Serial '
                                                                          'Interface',
                                                           'name': 'TWI',
                                                           'value': 0x18},
                                                          {'description': 'Store '
                                                                          'Program '
                                                                          'Memory '
                                                                          'Read',
                                                           'name': 'SPM_Ready',
                                                           'value': 0x19}],
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
                                                                        'addressOffset': 0x0,
                                                                        'description': 'General '
                                                                                       'Purpose '
                                                                                       'I/O '
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
                                                                                       'I/O '
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
                                                                                       'I/O '
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
                                                                                              'name': 'WDRF'}]},
                                                                        'name': 'MCUSR',
                                                                        'size': 0x8},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x28,
                                                                        'description': 'Oscillator '
                                                                                       'Calibration '
                                                                                       'Value '
                                                                                       '(read-only '
                                                                                       'for '
                                                                                       'debugger)',
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
                                                                                       'Register '
                                                                                       '(read-only '
                                                                                       'for '
                                                                                       'debugger)',
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
                                                                                                             'USART',
                                                                                              'name': 'PRUSART0'},
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
                                                                        'name': 'PRR',
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
                                                                        'addressOffset': 0x19,
                                                                        'description': 'Store '
                                                                                       'Program '
                                                                                       'Memory '
                                                                                       'Control '
                                                                                       'and '
                                                                                       'Status '
                                                                                       'Register',
                                                                        'fields': {'field': [{'access': 'read-write',
                                                                                              'bitRange': '[0:0]',
                                                                                              'description': 'Self '
                                                                                                             'Programming '
                                                                                                             'Enable',
                                                                                              'name': 'SELFPRGEN'},
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
                                                                                              'description': 'Read-While-Write '
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
                                                                        'size': 0x8},
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
                                                              'size': 0x3,
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
                                                                                              'bitRange': '[2:0]',
                                                                                              'description': 'Pin '
                                                                                                             'Change '
                                                                                                             'Interrupt '
                                                                                                             'Enables',
                                                                                              'name': 'PCIE',
                                                                                              'writeConstraint': {'range': {'maximum': 0x7,
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
                                                                                              'bitRange': '[2:0]',
                                                                                              'description': 'Pin '
                                                                                                             'Change '
                                                                                                             'Interrupt '
                                                                                                             'Flags',
                                                                                              'name': 'PCIF',
                                                                                              'writeConstraint': {'range': {'maximum': 0x7,
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
                                                                                              'bitRange': '[6:0]',
                                                                                              'description': 'Pin '
                                                                                                             'Change '
                                                                                                             'Enable '
                                                                                                             'Masks',
                                                                                              'name': 'PCINT',
                                                                                              'writeConstraint': {'range': {'maximum': 0x7F,
                                                                                                                            'minimum': 0x0}}}]},
                                                                        'name': 'PCMSK1',
                                                                        'size': 0x8},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x32,
                                                                        'description': 'Pin '
                                                                                       'Change '
                                                                                       'Mask '
                                                                                       'Register '
                                                                                       '2',
                                                                        'fields': {'field': [{'access': 'read-write',
                                                                                              'bitRange': '[7:0]',
                                                                                              'description': 'Pin '
                                                                                                             'Change '
                                                                                                             'Enable '
                                                                                                             'Masks',
                                                                                              'name': 'PCINT',
                                                                                              'writeConstraint': {'range': {'maximum': 0xFF,
                                                                                                                            'minimum': 0x0}}}]},
                                                                        'name': 'PCMSK2',
                                                                        'size': 0x8}]}},
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
                                                                                              'name': 'PB5'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[6:6]',
                                                                                              'description': 'Pin '
                                                                                                             'B6',
                                                                                              'name': 'PB6'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[7:7]',
                                                                                              'description': 'Pin '
                                                                                                             'B7',
                                                                                              'name': 'PB7'}]},
                                                                        'name': 'DDRB',
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
                                                                                              'name': 'PB5'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[6:6]',
                                                                                              'description': 'Pin '
                                                                                                             'B6',
                                                                                              'name': 'PB6'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[7:7]',
                                                                                              'description': 'Pin '
                                                                                                             'B7',
                                                                                              'name': 'PB7'}]},
                                                                        'name': 'PINB',
                                                                        'size': 0x8},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x2,
                                                                        'description': 'Port '
                                                                                       'B '
                                                                                       'Data '
                                                                                       'Register',
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
                                                                                              'name': 'PB5'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[6:6]',
                                                                                              'description': 'Pin '
                                                                                                             'B6',
                                                                                              'name': 'PB6'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[7:7]',
                                                                                              'description': 'Pin '
                                                                                                             'B7',
                                                                                              'name': 'PB7'}]},
                                                                        'name': 'PORTB',
                                                                        'size': 0x8}]}},
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
                                                                        'fields': {'field': [{'access': 'read-write',
                                                                                              'bitRange': '[0:0]',
                                                                                              'description': 'Pin '
                                                                                                             'C0',
                                                                                              'name': 'PC0'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[1:1]',
                                                                                              'description': 'Pin '
                                                                                                             'C1',
                                                                                              'name': 'PC1'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[2:2]',
                                                                                              'description': 'Pin '
                                                                                                             'C2',
                                                                                              'name': 'PC2'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[3:3]',
                                                                                              'description': 'Pin '
                                                                                                             'C3',
                                                                                              'name': 'PC3'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[4:4]',
                                                                                              'description': 'Pin '
                                                                                                             'C4',
                                                                                              'name': 'PC4'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[5:5]',
                                                                                              'description': 'Pin '
                                                                                                             'C5',
                                                                                              'name': 'PC5'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[6:6]',
                                                                                              'description': 'Pin '
                                                                                                             'C6',
                                                                                              'name': 'PC6'}]},
                                                                        'name': 'DDRC',
                                                                        'size': 0x8},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x0,
                                                                        'description': 'Port '
                                                                                       'C '
                                                                                       'Input '
                                                                                       'Pins '
                                                                                       '(read-only '
                                                                                       'for '
                                                                                       'debugger)',
                                                                        'fields': {'field': [{'access': 'read-write',
                                                                                              'bitRange': '[0:0]',
                                                                                              'description': 'Pin '
                                                                                                             'C0',
                                                                                              'name': 'PC0'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[1:1]',
                                                                                              'description': 'Pin '
                                                                                                             'C1',
                                                                                              'name': 'PC1'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[2:2]',
                                                                                              'description': 'Pin '
                                                                                                             'C2',
                                                                                              'name': 'PC2'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[3:3]',
                                                                                              'description': 'Pin '
                                                                                                             'C3',
                                                                                              'name': 'PC3'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[4:4]',
                                                                                              'description': 'Pin '
                                                                                                             'C4',
                                                                                              'name': 'PC4'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[5:5]',
                                                                                              'description': 'Pin '
                                                                                                             'C5',
                                                                                              'name': 'PC5'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[6:6]',
                                                                                              'description': 'Pin '
                                                                                                             'C6',
                                                                                              'name': 'PC6'}]},
                                                                        'name': 'PINC',
                                                                        'size': 0x8},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x2,
                                                                        'description': 'Port '
                                                                                       'C '
                                                                                       'Data '
                                                                                       'Register',
                                                                        'fields': {'field': [{'access': 'read-write',
                                                                                              'bitRange': '[0:0]',
                                                                                              'description': 'Pin '
                                                                                                             'C0',
                                                                                              'name': 'PC0'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[1:1]',
                                                                                              'description': 'Pin '
                                                                                                             'C1',
                                                                                              'name': 'PC1'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[2:2]',
                                                                                              'description': 'Pin '
                                                                                                             'C2',
                                                                                              'name': 'PC2'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[3:3]',
                                                                                              'description': 'Pin '
                                                                                                             'C3',
                                                                                              'name': 'PC3'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[4:4]',
                                                                                              'description': 'Pin '
                                                                                                             'C4',
                                                                                              'name': 'PC4'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[5:5]',
                                                                                              'description': 'Pin '
                                                                                                             'C5',
                                                                                              'name': 'PC5'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[6:6]',
                                                                                              'description': 'Pin '
                                                                                                             'C6',
                                                                                              'name': 'PC6'}]},
                                                                        'name': 'PORTC',
                                                                        'size': 0x8}]}},
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
                                                                        'fields': {'field': [{'access': 'read-write',
                                                                                              'bitRange': '[0:0]',
                                                                                              'description': 'Pin '
                                                                                                             'D0',
                                                                                              'name': 'PD0'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[1:1]',
                                                                                              'description': 'Pin '
                                                                                                             'D1',
                                                                                              'name': 'PD1'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[2:2]',
                                                                                              'description': 'Pin '
                                                                                                             'D2',
                                                                                              'name': 'PD2'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[3:3]',
                                                                                              'description': 'Pin '
                                                                                                             'D3',
                                                                                              'name': 'PD3'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[4:4]',
                                                                                              'description': 'Pin '
                                                                                                             'D4',
                                                                                              'name': 'PD4'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[5:5]',
                                                                                              'description': 'Pin '
                                                                                                             'D5',
                                                                                              'name': 'PD5'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[6:6]',
                                                                                              'description': 'Pin '
                                                                                                             'D6',
                                                                                              'name': 'PD6'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[7:7]',
                                                                                              'description': 'Pin '
                                                                                                             'D7',
                                                                                              'name': 'PD7'}]},
                                                                        'name': 'DDRD',
                                                                        'size': 0x8},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x0,
                                                                        'description': 'Port '
                                                                                       'D '
                                                                                       'Input '
                                                                                       'Pins '
                                                                                       '(read-only '
                                                                                       'for '
                                                                                       'debugger)',
                                                                        'fields': {'field': [{'access': 'read-write',
                                                                                              'bitRange': '[0:0]',
                                                                                              'description': 'Pin '
                                                                                                             'D0',
                                                                                              'name': 'PD0'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[1:1]',
                                                                                              'description': 'Pin '
                                                                                                             'D1',
                                                                                              'name': 'PD1'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[2:2]',
                                                                                              'description': 'Pin '
                                                                                                             'D2',
                                                                                              'name': 'PD2'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[3:3]',
                                                                                              'description': 'Pin '
                                                                                                             'D3',
                                                                                              'name': 'PD3'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[4:4]',
                                                                                              'description': 'Pin '
                                                                                                             'D4',
                                                                                              'name': 'PD4'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[5:5]',
                                                                                              'description': 'Pin '
                                                                                                             'D5',
                                                                                              'name': 'PD5'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[6:6]',
                                                                                              'description': 'Pin '
                                                                                                             'D6',
                                                                                              'name': 'PD6'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[7:7]',
                                                                                              'description': 'Pin '
                                                                                                             'D7',
                                                                                              'name': 'PD7'}]},
                                                                        'name': 'PIND',
                                                                        'size': 0x8},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x2,
                                                                        'description': 'Port '
                                                                                       'D '
                                                                                       'Data '
                                                                                       'Register',
                                                                        'fields': {'field': [{'access': 'read-write',
                                                                                              'bitRange': '[0:0]',
                                                                                              'description': 'Pin '
                                                                                                             'D0',
                                                                                              'name': 'PD0'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[1:1]',
                                                                                              'description': 'Pin '
                                                                                                             'D1',
                                                                                              'name': 'PD1'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[2:2]',
                                                                                              'description': 'Pin '
                                                                                                             'D2',
                                                                                              'name': 'PD2'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[3:3]',
                                                                                              'description': 'Pin '
                                                                                                             'D3',
                                                                                              'name': 'PD3'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[4:4]',
                                                                                              'description': 'Pin '
                                                                                                             'D4',
                                                                                              'name': 'PD4'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[5:5]',
                                                                                              'description': 'Pin '
                                                                                                             'D5',
                                                                                              'name': 'PD5'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[6:6]',
                                                                                              'description': 'Pin '
                                                                                                             'D6',
                                                                                              'name': 'PD6'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[7:7]',
                                                                                              'description': 'Pin '
                                                                                                             'D7',
                                                                                              'name': 'PD7'}]},
                                                                        'name': 'PORTD',
                                                                        'size': 0x8}]}},
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
                                                             {'offset': 0xD,
                                                              'size': 0x1,
                                                              'usage': 'registers'},
                                                             {'offset': 0x39,
                                                              'size': 0x1,
                                                              'usage': 'registers'},
                                                             {'offset': 0x4A,
                                                              'size': 0x3,
                                                              'usage': 'registers'},
                                                             {'offset': 0x4E,
                                                              'size': 0x8,
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
                                                                                       'Register  '
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
                                                                                       'Register  '
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
                                                                                              'description': 'Waveform '
                                                                                                             'Generation '
                                                                                                             'Mode',
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
                                                                        'description': 'Timer/Counter1 '
                                                                                       'Control '
                                                                                       'Register '
                                                                                       'C '
                                                                                       '(write-only '
                                                                                       'for '
                                                                                       'debugger)',
                                                                        'fields': {'field': [{'access': 'read-write',
                                                                                              'bitRange': '[6:6]',
                                                                                              'description': 'No '
                                                                                                             'Description.',
                                                                                              'name': 'FOC1B'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[7:7]',
                                                                                              'description': 'No '
                                                                                                             'Description.',
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
                                                                                                             'CompareA '
                                                                                                             'Match '
                                                                                                             'Interrupt '
                                                                                                             'Enable',
                                                                                              'name': 'OCIE1A'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[2:2]',
                                                                                              'description': 'Timer/Counter1 '
                                                                                                             'Output '
                                                                                                             'CompareB '
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
                                            'baseAddress': 0x8000C0,
                                            'description': 'USART',
                                            'name': 'USART0',
                                            'registers': {'register': [{'access': 'read-write',
                                                                        'addressOffset': 0x4,
                                                                        'description': 'USART '
                                                                                       'Baud '
                                                                                       'Rate '
                                                                                       'Register  '
                                                                                       'Bytes',
                                                                        'name': 'UBRR0',
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
                                                                                              'name': 'MPCM0'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[1:1]',
                                                                                              'description': 'Double '
                                                                                                             'the '
                                                                                                             'USART '
                                                                                                             'transmission '
                                                                                                             'speed',
                                                                                              'name': 'U2X0'},
                                                                                             {'access': 'read-only',
                                                                                              'bitRange': '[2:2]',
                                                                                              'description': 'Parity '
                                                                                                             'Error',
                                                                                              'name': 'UPE0'},
                                                                                             {'access': 'read-only',
                                                                                              'bitRange': '[3:3]',
                                                                                              'description': 'Data '
                                                                                                             'overRun',
                                                                                              'name': 'DOR0'},
                                                                                             {'access': 'read-only',
                                                                                              'bitRange': '[4:4]',
                                                                                              'description': 'Framing '
                                                                                                             'Error',
                                                                                              'name': 'FE0'},
                                                                                             {'access': 'read-only',
                                                                                              'bitRange': '[5:5]',
                                                                                              'description': 'USART '
                                                                                                             'Data '
                                                                                                             'Register '
                                                                                                             'Empty',
                                                                                              'name': 'UDRE0'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[6:6]',
                                                                                              'description': 'USART '
                                                                                                             'Transmit '
                                                                                                             'Complete',
                                                                                              'name': 'TXC0'},
                                                                                             {'access': 'read-only',
                                                                                              'bitRange': '[7:7]',
                                                                                              'description': 'USART '
                                                                                                             'Receive '
                                                                                                             'Complete',
                                                                                              'name': 'RXC0'}]},
                                                                        'name': 'UCSR0A',
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
                                                                                              'name': 'TXB80'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[1:1]',
                                                                                              'description': 'Receive '
                                                                                                             'Data '
                                                                                                             'Bit '
                                                                                                             '8',
                                                                                              'name': 'RXB80'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[2:2]',
                                                                                              'description': 'Character '
                                                                                                             'Size '
                                                                                                             '- '
                                                                                                             'together '
                                                                                                             'with '
                                                                                                             'UCSZ0 '
                                                                                                             'in '
                                                                                                             'UCSRnC',
                                                                                              'name': 'UCSZ02'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[3:3]',
                                                                                              'description': 'Transmitter '
                                                                                                             'Enable',
                                                                                              'name': 'TXEN0'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[4:4]',
                                                                                              'description': 'Receiver '
                                                                                                             'Enable',
                                                                                              'name': 'RXEN0'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[5:5]',
                                                                                              'description': 'USART '
                                                                                                             'Data '
                                                                                                             'register '
                                                                                                             'Empty '
                                                                                                             'Interrupt '
                                                                                                             'Enable',
                                                                                              'name': 'UDRIE0'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[6:6]',
                                                                                              'description': 'TX '
                                                                                                             'Complete '
                                                                                                             'Interrupt '
                                                                                                             'Enable',
                                                                                              'name': 'TXCIE0'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[7:7]',
                                                                                              'description': 'RX '
                                                                                                             'Complete '
                                                                                                             'Interrupt '
                                                                                                             'Enable',
                                                                                              'name': 'RXCIE0'}]},
                                                                        'name': 'UCSR0B',
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
                                                                                              'name': 'UCPOL0'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[2:1]',
                                                                                              'description': 'Character '
                                                                                                             'Size '
                                                                                                             '- '
                                                                                                             'together '
                                                                                                             'with '
                                                                                                             'UCSZ2 '
                                                                                                             'in '
                                                                                                             'UCSRnB',
                                                                                              'name': 'UCSZ0',
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
                                                                                              'name': 'USBS0',
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
                                                                                              'name': 'UPM0',
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
                                                                                              'name': 'UMSEL0',
                                                                                              'writeConstraint': {'useEnumeratedValues': 0x1}}]},
                                                                        'name': 'UCSR0C',
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
                                                                        'name': 'UDR0',
                                                                        'size': 0x8,
                                                                        'writeConstraint': {'range': {'maximum': 0xFF,
                                                                                                      'minimum': 0x0}}}]}},
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