# Device description for atmega16m1, generated from Microchip's ATmega16M1.atdf by
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
    'name': 'atmega16m1',
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
    'bootrst_base' : 0x01,
    'bootrst_mask' : 0x01,
    'eesave_base' : 0x01,
    'eesave_mask' : 0x08,
    'tcnt0_base' : 0x46,
    'cs0_base' : 0x45,
    'toie0_base' : 0x6E,
    'toie0_mask' : 0x01,
    'masked_registers' : [0x4e, 0x51, 0x82, 0xd2],
    'ronly_registers' : [0x23, 0x26, 0x29, 0x2c, 0x35, 0x36, 0x3c, 0x4d, 0x50, 0x60, 0x61, 0x66, 0x7a, 0xcb, 0xd9, 0xdc, 0xe0],
    'device_id': 0x1E9484,
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
            'name': 'ATmega16M1',
            'peripherals': {'peripheral': [{'addressBlock': [{'offset': 0x0,
                                                              'size': 0x1,
                                                              'usage': 'registers'},
                                                             {'offset': 0x44,
                                                              'size': 0x4,
                                                              'usage': 'registers'}],
                                            'baseAddress': 0x800050,
                                            'description': 'Analog Comparator',
                                            'name': 'AC',
                                            'registers': {'register': [{'access': 'read-write',
                                                                        'addressOffset': 0x44,
                                                                        'description': 'Analog '
                                                                                       'Comparator '
                                                                                       '0 '
                                                                                       'Control '
                                                                                       'Register',
                                                                        'fields': {'field': [{'access': 'read-write',
                                                                                              'bitRange': '[2:0]',
                                                                                              'description': 'Analog '
                                                                                                             'Comparator '
                                                                                                             '0 '
                                                                                                             'Multiplexer '
                                                                                                             'Register',
                                                                                              'name': 'AC0M',
                                                                                              'writeConstraint': {'range': {'maximum': 0x7,
                                                                                                                            'minimum': 0x0}}},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[3:3]',
                                                                                              'description': 'Analog '
                                                                                                             'Comparator '
                                                                                                             'Clock '
                                                                                                             'Select',
                                                                                              'name': 'ACCKSEL'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[5:4]',
                                                                                              'description': 'Analog '
                                                                                                             'Comparator '
                                                                                                             '0  '
                                                                                                             'Interrupt '
                                                                                                             'Select '
                                                                                                             'Bits',
                                                                                              'name': 'AC0IS',
                                                                                              'writeConstraint': {'range': {'maximum': 0x3,
                                                                                                                            'minimum': 0x0}}},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[6:6]',
                                                                                              'description': 'Analog '
                                                                                                             'Comparator '
                                                                                                             '0 '
                                                                                                             'Interrupt '
                                                                                                             'Enable '
                                                                                                             'Bit',
                                                                                              'name': 'AC0IE'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[7:7]',
                                                                                              'description': 'Analog '
                                                                                                             'Comparator '
                                                                                                             '0 '
                                                                                                             'Enable '
                                                                                                             'Bit',
                                                                                              'name': 'AC0EN'}]},
                                                                        'name': 'AC0CON',
                                                                        'size': 0x8},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x45,
                                                                        'description': 'Analog '
                                                                                       'Comparator '
                                                                                       '1 '
                                                                                       'Control '
                                                                                       'Register',
                                                                        'fields': {'field': [{'access': 'read-write',
                                                                                              'bitRange': '[2:0]',
                                                                                              'description': 'Analog '
                                                                                                             'Comparator '
                                                                                                             '1 '
                                                                                                             'Multiplexer '
                                                                                                             'Register',
                                                                                              'name': 'AC1M',
                                                                                              'writeConstraint': {'range': {'maximum': 0x7,
                                                                                                                            'minimum': 0x0}}},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[3:3]',
                                                                                              'description': 'Analog '
                                                                                                             'Comparator '
                                                                                                             '1 '
                                                                                                             'Interrupt '
                                                                                                             'Capture '
                                                                                                             'Enable '
                                                                                                             'Bit',
                                                                                              'name': 'AC1ICE'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[5:4]',
                                                                                              'description': 'Analog '
                                                                                                             'Comparator '
                                                                                                             '1  '
                                                                                                             'Interrupt '
                                                                                                             'Select '
                                                                                                             'Bit',
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
                                                                                              'name': 'AC1IS',
                                                                                              'writeConstraint': {'useEnumeratedValues': 0x1}},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[6:6]',
                                                                                              'description': 'Analog '
                                                                                                             'Comparator '
                                                                                                             '1 '
                                                                                                             'Interrupt '
                                                                                                             'Enable '
                                                                                                             'Bit',
                                                                                              'name': 'AC1IE'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[7:7]',
                                                                                              'description': 'Analog '
                                                                                                             'Comparator '
                                                                                                             '1 '
                                                                                                             'Enable '
                                                                                                             'Bit',
                                                                                              'name': 'AC1EN'}]},
                                                                        'name': 'AC1CON',
                                                                        'size': 0x8},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x46,
                                                                        'description': 'Analog '
                                                                                       'Comparator '
                                                                                       '2 '
                                                                                       'Control '
                                                                                       'Register',
                                                                        'fields': {'field': [{'access': 'read-write',
                                                                                              'bitRange': '[2:0]',
                                                                                              'description': 'Analog '
                                                                                                             'Comparator '
                                                                                                             '2 '
                                                                                                             'Multiplexer '
                                                                                                             'Register',
                                                                                              'name': 'AC2M',
                                                                                              'writeConstraint': {'range': {'maximum': 0x7,
                                                                                                                            'minimum': 0x0}}},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[5:4]',
                                                                                              'description': 'Analog '
                                                                                                             'Comparator '
                                                                                                             '2  '
                                                                                                             'Interrupt '
                                                                                                             'Select '
                                                                                                             'Bit',
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
                                                                                              'name': 'AC2IS',
                                                                                              'writeConstraint': {'useEnumeratedValues': 0x1}},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[6:6]',
                                                                                              'description': 'Analog '
                                                                                                             'Comparator '
                                                                                                             '2 '
                                                                                                             'Interrupt '
                                                                                                             'Enable '
                                                                                                             'Bit',
                                                                                              'name': 'AC2IE'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[7:7]',
                                                                                              'description': 'Analog '
                                                                                                             'Comparator '
                                                                                                             '2 '
                                                                                                             'Enable '
                                                                                                             'Bit',
                                                                                              'name': 'AC2EN'}]},
                                                                        'name': 'AC2CON',
                                                                        'size': 0x8},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x47,
                                                                        'description': 'Analog '
                                                                                       'Comparator '
                                                                                       '3 '
                                                                                       'Control '
                                                                                       'Register',
                                                                        'fields': {'field': [{'access': 'read-write',
                                                                                              'bitRange': '[2:0]',
                                                                                              'description': 'Analog '
                                                                                                             'Comparator '
                                                                                                             '3 '
                                                                                                             'Multiplexer '
                                                                                                             'Register',
                                                                                              'name': 'AC3M',
                                                                                              'writeConstraint': {'range': {'maximum': 0x7,
                                                                                                                            'minimum': 0x0}}},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[5:4]',
                                                                                              'description': 'Analog '
                                                                                                             'Comparator '
                                                                                                             '3  '
                                                                                                             'Interrupt '
                                                                                                             'Select '
                                                                                                             'Bit',
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
                                                                                              'name': 'AC3IS',
                                                                                              'writeConstraint': {'useEnumeratedValues': 0x1}},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[6:6]',
                                                                                              'description': 'Analog '
                                                                                                             'Comparator '
                                                                                                             '3 '
                                                                                                             'Interrupt '
                                                                                                             'Enable '
                                                                                                             'Bit',
                                                                                              'name': 'AC3IE'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[7:7]',
                                                                                              'description': 'Analog '
                                                                                                             'Comparator '
                                                                                                             '3 '
                                                                                                             'Enable '
                                                                                                             'Bit',
                                                                                              'name': 'AC3EN'}]},
                                                                        'name': 'AC3CON',
                                                                        'size': 0x8},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x0,
                                                                        'description': 'Analog '
                                                                                       'Comparator '
                                                                                       'Status '
                                                                                       'Register '
                                                                                       '(read-only '
                                                                                       'for '
                                                                                       'debugger)',
                                                                        'fields': {'field': [{'access': 'read-write',
                                                                                              'bitRange': '[0:0]',
                                                                                              'description': 'Analog '
                                                                                                             'Comparator '
                                                                                                             '0 '
                                                                                                             'Output '
                                                                                                             'Bit',
                                                                                              'name': 'AC0O'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[1:1]',
                                                                                              'description': 'Analog '
                                                                                                             'Comparator '
                                                                                                             '1 '
                                                                                                             'Output '
                                                                                                             'Bit',
                                                                                              'name': 'AC1O'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[2:2]',
                                                                                              'description': 'Analog '
                                                                                                             'Comparator '
                                                                                                             '2 '
                                                                                                             'Output '
                                                                                                             'Bit',
                                                                                              'name': 'AC2O'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[3:3]',
                                                                                              'description': 'Analog '
                                                                                                             'Comparator '
                                                                                                             '3 '
                                                                                                             'Output '
                                                                                                             'Bit',
                                                                                              'name': 'AC3O'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[4:4]',
                                                                                              'description': 'Analog '
                                                                                                             'Comparator '
                                                                                                             '0 '
                                                                                                             'Interrupt '
                                                                                                             'Flag '
                                                                                                             'Bit',
                                                                                              'name': 'AC0IF'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[5:5]',
                                                                                              'description': 'Analog '
                                                                                                             'Comparator '
                                                                                                             '1  '
                                                                                                             'Interrupt '
                                                                                                             'Flag '
                                                                                                             'Bit',
                                                                                              'name': 'AC1IF'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[6:6]',
                                                                                              'description': 'Analog '
                                                                                                             'Comparator '
                                                                                                             '2 '
                                                                                                             'Interrupt '
                                                                                                             'Flag '
                                                                                                             'Bit',
                                                                                              'name': 'AC2IF'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[7:7]',
                                                                                              'description': 'Analog '
                                                                                                             'Comparator '
                                                                                                             '3 '
                                                                                                             'Interrupt '
                                                                                                             'Flag '
                                                                                                             'Bit',
                                                                                              'name': 'AC3IF'}]},
                                                                        'name': 'ACSR',
                                                                        'size': 0x8}]}},
                                           {'addressBlock': [{'offset': 0x0,
                                                              'size': 0x8,
                                                              'usage': 'registers'},
                                                             {'offset': 0x9,
                                                              'size': 0x2,
                                                              'usage': 'registers'}],
                                            'baseAddress': 0x800075,
                                            'description': 'Analog-to-Digital '
                                                           'Converter',
                                            'name': 'ADC',
                                            'registers': {'register': [{'access': 'read-write',
                                                                        'addressOffset': 0x3,
                                                                        'description': 'ADC '
                                                                                       'Data '
                                                                                       'Register '
                                                                                       'Bytes',
                                                                        'fields': {'field': [{'access': 'read-write',
                                                                                              'bitRange': '[15:0]',
                                                                                              'description': 'ADC '
                                                                                                             'Data '
                                                                                                             'bits',
                                                                                              'name': 'ADC',
                                                                                              'writeConstraint': {'range': {'maximum': 0xFFFF,
                                                                                                                            'minimum': 0x0}}}]},
                                                                        'name': 'ADC',
                                                                        'size': 0x10},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x5,
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
                                                                                              'description': 'ADC  '
                                                                                                             'Prescaler '
                                                                                                             'Select '
                                                                                                             'Bits',
                                                                                              'name': 'ADPS',
                                                                                              'writeConstraint': {'range': {'maximum': 0x7,
                                                                                                                            'minimum': 0x0}}},
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
                                                                        'addressOffset': 0x6,
                                                                        'description': 'ADC '
                                                                                       'Control '
                                                                                       'and '
                                                                                       'Status '
                                                                                       'Register '
                                                                                       'B',
                                                                        'fields': {'field': [{'access': 'read-write',
                                                                                              'bitRange': '[3:0]',
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
                                                                                                                                        'value': 0x7},
                                                                                                                                       {'description': 'PSC0ASY '
                                                                                                                                                       'Event',
                                                                                                                                        'name': 'PSC0ASY_EVENT',
                                                                                                                                        'value': 0x8},
                                                                                                                                       {'description': 'PSC1ASY '
                                                                                                                                                       'Event',
                                                                                                                                        'name': 'PSC1ASY_EVENT',
                                                                                                                                        'value': 0x9},
                                                                                                                                       {'description': 'PSC2ASY '
                                                                                                                                                       'Event',
                                                                                                                                        'name': 'PSC2ASY_EVENT',
                                                                                                                                        'value': 0xA},
                                                                                                                                       {'description': 'Analog '
                                                                                                                                                       'comparator '
                                                                                                                                                       '1',
                                                                                                                                        'name': 'ANALOG_COMPARATOR_1',
                                                                                                                                        'value': 0xB},
                                                                                                                                       {'description': 'Analog '
                                                                                                                                                       'comparator '
                                                                                                                                                       '2',
                                                                                                                                        'name': 'ANALOG_COMPARATOR_2',
                                                                                                                                        'value': 0xC}]},
                                                                                              'name': 'ADTS',
                                                                                              'writeConstraint': {'useEnumeratedValues': 0x1}},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[5:5]',
                                                                                              'description': 'Analog '
                                                                                                             'Reference '
                                                                                                             'pin '
                                                                                                             'Enable',
                                                                                              'name': 'AREFEN'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[6:6]',
                                                                                              'description': 'Current '
                                                                                                             'Source '
                                                                                                             'Enable',
                                                                                              'name': 'ISRCEN'},
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
                                                                        'addressOffset': 0x7,
                                                                        'description': 'The '
                                                                                       'ADC '
                                                                                       'multiplexer '
                                                                                       'Selection '
                                                                                       'Register',
                                                                        'fields': {'field': [{'access': 'read-write',
                                                                                              'bitRange': '[4:0]',
                                                                                              'description': 'ADC '
                                                                                                             'channel '
                                                                                                             'selection '
                                                                                                             'bits',
                                                                                              'enumeratedValues': {'enumeratedValue': [{'description': 'ADC '
                                                                                                                                                       'input '
                                                                                                                                                       'pin '
                                                                                                                                                       '0',
                                                                                                                                        'name': 'ADC0',
                                                                                                                                        'value': 0x0},
                                                                                                                                       {'description': 'ADC '
                                                                                                                                                       'input '
                                                                                                                                                       'pin '
                                                                                                                                                       '1',
                                                                                                                                        'name': 'ADC1',
                                                                                                                                        'value': 0x1},
                                                                                                                                       {'description': 'ADC '
                                                                                                                                                       'input '
                                                                                                                                                       'pin '
                                                                                                                                                       '2',
                                                                                                                                        'name': 'ADC2',
                                                                                                                                        'value': 0x2},
                                                                                                                                       {'description': 'ADC '
                                                                                                                                                       'input '
                                                                                                                                                       'pin '
                                                                                                                                                       '3',
                                                                                                                                        'name': 'ADC3',
                                                                                                                                        'value': 0x3},
                                                                                                                                       {'description': 'ADC '
                                                                                                                                                       'input '
                                                                                                                                                       'pin '
                                                                                                                                                       '4',
                                                                                                                                        'name': 'ADC4',
                                                                                                                                        'value': 0x4},
                                                                                                                                       {'description': 'ADC '
                                                                                                                                                       'input '
                                                                                                                                                       'pin '
                                                                                                                                                       '5',
                                                                                                                                        'name': 'ADC5',
                                                                                                                                        'value': 0x5},
                                                                                                                                       {'description': 'ADC '
                                                                                                                                                       'input '
                                                                                                                                                       'pin '
                                                                                                                                                       '6',
                                                                                                                                        'name': 'ADC6',
                                                                                                                                        'value': 0x6},
                                                                                                                                       {'description': 'ADC '
                                                                                                                                                       'input '
                                                                                                                                                       'pin '
                                                                                                                                                       '7',
                                                                                                                                        'name': 'ADC7',
                                                                                                                                        'value': 0x7},
                                                                                                                                       {'description': 'ADC '
                                                                                                                                                       'input '
                                                                                                                                                       'pin '
                                                                                                                                                       '8',
                                                                                                                                        'name': 'ADC8',
                                                                                                                                        'value': 0x8},
                                                                                                                                       {'description': 'ADC '
                                                                                                                                                       'input '
                                                                                                                                                       'pin '
                                                                                                                                                       '9',
                                                                                                                                        'name': 'ADC9',
                                                                                                                                        'value': 0x9},
                                                                                                                                       {'description': 'ADC '
                                                                                                                                                       'input '
                                                                                                                                                       'pin '
                                                                                                                                                       '10',
                                                                                                                                        'name': 'ADC10',
                                                                                                                                        'value': 0xA},
                                                                                                                                       {'description': 'Temperature '
                                                                                                                                                       'sensor',
                                                                                                                                        'name': 'TEMPSENSE',
                                                                                                                                        'value': 0xB},
                                                                                                                                       {'description': 'Internal '
                                                                                                                                                       'VCC '
                                                                                                                                                       '/ '
                                                                                                                                                       '4',
                                                                                                                                        'name': 'VCC4',
                                                                                                                                        'value': 0xC},
                                                                                                                                       {'description': 'Current '
                                                                                                                                                       'source',
                                                                                                                                        'name': 'ISRC',
                                                                                                                                        'value': 0xD},
                                                                                                                                       {'description': 'Analog '
                                                                                                                                                       'Differential '
                                                                                                                                                       'Amplifier '
                                                                                                                                                       '0',
                                                                                                                                        'name': 'AMP0',
                                                                                                                                        'value': 0xE},
                                                                                                                                       {'description': 'Analog '
                                                                                                                                                       'Differential '
                                                                                                                                                       'Amplifier '
                                                                                                                                                       '1',
                                                                                                                                        'name': 'AMP1',
                                                                                                                                        'value': 0xF},
                                                                                                                                       {'description': 'Analog '
                                                                                                                                                       'Differential '
                                                                                                                                                       'Amplifier '
                                                                                                                                                       '2',
                                                                                                                                        'name': 'AMP2',
                                                                                                                                        'value': 0x10},
                                                                                                                                       {'description': 'Bandgap',
                                                                                                                                        'name': 'BNDGAP',
                                                                                                                                        'value': 0x11},
                                                                                                                                       {'description': '0V '
                                                                                                                                                       '(GND)',
                                                                                                                                        'name': 'GND',
                                                                                                                                        'value': 0x12}]},
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
                                                                                                                                                       'reference',
                                                                                                                                        'name': 'AVCC_REFERENCE',
                                                                                                                                        'value': 0x1},
                                                                                                                                       {'description': 'Reserved',
                                                                                                                                        'name': 'RESERVED',
                                                                                                                                        'value': 0x2},
                                                                                                                                       {'description': 'Internal '
                                                                                                                                                       '2.56V '
                                                                                                                                                       'Voltage '
                                                                                                                                                       'Reference',
                                                                                                                                        'name': 'INTERNAL_2_56V_VOLTAGE_REFERENCE',
                                                                                                                                        'value': 0x3}]},
                                                                                              'name': 'REFS',
                                                                                              'writeConstraint': {'useEnumeratedValues': 0x1}}]},
                                                                        'name': 'ADMUX',
                                                                        'size': 0x8},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x0,
                                                                        'description': 'Amplifier '
                                                                                       '0 '
                                                                                       'Control '
                                                                                       'and '
                                                                                       'Status '
                                                                                       'Register',
                                                                        'fields': {'field': [{'access': 'read-write',
                                                                                              'bitRange': '[2:0]',
                                                                                              'description': 'Amplifier '
                                                                                                             '0 '
                                                                                                             'Clock '
                                                                                                             'Source '
                                                                                                             'Selection',
                                                                                              'name': 'AMP0TS',
                                                                                              'writeConstraint': {'range': {'maximum': 0x7,
                                                                                                                            'minimum': 0x0}}},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[3:3]',
                                                                                              'description': 'Amplifier '
                                                                                                             '0 '
                                                                                                             '- '
                                                                                                             'Comparator '
                                                                                                             '0 '
                                                                                                             'connection',
                                                                                              'name': 'AMPCMP0'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[5:4]',
                                                                                              'description': 'Amplifier '
                                                                                                             '0 '
                                                                                                             'Gain '
                                                                                                             'Selection',
                                                                                              'name': 'AMP0G',
                                                                                              'writeConstraint': {'range': {'maximum': 0x3,
                                                                                                                            'minimum': 0x0}}},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[6:6]',
                                                                                              'description': 'Amplifier '
                                                                                                             '0 '
                                                                                                             'Input '
                                                                                                             'Shunt',
                                                                                              'name': 'AMP0IS'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[7:7]',
                                                                                              'description': 'Amplifier '
                                                                                                             '0 '
                                                                                                             'Enable',
                                                                                              'name': 'AMP0EN'}]},
                                                                        'name': 'AMP0CSR',
                                                                        'size': 0x8},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x1,
                                                                        'description': 'Amplifier '
                                                                                       '1 '
                                                                                       'Control '
                                                                                       'and '
                                                                                       'Status '
                                                                                       'Register',
                                                                        'fields': {'field': [{'access': 'read-write',
                                                                                              'bitRange': '[2:0]',
                                                                                              'description': 'Amplifier '
                                                                                                             '1 '
                                                                                                             'Clock '
                                                                                                             'Source '
                                                                                                             'Selection',
                                                                                              'name': 'AMP1TS',
                                                                                              'writeConstraint': {'range': {'maximum': 0x7,
                                                                                                                            'minimum': 0x0}}},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[3:3]',
                                                                                              'description': 'Amplifier '
                                                                                                             '1 '
                                                                                                             '- '
                                                                                                             'Comparator '
                                                                                                             '1 '
                                                                                                             'Connection',
                                                                                              'name': 'AMPCMP1'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[5:4]',
                                                                                              'description': 'Amplifier '
                                                                                                             '1 '
                                                                                                             'Gain '
                                                                                                             'Selection',
                                                                                              'name': 'AMP1G',
                                                                                              'writeConstraint': {'range': {'maximum': 0x3,
                                                                                                                            'minimum': 0x0}}},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[6:6]',
                                                                                              'description': 'Amplifier '
                                                                                                             '1 '
                                                                                                             'Input '
                                                                                                             'Shunt',
                                                                                              'name': 'AMP1IS'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[7:7]',
                                                                                              'description': 'Amplifier '
                                                                                                             '1 '
                                                                                                             'Enable',
                                                                                              'name': 'AMP1EN'}]},
                                                                        'name': 'AMP1CSR',
                                                                        'size': 0x8},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x2,
                                                                        'description': 'Amplifier '
                                                                                       '2 '
                                                                                       'Control '
                                                                                       'and '
                                                                                       'Status '
                                                                                       'Register',
                                                                        'fields': {'field': [{'access': 'read-write',
                                                                                              'bitRange': '[2:0]',
                                                                                              'description': 'Amplifier '
                                                                                                             '2 '
                                                                                                             'Clock '
                                                                                                             'Source '
                                                                                                             'Selection',
                                                                                              'name': 'AMP2TS',
                                                                                              'writeConstraint': {'range': {'maximum': 0x7,
                                                                                                                            'minimum': 0x0}}},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[3:3]',
                                                                                              'description': 'Amplifier '
                                                                                                             '2 '
                                                                                                             '- '
                                                                                                             'Comparator '
                                                                                                             '2 '
                                                                                                             'Connection',
                                                                                              'name': 'AMPCMP2'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[5:4]',
                                                                                              'description': 'Amplifier '
                                                                                                             '2 '
                                                                                                             'Gain '
                                                                                                             'Selection',
                                                                                              'name': 'AMP2G',
                                                                                              'writeConstraint': {'range': {'maximum': 0x3,
                                                                                                                            'minimum': 0x0}}},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[6:6]',
                                                                                              'description': 'Amplifier '
                                                                                                             '2 '
                                                                                                             'Input '
                                                                                                             'Shunt',
                                                                                              'name': 'AMP2IS'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[7:7]',
                                                                                              'description': 'Amplifier '
                                                                                                             '2 '
                                                                                                             'Enable',
                                                                                              'name': 'AMP2EN'}]},
                                                                        'name': 'AMP2CSR',
                                                                        'size': 0x8},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x9,
                                                                        'description': 'Digital '
                                                                                       'Input '
                                                                                       'Disable '
                                                                                       'Register '
                                                                                       '0',
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
                                                                        'size': 0x8},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0xA,
                                                                        'description': 'Digital '
                                                                                       'Input '
                                                                                       'Disable '
                                                                                       'Register '
                                                                                       '0',
                                                                        'fields': {'field': [{'access': 'read-write',
                                                                                              'bitRange': '[0:0]',
                                                                                              'description': 'ADC8 '
                                                                                                             'Pin '
                                                                                                             'Digital '
                                                                                                             'input '
                                                                                                             'Disable',
                                                                                              'name': 'ADC8D'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[1:1]',
                                                                                              'description': 'ADC9 '
                                                                                                             'Pin '
                                                                                                             'Digital '
                                                                                                             'input '
                                                                                                             'Disable',
                                                                                              'name': 'ADC9D'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[2:2]',
                                                                                              'description': 'ADC10 '
                                                                                                             'Pin '
                                                                                                             'Digital '
                                                                                                             'input '
                                                                                                             'Disable',
                                                                                              'name': 'ADC10D'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[3:3]',
                                                                                              'description': 'AMP0N '
                                                                                                             'Pin '
                                                                                                             'Digital '
                                                                                                             'input '
                                                                                                             'Disable',
                                                                                              'name': 'AMP0ND'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[4:4]',
                                                                                              'description': 'AMP0P '
                                                                                                             'Pin '
                                                                                                             'Digital '
                                                                                                             'input '
                                                                                                             'Disable',
                                                                                              'name': 'AMP0PD'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[5:5]',
                                                                                              'description': 'ACMP0 '
                                                                                                             'Pin '
                                                                                                             'Digital '
                                                                                                             'input '
                                                                                                             'Disable',
                                                                                              'name': 'ACMP0D'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[6:6]',
                                                                                              'description': 'AMP2P '
                                                                                                             'Pin '
                                                                                                             'Digital '
                                                                                                             'input '
                                                                                                             'Disable',
                                                                                              'name': 'AMP2PD'}]},
                                                                        'name': 'DIDR1',
                                                                        'size': 0x8}]}},
                                           {'addressBlock': [{'offset': 0x0,
                                                              'size': 0x23,
                                                              'usage': 'registers'}],
                                            'baseAddress': 0x8000D8,
                                            'description': 'Controller Area '
                                                           'Network',
                                            'name': 'CAN',
                                            'registers': {'register': [{'access': 'read-write',
                                                                        'addressOffset': 0xA,
                                                                        'description': 'CAN '
                                                                                       'Bit '
                                                                                       'Timing '
                                                                                       'Register '
                                                                                       '1',
                                                                        'fields': {'field': [{'access': 'read-write',
                                                                                              'bitRange': '[6:1]',
                                                                                              'description': 'Baud '
                                                                                                             'Rate '
                                                                                                             'Prescaler '
                                                                                                             'bits',
                                                                                              'name': 'BRP',
                                                                                              'writeConstraint': {'range': {'maximum': 0x3F,
                                                                                                                            'minimum': 0x0}}}]},
                                                                        'name': 'CANBT1',
                                                                        'size': 0x8},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0xB,
                                                                        'description': 'CAN '
                                                                                       'Bit '
                                                                                       'Timing '
                                                                                       'Register '
                                                                                       '2',
                                                                        'fields': {'field': [{'access': 'read-write',
                                                                                              'bitRange': '[3:1]',
                                                                                              'description': 'Propagation '
                                                                                                             'Time '
                                                                                                             'Segment '
                                                                                                             'bits',
                                                                                              'name': 'PRS',
                                                                                              'writeConstraint': {'range': {'maximum': 0x7,
                                                                                                                            'minimum': 0x0}}},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[6:5]',
                                                                                              'description': 'Re-Sync '
                                                                                                             'Jump '
                                                                                                             'Width '
                                                                                                             'bits',
                                                                                              'name': 'SJW',
                                                                                              'writeConstraint': {'range': {'maximum': 0x3,
                                                                                                                            'minimum': 0x0}}}]},
                                                                        'name': 'CANBT2',
                                                                        'size': 0x8},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0xC,
                                                                        'description': 'CAN '
                                                                                       'Bit '
                                                                                       'Timing '
                                                                                       'Register '
                                                                                       '3',
                                                                        'fields': {'field': [{'access': 'read-write',
                                                                                              'bitRange': '[0:0]',
                                                                                              'description': 'Sample '
                                                                                                             'Type',
                                                                                              'name': 'SMP'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[3:1]',
                                                                                              'description': 'Phase '
                                                                                                             'Segment '
                                                                                                             '1 '
                                                                                                             'bits',
                                                                                              'name': 'PHS1',
                                                                                              'writeConstraint': {'range': {'maximum': 0x7,
                                                                                                                            'minimum': 0x0}}},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[6:4]',
                                                                                              'description': 'Phase '
                                                                                                             'Segment '
                                                                                                             '2 '
                                                                                                             'bits',
                                                                                              'name': 'PHS2',
                                                                                              'writeConstraint': {'range': {'maximum': 0x7,
                                                                                                                            'minimum': 0x0}}}]},
                                                                        'name': 'CANBT3',
                                                                        'size': 0x8},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x17,
                                                                        'description': 'MOb '
                                                                                       'Control '
                                                                                       'and '
                                                                                       'DLC '
                                                                                       'Register',
                                                                        'fields': {'field': [{'access': 'read-write',
                                                                                              'bitRange': '[3:0]',
                                                                                              'description': 'Data '
                                                                                                             'Length '
                                                                                                             'Code '
                                                                                                             'bits',
                                                                                              'name': 'DLC',
                                                                                              'writeConstraint': {'range': {'maximum': 0xF,
                                                                                                                            'minimum': 0x0}}},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[4:4]',
                                                                                              'description': 'Identifier '
                                                                                                             'Extension',
                                                                                              'name': 'IDE'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[5:5]',
                                                                                              'description': 'Reply '
                                                                                                             'Valid',
                                                                                              'name': 'RPLV'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[7:6]',
                                                                                              'description': 'MOb '
                                                                                                             'Config '
                                                                                                             'bits',
                                                                                              'name': 'CONMOB',
                                                                                              'writeConstraint': {'range': {'maximum': 0x3,
                                                                                                                            'minimum': 0x0}}}]},
                                                                        'name': 'CANCDMOB',
                                                                        'size': 0x8},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x5,
                                                                        'description': 'Enable '
                                                                                       'MOb '
                                                                                       'Register '
                                                                                       '1(empty)',
                                                                        'name': 'CANEN1',
                                                                        'size': 0x8,
                                                                        'writeConstraint': {'range': {'maximum': 0xFF,
                                                                                                      'minimum': 0x0}}},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x4,
                                                                        'description': 'Enable '
                                                                                       'MOb '
                                                                                       'Register '
                                                                                       '2 '
                                                                                       '(read-only '
                                                                                       'for '
                                                                                       'debugger)',
                                                                        'fields': {'field': [{'access': 'read-write',
                                                                                              'bitRange': '[5:0]',
                                                                                              'description': 'Enable '
                                                                                                             'MObs',
                                                                                              'name': 'ENMOB',
                                                                                              'writeConstraint': {'range': {'maximum': 0x3F,
                                                                                                                            'minimum': 0x0}}}]},
                                                                        'name': 'CANEN2',
                                                                        'size': 0x8},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x0,
                                                                        'description': 'CAN '
                                                                                       'General '
                                                                                       'Control '
                                                                                       'Register',
                                                                        'fields': {'field': [{'access': 'read-write',
                                                                                              'bitRange': '[0:0]',
                                                                                              'description': 'Software '
                                                                                                             'Reset '
                                                                                                             'Request',
                                                                                              'name': 'SWRES'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[1:1]',
                                                                                              'description': 'Enable '
                                                                                                             '/ '
                                                                                                             'Standby',
                                                                                              'name': 'ENASTB'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[2:2]',
                                                                                              'description': 'Test '
                                                                                                             'Mode',
                                                                                              'name': 'TEST'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[3:3]',
                                                                                              'description': 'Listening '
                                                                                                             'Mode',
                                                                                              'name': 'LISTEN'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[4:4]',
                                                                                              'description': 'Synchronization '
                                                                                                             'of '
                                                                                                             'TTC',
                                                                                              'name': 'SYNTTC'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[5:5]',
                                                                                              'description': 'Time '
                                                                                                             'Trigger '
                                                                                                             'Communication',
                                                                                              'name': 'TTC'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[6:6]',
                                                                                              'description': 'Overload '
                                                                                                             'Frame '
                                                                                                             'Request',
                                                                                              'name': 'OVRQ'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[7:7]',
                                                                                              'description': 'Abort '
                                                                                                             'Request',
                                                                                              'name': 'ABRQ'}]},
                                                                        'name': 'CANGCON',
                                                                        'size': 0x8},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x3,
                                                                        'description': 'CAN '
                                                                                       'General '
                                                                                       'Interrupt '
                                                                                       'Enable '
                                                                                       'Register',
                                                                        'fields': {'field': [{'access': 'read-write',
                                                                                              'bitRange': '[0:0]',
                                                                                              'description': 'Enable '
                                                                                                             'CAN '
                                                                                                             'Timer '
                                                                                                             'Overrun '
                                                                                                             'Interrupt',
                                                                                              'name': 'ENOVRT'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[1:1]',
                                                                                              'description': 'Enable '
                                                                                                             'General '
                                                                                                             'Error '
                                                                                                             'Interrupt',
                                                                                              'name': 'ENERG'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[2:2]',
                                                                                              'description': 'Enable '
                                                                                                             'Burst '
                                                                                                             'Receive '
                                                                                                             'Interrupt',
                                                                                              'name': 'ENBX'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[3:3]',
                                                                                              'description': 'Enable '
                                                                                                             'MOb '
                                                                                                             'Error '
                                                                                                             'Interrupt',
                                                                                              'name': 'ENERR'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[4:4]',
                                                                                              'description': 'Enable '
                                                                                                             'Transmit '
                                                                                                             'Interrupt',
                                                                                              'name': 'ENTX'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[5:5]',
                                                                                              'description': 'Enable '
                                                                                                             'Receive '
                                                                                                             'Interrupt',
                                                                                              'name': 'ENRX'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[6:6]',
                                                                                              'description': 'Enable '
                                                                                                             'Bus '
                                                                                                             'Off '
                                                                                                             'Interrupt',
                                                                                              'name': 'ENBOFF'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[7:7]',
                                                                                              'description': 'Enable '
                                                                                                             'all '
                                                                                                             'Interrupts',
                                                                                              'name': 'ENIT'}]},
                                                                        'name': 'CANGIE',
                                                                        'size': 0x8},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x2,
                                                                        'description': 'CAN '
                                                                                       'General '
                                                                                       'Interrupt '
                                                                                       'Register '
                                                                                       'Flags',
                                                                        'fields': {'field': [{'access': 'read-write',
                                                                                              'bitRange': '[0:0]',
                                                                                              'description': 'Acknowledgement '
                                                                                                             'Error '
                                                                                                             'General '
                                                                                                             'Flag',
                                                                                              'name': 'AERG'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[1:1]',
                                                                                              'description': 'Form '
                                                                                                             'Error '
                                                                                                             'General '
                                                                                                             'Flag',
                                                                                              'name': 'FERG'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[2:2]',
                                                                                              'description': 'CRC '
                                                                                                             'Error '
                                                                                                             'General '
                                                                                                             'Flag',
                                                                                              'name': 'CERG'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[3:3]',
                                                                                              'description': 'Stuff '
                                                                                                             'Error '
                                                                                                             'General '
                                                                                                             'Flag',
                                                                                              'name': 'SERG'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[4:4]',
                                                                                              'description': 'Burst '
                                                                                                             'Receive '
                                                                                                             'Interrupt '
                                                                                                             'Flag',
                                                                                              'name': 'BXOK'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[5:5]',
                                                                                              'description': 'Overrun '
                                                                                                             'CAN '
                                                                                                             'Timer '
                                                                                                             'Flag',
                                                                                              'name': 'OVRTIM'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[6:6]',
                                                                                              'description': 'Bus '
                                                                                                             'Off '
                                                                                                             'Interrupt '
                                                                                                             'Flag',
                                                                                              'name': 'BOFFIT'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[7:7]',
                                                                                              'description': 'General '
                                                                                                             'Interrupt '
                                                                                                             'Flag',
                                                                                              'name': 'CANIT'}]},
                                                                        'name': 'CANGIT',
                                                                        'size': 0x8},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x1,
                                                                        'description': 'CAN '
                                                                                       'General '
                                                                                       'Status '
                                                                                       'Register '
                                                                                       '(read-only '
                                                                                       'for '
                                                                                       'debugger)',
                                                                        'fields': {'field': [{'access': 'read-write',
                                                                                              'bitRange': '[0:0]',
                                                                                              'description': 'Error '
                                                                                                             'Passive '
                                                                                                             'Mode',
                                                                                              'name': 'ERRP'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[1:1]',
                                                                                              'description': 'Bus '
                                                                                                             'Off '
                                                                                                             'Mode',
                                                                                              'name': 'BOFF'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[2:2]',
                                                                                              'description': 'Enable '
                                                                                                             'Flag',
                                                                                              'name': 'ENFG'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[3:3]',
                                                                                              'description': 'Receiver '
                                                                                                             'Busy',
                                                                                              'name': 'RXBSY'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[4:4]',
                                                                                              'description': 'Transmitter '
                                                                                                             'Busy',
                                                                                              'name': 'TXBSY'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[6:6]',
                                                                                              'description': 'Overload '
                                                                                                             'Frame '
                                                                                                             'Flag',
                                                                                              'name': 'OVFG'}]},
                                                                        'name': 'CANGSTA',
                                                                        'size': 0x8},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x14,
                                                                        'description': 'Highest '
                                                                                       'Priority '
                                                                                       'MOb '
                                                                                       'Register',
                                                                        'fields': {'field': [{'access': 'read-write',
                                                                                              'bitRange': '[3:0]',
                                                                                              'description': 'CAN '
                                                                                                             'General '
                                                                                                             'Purpose '
                                                                                                             'bits',
                                                                                              'name': 'CGP',
                                                                                              'writeConstraint': {'range': {'maximum': 0xF,
                                                                                                                            'minimum': 0x0}}},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[7:4]',
                                                                                              'description': 'Highest '
                                                                                                             'Priority '
                                                                                                             'MOb '
                                                                                                             'Number '
                                                                                                             'bits',
                                                                                              'name': 'HPMOB',
                                                                                              'writeConstraint': {'range': {'maximum': 0xF,
                                                                                                                            'minimum': 0x0}}}]},
                                                                        'name': 'CANHPMOB',
                                                                        'size': 0x8},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x1F,
                                                                        'description': 'Identifier '
                                                                                       'Mask '
                                                                                       'Register '
                                                                                       '1',
                                                                        'fields': {'field': [{'access': 'read-write',
                                                                                              'bitRange': '[7:0]',
                                                                                              'description': 'Identifier '
                                                                                                             'Mask',
                                                                                              'name': 'IDMSK',
                                                                                              'writeConstraint': {'range': {'maximum': 0xFF,
                                                                                                                            'minimum': 0x0}}}]},
                                                                        'name': 'CANIDM1',
                                                                        'size': 0x8},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x1E,
                                                                        'description': 'Identifier '
                                                                                       'Mask '
                                                                                       'Register '
                                                                                       '2',
                                                                        'fields': {'field': [{'access': 'read-write',
                                                                                              'bitRange': '[7:0]',
                                                                                              'description': 'Identifier '
                                                                                                             'Mask',
                                                                                              'name': 'IDMSK',
                                                                                              'writeConstraint': {'range': {'maximum': 0xFF,
                                                                                                                            'minimum': 0x0}}}]},
                                                                        'name': 'CANIDM2',
                                                                        'size': 0x8},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x1D,
                                                                        'description': 'Identifier '
                                                                                       'Mask '
                                                                                       'Register '
                                                                                       '3',
                                                                        'fields': {'field': [{'access': 'read-write',
                                                                                              'bitRange': '[7:0]',
                                                                                              'description': 'Identifier '
                                                                                                             'Mask',
                                                                                              'name': 'IDMSK',
                                                                                              'writeConstraint': {'range': {'maximum': 0xFF,
                                                                                                                            'minimum': 0x0}}}]},
                                                                        'name': 'CANIDM3',
                                                                        'size': 0x8},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x1C,
                                                                        'description': 'Identifier '
                                                                                       'Mask '
                                                                                       'Register '
                                                                                       '4',
                                                                        'fields': {'field': [{'access': 'read-write',
                                                                                              'bitRange': '[0:0]',
                                                                                              'description': 'Identifier '
                                                                                                             'Extension '
                                                                                                             'Mask',
                                                                                              'name': 'IDEMSK'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[2:2]',
                                                                                              'description': 'Remote '
                                                                                                             'Transmission '
                                                                                                             'Request '
                                                                                                             'Mask',
                                                                                              'name': 'RTRMSK'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[7:3]',
                                                                                              'description': 'Identifier '
                                                                                                             'Mask',
                                                                                              'name': 'IDMSK',
                                                                                              'writeConstraint': {'range': {'maximum': 0x1F,
                                                                                                                            'minimum': 0x0}}}]},
                                                                        'name': 'CANIDM4',
                                                                        'size': 0x8},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x1B,
                                                                        'description': 'Identifier '
                                                                                       'Tag '
                                                                                       'Register '
                                                                                       '1',
                                                                        'fields': {'field': [{'access': 'read-write',
                                                                                              'bitRange': '[7:0]',
                                                                                              'description': 'Identifier '
                                                                                                             'Tag',
                                                                                              'name': 'IDT',
                                                                                              'writeConstraint': {'range': {'maximum': 0xFF,
                                                                                                                            'minimum': 0x0}}}]},
                                                                        'name': 'CANIDT1',
                                                                        'size': 0x8},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x1A,
                                                                        'description': 'Identifier '
                                                                                       'Tag '
                                                                                       'Register '
                                                                                       '2',
                                                                        'fields': {'field': [{'access': 'read-write',
                                                                                              'bitRange': '[7:0]',
                                                                                              'description': 'Identifier '
                                                                                                             'Tag',
                                                                                              'name': 'IDT',
                                                                                              'writeConstraint': {'range': {'maximum': 0xFF,
                                                                                                                            'minimum': 0x0}}}]},
                                                                        'name': 'CANIDT2',
                                                                        'size': 0x8},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x19,
                                                                        'description': 'Identifier '
                                                                                       'Tag '
                                                                                       'Register '
                                                                                       '3',
                                                                        'fields': {'field': [{'access': 'read-write',
                                                                                              'bitRange': '[7:0]',
                                                                                              'description': 'Identifier '
                                                                                                             'Tag',
                                                                                              'name': 'IDT',
                                                                                              'writeConstraint': {'range': {'maximum': 0xFF,
                                                                                                                            'minimum': 0x0}}}]},
                                                                        'name': 'CANIDT3',
                                                                        'size': 0x8},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x18,
                                                                        'description': 'Identifier '
                                                                                       'Tag '
                                                                                       'Register '
                                                                                       '4',
                                                                        'fields': {'field': [{'access': 'read-write',
                                                                                              'bitRange': '[0:0]',
                                                                                              'description': 'Reserved '
                                                                                                             'Bit '
                                                                                                             '0 '
                                                                                                             'Tag',
                                                                                              'name': 'RB0TAG'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[1:1]',
                                                                                              'description': 'Reserved '
                                                                                                             'Bit '
                                                                                                             '1 '
                                                                                                             'Tag',
                                                                                              'name': 'RB1TAG'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[2:2]',
                                                                                              'description': 'Remote '
                                                                                                             'Transmission '
                                                                                                             'Request '
                                                                                                             'Tag',
                                                                                              'name': 'RTRTAG'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[7:3]',
                                                                                              'description': 'Identifier '
                                                                                                             'Tag',
                                                                                              'name': 'IDT',
                                                                                              'writeConstraint': {'range': {'maximum': 0x1F,
                                                                                                                            'minimum': 0x0}}}]},
                                                                        'name': 'CANIDT4',
                                                                        'size': 0x8},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x7,
                                                                        'description': 'Enable '
                                                                                       'Interrupt '
                                                                                       'MOb '
                                                                                       'Register '
                                                                                       '1 '
                                                                                       '(empty)',
                                                                        'name': 'CANIE1',
                                                                        'size': 0x8,
                                                                        'writeConstraint': {'range': {'maximum': 0xFF,
                                                                                                      'minimum': 0x0}}},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x6,
                                                                        'description': 'Enable '
                                                                                       'Interrupt '
                                                                                       'MOb '
                                                                                       'Register '
                                                                                       '2',
                                                                        'fields': {'field': [{'access': 'read-write',
                                                                                              'bitRange': '[5:0]',
                                                                                              'description': 'Interrupt '
                                                                                                             'Enable  '
                                                                                                             'MObs',
                                                                                              'name': 'IEMOB',
                                                                                              'writeConstraint': {'range': {'maximum': 0x3F,
                                                                                                                            'minimum': 0x0}}}]},
                                                                        'name': 'CANIE2',
                                                                        'size': 0x8},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x22,
                                                                        'description': 'Message '
                                                                                       'Data '
                                                                                       'Register',
                                                                        'fields': {'field': [{'access': 'read-write',
                                                                                              'bitRange': '[7:0]',
                                                                                              'description': 'Message '
                                                                                                             'Data '
                                                                                                             'bits',
                                                                                              'name': 'MSG',
                                                                                              'writeConstraint': {'range': {'maximum': 0xFF,
                                                                                                                            'minimum': 0x0}}}]},
                                                                        'name': 'CANMSG',
                                                                        'size': 0x8},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x15,
                                                                        'description': 'Page '
                                                                                       'MOb '
                                                                                       'Register',
                                                                        'fields': {'field': [{'access': 'read-write',
                                                                                              'bitRange': '[2:0]',
                                                                                              'description': 'Data '
                                                                                                             'Buffer '
                                                                                                             'Index '
                                                                                                             'bits',
                                                                                              'name': 'INDX',
                                                                                              'writeConstraint': {'range': {'maximum': 0x7,
                                                                                                                            'minimum': 0x0}}},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[3:3]',
                                                                                              'description': 'MOb '
                                                                                                             'Data '
                                                                                                             'Buffer '
                                                                                                             'Auto '
                                                                                                             'Increment '
                                                                                                             '(Active '
                                                                                                             'Low)',
                                                                                              'name': 'AINC'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[7:4]',
                                                                                              'description': 'MOb '
                                                                                                             'Number '
                                                                                                             'bits',
                                                                                              'name': 'MOBNB',
                                                                                              'writeConstraint': {'range': {'maximum': 0xF,
                                                                                                                            'minimum': 0x0}}}]},
                                                                        'name': 'CANPAGE',
                                                                        'size': 0x8},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x13,
                                                                        'description': 'Receive '
                                                                                       'Error '
                                                                                       'Counter '
                                                                                       'Register',
                                                                        'fields': {'field': [{'access': 'read-write',
                                                                                              'bitRange': '[7:0]',
                                                                                              'description': 'Receive '
                                                                                                             'Error '
                                                                                                             'Counter '
                                                                                                             'bits',
                                                                                              'name': 'REC',
                                                                                              'writeConstraint': {'range': {'maximum': 0xFF,
                                                                                                                            'minimum': 0x0}}}]},
                                                                        'name': 'CANREC',
                                                                        'size': 0x8},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x9,
                                                                        'description': 'CAN '
                                                                                       'Status '
                                                                                       'Interrupt '
                                                                                       'MOb '
                                                                                       'Register '
                                                                                       '1 '
                                                                                       '(empty)',
                                                                        'name': 'CANSIT1',
                                                                        'size': 0x8,
                                                                        'writeConstraint': {'range': {'maximum': 0xFF,
                                                                                                      'minimum': 0x0}}},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x8,
                                                                        'description': 'CAN '
                                                                                       'Status '
                                                                                       'Interrupt '
                                                                                       'MOb '
                                                                                       'Register '
                                                                                       '2 '
                                                                                       '(read-only '
                                                                                       'for '
                                                                                       'debugger)',
                                                                        'fields': {'field': [{'access': 'read-write',
                                                                                              'bitRange': '[5:0]',
                                                                                              'description': 'Status '
                                                                                                             'of '
                                                                                                             'Interrupt '
                                                                                                             'MObs',
                                                                                              'name': 'SIT',
                                                                                              'writeConstraint': {'range': {'maximum': 0x3F,
                                                                                                                            'minimum': 0x0}}}]},
                                                                        'name': 'CANSIT2',
                                                                        'size': 0x8},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x20,
                                                                        'description': 'Time '
                                                                                       'Stamp '
                                                                                       'Register',
                                                                        'fields': {'field': [{'access': 'read-write',
                                                                                              'bitRange': '[15:0]',
                                                                                              'description': 'TIMSTM',
                                                                                              'name': 'TIMSTM',
                                                                                              'writeConstraint': {'range': {'maximum': 0xFFFF,
                                                                                                                            'minimum': 0x0}}}]},
                                                                        'name': 'CANSTM',
                                                                        'size': 0x10},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x16,
                                                                        'description': 'MOb '
                                                                                       'Status '
                                                                                       'Register',
                                                                        'fields': {'field': [{'access': 'read-write',
                                                                                              'bitRange': '[0:0]',
                                                                                              'description': 'Acknowledgement '
                                                                                                             'Error '
                                                                                                             'on '
                                                                                                             'MOb',
                                                                                              'name': 'AERR'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[1:1]',
                                                                                              'description': 'Form '
                                                                                                             'Error '
                                                                                                             'on '
                                                                                                             'MOb',
                                                                                              'name': 'FERR'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[2:2]',
                                                                                              'description': 'CRC '
                                                                                                             'Error '
                                                                                                             'on '
                                                                                                             'MOb',
                                                                                              'name': 'CERR'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[3:3]',
                                                                                              'description': 'Stuff '
                                                                                                             'Error '
                                                                                                             'on '
                                                                                                             'MOb',
                                                                                              'name': 'SERR'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[4:4]',
                                                                                              'description': 'Bit '
                                                                                                             'Error '
                                                                                                             'on '
                                                                                                             'MOb',
                                                                                              'name': 'BERR'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[5:5]',
                                                                                              'description': 'Receive '
                                                                                                             'OK '
                                                                                                             'on '
                                                                                                             'MOb',
                                                                                              'name': 'RXOK'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[6:6]',
                                                                                              'description': 'Transmit '
                                                                                                             'OK '
                                                                                                             'on '
                                                                                                             'MOb',
                                                                                              'name': 'TXOK'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[7:7]',
                                                                                              'description': 'Data '
                                                                                                             'Length '
                                                                                                             'Code '
                                                                                                             'Warning '
                                                                                                             'on '
                                                                                                             'MOb',
                                                                                              'name': 'DLCW'}]},
                                                                        'name': 'CANSTMOB',
                                                                        'size': 0x8},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0xD,
                                                                        'description': 'Timer '
                                                                                       'Control '
                                                                                       'Register',
                                                                        'fields': {'field': [{'access': 'read-write',
                                                                                              'bitRange': '[7:0]',
                                                                                              'description': 'Timer '
                                                                                                             'Control '
                                                                                                             'bits',
                                                                                              'name': 'TPRSC',
                                                                                              'writeConstraint': {'range': {'maximum': 0xFF,
                                                                                                                            'minimum': 0x0}}}]},
                                                                        'name': 'CANTCON',
                                                                        'size': 0x8},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x12,
                                                                        'description': 'Transmit '
                                                                                       'Error '
                                                                                       'Counter '
                                                                                       'Register',
                                                                        'fields': {'field': [{'access': 'read-write',
                                                                                              'bitRange': '[7:0]',
                                                                                              'description': 'Transmit '
                                                                                                             'Error '
                                                                                                             'Counter '
                                                                                                             'bits',
                                                                                              'name': 'TEC',
                                                                                              'writeConstraint': {'range': {'maximum': 0xFF,
                                                                                                                            'minimum': 0x0}}}]},
                                                                        'name': 'CANTEC',
                                                                        'size': 0x8},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0xE,
                                                                        'description': 'Timer '
                                                                                       'Register',
                                                                        'fields': {'field': [{'access': 'read-write',
                                                                                              'bitRange': '[15:0]',
                                                                                              'description': 'Timer '
                                                                                                             'bits',
                                                                                              'name': 'CANTIM',
                                                                                              'writeConstraint': {'range': {'maximum': 0xFFFF,
                                                                                                                            'minimum': 0x0}}}]},
                                                                        'name': 'CANTIM',
                                                                        'size': 0x10},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x10,
                                                                        'description': 'TTC '
                                                                                       'Timer '
                                                                                       'Register',
                                                                        'fields': {'field': [{'access': 'read-write',
                                                                                              'bitRange': '[15:0]',
                                                                                              'description': 'TTC '
                                                                                                             'Timer '
                                                                                                             'Count',
                                                                                              'name': 'TIMTTC',
                                                                                              'writeConstraint': {'range': {'maximum': 0xFFFF,
                                                                                                                            'minimum': 0x0}}}]},
                                                                        'name': 'CANTTC',
                                                                        'size': 0x10}]}},
                                           {'addressBlock': [{'offset': 0x0,
                                                              'size': 0x2,
                                                              'usage': 'registers'},
                                                             {'offset': 0x5,
                                                              'size': 0x1,
                                                              'usage': 'registers'},
                                                             {'offset': 0x10,
                                                              'size': 0x1,
                                                              'usage': 'registers'},
                                                             {'offset': 0x1A,
                                                              'size': 0x3,
                                                              'usage': 'registers'},
                                                             {'offset': 0x1E,
                                                              'size': 0x1,
                                                              'usage': 'registers'},
                                                             {'offset': 0x24,
                                                              'size': 0x3,
                                                              'usage': 'registers'},
                                                             {'offset': 0x28,
                                                              'size': 0x1,
                                                              'usage': 'registers'},
                                                             {'offset': 0x2B,
                                                              'size': 0x1,
                                                              'usage': 'registers'},
                                                             {'offset': 0x2D,
                                                              'size': 0x1,
                                                              'usage': 'registers'}],
                                            'baseAddress': 0x800039,
                                            'description': 'CPU Registers',
                                            'interrupt': [{'description': 'External '
                                                                          'Pin, '
                                                                          'Power-on '
                                                                          'Reset, '
                                                                          'Brown-out '
                                                                          'Reset, '
                                                                          'Watchdog '
                                                                          'Reset '
                                                                          'and '
                                                                          'JTAG '
                                                                          'AVR '
                                                                          'Reset',
                                                           'name': 'RESET',
                                                           'value': 0x0},
                                                          {'description': 'Analog '
                                                                          'Comparator '
                                                                          '0',
                                                           'name': 'ANACOMP0',
                                                           'value': 0x1},
                                                          {'description': 'Analog '
                                                                          'Comparator '
                                                                          '1',
                                                           'name': 'ANACOMP1',
                                                           'value': 0x2},
                                                          {'description': 'Analog '
                                                                          'Comparator '
                                                                          '2',
                                                           'name': 'ANACOMP2',
                                                           'value': 0x3},
                                                          {'description': 'Analog '
                                                                          'Comparator '
                                                                          '3',
                                                           'name': 'ANACOMP3',
                                                           'value': 0x4},
                                                          {'description': 'PSC '
                                                                          'Fault',
                                                           'name': 'PSC_FAULT',
                                                           'value': 0x5},
                                                          {'description': 'PSC '
                                                                          'End '
                                                                          'of '
                                                                          'Cycle',
                                                           'name': 'PSC_EC',
                                                           'value': 0x6},
                                                          {'description': 'External '
                                                                          'Interrupt '
                                                                          'Request '
                                                                          '0',
                                                           'name': 'INT0',
                                                           'value': 0x7},
                                                          {'description': 'External '
                                                                          'Interrupt '
                                                                          'Request '
                                                                          '1',
                                                           'name': 'INT1',
                                                           'value': 0x8},
                                                          {'description': 'External '
                                                                          'Interrupt '
                                                                          'Request '
                                                                          '2',
                                                           'name': 'INT2',
                                                           'value': 0x9},
                                                          {'description': 'External '
                                                                          'Interrupt '
                                                                          'Request '
                                                                          '3',
                                                           'name': 'INT3',
                                                           'value': 0xA},
                                                          {'description': 'Timer/Counter1 '
                                                                          'Capture '
                                                                          'Event',
                                                           'name': 'TIMER1_CAPT',
                                                           'value': 0xB},
                                                          {'description': 'Timer/Counter1 '
                                                                          'Compare '
                                                                          'Match '
                                                                          'A',
                                                           'name': 'TIMER1_COMPA',
                                                           'value': 0xC},
                                                          {'description': 'Timer/Counter1 '
                                                                          'Compare '
                                                                          'Match '
                                                                          'B',
                                                           'name': 'TIMER1_COMPB',
                                                           'value': 0xD},
                                                          {'description': 'Timer1/Counter1 '
                                                                          'Overflow',
                                                           'name': 'TIMER1_OVF',
                                                           'value': 0xE},
                                                          {'description': 'Timer/Counter0 '
                                                                          'Compare '
                                                                          'Match '
                                                                          'A',
                                                           'name': 'TIMER0_COMPA',
                                                           'value': 0xF},
                                                          {'description': 'Timer/Counter0 '
                                                                          'Compare '
                                                                          'Match '
                                                                          'B',
                                                           'name': 'TIMER0_COMPB',
                                                           'value': 0x10},
                                                          {'description': 'Timer/Counter0 '
                                                                          'Overflow',
                                                           'name': 'TIMER0_OVF',
                                                           'value': 0x11},
                                                          {'description': 'CAN '
                                                                          'MOB, '
                                                                          'Burst, '
                                                                          'General '
                                                                          'Errors',
                                                           'name': 'CAN_INT',
                                                           'value': 0x12},
                                                          {'description': 'CAN '
                                                                          'Timer '
                                                                          'Overflow',
                                                           'name': 'CAN_TOVF',
                                                           'value': 0x13},
                                                          {'description': 'LIN '
                                                                          'Transfer '
                                                                          'Complete',
                                                           'name': 'LIN_TC',
                                                           'value': 0x14},
                                                          {'description': 'LIN '
                                                                          'Error',
                                                           'name': 'LIN_ERR',
                                                           'value': 0x15},
                                                          {'description': 'Pin '
                                                                          'Change '
                                                                          'Interrupt '
                                                                          'Request '
                                                                          '0',
                                                           'name': 'PCINT0',
                                                           'value': 0x16},
                                                          {'description': 'Pin '
                                                                          'Change '
                                                                          'Interrupt '
                                                                          'Request '
                                                                          '1',
                                                           'name': 'PCINT1',
                                                           'value': 0x17},
                                                          {'description': 'Pin '
                                                                          'Change '
                                                                          'Interrupt '
                                                                          'Request '
                                                                          '2',
                                                           'name': 'PCINT2',
                                                           'value': 0x18},
                                                          {'description': 'Pin '
                                                                          'Change '
                                                                          'Interrupt '
                                                                          'Request '
                                                                          '3',
                                                           'name': 'PCINT3',
                                                           'value': 0x19},
                                                          {'description': 'SPI '
                                                                          'Serial '
                                                                          'Transfer '
                                                                          'Complete',
                                                           'name': 'SPI_STC',
                                                           'value': 0x1A},
                                                          {'description': 'ADC '
                                                                          'Conversion '
                                                                          'Complete',
                                                           'name': 'ADC',
                                                           'value': 0x1B},
                                                          {'description': 'Watchdog '
                                                                          'Time-Out '
                                                                          'Interrupt',
                                                           'name': 'WDT',
                                                           'value': 0x1C},
                                                          {'description': 'EEPROM '
                                                                          'Ready',
                                                           'name': 'EE_READY',
                                                           'value': 0x1D},
                                                          {'description': 'Store '
                                                                          'Program '
                                                                          'Memory '
                                                                          'Read',
                                                           'name': 'SPM_READY',
                                                           'value': 0x1E}],
                                            'name': 'CPU',
                                            'registers': {'register': [{'access': 'read-write',
                                                                        'addressOffset': 0x28,
                                                                        'description': 'No '
                                                                                       'Description.',
                                                                        'fields': {'field': [{'access': 'read-write',
                                                                                              'bitRange': '[3:0]',
                                                                                              'description': 'Clock '
                                                                                                             'Prescaler '
                                                                                                             'Select',
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
                                                                        'addressOffset': 0x5,
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
                                                                        'addressOffset': 0x0,
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
                                                                        'addressOffset': 0x1,
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
                                                                        'addressOffset': 0x1C,
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
                                                                                              'description': 'SPI '
                                                                                                             'Pin '
                                                                                                             'Select',
                                                                                              'name': 'SPIPS'}]},
                                                                        'name': 'MCUCR',
                                                                        'size': 0x8},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x1B,
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
                                                                        'addressOffset': 0x2D,
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
                                                                        'addressOffset': 0x10,
                                                                        'description': 'PLL '
                                                                                       'Control '
                                                                                       'And '
                                                                                       'Status '
                                                                                       'Register',
                                                                        'fields': {'field': [{'access': 'read-write',
                                                                                              'bitRange': '[0:0]',
                                                                                              'description': 'PLL '
                                                                                                             'Lock '
                                                                                                             'Detector',
                                                                                              'name': 'PLOCK'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[1:1]',
                                                                                              'description': 'PLL '
                                                                                                             'Enable',
                                                                                              'name': 'PLLE'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[2:2]',
                                                                                              'description': 'PLL '
                                                                                                             'Factor',
                                                                                              'name': 'PLLF'}]},
                                                                        'name': 'PLLCSR',
                                                                        'size': 0x8},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x2B,
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
                                                                                                             'LIN '
                                                                                                             'UART',
                                                                                              'name': 'PRLIN'},
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
                                                                                                             'Timer/Counter0',
                                                                                              'name': 'PRTIM0'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[4:4]',
                                                                                              'description': 'Power '
                                                                                                             'Reduction '
                                                                                                             'Timer/Counter1',
                                                                                              'name': 'PRTIM1'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[5:5]',
                                                                                              'description': 'Power '
                                                                                                             'Reduction '
                                                                                                             'PSC',
                                                                                              'name': 'PRPSC'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[6:6]',
                                                                                              'description': 'Power '
                                                                                                             'Reduction '
                                                                                                             'CAN',
                                                                                              'name': 'PRCAN'}]},
                                                                        'name': 'PRR',
                                                                        'size': 0x8},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x1A,
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
                                                                                                                                       {'description': 'Reserved',
                                                                                                                                        'name': 'VAL_0x03',
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
                                                                                                                                       {'description': 'Reserved',
                                                                                                                                        'name': 'VAL_0x07',
                                                                                                                                        'value': 0x7}]},
                                                                                              'name': 'SM',
                                                                                              'writeConstraint': {'useEnumeratedValues': 0x1}}]},
                                                                        'name': 'SMCR',
                                                                        'size': 0x8},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x24,
                                                                        'description': 'Stack '
                                                                                       'Pointer ',
                                                                        'name': 'SP',
                                                                        'size': 0x10,
                                                                        'writeConstraint': {'range': {'maximum': 0xFFFF,
                                                                                                      'minimum': 0x0}}},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x1E,
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
                                                                        'size': 0x8},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x26,
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
                                                              'size': 0x3,
                                                              'usage': 'registers'}],
                                            'baseAddress': 0x800090,
                                            'description': 'Digital-to-Analog '
                                                           'Converter',
                                            'name': 'DAC',
                                            'registers': {'register': [{'access': 'read-write',
                                                                        'addressOffset': 0x1,
                                                                        'description': 'DAC '
                                                                                       'Data '
                                                                                       'Register',
                                                                        'fields': {'field': [{'access': 'read-write',
                                                                                              'bitRange': '[15:0]',
                                                                                              'description': 'DAC '
                                                                                                             'Data '
                                                                                                             'Register '
                                                                                                             'Bits',
                                                                                              'name': 'DAC',
                                                                                              'writeConstraint': {'range': {'maximum': 0xFFFF,
                                                                                                                            'minimum': 0x0}}}]},
                                                                        'name': 'DAC',
                                                                        'size': 0x10},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x0,
                                                                        'description': 'DAC '
                                                                                       'Control '
                                                                                       'Register',
                                                                        'fields': {'field': [{'access': 'read-write',
                                                                                              'bitRange': '[0:0]',
                                                                                              'description': 'DAC '
                                                                                                             'Enable '
                                                                                                             'Bit',
                                                                                              'name': 'DAEN'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[1:1]',
                                                                                              'description': 'DAC '
                                                                                                             'Output '
                                                                                                             'Enable',
                                                                                              'name': 'DAOE'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[2:2]',
                                                                                              'description': 'DAC '
                                                                                                             'Left '
                                                                                                             'Adjust',
                                                                                              'name': 'DALA'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[6:4]',
                                                                                              'description': 'DAC '
                                                                                                             'Trigger '
                                                                                                             'Selection '
                                                                                                             'Bits',
                                                                                              'enumeratedValues': {'enumeratedValue': [{'description': 'Analog '
                                                                                                                                                       'Comparator '
                                                                                                                                                       '0',
                                                                                                                                        'name': 'ANALOG_COMPARATOR_0',
                                                                                                                                        'value': 0x0},
                                                                                                                                       {'description': 'Analog '
                                                                                                                                                       'Comparator '
                                                                                                                                                       '1',
                                                                                                                                        'name': 'ANALOG_COMPARATOR_1',
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
                                                                                              'name': 'DATS',
                                                                                              'writeConstraint': {'useEnumeratedValues': 0x1}},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[7:7]',
                                                                                              'description': 'DAC '
                                                                                                             'Auto '
                                                                                                             'Trigger '
                                                                                                             'Enable '
                                                                                                             'Bit',
                                                                                              'name': 'DAATE'}]},
                                                                        'name': 'DACON',
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
                                                                        'fields': {'field': [{'access': 'read-write',
                                                                                              'bitRange': '[9:0]',
                                                                                              'description': 'EEPROM '
                                                                                                             'Address '
                                                                                                             'bits',
                                                                                              'name': 'EEAR',
                                                                                              'writeConstraint': {'range': {'maximum': 0x3FF,
                                                                                                                            'minimum': 0x0}}}]},
                                                                        'name': 'EEAR',
                                                                        'size': 0x10},
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
                                                                                              'name': 'EEWE'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[2:2]',
                                                                                              'description': 'EEPROM '
                                                                                                             'Master '
                                                                                                             'Write '
                                                                                                             'Enable',
                                                                                              'name': 'EEMWE'},
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
                                                                                                             'mode',
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
                                                                        'fields': {'field': [{'access': 'read-write',
                                                                                              'bitRange': '[7:0]',
                                                                                              'description': 'EEPROM '
                                                                                                             'Data '
                                                                                                             'bits',
                                                                                              'name': 'EEDR',
                                                                                              'writeConstraint': {'range': {'maximum': 0xFF,
                                                                                                                            'minimum': 0x0}}}]},
                                                                        'name': 'EEDR',
                                                                        'size': 0x8}]}},
                                           {'addressBlock': [{'offset': 0x0,
                                                              'size': 0x3,
                                                              'usage': 'registers'},
                                                             {'offset': 0x2D,
                                                              'size': 0x6,
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
                                                                                                             '3 '
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
                                                                                              'bitRange': '[3:0]',
                                                                                              'description': 'Pin '
                                                                                                             'Change '
                                                                                                             'Interrupt '
                                                                                                             'Enables',
                                                                                              'name': 'PCIE',
                                                                                              'writeConstraint': {'range': {'maximum': 0xF,
                                                                                                                            'minimum': 0x0}}}]},
                                                                        'name': 'PCICR',
                                                                        'size': 0x8},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x0,
                                                                        'description': 'Pin '
                                                                                       'Change '
                                                                                       'Interrupt '
                                                                                       'Flag '
                                                                                       'Register',
                                                                        'fields': {'field': [{'access': 'read-write',
                                                                                              'bitRange': '[3:0]',
                                                                                              'description': 'Pin '
                                                                                                             'Change '
                                                                                                             'Interrupt '
                                                                                                             'Flags',
                                                                                              'name': 'PCIF',
                                                                                              'writeConstraint': {'range': {'maximum': 0xF,
                                                                                                                            'minimum': 0x0}}}]},
                                                                        'name': 'PCIFR',
                                                                        'size': 0x8},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x2F,
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
                                                                        'addressOffset': 0x30,
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
                                                                        'size': 0x8},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x31,
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
                                                                        'size': 0x8},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x32,
                                                                        'description': 'Pin '
                                                                                       'Change '
                                                                                       'Mask '
                                                                                       'Register '
                                                                                       '3',
                                                                        'fields': {'field': [{'access': 'read-write',
                                                                                              'bitRange': '[2:0]',
                                                                                              'description': 'Pin '
                                                                                                             'Change '
                                                                                                             'Enable '
                                                                                                             'Masks',
                                                                                              'name': 'PCINT',
                                                                                              'writeConstraint': {'range': {'maximum': 0x7,
                                                                                                                            'minimum': 0x0}}}]},
                                                                        'name': 'PCMSK3',
                                                                        'size': 0x8}]}},
                                           {'addressBlock': [{'offset': 0x0,
                                                              'size': 0xB,
                                                              'usage': 'registers'}],
                                            'baseAddress': 0x8000C8,
                                            'description': 'Local Interconnect '
                                                           'Network',
                                            'name': 'LINUART',
                                            'registers': {'register': [{'access': 'read-write',
                                                                        'addressOffset': 0x5,
                                                                        'description': 'LIN '
                                                                                       'Baud '
                                                                                       'Rate '
                                                                                       'Register',
                                                                        'fields': {'field': [{'access': 'read-write',
                                                                                              'bitRange': '[11:0]',
                                                                                              'description': 'No '
                                                                                                             'Description.',
                                                                                              'name': 'LDIV',
                                                                                              'writeConstraint': {'range': {'maximum': 0xFFF,
                                                                                                                            'minimum': 0x0}}}]},
                                                                        'name': 'LINBRR',
                                                                        'size': 0x10},
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
                                                                                              'description': 'LIN '
                                                                                                             'Data '
                                                                                                             'In '
                                                                                                             '/ '
                                                                                                             'Data '
                                                                                                             'out',
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
                                                                                              'name': 'PC6'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[7:7]',
                                                                                              'description': 'Pin '
                                                                                                             'C7',
                                                                                              'name': 'PC7'}]},
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
                                                                                              'name': 'PC6'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[7:7]',
                                                                                              'description': 'Pin '
                                                                                                             'C7',
                                                                                              'name': 'PC7'}]},
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
                                                                                              'name': 'PC6'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[7:7]',
                                                                                              'description': 'Pin '
                                                                                                             'C7',
                                                                                              'name': 'PC7'}]},
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
                                            'baseAddress': 0x80002C,
                                            'description': 'I/O Port',
                                            'name': 'PORTE',
                                            'registers': {'register': [{'access': 'read-write',
                                                                        'addressOffset': 0x1,
                                                                        'description': 'Port '
                                                                                       'E '
                                                                                       'Data '
                                                                                       'Direction '
                                                                                       'Register',
                                                                        'fields': {'field': [{'access': 'read-write',
                                                                                              'bitRange': '[0:0]',
                                                                                              'description': 'Pin '
                                                                                                             'E0',
                                                                                              'name': 'PE0'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[1:1]',
                                                                                              'description': 'Pin '
                                                                                                             'E1',
                                                                                              'name': 'PE1'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[2:2]',
                                                                                              'description': 'Pin '
                                                                                                             'E2',
                                                                                              'name': 'PE2'}]},
                                                                        'name': 'DDRE',
                                                                        'size': 0x8},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x0,
                                                                        'description': 'Port '
                                                                                       'E '
                                                                                       'Input '
                                                                                       'Pins '
                                                                                       '(read-only '
                                                                                       'for '
                                                                                       'debugger)',
                                                                        'fields': {'field': [{'access': 'read-write',
                                                                                              'bitRange': '[0:0]',
                                                                                              'description': 'Pin '
                                                                                                             'E0',
                                                                                              'name': 'PE0'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[1:1]',
                                                                                              'description': 'Pin '
                                                                                                             'E1',
                                                                                              'name': 'PE1'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[2:2]',
                                                                                              'description': 'Pin '
                                                                                                             'E2',
                                                                                              'name': 'PE2'}]},
                                                                        'name': 'PINE',
                                                                        'size': 0x8},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x2,
                                                                        'description': 'Port '
                                                                                       'E '
                                                                                       'Data '
                                                                                       'Register',
                                                                        'fields': {'field': [{'access': 'read-write',
                                                                                              'bitRange': '[0:0]',
                                                                                              'description': 'Pin '
                                                                                                             'E0',
                                                                                              'name': 'PE0'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[1:1]',
                                                                                              'description': 'Pin '
                                                                                                             'E1',
                                                                                              'name': 'PE1'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[2:2]',
                                                                                              'description': 'Pin '
                                                                                                             'E2',
                                                                                              'name': 'PE2'}]},
                                                                        'name': 'PORTE',
                                                                        'size': 0x8}]}},
                                           {'addressBlock': [{'offset': 0x0,
                                                              'size': 0x1D,
                                                              'usage': 'registers'}],
                                            'baseAddress': 0x8000A0,
                                            'description': 'Power Stage '
                                                           'Controller',
                                            'name': 'PSC',
                                            'registers': {'register': [{'access': 'read-write',
                                                                        'addressOffset': 0x15,
                                                                        'description': 'PSC '
                                                                                       'Configuration '
                                                                                       'Register',
                                                                        'fields': {'field': [{'access': 'read-write',
                                                                                              'bitRange': '[2:2]',
                                                                                              'description': 'PSC '
                                                                                                             'Output '
                                                                                                             'A '
                                                                                                             'Polarity',
                                                                                              'name': 'POPA'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[3:3]',
                                                                                              'description': 'PSC '
                                                                                                             'Output '
                                                                                                             'B '
                                                                                                             'Polarity',
                                                                                              'name': 'POPB'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[4:4]',
                                                                                              'description': 'PSC '
                                                                                                             'Mode',
                                                                                              'name': 'PMODE'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[5:5]',
                                                                                              'description': 'PSC '
                                                                                                             'Update '
                                                                                                             'Lock',
                                                                                              'name': 'PULOCK'}]},
                                                                        'name': 'PCNF',
                                                                        'size': 0x8},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x17,
                                                                        'description': 'PSC '
                                                                                       'Control '
                                                                                       'Register',
                                                                        'fields': {'field': [{'access': 'read-write',
                                                                                              'bitRange': '[0:0]',
                                                                                              'description': 'PSC '
                                                                                                             'Run',
                                                                                              'name': 'PRUN'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[1:1]',
                                                                                              'description': 'PSC '
                                                                                                             'Complete '
                                                                                                             'Cycle',
                                                                                              'name': 'PCCYC'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[5:5]',
                                                                                              'description': 'PSC '
                                                                                                             'Input '
                                                                                                             'Clock '
                                                                                                             'Select',
                                                                                              'name': 'PCLKSEL'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[7:6]',
                                                                                              'description': 'PSC '
                                                                                                             'Prescaler '
                                                                                                             'Select '
                                                                                                             'bits',
                                                                                              'name': 'PPRE',
                                                                                              'writeConstraint': {'range': {'maximum': 0x3,
                                                                                                                            'minimum': 0x0}}}]},
                                                                        'name': 'PCTL',
                                                                        'size': 0x8},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x1C,
                                                                        'description': 'PSC '
                                                                                       'Interrupt '
                                                                                       'Flag '
                                                                                       'Register',
                                                                        'fields': {'field': [{'access': 'read-write',
                                                                                              'bitRange': '[0:0]',
                                                                                              'description': 'PSC '
                                                                                                             'End '
                                                                                                             'of '
                                                                                                             'Cycle '
                                                                                                             'Interrupt',
                                                                                              'name': 'PEOP'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[3:1]',
                                                                                              'description': 'PSC '
                                                                                                             'External '
                                                                                                             'Event '
                                                                                                             '2 '
                                                                                                             'Interrupt',
                                                                                              'name': 'PEV',
                                                                                              'writeConstraint': {'range': {'maximum': 0x7,
                                                                                                                            'minimum': 0x0}}}]},
                                                                        'name': 'PIFR',
                                                                        'size': 0x8},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x1B,
                                                                        'description': 'PSC '
                                                                                       'Interrupt '
                                                                                       'Mask '
                                                                                       'Register',
                                                                        'fields': {'field': [{'access': 'read-write',
                                                                                              'bitRange': '[0:0]',
                                                                                              'description': 'PSC '
                                                                                                             'End '
                                                                                                             'of '
                                                                                                             'Cycle '
                                                                                                             'Interrupt '
                                                                                                             'Enable',
                                                                                              'name': 'PEOPE'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[3:1]',
                                                                                              'description': 'External '
                                                                                                             'Event '
                                                                                                             '2 '
                                                                                                             'Interrupt '
                                                                                                             'Enable',
                                                                                              'name': 'PEVE',
                                                                                              'writeConstraint': {'range': {'maximum': 0x7,
                                                                                                                            'minimum': 0x0}}}]},
                                                                        'name': 'PIM',
                                                                        'size': 0x8},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x18,
                                                                        'description': 'PSC '
                                                                                       'Module '
                                                                                       '0 '
                                                                                       'Input '
                                                                                       'Control '
                                                                                       'Register',
                                                                        'fields': {'field': [{'access': 'read-write',
                                                                                              'bitRange': '[2:0]',
                                                                                              'description': 'PSC '
                                                                                                             'Module '
                                                                                                             '0 '
                                                                                                             'Input '
                                                                                                             'Mode '
                                                                                                             'bits',
                                                                                              'name': 'PRFM0',
                                                                                              'writeConstraint': {'range': {'maximum': 0x7,
                                                                                                                            'minimum': 0x0}}},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[3:3]',
                                                                                              'description': 'PSC '
                                                                                                             'Module '
                                                                                                             '0 '
                                                                                                             'Asynchronous '
                                                                                                             'Output '
                                                                                                             'Control',
                                                                                              'name': 'PAOC0'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[4:4]',
                                                                                              'description': 'PSC '
                                                                                                             'Module '
                                                                                                             '0 '
                                                                                                             'Input '
                                                                                                             'Filter '
                                                                                                             'Enable',
                                                                                              'name': 'PFLTE0'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[5:5]',
                                                                                              'description': 'PSC '
                                                                                                             'Module '
                                                                                                             '0 '
                                                                                                             'Input '
                                                                                                             'Level '
                                                                                                             'Selector',
                                                                                              'name': 'PELEV0'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[6:6]',
                                                                                              'description': 'PSC '
                                                                                                             'Module '
                                                                                                             '0 '
                                                                                                             'Input '
                                                                                                             'Select',
                                                                                              'name': 'PISEL0'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[7:7]',
                                                                                              'description': 'PSC '
                                                                                                             'Module '
                                                                                                             '0 '
                                                                                                             'Overlap '
                                                                                                             'Enable',
                                                                                              'name': 'POVEN0'}]},
                                                                        'name': 'PMIC0',
                                                                        'size': 0x8},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x19,
                                                                        'description': 'PSC '
                                                                                       'Module '
                                                                                       '1 '
                                                                                       'Input '
                                                                                       'Control '
                                                                                       'Register',
                                                                        'fields': {'field': [{'access': 'read-write',
                                                                                              'bitRange': '[2:0]',
                                                                                              'description': 'PSC '
                                                                                                             'Module '
                                                                                                             '1 '
                                                                                                             'Input '
                                                                                                             'Mode '
                                                                                                             'bits',
                                                                                              'name': 'PRFM1',
                                                                                              'writeConstraint': {'range': {'maximum': 0x7,
                                                                                                                            'minimum': 0x0}}},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[3:3]',
                                                                                              'description': 'PSC '
                                                                                                             'Module '
                                                                                                             '1 '
                                                                                                             'Asynchronous '
                                                                                                             'Output '
                                                                                                             'Control',
                                                                                              'name': 'PAOC1'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[4:4]',
                                                                                              'description': 'PSC '
                                                                                                             'Module '
                                                                                                             '1 '
                                                                                                             'Input '
                                                                                                             'Filter '
                                                                                                             'Enable',
                                                                                              'name': 'PFLTE1'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[5:5]',
                                                                                              'description': 'PSC '
                                                                                                             'Module '
                                                                                                             '1 '
                                                                                                             'Input '
                                                                                                             'Level '
                                                                                                             'Selector',
                                                                                              'name': 'PELEV1'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[6:6]',
                                                                                              'description': 'PSC '
                                                                                                             'Module '
                                                                                                             '1 '
                                                                                                             'Input '
                                                                                                             'Select',
                                                                                              'name': 'PISEL1'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[7:7]',
                                                                                              'description': 'PSC '
                                                                                                             'Module '
                                                                                                             '1 '
                                                                                                             'Overlap '
                                                                                                             'Enable',
                                                                                              'name': 'POVEN1'}]},
                                                                        'name': 'PMIC1',
                                                                        'size': 0x8},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x1A,
                                                                        'description': 'PSC '
                                                                                       'Module '
                                                                                       '2 '
                                                                                       'Input '
                                                                                       'Control '
                                                                                       'Register',
                                                                        'fields': {'field': [{'access': 'read-write',
                                                                                              'bitRange': '[2:0]',
                                                                                              'description': 'PSC '
                                                                                                             'Module '
                                                                                                             '2 '
                                                                                                             'Input '
                                                                                                             'Mode '
                                                                                                             'bits',
                                                                                              'name': 'PRFM2',
                                                                                              'writeConstraint': {'range': {'maximum': 0x7,
                                                                                                                            'minimum': 0x0}}},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[3:3]',
                                                                                              'description': 'PSC '
                                                                                                             'Module '
                                                                                                             '2 '
                                                                                                             'Asynchronous '
                                                                                                             'Output '
                                                                                                             'Control',
                                                                                              'name': 'PAOC2'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[4:4]',
                                                                                              'description': 'PSC '
                                                                                                             'Module '
                                                                                                             '2 '
                                                                                                             'Input '
                                                                                                             'Filter '
                                                                                                             'Enable',
                                                                                              'name': 'PFLTE2'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[5:5]',
                                                                                              'description': 'PSC '
                                                                                                             'Module '
                                                                                                             '2 '
                                                                                                             'Input '
                                                                                                             'Level '
                                                                                                             'Selector',
                                                                                              'name': 'PELEV2'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[6:6]',
                                                                                              'description': 'PSC '
                                                                                                             'Module '
                                                                                                             '2 '
                                                                                                             'Input '
                                                                                                             'Select',
                                                                                              'name': 'PISEL2'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[7:7]',
                                                                                              'description': 'PSC '
                                                                                                             'Module '
                                                                                                             '2 '
                                                                                                             'Overlap '
                                                                                                             'Enable',
                                                                                              'name': 'POVEN2'}]},
                                                                        'name': 'PMIC2',
                                                                        'size': 0x8},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x16,
                                                                        'description': 'PSC '
                                                                                       'Output '
                                                                                       'Configuration',
                                                                        'fields': {'field': [{'access': 'read-write',
                                                                                              'bitRange': '[0:0]',
                                                                                              'description': 'PSC '
                                                                                                             'Output '
                                                                                                             '0A '
                                                                                                             'Enable',
                                                                                              'name': 'POEN0A'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[1:1]',
                                                                                              'description': 'PSC '
                                                                                                             'Output '
                                                                                                             '0B '
                                                                                                             'Enable',
                                                                                              'name': 'POEN0B'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[2:2]',
                                                                                              'description': 'PSC '
                                                                                                             'Output '
                                                                                                             '1A '
                                                                                                             'Enable',
                                                                                              'name': 'POEN1A'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[3:3]',
                                                                                              'description': 'PSC '
                                                                                                             'Output '
                                                                                                             '1B '
                                                                                                             'Enable',
                                                                                              'name': 'POEN1B'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[4:4]',
                                                                                              'description': 'PSC '
                                                                                                             'Output '
                                                                                                             '2A '
                                                                                                             'Enable',
                                                                                              'name': 'POEN2A'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[5:5]',
                                                                                              'description': 'PSC '
                                                                                                             'Output '
                                                                                                             '2B '
                                                                                                             'Enable',
                                                                                              'name': 'POEN2B'}]},
                                                                        'name': 'POC',
                                                                        'size': 0x8},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x2,
                                                                        'description': 'PSC '
                                                                                       'Module '
                                                                                       '0 '
                                                                                       'Output '
                                                                                       'Compare '
                                                                                       'RA '
                                                                                       'Register',
                                                                        'fields': {'field': [{'access': 'read-write',
                                                                                              'bitRange': '[11:0]',
                                                                                              'description': 'PSC '
                                                                                                             'Output '
                                                                                                             'Compare '
                                                                                                             'RA '
                                                                                                             'bits',
                                                                                              'name': 'POCR0RA',
                                                                                              'writeConstraint': {'range': {'maximum': 0xFFF,
                                                                                                                            'minimum': 0x0}}}]},
                                                                        'name': 'POCR0RA',
                                                                        'size': 0x10},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x0,
                                                                        'description': 'PSC '
                                                                                       'Module '
                                                                                       '0 '
                                                                                       'Output '
                                                                                       'Compare '
                                                                                       'SA '
                                                                                       'Register',
                                                                        'fields': {'field': [{'access': 'read-write',
                                                                                              'bitRange': '[11:0]',
                                                                                              'description': 'PSC '
                                                                                                             'Output '
                                                                                                             'Compare '
                                                                                                             'SA '
                                                                                                             'bits',
                                                                                              'name': 'POCR0SA',
                                                                                              'writeConstraint': {'range': {'maximum': 0xFFF,
                                                                                                                            'minimum': 0x0}}}]},
                                                                        'name': 'POCR0SA',
                                                                        'size': 0x10},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x4,
                                                                        'description': 'PSC '
                                                                                       'Module '
                                                                                       '0 '
                                                                                       'Output '
                                                                                       'Compare '
                                                                                       'SB '
                                                                                       'Register',
                                                                        'fields': {'field': [{'access': 'read-write',
                                                                                              'bitRange': '[11:0]',
                                                                                              'description': 'PSC '
                                                                                                             'Output '
                                                                                                             'Compare '
                                                                                                             'SB '
                                                                                                             'bits',
                                                                                              'name': 'POCR0SB',
                                                                                              'writeConstraint': {'range': {'maximum': 0xFFF,
                                                                                                                            'minimum': 0x0}}}]},
                                                                        'name': 'POCR0SB',
                                                                        'size': 0x10},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x8,
                                                                        'description': 'PSC '
                                                                                       'Module '
                                                                                       '1 '
                                                                                       'Output '
                                                                                       'Compare '
                                                                                       'RA '
                                                                                       'Register',
                                                                        'fields': {'field': [{'access': 'read-write',
                                                                                              'bitRange': '[11:0]',
                                                                                              'description': 'PSC '
                                                                                                             'Output '
                                                                                                             'Compare '
                                                                                                             'RA '
                                                                                                             'bits',
                                                                                              'name': 'POCR1RA',
                                                                                              'writeConstraint': {'range': {'maximum': 0xFFF,
                                                                                                                            'minimum': 0x0}}}]},
                                                                        'name': 'POCR1RA',
                                                                        'size': 0x10},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x6,
                                                                        'description': 'PSC '
                                                                                       'Module '
                                                                                       '1 '
                                                                                       'Output '
                                                                                       'Compare '
                                                                                       'SA '
                                                                                       'Register',
                                                                        'fields': {'field': [{'access': 'read-write',
                                                                                              'bitRange': '[11:0]',
                                                                                              'description': 'PSC '
                                                                                                             'Output '
                                                                                                             'Compare '
                                                                                                             'SA '
                                                                                                             'bits',
                                                                                              'name': 'POCR1SA',
                                                                                              'writeConstraint': {'range': {'maximum': 0xFFF,
                                                                                                                            'minimum': 0x0}}}]},
                                                                        'name': 'POCR1SA',
                                                                        'size': 0x10},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0xA,
                                                                        'description': 'PSC '
                                                                                       'Module '
                                                                                       '1 '
                                                                                       'Output '
                                                                                       'Compare '
                                                                                       'SB '
                                                                                       'Register',
                                                                        'fields': {'field': [{'access': 'read-write',
                                                                                              'bitRange': '[11:0]',
                                                                                              'description': 'PSC '
                                                                                                             'Output '
                                                                                                             'Compare '
                                                                                                             'SB '
                                                                                                             'bits',
                                                                                              'name': 'POCR1SB',
                                                                                              'writeConstraint': {'range': {'maximum': 0xFFF,
                                                                                                                            'minimum': 0x0}}}]},
                                                                        'name': 'POCR1SB',
                                                                        'size': 0x10},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0xE,
                                                                        'description': 'PSC '
                                                                                       'Module '
                                                                                       '2 '
                                                                                       'Output '
                                                                                       'Compare '
                                                                                       'RA '
                                                                                       'Register',
                                                                        'fields': {'field': [{'access': 'read-write',
                                                                                              'bitRange': '[11:0]',
                                                                                              'description': 'PSC '
                                                                                                             'Output '
                                                                                                             'Compare '
                                                                                                             'RA '
                                                                                                             'bits',
                                                                                              'name': 'POCR2RA',
                                                                                              'writeConstraint': {'range': {'maximum': 0xFFF,
                                                                                                                            'minimum': 0x0}}}]},
                                                                        'name': 'POCR2RA',
                                                                        'size': 0x10},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0xC,
                                                                        'description': 'PSC '
                                                                                       'Module '
                                                                                       '2 '
                                                                                       'Output '
                                                                                       'Compare '
                                                                                       'SA '
                                                                                       'Register',
                                                                        'fields': {'field': [{'access': 'read-write',
                                                                                              'bitRange': '[11:0]',
                                                                                              'description': 'PSC '
                                                                                                             'Output '
                                                                                                             'Compare '
                                                                                                             'SA '
                                                                                                             'bits',
                                                                                              'name': 'POCR2SA',
                                                                                              'writeConstraint': {'range': {'maximum': 0xFFF,
                                                                                                                            'minimum': 0x0}}}]},
                                                                        'name': 'POCR2SA',
                                                                        'size': 0x10},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x10,
                                                                        'description': 'PSC '
                                                                                       'Module '
                                                                                       '2 '
                                                                                       'Output '
                                                                                       'Compare '
                                                                                       'SB '
                                                                                       'Register',
                                                                        'fields': {'field': [{'access': 'read-write',
                                                                                              'bitRange': '[11:0]',
                                                                                              'description': 'PSC '
                                                                                                             'Output '
                                                                                                             'Compare '
                                                                                                             'SB '
                                                                                                             'bits',
                                                                                              'name': 'POCR2SB',
                                                                                              'writeConstraint': {'range': {'maximum': 0xFFF,
                                                                                                                            'minimum': 0x0}}}]},
                                                                        'name': 'POCR2SB',
                                                                        'size': 0x10},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x12,
                                                                        'description': 'PSC '
                                                                                       'Output '
                                                                                       'Compare '
                                                                                       'RB '
                                                                                       'Register',
                                                                        'fields': {'field': [{'access': 'read-write',
                                                                                              'bitRange': '[11:0]',
                                                                                              'description': 'PSC '
                                                                                                             'Output '
                                                                                                             'Compare '
                                                                                                             'RB '
                                                                                                             'bits',
                                                                                              'name': 'POCR_RB',
                                                                                              'writeConstraint': {'range': {'maximum': 0xFFF,
                                                                                                                            'minimum': 0x0}}}]},
                                                                        'name': 'POCR_RB',
                                                                        'size': 0x10},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x14,
                                                                        'description': 'PSC '
                                                                                       'Synchro '
                                                                                       'Configuration',
                                                                        'fields': {'field': [{'access': 'read-write',
                                                                                              'bitRange': '[1:0]',
                                                                                              'description': 'Selection '
                                                                                                             'of '
                                                                                                             'Synchronization '
                                                                                                             'Out '
                                                                                                             'for '
                                                                                                             'ADC',
                                                                                              'name': 'PSYNC0',
                                                                                              'writeConstraint': {'range': {'maximum': 0x3,
                                                                                                                            'minimum': 0x0}}},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[3:2]',
                                                                                              'description': 'Selection '
                                                                                                             'of '
                                                                                                             'Synchronization '
                                                                                                             'Out '
                                                                                                             'for '
                                                                                                             'ADC',
                                                                                              'name': 'PSYNC1',
                                                                                              'writeConstraint': {'range': {'maximum': 0x3,
                                                                                                                            'minimum': 0x0}}},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[5:4]',
                                                                                              'description': 'Selection '
                                                                                                             'of '
                                                                                                             'Synchronization '
                                                                                                             'Out '
                                                                                                             'for '
                                                                                                             'ADC',
                                                                                              'name': 'PSYNC2',
                                                                                              'writeConstraint': {'range': {'maximum': 0x3,
                                                                                                                            'minimum': 0x0}}}]},
                                                                        'name': 'PSYNC',
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
                                                                                              'description': 'Timer/Counter '
                                                                                                             'Prescaler '
                                                                                                             'Reset',
                                                                                              'name': 'PSRSYNC'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[6:6]',
                                                                                              'description': 'Timer/Counter1 '
                                                                                                             'Input '
                                                                                                             'Capture '
                                                                                                             'Selection',
                                                                                              'name': 'ICPSEL1'},
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
                                                                                       'Register '
                                                                                       'A',
                                                                        'fields': {'field': [{'access': 'read-write',
                                                                                              'bitRange': '[7:0]',
                                                                                              'description': 'Timer/Counter0 '
                                                                                                             'Output '
                                                                                                             'Compare '
                                                                                                             'bits',
                                                                                              'name': 'OCR0A',
                                                                                              'writeConstraint': {'range': {'maximum': 0xFF,
                                                                                                                            'minimum': 0x0}}}]},
                                                                        'name': 'OCR0A',
                                                                        'size': 0x8},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x13,
                                                                        'description': 'Timer/Counter0 '
                                                                                       'Output '
                                                                                       'Compare '
                                                                                       'Register '
                                                                                       'B',
                                                                        'fields': {'field': [{'access': 'read-write',
                                                                                              'bitRange': '[7:0]',
                                                                                              'description': 'Timer/Counter0 '
                                                                                                             'Output '
                                                                                                             'Compare '
                                                                                                             'bits',
                                                                                              'name': 'OCR0B',
                                                                                              'writeConstraint': {'range': {'maximum': 0xFF,
                                                                                                                            'minimum': 0x0}}}]},
                                                                        'name': 'OCR0B',
                                                                        'size': 0x8},
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
                                                                                                             'Mode '
                                                                                                             'for '
                                                                                                             'Channel '
                                                                                                             'B',
                                                                                              'name': 'COM0B',
                                                                                              'writeConstraint': {'range': {'maximum': 0x3,
                                                                                                                            'minimum': 0x0}}},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[7:6]',
                                                                                              'description': 'Compare '
                                                                                                             'Output '
                                                                                                             'Mode '
                                                                                                             'for '
                                                                                                             'Channel '
                                                                                                             'A',
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
                                                                        'fields': {'field': [{'access': 'read-write',
                                                                                              'bitRange': '[7:0]',
                                                                                              'description': 'Timer/Counter0 '
                                                                                                             'bits',
                                                                                              'name': 'TCNT0',
                                                                                              'writeConstraint': {'range': {'maximum': 0xFF,
                                                                                                                            'minimum': 0x0}}}]},
                                                                        'name': 'TCNT0',
                                                                        'size': 0x8},
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
                                                                                              'description': 'Timer/Counter '
                                                                                                             'Prescaler '
                                                                                                             'Reset',
                                                                                              'name': 'PSRSYNC'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[6:6]',
                                                                                              'description': 'Timer/Counter1 '
                                                                                                             'Input '
                                                                                                             'Capture '
                                                                                                             'Selection',
                                                                                              'name': 'ICPSEL1'},
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
                                                                                       'Register',
                                                                        'fields': {'field': [{'access': 'read-write',
                                                                                              'bitRange': '[15:0]',
                                                                                              'description': 'Timer/Counter1 '
                                                                                                             'Input '
                                                                                                             'Capture '
                                                                                                             'bits',
                                                                                              'name': 'ICR1',
                                                                                              'writeConstraint': {'range': {'maximum': 0xFFFF,
                                                                                                                            'minimum': 0x0}}}]},
                                                                        'name': 'ICR1',
                                                                        'size': 0x10},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x52,
                                                                        'description': 'Timer/Counter1 '
                                                                                       'Output '
                                                                                       'Compare '
                                                                                       'Register '
                                                                                       'A',
                                                                        'fields': {'field': [{'access': 'read-write',
                                                                                              'bitRange': '[15:0]',
                                                                                              'description': 'Timer/Counter1 '
                                                                                                             'Output '
                                                                                                             'Compare '
                                                                                                             'bits',
                                                                                              'name': 'OCR1A',
                                                                                              'writeConstraint': {'range': {'maximum': 0xFFFF,
                                                                                                                            'minimum': 0x0}}}]},
                                                                        'name': 'OCR1A',
                                                                        'size': 0x10},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x54,
                                                                        'description': 'Timer/Counter1 '
                                                                                       'Output '
                                                                                       'Compare '
                                                                                       'Register '
                                                                                       'B',
                                                                        'fields': {'field': [{'access': 'read-write',
                                                                                              'bitRange': '[15:0]',
                                                                                              'description': 'Timer/Counter1 '
                                                                                                             'Output '
                                                                                                             'Compare '
                                                                                                             'bits',
                                                                                              'name': 'OCR1B',
                                                                                              'writeConstraint': {'range': {'maximum': 0xFFFF,
                                                                                                                            'minimum': 0x0}}}]},
                                                                        'name': 'OCR1B',
                                                                        'size': 0x10},
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
                                                                                                             'for '
                                                                                                             'Channel '
                                                                                                             'B',
                                                                                              'name': 'COM1B',
                                                                                              'writeConstraint': {'range': {'maximum': 0x3,
                                                                                                                            'minimum': 0x0}}},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[7:6]',
                                                                                              'description': 'Compare '
                                                                                                             'Output '
                                                                                                             'Mode '
                                                                                                             'for '
                                                                                                             'Channel '
                                                                                                             'A',
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
                                                                                              'description': 'Force '
                                                                                                             'Output '
                                                                                                             'Compare '
                                                                                                             'for '
                                                                                                             'Channel '
                                                                                                             'B',
                                                                                              'name': 'FOC1B'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[7:7]',
                                                                                              'description': 'Force '
                                                                                                             'Output '
                                                                                                             'Compare '
                                                                                                             'for '
                                                                                                             'Channel '
                                                                                                             'A',
                                                                                              'name': 'FOC1A'}]},
                                                                        'name': 'TCCR1C',
                                                                        'size': 0x8},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x4E,
                                                                        'description': 'Timer/Counter1 '
                                                                                       'Bytes',
                                                                        'fields': {'field': [{'access': 'read-write',
                                                                                              'bitRange': '[15:0]',
                                                                                              'description': 'Timer/Counter1 '
                                                                                                             'bits',
                                                                                              'name': 'TCNT1',
                                                                                              'writeConstraint': {'range': {'maximum': 0xFFFF,
                                                                                                                            'minimum': 0x0}}}]},
                                                                        'name': 'TCNT1',
                                                                        'size': 0x10},
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