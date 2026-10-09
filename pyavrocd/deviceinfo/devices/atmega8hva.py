# Device description for atmega8hva, generated from Microchip's ATmega8HVA.atdf by
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
    'name': 'atmega8hva',
    'architecture': 'avr8',

    # eeprom
    'eeprom_address_byte': 0x0000,
    'eeprom_size_bytes': 0x0100,
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
    'fuses_size_bytes': 0x0001,
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
    'eear_size' : 1,
    'eecr_base' : 0x1F,
    'eedr_base' : 0x20,
    'spmcsr_base' : 0x57,
    'osccal_base' : 0x46,
    'dwen_base' : 0x00,
    'dwen_mask' : 0x10,
    'eesave_base' : 0x00,
    'eesave_mask' : 0x40,
    'tcnt0_base' : 0x46,
    'cs0_base' : 0x45,
    'toie0_base' : 0x6E,
    'toie0_mask' : 0x01,
    'masked_registers' : [0x4e, 0x51],
    'ronly_registers' : [0x20, 0x23, 0x26, 0x35, 0x36, 0x37, 0x3c, 0x4d, 0x54, 0x60, 0x61, 0x7a, 0xc8, 0xe0, 0xe1, 0xe2, 0xe3, 0xfe],
    'device_id': 0x1E9310,
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
            'name': 'ATmega8HVA',
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
                                                                        'fields': {'field': [{'access': 'read-write',
                                                                                              'bitRange': '[7:0]',
                                                                                              'description': 'Bandgap '
                                                                                                             'calibration '
                                                                                                             'bits',
                                                                                              'name': 'BGCR',
                                                                                              'writeConstraint': {'range': {'maximum': 0xFF,
                                                                                                                            'minimum': 0x0}}}]},
                                                                        'name': 'BGCRR',
                                                                        'size': 0x8}]}},
                                           {'addressBlock': [{'offset': 0x0,
                                                              'size': 0x2,
                                                              'usage': 'registers'},
                                                             {'offset': 0x3,
                                                              'size': 0xA,
                                                              'usage': 'registers'}],
                                            'baseAddress': 0x8000F2,
                                            'description': 'Battery Protection',
                                            'name': 'BATTERY_PROTECTION',
                                            'registers': {'register': [{'access': 'read-write',
                                                                        'addressOffset': 0x7,
                                                                        'description': 'Battery '
                                                                                       'Protection '
                                                                                       'Charge-High-current '
                                                                                       'Detection '
                                                                                       'Level '
                                                                                       'Register',
                                                                        'name': 'BPCHCD',
                                                                        'size': 0x8,
                                                                        'writeConstraint': {'range': {'maximum': 0xFF,
                                                                                                      'minimum': 0x0}}},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x5,
                                                                        'description': 'Battery '
                                                                                       'Protection '
                                                                                       'Charge-Over-current '
                                                                                       'Detection '
                                                                                       'Level '
                                                                                       'Register',
                                                                        'name': 'BPCOCD',
                                                                        'size': 0x8,
                                                                        'writeConstraint': {'range': {'maximum': 0xFF,
                                                                                                      'minimum': 0x0}}},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0xB,
                                                                        'description': 'Battery '
                                                                                       'Protection '
                                                                                       'Control '
                                                                                       'Register',
                                                                        'fields': {'field': [{'access': 'read-write',
                                                                                              'bitRange': '[0:0]',
                                                                                              'description': 'Charge '
                                                                                                             'High-current '
                                                                                                             'Protection '
                                                                                                             'Disable',
                                                                                              'name': 'CHCD'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[1:1]',
                                                                                              'description': 'Discharge '
                                                                                                             'High-current '
                                                                                                             'Protection '
                                                                                                             'Disable',
                                                                                              'name': 'DHCD'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[2:2]',
                                                                                              'description': 'Charge '
                                                                                                             'Over-current '
                                                                                                             'Protection '
                                                                                                             'Disabled',
                                                                                              'name': 'COCD'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[3:3]',
                                                                                              'description': 'Discharge '
                                                                                                             'Over-current '
                                                                                                             'Protection '
                                                                                                             'Disabled',
                                                                                              'name': 'DOCD'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[4:4]',
                                                                                              'description': 'Short '
                                                                                                             'Circuit '
                                                                                                             'Protection '
                                                                                                             'Disabled',
                                                                                              'name': 'SCD'}]},
                                                                        'name': 'BPCR',
                                                                        'size': 0x8},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x6,
                                                                        'description': 'Battery '
                                                                                       'Protection '
                                                                                       'Discharge-High-current '
                                                                                       'Detection '
                                                                                       'Level '
                                                                                       'Register',
                                                                        'name': 'BPDHCD',
                                                                        'size': 0x8,
                                                                        'writeConstraint': {'range': {'maximum': 0xFF,
                                                                                                      'minimum': 0x0}}},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x4,
                                                                        'description': 'Battery '
                                                                                       'Protection '
                                                                                       'Discharge-Over-current '
                                                                                       'Detection '
                                                                                       'Level '
                                                                                       'Register',
                                                                        'name': 'BPDOCD',
                                                                        'size': 0x8,
                                                                        'writeConstraint': {'range': {'maximum': 0xFF,
                                                                                                      'minimum': 0x0}}},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0xA,
                                                                        'description': 'Battery '
                                                                                       'Protection '
                                                                                       'Short-current '
                                                                                       'Timing '
                                                                                       'Register',
                                                                        'name': 'BPHCTR',
                                                                        'size': 0x8,
                                                                        'writeConstraint': {'range': {'maximum': 0xFF,
                                                                                                      'minimum': 0x0}}},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x1,
                                                                        'description': 'Battery '
                                                                                       'Protection '
                                                                                       'Interrupt '
                                                                                       'Flag '
                                                                                       'Register',
                                                                        'fields': {'field': [{'access': 'read-write',
                                                                                              'bitRange': '[0:0]',
                                                                                              'description': 'Charge '
                                                                                                             'High-current '
                                                                                                             'Protection '
                                                                                                             'Activated '
                                                                                                             'Interrupt',
                                                                                              'name': 'CHCIF'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[1:1]',
                                                                                              'description': 'Discharge '
                                                                                                             'High-current '
                                                                                                             'Protection '
                                                                                                             'Activated '
                                                                                                             'Interrupt',
                                                                                              'name': 'DHCIF'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[2:2]',
                                                                                              'description': 'Charge '
                                                                                                             'Over-current '
                                                                                                             'Protection '
                                                                                                             'Activated '
                                                                                                             'Interrupt '
                                                                                                             'Flag',
                                                                                              'name': 'COCIF'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[3:3]',
                                                                                              'description': 'Discharge '
                                                                                                             'Over-current '
                                                                                                             'Protection '
                                                                                                             'Activated '
                                                                                                             'Interrupt '
                                                                                                             'Flag',
                                                                                              'name': 'DOCIF'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[4:4]',
                                                                                              'description': 'Short-circuit '
                                                                                                             'Protection '
                                                                                                             'Activated '
                                                                                                             'Interrupt '
                                                                                                             'Flag',
                                                                                              'name': 'SCIF'}]},
                                                                        'name': 'BPIFR',
                                                                        'size': 0x8},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x0,
                                                                        'description': 'Battery '
                                                                                       'Protection '
                                                                                       'Interrupt '
                                                                                       'Mask '
                                                                                       'Register',
                                                                        'fields': {'field': [{'access': 'read-write',
                                                                                              'bitRange': '[0:0]',
                                                                                              'description': 'Charger '
                                                                                                             'High-current '
                                                                                                             'Protection '
                                                                                                             'Activated '
                                                                                                             'Interrupt',
                                                                                              'name': 'CHCIE'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[1:1]',
                                                                                              'description': 'Discharger '
                                                                                                             'High-current '
                                                                                                             'Protection '
                                                                                                             'Activated '
                                                                                                             'Interrupt',
                                                                                              'name': 'DHCIE'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[2:2]',
                                                                                              'description': 'Charge '
                                                                                                             'Over-current '
                                                                                                             'Protection '
                                                                                                             'Activated '
                                                                                                             'Interrupt '
                                                                                                             'Enable',
                                                                                              'name': 'COCIE'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[3:3]',
                                                                                              'description': 'Discharge '
                                                                                                             'Over-current '
                                                                                                             'Protection '
                                                                                                             'Activated '
                                                                                                             'Interrupt '
                                                                                                             'Enable',
                                                                                              'name': 'DOCIE'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[4:4]',
                                                                                              'description': 'Short-circuit '
                                                                                                             'Protection '
                                                                                                             'Activated '
                                                                                                             'Interrupt '
                                                                                                             'Enable',
                                                                                              'name': 'SCIE'}]},
                                                                        'name': 'BPIMSK',
                                                                        'size': 0x8},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x9,
                                                                        'description': 'Battery '
                                                                                       'Protection '
                                                                                       'Over-current '
                                                                                       'Timing '
                                                                                       'Register',
                                                                        'name': 'BPOCTR',
                                                                        'size': 0x8,
                                                                        'writeConstraint': {'range': {'maximum': 0xFF,
                                                                                                      'minimum': 0x0}}},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0xC,
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
                                                                        'addressOffset': 0x3,
                                                                        'description': 'Battery '
                                                                                       'Protection '
                                                                                       'Short-Circuit '
                                                                                       'Detection '
                                                                                       'Level '
                                                                                       'Register',
                                                                        'name': 'BPSCD',
                                                                        'size': 0x8,
                                                                        'writeConstraint': {'range': {'maximum': 0xFF,
                                                                                                      'minimum': 0x0}}},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x8,
                                                                        'description': 'Battery '
                                                                                       'Protection '
                                                                                       'Short-current '
                                                                                       'Timing '
                                                                                       'Register',
                                                                        'name': 'BPSCTR',
                                                                        'size': 0x8,
                                                                        'writeConstraint': {'range': {'maximum': 0xFF,
                                                                                                      'minimum': 0x0}}}]}},
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
                                                                                              'name': 'SIGRD'}]},
                                                                        'name': 'SPMCSR',
                                                                        'size': 0x8}]}},
                                           {'addressBlock': [{'offset': 0x0,
                                                              'size': 0x7,
                                                              'usage': 'registers'},
                                                             {'offset': 0x8,
                                                              'size': 0x2,
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
                                                                                              'name': 'CADSI',
                                                                                              'writeConstraint': {'range': {'maximum': 0x3,
                                                                                                                            'minimum': 0x0}}},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[4:3]',
                                                                                              'description': 'CC_ADC '
                                                                                                             'Accumulate '
                                                                                                             'Current '
                                                                                                             'Select '
                                                                                                             'Bits',
                                                                                              'name': 'CADAS',
                                                                                              'writeConstraint': {'range': {'maximum': 0x3,
                                                                                                                            'minimum': 0x0}}},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[5:5]',
                                                                                              'description': 'CC_ADC '
                                                                                                             'Update '
                                                                                                             'Busy',
                                                                                              'name': 'CADUB'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[6:6]',
                                                                                              'description': 'No '
                                                                                                             'Description.',
                                                                                              'name': 'CADPOL'},
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
                                                                                       'B',
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
                                                                                       'Current',
                                                                        'name': 'CADRC',
                                                                        'size': 0x8,
                                                                        'writeConstraint': {'range': {'maximum': 0xFF,
                                                                                                      'minimum': 0x0}}}]}},
                                           {'addressBlock': [{'offset': 0x0,
                                                              'size': 0x1,
                                                              'usage': 'registers'},
                                                             {'offset': 0x7,
                                                              'size': 0x1,
                                                              'usage': 'registers'},
                                                             {'offset': 0x13,
                                                              'size': 0x2,
                                                              'usage': 'registers'},
                                                             {'offset': 0x1C,
                                                              'size': 0x3,
                                                              'usage': 'registers'},
                                                             {'offset': 0x26,
                                                              'size': 0x3,
                                                              'usage': 'registers'},
                                                             {'offset': 0x2A,
                                                              'size': 0x1,
                                                              'usage': 'registers'},
                                                             {'offset': 0x2D,
                                                              'size': 0x1,
                                                              'usage': 'registers'},
                                                             {'offset': 0x2F,
                                                              'size': 0x1,
                                                              'usage': 'registers'},
                                                             {'offset': 0x47,
                                                              'size': 0x1,
                                                              'usage': 'registers'}],
                                            'baseAddress': 0x800037,
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
                                                          {'description': 'Voltage '
                                                                          'regulator '
                                                                          'monitor '
                                                                          'interrupt',
                                                           'name': 'VREGMON',
                                                           'value': 0x2},
                                                          {'description': 'External '
                                                                          'Interrupt '
                                                                          'Request '
                                                                          '0',
                                                           'name': 'INT0',
                                                           'value': 0x3},
                                                          {'description': 'External '
                                                                          'Interrupt '
                                                                          'Request '
                                                                          '1',
                                                           'name': 'INT1',
                                                           'value': 0x4},
                                                          {'description': 'External '
                                                                          'Interrupt '
                                                                          'Request '
                                                                          '2',
                                                           'name': 'INT2',
                                                           'value': 0x5},
                                                          {'description': 'Watchdog '
                                                                          'Timeout '
                                                                          'Interrupt',
                                                           'name': 'WDT',
                                                           'value': 0x6},
                                                          {'description': 'Timer '
                                                                          '1 '
                                                                          'Input '
                                                                          'capture',
                                                           'name': 'TIMER1_IC',
                                                           'value': 0x7},
                                                          {'description': 'Timer '
                                                                          '1 '
                                                                          'Compare '
                                                                          'Match '
                                                                          'A',
                                                           'name': 'TIMER1_COMPA',
                                                           'value': 0x8},
                                                          {'description': 'Timer '
                                                                          '1 '
                                                                          'Compare '
                                                                          'Match '
                                                                          'B',
                                                           'name': 'TIMER1_COMPB',
                                                           'value': 0x9},
                                                          {'description': 'Timer '
                                                                          '1 '
                                                                          'overflow',
                                                           'name': 'TIMER1_OVF',
                                                           'value': 0xA},
                                                          {'description': 'Timer '
                                                                          '0 '
                                                                          'Input '
                                                                          'Capture',
                                                           'name': 'TIMER0_IC',
                                                           'value': 0xB},
                                                          {'description': 'Timer '
                                                                          '0 '
                                                                          'Compare '
                                                                          'Match '
                                                                          'A',
                                                           'name': 'TIMER0_COMPA',
                                                           'value': 0xC},
                                                          {'description': 'Timer '
                                                                          '0 '
                                                                          'Compare '
                                                                          'Match '
                                                                          'B',
                                                           'name': 'TIMER0_COMPB',
                                                           'value': 0xD},
                                                          {'description': 'Timer '
                                                                          '0 '
                                                                          'Overflow',
                                                           'name': 'TIMER0_OVF',
                                                           'value': 0xE},
                                                          {'description': 'SPI '
                                                                          'Serial '
                                                                          'transfer '
                                                                          'complete',
                                                           'name': 'SPI_STC',
                                                           'value': 0xF},
                                                          {'description': 'Voltage '
                                                                          'ADC '
                                                                          'Conversion '
                                                                          'Complete',
                                                           'name': 'VADC',
                                                           'value': 0x10},
                                                          {'description': 'Coulomb '
                                                                          'Counter '
                                                                          'ADC '
                                                                          'Conversion '
                                                                          'Complete',
                                                           'name': 'CCADC_CONV',
                                                           'value': 0x11},
                                                          {'description': 'Coloumb '
                                                                          'Counter '
                                                                          'ADC '
                                                                          'Regular '
                                                                          'Current',
                                                           'name': 'CCADC_REG_CUR',
                                                           'value': 0x12},
                                                          {'description': 'Coloumb '
                                                                          'Counter '
                                                                          'ADC '
                                                                          'Accumulator',
                                                           'name': 'CCADC_ACC',
                                                           'value': 0x13},
                                                          {'description': 'EEPROM '
                                                                          'Ready',
                                                           'name': 'EE_READY',
                                                           'value': 0x14}],
                                            'name': 'CPU',
                                            'registers': {'register': [{'access': 'read-write',
                                                                        'addressOffset': 0x2A,
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
                                                                        'addressOffset': 0x47,
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
                                                                        'addressOffset': 0x2F,
                                                                        'description': 'Fast '
                                                                                       'Oscillator '
                                                                                       'Calibration '
                                                                                       'Value',
                                                                        'name': 'FOSCCAL',
                                                                        'size': 0x8,
                                                                        'writeConstraint': {'range': {'maximum': 0xFF,
                                                                                                      'minimum': 0x0}}},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x7,
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
                                                                        'addressOffset': 0x13,
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
                                                                        'addressOffset': 0x14,
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
                                                                        'addressOffset': 0x1E,
                                                                        'description': 'MCU '
                                                                                       'Control '
                                                                                       'Register',
                                                                        'fields': {'field': [{'access': 'read-write',
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
                                                                        'addressOffset': 0x1D,
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
                                                                        'addressOffset': 0x0,
                                                                        'description': 'Oscillator '
                                                                                       'Sampling '
                                                                                       'Interface '
                                                                                       'Control '
                                                                                       'and '
                                                                                       'Status '
                                                                                       'Register '
                                                                                       '(read-only '
                                                                                       'for '
                                                                                       'debugger)',
                                                                        'fields': {'field': [{'access': 'read-write',
                                                                                              'bitRange': '[0:0]',
                                                                                              'description': 'Oscillator '
                                                                                                             'Sampling '
                                                                                                             'Interface '
                                                                                                             'Enable',
                                                                                              'name': 'OSIEN'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[1:1]',
                                                                                              'description': 'Oscillator '
                                                                                                             'Sampling '
                                                                                                             'Interface '
                                                                                                             'Status',
                                                                                              'name': 'OSIST'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[4:4]',
                                                                                              'description': 'Oscillator '
                                                                                                             'Sampling '
                                                                                                             'Interface '
                                                                                                             'Select '
                                                                                                             '0',
                                                                                              'name': 'OSISEL0'}]},
                                                                        'name': 'OSICSR',
                                                                        'size': 0x8},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x2D,
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
                                                                                                             'reduction '
                                                                                                             'SPI',
                                                                                              'name': 'PRSPI'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[5:5]',
                                                                                              'description': 'Power '
                                                                                                             'Reduction '
                                                                                                             'Voltage '
                                                                                                             'Regulator '
                                                                                                             'Monitor',
                                                                                              'name': 'PRVRM'}]},
                                                                        'name': 'PRR0',
                                                                        'size': 0x8},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x1C,
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
                                                                                                                                       {'description': 'Reserved',
                                                                                                                                        'name': 'VAL_0x02',
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
                                                                        'addressOffset': 0x26,
                                                                        'description': 'Stack '
                                                                                       'Pointer ',
                                                                        'name': 'SP',
                                                                        'size': 0x10,
                                                                        'writeConstraint': {'range': {'maximum': 0xFFFF,
                                                                                                      'minimum': 0x0}}},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x28,
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
                                            'baseAddress': 0x80003F,
                                            'description': 'EEPROM',
                                            'name': 'EEPROM',
                                            'registers': {'register': [{'access': 'read-write',
                                                                        'addressOffset': 0x2,
                                                                        'description': 'EEPROM '
                                                                                       'Read/Write '
                                                                                       'Access',
                                                                        'name': 'EEAR',
                                                                        'size': 0x8,
                                                                        'writeConstraint': {'range': {'maximum': 0xFF,
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
                                                              'size': 0x2,
                                                              'usage': 'registers'},
                                                             {'offset': 0x2D,
                                                              'size': 0x1,
                                                              'usage': 'registers'}],
                                            'baseAddress': 0x80003C,
                                            'description': 'External '
                                                           'Interrupts',
                                            'name': 'EXINT',
                                            'registers': {'register': [{'access': 'read-write',
                                                                        'addressOffset': 0x2D,
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
                                                              'size': 0x1,
                                                              'usage': 'registers'}],
                                            'baseAddress': 0x8000F0,
                                            'description': 'FET Control',
                                            'name': 'FET',
                                            'registers': {'register': [{'access': 'read-write',
                                                                        'addressOffset': 0x0,
                                                                        'description': 'FET '
                                                                                       'Control '
                                                                                       'and '
                                                                                       'Status '
                                                                                       'Register',
                                                                        'fields': {'field': [{'access': 'read-write',
                                                                                              'bitRange': '[0:0]',
                                                                                              'description': 'Charge '
                                                                                                             'FET '
                                                                                                             'Enable',
                                                                                              'name': 'CFE'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[1:1]',
                                                                                              'description': 'Discharge '
                                                                                                             'FET '
                                                                                                             'Enable',
                                                                                              'name': 'DFE'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[2:2]',
                                                                                              'description': 'Current '
                                                                                                             'Protection '
                                                                                                             'Status',
                                                                                              'name': 'CPS'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[3:3]',
                                                                                              'description': 'Deep '
                                                                                                             'Under-Voltage '
                                                                                                             'Recovery '
                                                                                                             'Disable',
                                                                                              'name': 'DUVRD'}]},
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
                                                                        'description': 'Data '
                                                                                       'Direction '
                                                                                       'Register, '
                                                                                       'Port '
                                                                                       'B',
                                                                        'name': 'DDRB',
                                                                        'size': 0x8,
                                                                        'writeConstraint': {'range': {'maximum': 0xFF,
                                                                                                      'minimum': 0x0}}},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x0,
                                                                        'description': 'Input '
                                                                                       'Pins, '
                                                                                       'Port '
                                                                                       'B '
                                                                                       '(read-only '
                                                                                       'for '
                                                                                       'debugger)',
                                                                        'name': 'PINB',
                                                                        'size': 0x8,
                                                                        'writeConstraint': {'range': {'maximum': 0xFF,
                                                                                                      'minimum': 0x0}}},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x2,
                                                                        'description': 'Data '
                                                                                       'Register, '
                                                                                       'Port '
                                                                                       'B',
                                                                        'name': 'PORTB',
                                                                        'size': 0x8,
                                                                        'writeConstraint': {'range': {'maximum': 0xFF,
                                                                                                      'minimum': 0x0}}}]}},
                                           {'addressBlock': [{'offset': 0x0,
                                                              'size': 0x1,
                                                              'usage': 'registers'},
                                                             {'offset': 0x2,
                                                              'size': 0x1,
                                                              'usage': 'registers'}],
                                            'baseAddress': 0x800026,
                                            'description': 'I/O Port',
                                            'name': 'PORTC',
                                            'registers': {'register': [{'access': 'read-write',
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
                                                             {'offset': 0xF,
                                                              'size': 0x6,
                                                              'usage': 'registers'},
                                                             {'offset': 0x39,
                                                              'size': 0x1,
                                                              'usage': 'registers'}],
                                            'baseAddress': 0x800035,
                                            'description': 'Timer/Counter, '
                                                           '16-bit',
                                            'name': 'TC0',
                                            'registers': {'register': [{'access': 'read-write',
                                                                        'addressOffset': 0x13,
                                                                        'description': 'Output '
                                                                                       'compare '
                                                                                       'Register '
                                                                                       'A',
                                                                        'name': 'OCR0A',
                                                                        'size': 0x8,
                                                                        'writeConstraint': {'range': {'maximum': 0xFF,
                                                                                                      'minimum': 0x0}}},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0x14,
                                                                        'description': 'Output '
                                                                                       'compare '
                                                                                       'Register '
                                                                                       'B',
                                                                        'name': 'OCR0B',
                                                                        'size': 0x8,
                                                                        'writeConstraint': {'range': {'maximum': 0xFF,
                                                                                                      'minimum': 0x0}}},
                                                                       {'access': 'read-write',
                                                                        'addressOffset': 0xF,
                                                                        'description': 'Timer/Counter0 '
                                                                                       'Control '
                                                                                       'Register',
                                                                        'fields': {'field': [{'access': 'read-write',
                                                                                              'bitRange': '[0:0]',
                                                                                              'description': 'Clock '
                                                                                                             'Select0 '
                                                                                                             'bit '
                                                                                                             '0',
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
                                                                                       'Register',
                                                                        'fields': {'field': [{'access': 'read-write',
                                                                                              'bitRange': '[0:0]',
                                                                                              'description': 'Clock '
                                                                                                             'Select0 '
                                                                                                             'bit '
                                                                                                             '0',
                                                                                              'name': 'CS00'},
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
                                                                                              'name': 'OCF0B'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[3:3]',
                                                                                              'description': 'Timer/Counter '
                                                                                                             'Interrupt '
                                                                                                             'Flag '
                                                                                                             'Register',
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
                                                                                              'name': 'CS',
                                                                                              'writeConstraint': {'range': {'maximum': 0x7,
                                                                                                                            'minimum': 0x0}}}]},
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
                                            'baseAddress': 0x8000C8,
                                            'description': 'Voltage Regulator',
                                            'name': 'VOLTAGE_REGULATOR',
                                            'registers': {'register': [{'access': 'read-write',
                                                                        'addressOffset': 0x0,
                                                                        'description': 'Regulator '
                                                                                       'Operating '
                                                                                       'Condition '
                                                                                       'Register '
                                                                                       '(read-only '
                                                                                       'for '
                                                                                       'debugger)',
                                                                        'fields': {'field': [{'access': 'read-write',
                                                                                              'bitRange': '[0:0]',
                                                                                              'description': 'ROC '
                                                                                                             'Warning '
                                                                                                             'Interrupt '
                                                                                                             'Enable',
                                                                                              'name': 'ROCWIE'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[1:1]',
                                                                                              'description': 'ROC '
                                                                                                             'Warning '
                                                                                                             'Interrupt '
                                                                                                             'Flag',
                                                                                              'name': 'ROCWIF'},
                                                                                             {'access': 'read-write',
                                                                                              'bitRange': '[7:7]',
                                                                                              'description': 'ROC '
                                                                                                             'Status',
                                                                                              'name': 'ROCS'}]},
                                                                        'name': 'ROCR',
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