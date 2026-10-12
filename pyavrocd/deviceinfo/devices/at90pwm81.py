# Device description for at90pwm81, generated from Microchip's AT90PWM81.atdf by
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
    'name': 'at90pwm81',
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
    'flash_page_size_bytes': 0x40,
    'flash_read_size_bytes': 0x02,
    'flash_write_size_bytes': 0x40,
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
    'internal_sram_size_bytes': 0x0100,
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
    'eear_base' : 0x1E,
    'eear_size' : 2,
    'eecr_base' : 0x1C,
    'eedr_base' : 0x1D,
    'spmcsr_base' : 0x57,
    'osccal_base' : 0x68,
    'dwen_base' : 0x01,
    'dwen_mask' : 0x40,
    'bootrst_base' : 0x01,
    'bootrst_mask' : 0x01,
    'eesave_base' : 0x01,
    'eesave_mask' : 0x08,
    'masked_registers' : [0x51, 0x56, 0x58],
    'ronly_registers' : [0x20, 0x22, 0x23, 0x26, 0x29, 0x2c, 0x38, 0x40, 0x82, 0x83, 0x88],
    'device_id': 0x1E9388,
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
            'name': 'AT90PWM81',
            'peripherals': {'peripheral': [{'addressBlock': [{'offset': 0x0,
                                                              'size': 0x1,
                                                              'usage': 'registers'},
                                                             {'offset': 0x5A,
                                                              'size': 0x6,
                                                              'usage': 'registers'}],
                                            'baseAddress': 0x800020,
                                            'description': 'Analog Comparator',
                                            'name': 'AC',
                                            'registers': {'register': [{'access': 'read-write',
                                                                        'addressOffset': 0x5D,
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
                                                                        'addressOffset': 0x5A,
                                                                        'description': 'No '
                                                                                       'Description.',
                                                                        'fields': {'field': [{'access': 'read-write',
                                                                                              'bitRange': '[2:0]',
                                                                                              'description': 'Analog '
                                                                                                             'Comparator '
                                                                                                             'Hysteresis '
                                                                                                             'Select',
                                                                                              'name': 'AC1H',
                                                                                              'writeConstraint': {'range': {'maximum': 0x7,
                                                                                                                            'minimum': 0x0}}},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[3:3]',
                                                                                              'description': 'Analog '
                                                                                                             'Comparator '
                                                                                                             'Interrupt '
                                                                                                             'Capture '
                                                                                                             'Enable',
                                                                                              'name': 'AC1ICE'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[4:4]',
                                                                                              'description': 'Analog '
                                                                                                             'Comparator '
                                                                                                             'Output '
                                                                                                             'Enable',
                                                                                              'name': 'AC1OE'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[5:5]',
                                                                                              'description': 'Analog '
                                                                                                             'Comparator '
                                                                                                             'Output '
                                                                                                             'Invert',
                                                                                              'name': 'AC1OI'}]},
                                                                        'name': 'AC1ECON',
                                                                        'size': 0x8},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x5E,
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
                                                                        'addressOffset': 0x5B,
                                                                        'description': 'No '
                                                                                       'Description.',
                                                                        'fields': {'field': [{'access': 'read-write',
                                                                                              'bitRange': '[2:0]',
                                                                                              'description': 'Analog '
                                                                                                             'Comparator '
                                                                                                             'Hysteresis '
                                                                                                             'Select',
                                                                                              'name': 'AC2H',
                                                                                              'writeConstraint': {'range': {'maximum': 0x7,
                                                                                                                            'minimum': 0x0}}},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[4:4]',
                                                                                              'description': 'Analog '
                                                                                                             'Comparator '
                                                                                                             'Output '
                                                                                                             'Enable',
                                                                                              'name': 'AC2OE'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[5:5]',
                                                                                              'description': 'Analog '
                                                                                                             'Comparator '
                                                                                                             'Output '
                                                                                                             'Invert',
                                                                                              'name': 'AC2OI'}]},
                                                                        'name': 'AC2ECON',
                                                                        'size': 0x8},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x5F,
                                                                        'description': 'Analog '
                                                                                       'Comparator3 '
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
                                                                                              'bitRange': '[3:3]',
                                                                                              'description': 'Analog '
                                                                                                             'Comparator '
                                                                                                             '3 '
                                                                                                             'Alternate '
                                                                                                             'Output '
                                                                                                             'Enable',
                                                                                              'name': 'AC3OEA'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[5:4]',
                                                                                              'description': 'Analog '
                                                                                                             'Comparator '
                                                                                                             '3  '
                                                                                                             'Interrupt '
                                                                                                             'Select '
                                                                                                             'Bit',
                                                                                              'name': 'AC3IS',
                                                                                              'writeConstraint': {'range': {'maximum': 0x3,
                                                                                                                            'minimum': 0x0}}},
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
                                                                                                             'Comparator3 '
                                                                                                             'Enable '
                                                                                                             'Bit',
                                                                                              'name': 'AC3EN'}]},
                                                                        'name': 'AC3CON',
                                                                        'size': 0x8},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x5C,
                                                                        'description': 'No '
                                                                                       'Description.',
                                                                        'fields': {'field': [{'access': 'read-write',
                                                                                              'bitRange': '[2:0]',
                                                                                              'description': 'Analog '
                                                                                                             'Comparator '
                                                                                                             'Hysteresis '
                                                                                                             'Select',
                                                                                              'name': 'AC3H',
                                                                                              'writeConstraint': {'range': {'maximum': 0x7,
                                                                                                                            'minimum': 0x0}}},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[4:4]',
                                                                                              'description': 'Analog '
                                                                                                             'Comparator '
                                                                                                             'Output '
                                                                                                             'Enable',
                                                                                              'name': 'AC3OE'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[5:5]',
                                                                                              'description': 'Analog '
                                                                                                             'Comparator '
                                                                                                             'Output '
                                                                                                             'Invert',
                                                                                              'name': 'AC3OI'}]},
                                                                        'name': 'AC3ECON',
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
                                                              'size': 0x3,
                                                              'usage': 'registers'},
                                                             {'offset': 0x26,
                                                              'size': 0x2,
                                                              'usage': 'registers'},
                                                             {'offset': 0x51,
                                                              'size': 0x3,
                                                              'usage': 'registers'}],
                                            'baseAddress': 0x800026,
                                            'description': 'Analog-to-Digital '
                                                           'Converter',
                                            'name': 'ADC',
                                            'registers': {'register': [{'access': 'read-write',
                                                                        'addressOffset': 0x26,
                                                                        'description': 'ADC '
                                                                                       'Data '
                                                                                       'Register '
                                                                                       'Bytes',
                                                                        'fields': {'field': [{'access': 'read-write',
                                                                                              'bitRange': '[15:0]',
                                                                                              'description': 'ADC '
                                                                                                             'Data '
                                                                                                             'Register',
                                                                                              'name': 'ADC',
                                                                                              'writeConstraint': {'range': {'maximum': 0xFFFF,
                                                                                                                            'minimum': 0x0}}}]},
                                                                        'name': 'ADC',
                                                                        'size': 0x10},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x0,
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
                                                                        'addressOffset': 0x1,
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
                                                                                              'bitRange': '[4:4]',
                                                                                              'description': 'ADC '
                                                                                                             'Single '
                                                                                                             'Shot '
                                                                                                             'Enable '
                                                                                                             'on '
                                                                                                             "PSC's "
                                                                                                             'Synchronisation '
                                                                                                             'Signals',
                                                                                              'name': 'ADSSEN'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[6:6]',
                                                                                              'description': 'ADC '
                                                                                                             'Noise '
                                                                                                             'Canceller '
                                                                                                             'Disable',
                                                                                              'name': 'ADNCDIS'},
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
                                                                        'addressOffset': 0x2,
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
                                                                        'addressOffset': 0x53,
                                                                        'description': 'No '
                                                                                       'Description.',
                                                                        'fields': {'field': [{'access': 'read-write',
                                                                                              'bitRange': '[1:0]',
                                                                                              'description': 'No '
                                                                                                             'Description.',
                                                                                              'name': 'AMP0TS',
                                                                                              'writeConstraint': {'range': {'maximum': 0x3,
                                                                                                                            'minimum': 0x0}}},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[3:3]',
                                                                                              'description': 'No '
                                                                                                             'Description.',
                                                                                              'name': 'AMP0GS'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[5:4]',
                                                                                              'description': 'No '
                                                                                                             'Description.',
                                                                                              'name': 'AMP0G',
                                                                                              'writeConstraint': {'range': {'maximum': 0x3,
                                                                                                                            'minimum': 0x0}}},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[6:6]',
                                                                                              'description': 'No '
                                                                                                             'Description.',
                                                                                              'name': 'AMP0IS'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[7:7]',
                                                                                              'description': 'No '
                                                                                                             'Description.',
                                                                                              'name': 'AMP0EN'}]},
                                                                        'name': 'AMP0CSR',
                                                                        'size': 0x8},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x51,
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
                                                                                              'description': 'ADC7 '
                                                                                                             'Digital '
                                                                                                             'input '
                                                                                                             'Disable',
                                                                                              'name': 'ADC7D'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[7:7]',
                                                                                              'description': 'ADC8 '
                                                                                                             'Digital '
                                                                                                             'input '
                                                                                                             'Disable',
                                                                                              'name': 'ADC8D'}]},
                                                                        'name': 'DIDR0',
                                                                        'size': 0x8},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x52,
                                                                        'description': 'Digital '
                                                                                       'Input '
                                                                                       'Disable '
                                                                                       'Register '
                                                                                       '1',
                                                                        'fields': {'field': [{'access': 'read-write',
                                                                                              'bitRange': '[0:0]',
                                                                                              'description': 'ADC9 '
                                                                                                             'Digital '
                                                                                                             'input '
                                                                                                             'Disable',
                                                                                              'name': 'ADC9D'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[1:1]',
                                                                                              'description': 'ADC10 '
                                                                                                             'Digital '
                                                                                                             'input '
                                                                                                             'Disable',
                                                                                              'name': 'ADC10D'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[2:2]',
                                                                                              'description': 'No '
                                                                                                             'Description.',
                                                                                              'name': 'AMP0PD'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[3:3]',
                                                                                              'description': 'No '
                                                                                                             'Description.',
                                                                                              'name': 'ACMP1MD'}]},
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
                                                              'size': 0x3,
                                                              'usage': 'registers'},
                                                             {'offset': 0x1A,
                                                              'size': 0x3,
                                                              'usage': 'registers'},
                                                             {'offset': 0x24,
                                                              'size': 0x3,
                                                              'usage': 'registers'},
                                                             {'offset': 0x47,
                                                              'size': 0x2,
                                                              'usage': 'registers'},
                                                             {'offset': 0x4A,
                                                              'size': 0x6,
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
                                                          {'description': 'PSC2 '
                                                                          'Capture '
                                                                          'Event',
                                                           'name': 'PSC2_CAPT',
                                                           'value': 0x1},
                                                          {'description': 'PSC2 '
                                                                          'End '
                                                                          'Cycle',
                                                           'name': 'PSC2_EC',
                                                           'value': 0x2},
                                                          {'description': 'PSC2 '
                                                                          'End '
                                                                          'Of '
                                                                          'Enhanced '
                                                                          'Cycle',
                                                           'name': 'PSC2_EEC',
                                                           'value': 0x3},
                                                          {'description': 'PSC0 '
                                                                          'Capture '
                                                                          'Event',
                                                           'name': 'PSC0_CAPT',
                                                           'value': 0x4},
                                                          {'description': 'PSC0 '
                                                                          'End '
                                                                          'Cycle',
                                                           'name': 'PSC0_EC',
                                                           'value': 0x5},
                                                          {'description': 'PSC0 '
                                                                          'End '
                                                                          'Of '
                                                                          'Enhanced '
                                                                          'Cycle',
                                                           'name': 'PSC0_EEC',
                                                           'value': 0x6},
                                                          {'description': 'Analog '
                                                                          'Comparator '
                                                                          '1',
                                                           'name': 'ANALOG_COMP_1',
                                                           'value': 0x7},
                                                          {'description': 'Analog '
                                                                          'Comparator '
                                                                          '2',
                                                           'name': 'ANALOG_COMP_2',
                                                           'value': 0x8},
                                                          {'description': 'Analog '
                                                                          'Comparator '
                                                                          '3',
                                                           'name': 'ANALOG_COMP_3',
                                                           'value': 0x9},
                                                          {'description': 'External '
                                                                          'Interrupt '
                                                                          'Request '
                                                                          '0',
                                                           'name': 'INT0',
                                                           'value': 0xA},
                                                          {'description': 'Timer/Counter1 '
                                                                          'Capture '
                                                                          'Event',
                                                           'name': 'TIMER1_CAPT',
                                                           'value': 0xB},
                                                          {'description': 'Timer/Counter1 '
                                                                          'Overflow',
                                                           'name': 'TIMER1_OVF',
                                                           'value': 0xC},
                                                          {'description': 'ADC '
                                                                          'Conversion '
                                                                          'Complete',
                                                           'name': 'ADC',
                                                           'value': 0xD},
                                                          {'description': 'External '
                                                                          'Interrupt '
                                                                          'Request '
                                                                          '1',
                                                           'name': 'INT1',
                                                           'value': 0xE},
                                                          {'description': 'SPI '
                                                                          'Serial '
                                                                          'Transfer '
                                                                          'Complet',
                                                           'name': 'SPI_STC',
                                                           'value': 0xF},
                                                          {'description': 'External '
                                                                          'Interrupt '
                                                                          'Request '
                                                                          '2',
                                                           'name': 'INT2',
                                                           'value': 0x10},
                                                          {'description': 'Watchdog '
                                                                          'Timeout '
                                                                          'Interrupt',
                                                           'name': 'WDT',
                                                           'value': 0x11},
                                                          {'description': 'EEPROM '
                                                                          'Ready',
                                                           'name': 'EE_READY',
                                                           'value': 0x12},
                                                          {'description': 'Store '
                                                                          'Program '
                                                                          'Memory '
                                                                          'Read',
                                                           'name': 'SPM_READY',
                                                           'value': 0x13}],
                                            'name': 'CPU',
                                            'registers': {'register': [{'access': 'read-write',
                                                                        'addressOffset': 0x48,
                                                                        'description': 'BandGap '
                                                                                       'Current '
                                                                                       'Calibration '
                                                                                       'Register',
                                                                        'fields': {'field': [{'access': 'read-write',
                                                                                              'bitRange': '[3:0]',
                                                                                              'description': 'No '
                                                                                                             'Description.',
                                                                                              'name': 'BGCC',
                                                                                              'writeConstraint': {'range': {'maximum': 0xF,
                                                                                                                            'minimum': 0x0}}}]},
                                                                        'name': 'BGCCR',
                                                                        'size': 0x8},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x47,
                                                                        'description': 'BandGap '
                                                                                       'Resistor '
                                                                                       'Calibration '
                                                                                       'Register',
                                                                        'fields': {'field': [{'access': 'read-write',
                                                                                              'bitRange': '[3:0]',
                                                                                              'description': 'No '
                                                                                                             'Description.',
                                                                                              'name': 'BGCR',
                                                                                              'writeConstraint': {'range': {'maximum': 0xF,
                                                                                                                            'minimum': 0x0}}}]},
                                                                        'name': 'BGCRR',
                                                                        'size': 0x8},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x4B,
                                                                        'description': 'No '
                                                                                       'Description.',
                                                                        'fields': {'field': [{'access': 'read-write',
                                                                                              'bitRange': '[3:0]',
                                                                                              'description': 'Clock '
                                                                                                             'Control',
                                                                                              'name': 'CLKC',
                                                                                              'writeConstraint': {'range': {'maximum': 0xF,
                                                                                                                            'minimum': 0x0}}},
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
                                                                        'addressOffset': 0x4A,
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
                                                                        'addressOffset': 0x4C,
                                                                        'description': 'No '
                                                                                       'Description.',
                                                                        'fields': {'field': [{'access': 'read-write',
                                                                                              'bitRange': '[3:0]',
                                                                                              'description': 'Clock '
                                                                                                             'Source '
                                                                                                             'Select',
                                                                                              'name': 'CKSEL',
                                                                                              'writeConstraint': {'range': {'maximum': 0xF,
                                                                                                                            'minimum': 0x0}}},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[5:4]',
                                                                                              'description': 'Clock '
                                                                                                             'Start '
                                                                                                             'up '
                                                                                                             'Time',
                                                                                              'name': 'CSUT',
                                                                                              'writeConstraint': {'range': {'maximum': 0x3,
                                                                                                                            'minimum': 0x0}}},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[6:6]',
                                                                                              'description': 'Clock '
                                                                                                             'OUT',
                                                                                              'name': 'COUT'}]},
                                                                        'name': 'CLKSELR',
                                                                        'size': 0x8},
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
                                                                        'addressOffset': 0x1,
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
                                                                        'addressOffset': 0x2,
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
                                                                                              'bitRange': '[2:2]',
                                                                                              'description': 'Frequency '
                                                                                                             'Selection '
                                                                                                             'of '
                                                                                                             'the '
                                                                                                             'Calibrated '
                                                                                                             'RC '
                                                                                                             'Oscillator',
                                                                                              'name': 'CKRC81'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[3:3]',
                                                                                              'description': 'Reset '
                                                                                                             'Pin '
                                                                                                             'Disable',
                                                                                              'name': 'RSTDIS'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[4:4]',
                                                                                              'description': 'Pull-up '
                                                                                                             'disable',
                                                                                              'name': 'PUD'}]},
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
                                                                        'addressOffset': 0x4F,
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
                                                                        'addressOffset': 0x4E,
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
                                                                                              'bitRange': '[5:2]',
                                                                                              'description': 'No '
                                                                                                             'Description.',
                                                                                              'name': 'PLLF',
                                                                                              'writeConstraint': {'range': {'maximum': 0xF,
                                                                                                                            'minimum': 0x0}}}]},
                                                                        'name': 'PLLCSR',
                                                                        'size': 0x8},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x4D,
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
                                                                                              'bitRange': '[2:2]',
                                                                                              'description': 'Power '
                                                                                                             'Reduction '
                                                                                                             'Serial '
                                                                                                             'Peripheral '
                                                                                                             'Interface',
                                                                                              'name': 'PRSPI'},
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
                                                                                                             'PSC0',
                                                                                              'name': 'PRPSCR'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[7:7]',
                                                                                              'description': 'Power '
                                                                                                             'Reduction '
                                                                                                             'PSC2',
                                                                                              'name': 'PRPSC2'}]},
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
                                                              'size': 0x2,
                                                              'usage': 'registers'},
                                                             {'offset': 0x1E,
                                                              'size': 0x1,
                                                              'usage': 'registers'}],
                                            'baseAddress': 0x800058,
                                            'description': 'Digital-to-Analog '
                                                           'Converter',
                                            'name': 'DAC',
                                            'registers': {'register': [{'access': 'read-write',
                                                                        'addressOffset': 0x0,
                                                                        'description': 'DAC '
                                                                                       'Data '
                                                                                       'Register '
                                                                                       '(write-only '
                                                                                       'for '
                                                                                       'debugger)',
                                                                        'fields': {'field': [{'access': 'read-write',
                                                                                              'bitRange': '[9:0]',
                                                                                              'description': 'DAC '
                                                                                                             'Data '
                                                                                                             'Register '
                                                                                                             'Bits',
                                                                                              'name': 'DACH',
                                                                                              'writeConstraint': {'range': {'maximum': 0x3FF,
                                                                                                                            'minimum': 0x0}}}]},
                                                                        'name': 'DAC',
                                                                        'size': 0x10},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x1E,
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
                                            'baseAddress': 0x80003C,
                                            'description': 'EEPROM',
                                            'name': 'EEPROM',
                                            'registers': {'register': [{'access': 'read-write',
                                                                        'addressOffset': 0x2,
                                                                        'description': 'EEPROM '
                                                                                       'Read/Write '
                                                                                       'Access '
                                                                                       'Bytes',
                                                                        'fields': {'field': [{'access': 'read-write',
                                                                                              'bitRange': '[8:0]',
                                                                                              'description': 'EEPROM '
                                                                                                             'Address '
                                                                                                             'bytes',
                                                                                              'name': 'EEAR',
                                                                                              'writeConstraint': {'range': {'maximum': 0x1FF,
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
                                                                                                             'Mode',
                                                                                              'name': 'EEPM',
                                                                                              'writeConstraint': {'range': {'maximum': 0x3,
                                                                                                                            'minimum': 0x0}}},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[6:6]',
                                                                                              'description': 'EEPROM '
                                                                                                             'Page '
                                                                                                             'Access',
                                                                                              'name': 'EEPAGE'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[7:7]',
                                                                                              'description': 'None '
                                                                                                             'Volatile '
                                                                                                             'Busy '
                                                                                                             'Memory '
                                                                                                             'Busy',
                                                                                              'name': 'NVMBSY'}]},
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
                                                              'size': 0x2,
                                                              'usage': 'registers'},
                                                             {'offset': 0x49,
                                                              'size': 0x1,
                                                              'usage': 'registers'}],
                                            'baseAddress': 0x800040,
                                            'description': 'External '
                                                           'Interrupts',
                                            'name': 'EXINT',
                                            'registers': {'register': [{'access': 'read-write',
                                                                        'addressOffset': 0x49,
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
                                                                                              'writeConstraint': {'useEnumeratedValues': 0x1}}]},
                                                                        'name': 'EICRA',
                                                                        'size': 0x8},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x0,
                                                                        'description': 'External '
                                                                                       'Interrupt '
                                                                                       'Flag '
                                                                                       'Register '
                                                                                       '(read-only '
                                                                                       'for '
                                                                                       'debugger)',
                                                                        'fields': {'field': [{'access': 'read-write',
                                                                                              'bitRange': '[2:0]',
                                                                                              'description': 'External '
                                                                                                             'Interrupt '
                                                                                                             'Flags',
                                                                                              'name': 'INTF',
                                                                                              'writeConstraint': {'range': {'maximum': 0x7,
                                                                                                                            'minimum': 0x0}}}]},
                                                                        'name': 'EIFR',
                                                                        'size': 0x8},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x1,
                                                                        'description': 'External '
                                                                                       'Interrupt '
                                                                                       'Mask '
                                                                                       'Register',
                                                                        'fields': {'field': [{'access': 'read-write',
                                                                                              'bitRange': '[2:0]',
                                                                                              'description': 'External '
                                                                                                             'Interrupt '
                                                                                                             'Request '
                                                                                                             '2 '
                                                                                                             'Enable',
                                                                                              'name': 'INT',
                                                                                              'writeConstraint': {'range': {'maximum': 0x7,
                                                                                                                            'minimum': 0x0}}}]},
                                                                        'name': 'EIMSK',
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
                                                                        'description': 'Port '
                                                                                       'E '
                                                                                       'Data '
                                                                                       'Direction '
                                                                                       'Register',
                                                                        'name': 'DDRE',
                                                                        'size': 0x8,
                                                                        'writeConstraint': {'range': {'maximum': 0xFF,
                                                                                                      'minimum': 0x0}}},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x0,
                                                                        'description': 'Port '
                                                                                       'E '
                                                                                       'Input '
                                                                                       'Pins '
                                                                                       '(read-only '
                                                                                       'for '
                                                                                       'debugger)',
                                                                        'name': 'PINE',
                                                                        'size': 0x8,
                                                                        'writeConstraint': {'range': {'maximum': 0xFF,
                                                                                                      'minimum': 0x0}}},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x2,
                                                                        'description': 'Port '
                                                                                       'E '
                                                                                       'Data '
                                                                                       'Register',
                                                                        'name': 'PORTE',
                                                                        'size': 0x8,
                                                                        'writeConstraint': {'range': {'maximum': 0xFF,
                                                                                                      'minimum': 0x0}}}]}},
                                           {'addressBlock': [{'offset': 0x0,
                                                              'size': 0x4,
                                                              'usage': 'registers'},
                                                             {'offset': 0x13,
                                                              'size': 0x4,
                                                              'usage': 'registers'},
                                                             {'offset': 0x1B,
                                                              'size': 0x2,
                                                              'usage': 'registers'},
                                                             {'offset': 0x31,
                                                              'size': 0x4,
                                                              'usage': 'registers'},
                                                             {'offset': 0x39,
                                                              'size': 0x3,
                                                              'usage': 'registers'}],
                                            'baseAddress': 0x80002F,
                                            'description': 'Power Stage '
                                                           'Controller',
                                            'name': 'PSC0',
                                            'registers': {'register': [{'access': 'read-write',
                                                                        'addressOffset': 0x1B,
                                                                        'description': 'Output '
                                                                                       'Compare '
                                                                                       'RA '
                                                                                       'Register ',
                                                                        'fields': {'field': [{'access': 'read-write',
                                                                                              'bitRange': '[11:0]',
                                                                                              'description': 'Output '
                                                                                                             'Compare '
                                                                                                             '0 '
                                                                                                             'RA',
                                                                                              'name': 'OCR0RA',
                                                                                              'writeConstraint': {'range': {'maximum': 0xFFF,
                                                                                                                            'minimum': 0x0}}}]},
                                                                        'name': 'OCR0RA',
                                                                        'size': 0x10},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x15,
                                                                        'description': 'Output '
                                                                                       'Compare '
                                                                                       'RB '
                                                                                       'Register ',
                                                                        'fields': {'field': [{'access': 'read-write',
                                                                                              'bitRange': '[15:0]',
                                                                                              'description': 'Output '
                                                                                                             'Compare '
                                                                                                             '0 '
                                                                                                             'RB',
                                                                                              'name': 'OCR0RB',
                                                                                              'writeConstraint': {'range': {'maximum': 0xFFFF,
                                                                                                                            'minimum': 0x0}}}]},
                                                                        'name': 'OCR0RB',
                                                                        'size': 0x10},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x31,
                                                                        'description': 'Output '
                                                                                       'Compare '
                                                                                       'SA '
                                                                                       'Register ',
                                                                        'fields': {'field': [{'access': 'read-write',
                                                                                              'bitRange': '[11:0]',
                                                                                              'description': 'Output '
                                                                                                             'Compare '
                                                                                                             '0 '
                                                                                                             'SA',
                                                                                              'name': 'OCR0SA',
                                                                                              'writeConstraint': {'range': {'maximum': 0xFFF,
                                                                                                                            'minimum': 0x0}}}]},
                                                                        'name': 'OCR0SA',
                                                                        'size': 0x10},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x13,
                                                                        'description': 'Output '
                                                                                       'Compare '
                                                                                       'SB '
                                                                                       'Register ',
                                                                        'fields': {'field': [{'access': 'read-write',
                                                                                              'bitRange': '[11:0]',
                                                                                              'description': 'Output '
                                                                                                             'Compare '
                                                                                                             '0 '
                                                                                                             'SB',
                                                                                              'name': 'OCR0SB',
                                                                                              'writeConstraint': {'range': {'maximum': 0xFFF,
                                                                                                                            'minimum': 0x0}}}]},
                                                                        'name': 'OCR0SB',
                                                                        'size': 0x10},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x2,
                                                                        'description': 'PSC '
                                                                                       '0 '
                                                                                       'Configuration '
                                                                                       'Register',
                                                                        'fields': {'field': [{'access': 'read-write',
                                                                                              'bitRange': '[1:1]',
                                                                                              'description': 'PSC '
                                                                                                             '0 '
                                                                                                             'Input '
                                                                                                             'Clock '
                                                                                                             'Select',
                                                                                              'name': 'PCLKSEL0'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[2:2]',
                                                                                              'description': 'PSC '
                                                                                                             '0 '
                                                                                                             'Output '
                                                                                                             'Polarity',
                                                                                              'name': 'POP0'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[4:3]',
                                                                                              'description': 'PSC '
                                                                                                             '0 '
                                                                                                             'Mode',
                                                                                              'name': 'PMODE0',
                                                                                              'writeConstraint': {'range': {'maximum': 0x3,
                                                                                                                            'minimum': 0x0}}},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[5:5]',
                                                                                              'description': 'PSC '
                                                                                                             '0 '
                                                                                                             'Lock',
                                                                                              'name': 'PLOCK0'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[6:6]',
                                                                                              'description': 'PSC '
                                                                                                             '0 '
                                                                                                             'Autolock',
                                                                                              'name': 'PALOCK0'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[7:7]',
                                                                                              'description': 'PSC '
                                                                                                             '0 '
                                                                                                             'Fifty',
                                                                                              'name': 'PFIFTY0'}]},
                                                                        'name': 'PCNF0',
                                                                        'size': 0x8},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x3,
                                                                        'description': 'PSC '
                                                                                       '0 '
                                                                                       'Control '
                                                                                       'Register',
                                                                        'fields': {'field': [{'access': 'read-write',
                                                                                              'bitRange': '[0:0]',
                                                                                              'description': 'PSC '
                                                                                                             '0 '
                                                                                                             'Run',
                                                                                              'name': 'PRUN0'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[1:1]',
                                                                                              'description': 'PSC0 '
                                                                                                             'Complete '
                                                                                                             'Cycle',
                                                                                              'name': 'PCCYC0'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[5:2]',
                                                                                              'description': 'PSC '
                                                                                                             '0 '
                                                                                                             'Balance '
                                                                                                             'Flank '
                                                                                                             'Width '
                                                                                                             'Modulation',
                                                                                              'name': 'PBFM0'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[3:3]',
                                                                                              'description': 'PSC '
                                                                                                             '0 '
                                                                                                             'Asynchronous '
                                                                                                             'Output '
                                                                                                             'Control '
                                                                                                             'A',
                                                                                              'name': 'PAOC0A'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[4:4]',
                                                                                              'description': 'PSC '
                                                                                                             '0 '
                                                                                                             'Asynchronous '
                                                                                                             'Output '
                                                                                                             'Control '
                                                                                                             'B',
                                                                                              'name': 'PAOC0B'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[7:6]',
                                                                                              'description': 'PSC '
                                                                                                             '0 '
                                                                                                             'Prescaler '
                                                                                                             'Selects',
                                                                                              'name': 'PPRE0',
                                                                                              'writeConstraint': {'range': {'maximum': 0x3,
                                                                                                                            'minimum': 0x0}}}]},
                                                                        'name': 'PCTL0',
                                                                        'size': 0x8},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x33,
                                                                        'description': 'PSC '
                                                                                       '0 '
                                                                                       'Input '
                                                                                       'A '
                                                                                       'Control',
                                                                        'fields': {'field': [{'access': 'read-write',
                                                                                              'bitRange': '[3:0]',
                                                                                              'description': 'PSC '
                                                                                                             '0 '
                                                                                                             'Retrigger '
                                                                                                             'and '
                                                                                                             'Fault '
                                                                                                             'Mode '
                                                                                                             'for '
                                                                                                             'Part '
                                                                                                             'A',
                                                                                              'name': 'PRFM0A',
                                                                                              'writeConstraint': {'range': {'maximum': 0xF,
                                                                                                                            'minimum': 0x0}}},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[4:4]',
                                                                                              'description': 'PSC '
                                                                                                             '0 '
                                                                                                             'Filter '
                                                                                                             'Enable '
                                                                                                             'on '
                                                                                                             'Input '
                                                                                                             'Part '
                                                                                                             'A',
                                                                                              'name': 'PFLTE0A'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[5:5]',
                                                                                              'description': 'PSC '
                                                                                                             '0 '
                                                                                                             'Edge '
                                                                                                             'Level '
                                                                                                             'Selector '
                                                                                                             'on '
                                                                                                             'Input '
                                                                                                             'Part '
                                                                                                             'A',
                                                                                              'name': 'PELEV0A'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[6:6]',
                                                                                              'description': 'PSC '
                                                                                                             '0 '
                                                                                                             'Input '
                                                                                                             'Select '
                                                                                                             'for '
                                                                                                             'Part '
                                                                                                             'A',
                                                                                              'name': 'PISEL0A'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[7:7]',
                                                                                              'description': 'PSC '
                                                                                                             '0 '
                                                                                                             'Capture '
                                                                                                             'Enable '
                                                                                                             'Input '
                                                                                                             'Part '
                                                                                                             'A',
                                                                                              'name': 'PCAE0A'}]},
                                                                        'name': 'PFRC0A',
                                                                        'size': 0x8},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x34,
                                                                        'description': 'PSC '
                                                                                       '0 '
                                                                                       'Input '
                                                                                       'B '
                                                                                       'Control',
                                                                        'fields': {'field': [{'access': 'read-write',
                                                                                              'bitRange': '[3:0]',
                                                                                              'description': 'PSC '
                                                                                                             '0 '
                                                                                                             'Retrigger '
                                                                                                             'and '
                                                                                                             'Fault '
                                                                                                             'Mode '
                                                                                                             'for '
                                                                                                             'Part '
                                                                                                             'B',
                                                                                              'name': 'PRFM0B',
                                                                                              'writeConstraint': {'range': {'maximum': 0xF,
                                                                                                                            'minimum': 0x0}}},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[4:4]',
                                                                                              'description': 'PSC '
                                                                                                             '0 '
                                                                                                             'Filter '
                                                                                                             'Enable '
                                                                                                             'on '
                                                                                                             'Input '
                                                                                                             'Part '
                                                                                                             'B',
                                                                                              'name': 'PFLTE0B'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[5:5]',
                                                                                              'description': 'PSC '
                                                                                                             '0 '
                                                                                                             'Edge '
                                                                                                             'Level '
                                                                                                             'Selector '
                                                                                                             'on '
                                                                                                             'Input '
                                                                                                             'Part '
                                                                                                             'B',
                                                                                              'name': 'PELEV0B'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[6:6]',
                                                                                              'description': 'PSC '
                                                                                                             '0 '
                                                                                                             'Input '
                                                                                                             'Select '
                                                                                                             'for '
                                                                                                             'Part '
                                                                                                             'B',
                                                                                              'name': 'PISEL0B'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[7:7]',
                                                                                              'description': 'PSC '
                                                                                                             '0 '
                                                                                                             'Capture '
                                                                                                             'Enable '
                                                                                                             'Input '
                                                                                                             'Part '
                                                                                                             'B',
                                                                                              'name': 'PCAE0B'}]},
                                                                        'name': 'PFRC0B',
                                                                        'size': 0x8},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x39,
                                                                        'description': 'PSC '
                                                                                       '0 '
                                                                                       'Input '
                                                                                       'Capture '
                                                                                       'Register ',
                                                                        'fields': {'field': [{'access': 'read-write',
                                                                                              'bitRange': '[11:0]',
                                                                                              'description': 'PSC '
                                                                                                             '0 '
                                                                                                             'Input '
                                                                                                             'Capture '
                                                                                                             'Bytes',
                                                                                              'name': 'PICR0',
                                                                                              'writeConstraint': {'range': {'maximum': 0xFFF,
                                                                                                                            'minimum': 0x0}}},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[15:15]',
                                                                                              'description': 'PSC '
                                                                                                             '0 '
                                                                                                             'Capture '
                                                                                                             'Software '
                                                                                                             'Trigger '
                                                                                                             'Bit',
                                                                                              'name': 'PCST0'}]},
                                                                        'name': 'PICR0',
                                                                        'size': 0x10},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x1,
                                                                        'description': 'PSC0 '
                                                                                       'Interrupt '
                                                                                       'Flag '
                                                                                       'Register',
                                                                        'fields': {'field': [{'access': 'read-write',
                                                                                              'bitRange': '[0:0]',
                                                                                              'description': 'End '
                                                                                                             'of '
                                                                                                             'PSC0 '
                                                                                                             'Interrupt',
                                                                                              'name': 'PEOP0'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[2:1]',
                                                                                              'description': 'Ramp '
                                                                                                             'Number',
                                                                                              'name': 'PRN0',
                                                                                              'writeConstraint': {'range': {'maximum': 0x3,
                                                                                                                            'minimum': 0x0}}},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[3:3]',
                                                                                              'description': 'External '
                                                                                                             'Event '
                                                                                                             'A '
                                                                                                             'Interrupt',
                                                                                              'name': 'PEV0A'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[4:4]',
                                                                                              'description': 'External '
                                                                                                             'Event '
                                                                                                             'B '
                                                                                                             'Interrupt',
                                                                                              'name': 'PEV0B'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[6:6]',
                                                                                              'description': 'PSC '
                                                                                                             '0 '
                                                                                                             'Output '
                                                                                                             'A '
                                                                                                             'Activity',
                                                                                              'name': 'POAC0A'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[7:7]',
                                                                                              'description': 'PSC '
                                                                                                             '0 '
                                                                                                             'Output '
                                                                                                             'A '
                                                                                                             'Activity',
                                                                                              'name': 'POAC0B'}]},
                                                                        'name': 'PIFR0',
                                                                        'size': 0x8},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x0,
                                                                        'description': 'PSC0 '
                                                                                       'Interrupt '
                                                                                       'Mask '
                                                                                       'Register',
                                                                        'fields': {'field': [{'access': 'read-write',
                                                                                              'bitRange': '[0:0]',
                                                                                              'description': 'End '
                                                                                                             'of '
                                                                                                             'Cycle '
                                                                                                             'Interrupt '
                                                                                                             'Enable',
                                                                                              'name': 'PEOPE0'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[1:1]',
                                                                                              'description': 'End '
                                                                                                             'of '
                                                                                                             'Enhanced '
                                                                                                             'Cycle '
                                                                                                             'Enable',
                                                                                              'name': 'PEOEPE0'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[3:3]',
                                                                                              'description': 'External '
                                                                                                             'Event '
                                                                                                             'A '
                                                                                                             'Interrupt '
                                                                                                             'Enable',
                                                                                              'name': 'PEVE0A'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[4:4]',
                                                                                              'description': 'External '
                                                                                                             'Event '
                                                                                                             'B '
                                                                                                             'Interrupt '
                                                                                                             'Enable',
                                                                                              'name': 'PEVE0B'}]},
                                                                        'name': 'PIM0',
                                                                        'size': 0x8},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x3B,
                                                                        'description': 'PSC0 '
                                                                                       'Synchro '
                                                                                       'and '
                                                                                       'Output '
                                                                                       'Configuration',
                                                                        'fields': {'field': [{'access': 'read-write',
                                                                                              'bitRange': '[0:0]',
                                                                                              'description': 'PSCOUT00 '
                                                                                                             'Output '
                                                                                                             'Enable',
                                                                                              'name': 'POEN0A'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[2:2]',
                                                                                              'description': 'PSCOUT01 '
                                                                                                             'Output '
                                                                                                             'Enable',
                                                                                              'name': 'POEN0B'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[5:4]',
                                                                                              'description': 'Synchronisation '
                                                                                                             'out '
                                                                                                             'for '
                                                                                                             'ADC '
                                                                                                             'selection',
                                                                                              'name': 'PSYNC0',
                                                                                              'writeConstraint': {'range': {'maximum': 0x3,
                                                                                                                            'minimum': 0x0}}},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[6:6]',
                                                                                              'description': 'PSC '
                                                                                                             'Input '
                                                                                                             'Select',
                                                                                              'name': 'PISEL0B1'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[7:7]',
                                                                                              'description': 'PSC '
                                                                                                             'Input '
                                                                                                             'Select',
                                                                                              'name': 'PISEL0A1'}]},
                                                                        'name': 'PSOC0',
                                                                        'size': 0x8}]}},
                                           {'addressBlock': [{'offset': 0x0,
                                                              'size': 0x4,
                                                              'usage': 'registers'},
                                                             {'offset': 0x13,
                                                              'size': 0x4,
                                                              'usage': 'registers'},
                                                             {'offset': 0x1B,
                                                              'size': 0x2,
                                                              'usage': 'registers'},
                                                             {'offset': 0x31,
                                                              'size': 0x4,
                                                              'usage': 'registers'},
                                                             {'offset': 0x39,
                                                              'size': 0x6,
                                                              'usage': 'registers'}],
                                            'baseAddress': 0x800033,
                                            'description': 'Power Stage '
                                                           'Controller',
                                            'name': 'PSC2',
                                            'registers': {'register': [{'access': 'read-write',
                                                                        'addressOffset': 0x1B,
                                                                        'description': 'Output '
                                                                                       'Compare '
                                                                                       'RA '
                                                                                       'Register ',
                                                                        'fields': {'field': [{'access': 'read-write',
                                                                                              'bitRange': '[11:0]',
                                                                                              'description': 'Output '
                                                                                                             'Compare '
                                                                                                             '2 '
                                                                                                             'RA',
                                                                                              'name': 'OCR2RA',
                                                                                              'writeConstraint': {'range': {'maximum': 0xFFF,
                                                                                                                            'minimum': 0x0}}}]},
                                                                        'name': 'OCR2RA',
                                                                        'size': 0x10},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x15,
                                                                        'description': 'Output '
                                                                                       'Compare '
                                                                                       'RB '
                                                                                       'Register ',
                                                                        'fields': {'field': [{'access': 'read-write',
                                                                                              'bitRange': '[15:0]',
                                                                                              'description': 'Output '
                                                                                                             'Compare '
                                                                                                             '2 '
                                                                                                             'RB',
                                                                                              'name': 'OCR2RB',
                                                                                              'writeConstraint': {'range': {'maximum': 0xFFFF,
                                                                                                                            'minimum': 0x0}}}]},
                                                                        'name': 'OCR2RB',
                                                                        'size': 0x10},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x31,
                                                                        'description': 'Output '
                                                                                       'Compare '
                                                                                       'SA '
                                                                                       'Register ',
                                                                        'fields': {'field': [{'access': 'read-write',
                                                                                              'bitRange': '[11:0]',
                                                                                              'description': 'Output '
                                                                                                             'Compare '
                                                                                                             '2 '
                                                                                                             'SA',
                                                                                              'name': 'OCR2SA',
                                                                                              'writeConstraint': {'range': {'maximum': 0xFFF,
                                                                                                                            'minimum': 0x0}}}]},
                                                                        'name': 'OCR2SA',
                                                                        'size': 0x10},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x13,
                                                                        'description': 'Output '
                                                                                       'Compare '
                                                                                       'SB '
                                                                                       'Register ',
                                                                        'fields': {'field': [{'access': 'read-write',
                                                                                              'bitRange': '[11:0]',
                                                                                              'description': 'Output '
                                                                                                             'Compare '
                                                                                                             '2 '
                                                                                                             'SB',
                                                                                              'name': 'OCR2SB',
                                                                                              'writeConstraint': {'range': {'maximum': 0xFFF,
                                                                                                                            'minimum': 0x0}}}]},
                                                                        'name': 'OCR2SB',
                                                                        'size': 0x10},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x3E,
                                                                        'description': 'Analog '
                                                                                       'Synchronization '
                                                                                       'Delay '
                                                                                       'Register',
                                                                        'fields': {'field': [{'access': 'read-write',
                                                                                              'bitRange': '[7:0]',
                                                                                              'description': 'Analog '
                                                                                                             'Synchronization '
                                                                                                             'Delay '
                                                                                                             'bits',
                                                                                              'name': 'PASDLY2',
                                                                                              'writeConstraint': {'range': {'maximum': 0xFF,
                                                                                                                            'minimum': 0x0}}}]},
                                                                        'name': 'PASDLY2',
                                                                        'size': 0x8},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x2,
                                                                        'description': 'PSC '
                                                                                       '2 '
                                                                                       'Configuration '
                                                                                       'Register',
                                                                        'fields': {'field': [{'access': 'read-write',
                                                                                              'bitRange': '[0:0]',
                                                                                              'description': 'PSC '
                                                                                                             '2 '
                                                                                                             'Output '
                                                                                                             'Matrix '
                                                                                                             'Enable',
                                                                                              'name': 'POME2'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[1:1]',
                                                                                              'description': 'PSC '
                                                                                                             '2 '
                                                                                                             'Input '
                                                                                                             'Clock '
                                                                                                             'Select',
                                                                                              'name': 'PCLKSEL2'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[2:2]',
                                                                                              'description': 'PSC '
                                                                                                             '2 '
                                                                                                             'Output '
                                                                                                             'Polarity',
                                                                                              'name': 'POP2'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[4:3]',
                                                                                              'description': 'PSC '
                                                                                                             '2 '
                                                                                                             'Mode',
                                                                                              'name': 'PMODE2',
                                                                                              'writeConstraint': {'range': {'maximum': 0x3,
                                                                                                                            'minimum': 0x0}}},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[5:5]',
                                                                                              'description': 'PSC '
                                                                                                             '2 '
                                                                                                             'Lock',
                                                                                              'name': 'PLOCK2'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[6:6]',
                                                                                              'description': 'PSC '
                                                                                                             '2 '
                                                                                                             'Autolock',
                                                                                              'name': 'PALOCK2'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[7:7]',
                                                                                              'description': 'PSC '
                                                                                                             '2 '
                                                                                                             'Fifty',
                                                                                              'name': 'PFIFTY2'}]},
                                                                        'name': 'PCNF2',
                                                                        'size': 0x8},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x3D,
                                                                        'description': 'PSC '
                                                                                       '2 '
                                                                                       'Enhanced '
                                                                                       'Configuration '
                                                                                       'Register',
                                                                        'fields': {'field': [{'access': 'read-write',
                                                                                              'bitRange': '[0:0]',
                                                                                              'description': 'No '
                                                                                                             'Description.',
                                                                                              'name': 'PISEL2B1'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[1:1]',
                                                                                              'description': 'No '
                                                                                                             'Description.',
                                                                                              'name': 'PISEL2A1'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[2:2]',
                                                                                              'description': 'No '
                                                                                                             'Description.',
                                                                                              'name': 'PELEV2B1'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[3:3]',
                                                                                              'description': 'No '
                                                                                                             'Description.',
                                                                                              'name': 'PELEV2A1'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[4:4]',
                                                                                              'description': 'No '
                                                                                                             'Description.',
                                                                                              'name': 'PBFM21'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[7:5]',
                                                                                              'description': 'No '
                                                                                                             'Description.',
                                                                                              'name': 'PASDLK2',
                                                                                              'writeConstraint': {'range': {'maximum': 0x7,
                                                                                                                            'minimum': 0x0}}}]},
                                                                        'name': 'PCNFE2',
                                                                        'size': 0x8},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x3,
                                                                        'description': 'PSC '
                                                                                       '2 '
                                                                                       'Control '
                                                                                       'Register',
                                                                        'fields': {'field': [{'access': 'read-write',
                                                                                              'bitRange': '[0:0]',
                                                                                              'description': 'PSC '
                                                                                                             '2 '
                                                                                                             'Run',
                                                                                              'name': 'PRUN2'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[1:1]',
                                                                                              'description': 'PSC2 '
                                                                                                             'Complete '
                                                                                                             'Cycle',
                                                                                              'name': 'PCCYC2'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[2:2]',
                                                                                              'description': 'PSC2 '
                                                                                                             'Auto '
                                                                                                             'Run',
                                                                                              'name': 'PARUN2'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[3:3]',
                                                                                              'description': 'PSC '
                                                                                                             '2 '
                                                                                                             'Asynchronous '
                                                                                                             'Output '
                                                                                                             'Control '
                                                                                                             'A',
                                                                                              'name': 'PAOC2A'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[4:4]',
                                                                                              'description': 'PSC '
                                                                                                             '2 '
                                                                                                             'Asynchronous '
                                                                                                             'Output '
                                                                                                             'Control '
                                                                                                             'B',
                                                                                              'name': 'PAOC2B'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[5:5]',
                                                                                              'description': 'Balance '
                                                                                                             'Flank '
                                                                                                             'Width '
                                                                                                             'Modulation',
                                                                                              'name': 'PBFM2'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[7:6]',
                                                                                              'description': 'PSC '
                                                                                                             '2 '
                                                                                                             'Prescaler '
                                                                                                             'Selects',
                                                                                              'name': 'PPRE2',
                                                                                              'writeConstraint': {'range': {'maximum': 0x3,
                                                                                                                            'minimum': 0x0}}}]},
                                                                        'name': 'PCTL2',
                                                                        'size': 0x8},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x33,
                                                                        'description': 'PSC '
                                                                                       '2 '
                                                                                       'Input '
                                                                                       'B '
                                                                                       'Control',
                                                                        'fields': {'field': [{'access': 'read-write',
                                                                                              'bitRange': '[3:0]',
                                                                                              'description': 'PSC '
                                                                                                             '2 '
                                                                                                             'Retrigger '
                                                                                                             'and '
                                                                                                             'Fault '
                                                                                                             'Mode '
                                                                                                             'for '
                                                                                                             'Part '
                                                                                                             'A',
                                                                                              'name': 'PRFM2A',
                                                                                              'writeConstraint': {'range': {'maximum': 0xF,
                                                                                                                            'minimum': 0x0}}},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[4:4]',
                                                                                              'description': 'PSC '
                                                                                                             '2 '
                                                                                                             'Filter '
                                                                                                             'Enable '
                                                                                                             'on '
                                                                                                             'Input '
                                                                                                             'Part '
                                                                                                             'A',
                                                                                              'name': 'PFLTE2A'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[5:5]',
                                                                                              'description': 'PSC '
                                                                                                             '2 '
                                                                                                             'Edge '
                                                                                                             'Level '
                                                                                                             'Selector '
                                                                                                             'on '
                                                                                                             'Input '
                                                                                                             'Part '
                                                                                                             'A',
                                                                                              'name': 'PELEV2A'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[6:6]',
                                                                                              'description': 'PSC '
                                                                                                             '2 '
                                                                                                             'Input '
                                                                                                             'Select '
                                                                                                             'for '
                                                                                                             'Part '
                                                                                                             'A',
                                                                                              'name': 'PISEL2A'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[7:7]',
                                                                                              'description': 'PSC '
                                                                                                             '2 '
                                                                                                             'Capture '
                                                                                                             'Enable '
                                                                                                             'Input '
                                                                                                             'Part '
                                                                                                             'A',
                                                                                              'name': 'PCAE2A'}]},
                                                                        'name': 'PFRC2A',
                                                                        'size': 0x8},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x34,
                                                                        'description': 'PSC '
                                                                                       '2 '
                                                                                       'Input '
                                                                                       'B '
                                                                                       'Control',
                                                                        'fields': {'field': [{'access': 'read-write',
                                                                                              'bitRange': '[3:0]',
                                                                                              'description': 'PSC '
                                                                                                             '2 '
                                                                                                             'Retrigger '
                                                                                                             'and '
                                                                                                             'Fault '
                                                                                                             'Mode '
                                                                                                             'for '
                                                                                                             'Part '
                                                                                                             'B',
                                                                                              'name': 'PRFM2B',
                                                                                              'writeConstraint': {'range': {'maximum': 0xF,
                                                                                                                            'minimum': 0x0}}},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[4:4]',
                                                                                              'description': 'PSC '
                                                                                                             '2 '
                                                                                                             'Filter '
                                                                                                             'Enable '
                                                                                                             'on '
                                                                                                             'Input '
                                                                                                             'Part '
                                                                                                             'B',
                                                                                              'name': 'PFLTE2B'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[5:5]',
                                                                                              'description': 'PSC '
                                                                                                             '2 '
                                                                                                             'Edge '
                                                                                                             'Level '
                                                                                                             'Selector '
                                                                                                             'on '
                                                                                                             'Input '
                                                                                                             'Part '
                                                                                                             'B',
                                                                                              'name': 'PELEV2B'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[6:6]',
                                                                                              'description': 'PSC '
                                                                                                             '2 '
                                                                                                             'Input '
                                                                                                             'Select '
                                                                                                             'for '
                                                                                                             'Part '
                                                                                                             'B',
                                                                                              'name': 'PISEL2B'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[7:7]',
                                                                                              'description': 'PSC '
                                                                                                             '2 '
                                                                                                             'Capture '
                                                                                                             'Enable '
                                                                                                             'Input '
                                                                                                             'Part '
                                                                                                             'B',
                                                                                              'name': 'PCAE2B'}]},
                                                                        'name': 'PFRC2B',
                                                                        'size': 0x8},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x39,
                                                                        'description': 'PSC '
                                                                                       '2 '
                                                                                       'Input '
                                                                                       'Capture '
                                                                                       'Register',
                                                                        'fields': {'field': [{'access': 'read-write',
                                                                                              'bitRange': '[11:0]',
                                                                                              'description': 'PSC '
                                                                                                             '2 '
                                                                                                             'Input '
                                                                                                             'Capture '
                                                                                                             'Bytes',
                                                                                              'name': 'PICR2',
                                                                                              'writeConstraint': {'range': {'maximum': 0xFFF,
                                                                                                                            'minimum': 0x0}}},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[15:15]',
                                                                                              'description': 'PSC '
                                                                                                             '2 '
                                                                                                             'Capture '
                                                                                                             'Software '
                                                                                                             'Trigger '
                                                                                                             'Bit',
                                                                                              'name': 'PCST2'}]},
                                                                        'name': 'PICR2',
                                                                        'size': 0x10},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x1,
                                                                        'description': 'PSC2 '
                                                                                       'Interrupt '
                                                                                       'Flag '
                                                                                       'Register',
                                                                        'fields': {'field': [{'access': 'read-write',
                                                                                              'bitRange': '[0:0]',
                                                                                              'description': 'End '
                                                                                                             'of '
                                                                                                             'PSC2 '
                                                                                                             'Interrupt',
                                                                                              'name': 'PEOP2'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[2:1]',
                                                                                              'description': 'Ramp '
                                                                                                             'Number',
                                                                                              'name': 'PRN2',
                                                                                              'writeConstraint': {'range': {'maximum': 0x3,
                                                                                                                            'minimum': 0x0}}},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[3:3]',
                                                                                              'description': 'External '
                                                                                                             'Event '
                                                                                                             'A '
                                                                                                             'Interrupt',
                                                                                              'name': 'PEV2A'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[4:4]',
                                                                                              'description': 'External '
                                                                                                             'Event '
                                                                                                             'B '
                                                                                                             'Interrupt',
                                                                                              'name': 'PEV2B'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[5:5]',
                                                                                              'description': 'PSC '
                                                                                                             '2 '
                                                                                                             'Synchro '
                                                                                                             'Error '
                                                                                                             'Interrupt',
                                                                                              'name': 'PSEI2'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[6:6]',
                                                                                              'description': 'PSC '
                                                                                                             '2 '
                                                                                                             'Output '
                                                                                                             'A '
                                                                                                             'Activity',
                                                                                              'name': 'POAC2A'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[7:7]',
                                                                                              'description': 'PSC '
                                                                                                             '2 '
                                                                                                             'Output '
                                                                                                             'A '
                                                                                                             'Activity',
                                                                                              'name': 'POAC2B'}]},
                                                                        'name': 'PIFR2',
                                                                        'size': 0x8},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x0,
                                                                        'description': 'PSC2 '
                                                                                       'Interrupt '
                                                                                       'Mask '
                                                                                       'Register',
                                                                        'fields': {'field': [{'access': 'read-write',
                                                                                              'bitRange': '[0:0]',
                                                                                              'description': 'End '
                                                                                                             'of '
                                                                                                             'Cycle '
                                                                                                             'Interrupt '
                                                                                                             'Enable',
                                                                                              'name': 'PEOPE2'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[1:1]',
                                                                                              'description': 'End '
                                                                                                             'of '
                                                                                                             'Enhanced '
                                                                                                             'Cycle '
                                                                                                             'Interrupt '
                                                                                                             'Enable',
                                                                                              'name': 'PEOEPE2'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[3:3]',
                                                                                              'description': 'External '
                                                                                                             'Event '
                                                                                                             'A '
                                                                                                             'Interrupt '
                                                                                                             'Enable',
                                                                                              'name': 'PEVE2A'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[4:4]',
                                                                                              'description': 'External '
                                                                                                             'Event '
                                                                                                             'B '
                                                                                                             'Interrupt '
                                                                                                             'Enable',
                                                                                              'name': 'PEVE2B'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[5:5]',
                                                                                              'description': 'PSC '
                                                                                                             '2 '
                                                                                                             'Synchro '
                                                                                                             'Error '
                                                                                                             'Interrupt '
                                                                                                             'Enable',
                                                                                              'name': 'PSEIE2'}]},
                                                                        'name': 'PIM2',
                                                                        'size': 0x8},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x3C,
                                                                        'description': 'PSC '
                                                                                       '2 '
                                                                                       'Output '
                                                                                       'Matrix',
                                                                        'fields': {'field': [{'access': 'read-write',
                                                                                              'bitRange': '[3:0]',
                                                                                              'description': 'Output '
                                                                                                             'Matrix '
                                                                                                             'Output '
                                                                                                             'A '
                                                                                                             'Ramps',
                                                                                              'name': 'POMV2A',
                                                                                              'writeConstraint': {'range': {'maximum': 0xF,
                                                                                                                            'minimum': 0x0}}},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[7:4]',
                                                                                              'description': 'Output '
                                                                                                             'Matrix '
                                                                                                             'Output '
                                                                                                             'B '
                                                                                                             'Ramps',
                                                                                              'name': 'POMV2B',
                                                                                              'writeConstraint': {'range': {'maximum': 0xF,
                                                                                                                            'minimum': 0x0}}}]},
                                                                        'name': 'POM2',
                                                                        'size': 0x8},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x3B,
                                                                        'description': 'PSC2 '
                                                                                       'Synchro '
                                                                                       'and '
                                                                                       'Output '
                                                                                       'Configuration',
                                                                        'fields': {'field': [{'access': 'read-write',
                                                                                              'bitRange': '[0:0]',
                                                                                              'description': 'PSCOUT20 '
                                                                                                             'Output '
                                                                                                             'Enable',
                                                                                              'name': 'POEN2A'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[1:1]',
                                                                                              'description': 'PSCOUT22 '
                                                                                                             'Output '
                                                                                                             'Enable',
                                                                                              'name': 'POEN2C'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[2:2]',
                                                                                              'description': 'PSCOUT21 '
                                                                                                             'Output '
                                                                                                             'Enable',
                                                                                              'name': 'POEN2B'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[3:3]',
                                                                                              'description': 'PSCOUT23 '
                                                                                                             'Output '
                                                                                                             'Enable',
                                                                                              'name': 'POEN2D'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[5:4]',
                                                                                              'description': 'Synchronization '
                                                                                                             'Out '
                                                                                                             'for '
                                                                                                             'ADC '
                                                                                                             'Selection',
                                                                                              'name': 'PSYNC2',
                                                                                              'writeConstraint': {'range': {'maximum': 0x3,
                                                                                                                            'minimum': 0x0}}},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[7:6]',
                                                                                              'description': 'PSC '
                                                                                                             '2 '
                                                                                                             'Output '
                                                                                                             '23 '
                                                                                                             'Select',
                                                                                              'name': 'POS2',
                                                                                              'writeConstraint': {'range': {'maximum': 0x3,
                                                                                                                            'minimum': 0x0}}}]},
                                                                        'name': 'PSOC2',
                                                                        'size': 0x8}]}},
                                           {'addressBlock': [{'offset': 0x0,
                                                              'size': 0x2,
                                                              'usage': 'registers'},
                                                             {'offset': 0x1F,
                                                              'size': 0x1,
                                                              'usage': 'registers'}],
                                            'baseAddress': 0x800037,
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
                                                                        'addressOffset': 0x1F,
                                                                        'description': 'SPI '
                                                                                       'Data '
                                                                                       'Register '
                                                                                       '(write-only '
                                                                                       'for '
                                                                                       'debugger)',
                                                                        'fields': {'field': [{'access': 'read-write',
                                                                                              'bitRange': '[7:0]',
                                                                                              'description': 'SPI '
                                                                                                             'Data '
                                                                                                             'bits',
                                                                                              'name': 'SPD',
                                                                                              'writeConstraint': {'range': {'maximum': 0xFF,
                                                                                                                            'minimum': 0x0}}}]},
                                                                        'name': 'SPDR',
                                                                        'size': 0x8},
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
                                                              'size': 0x2,
                                                              'usage': 'registers'},
                                                             {'offset': 0x39,
                                                              'size': 0x2,
                                                              'usage': 'registers'},
                                                             {'offset': 0x69,
                                                              'size': 0x1,
                                                              'usage': 'registers'},
                                                             {'offset': 0x6B,
                                                              'size': 0x2,
                                                              'usage': 'registers'}],
                                            'baseAddress': 0x800021,
                                            'description': 'Timer/Counter, '
                                                           '16-bit',
                                            'name': 'TC1',
                                            'registers': {'register': [{'access': 'read-write',
                                                                        'addressOffset': 0x6B,
                                                                        'description': 'Timer/Counter1 '
                                                                                       'Input '
                                                                                       'Capture '
                                                                                       'Register '
                                                                                       'Bytes',
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
                                                                        'addressOffset': 0x69,
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
                                                                                              'bitRange': '[4:4]',
                                                                                              'description': 'Waveform '
                                                                                                             'Generation '
                                                                                                             'Mode',
                                                                                              'name': 'WGM13'},
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
                                                                        'addressOffset': 0x39,
                                                                        'description': 'Timer/Counter1 '
                                                                                       'Bytes',
                                                                        'fields': {'field': [{'access': 'read-write',
                                                                                              'bitRange': '[15:0]',
                                                                                              'description': 'Timer/Counter '
                                                                                                             '1 '
                                                                                                             'bits',
                                                                                              'name': 'TCNT1',
                                                                                              'writeConstraint': {'range': {'maximum': 0xFFFF,
                                                                                                                            'minimum': 0x0}}}]},
                                                                        'name': 'TCNT1',
                                                                        'size': 0x10},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x1,
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
                                                                                              'bitRange': '[5:5]',
                                                                                              'description': 'Input '
                                                                                                             'Capture '
                                                                                                             'Flag '
                                                                                                             '1',
                                                                                              'name': 'ICF1'}]},
                                                                        'name': 'TIFR1',
                                                                        'size': 0x8},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x0,
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
                                            'baseAddress': 0x800082,
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