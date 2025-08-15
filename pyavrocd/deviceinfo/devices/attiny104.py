
from pymcuprog.deviceinfo.eraseflags import ChiperaseEffect

DEVICE_INFO = {
    'name': 'attiny104',
    'architecture': 'avr8l',

    # flash
    'flash_address_byte': 0x0000,
    'flash_size_bytes': 0x0400,
    'flash_page_size_bytes': 0x80,
    'flash_read_size_bytes': 0x02,
    'flash_write_size_bytes': 0x80,
    'flash_chiperase_effect': ChiperaseEffect.ALWAYS_ERASED,
    'flash_isolated_erase': True,

    # fuses
    'fuses_address_byte': 0,
    'fuses_size_bytes': 0x0001,
    'fuses_page_size_bytes': 0x01,
    'fuses_read_size_bytes': 0x01,
    'fuses_write_size_bytes': 0x01,
    'fuses_chiperase_effect': ChiperaseEffect.NOT_ERASED,
    'fuses_isolated_erase': True,

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
    'osccal_base' : 0x19,
    'device_id': 0x1E900B,
    'interface': 'TPI'
}