"""
The test suite for filtering out unsafe instructions and simulate them offline
"""
#pylint: disable=protected-access,missing-function-docstring,invalid-name,line-too-long,missing-class-docstring,too-many-public-methods,too-many-positional-arguments

import logging

from unittest import TestCase
from unittest.mock import Mock, create_autospec, call
from pyavrocd.breakexec import BreakAndExec
from pyavrocd.xavrdebugger import XAvrDebugger
from pyavrocd.errors import FatalError

logging.basicConfig(level=logging.CRITICAL)

class TestBreakAndExecFilter(TestCase):

    def setUp(self):
        mock_dbg = create_autospec(XAvrDebugger, spec_set=False, instance=True)
        mock_dbg.memory_info = Mock()
        mock_dbg.memory_info.memory_info_by_name.return_value = {'size' : 100,'address' : 0x60 }
        mock_dbg.get_hwbpnum.return_value = 1
        mock_dbg.get_architecture.return_value = "avr8"
        self.bp = BreakAndExec(Mock(), mock_dbg, Mock())

    def verify_load_or_store(self, opcode, store=None, reg=None, ixreg=None, ixregval=None, predec=False, postinc=False):
        if ixreg:
            if ixreg == 'X':
                ixreg = 26
            elif ixreg == 'Y':
                ixreg = 28
            elif ixreg == 'Z':
                ixreg = 30
            else:
                raise FatalError("Wrong index register id")
        sramwrite_calls = []
        sramread_calls = []
        sramread_returns = []
        if ixreg is not None:
            sramread_calls = [call(ixreg,2)]
            sramread_returns = [ bytearray([ixregval, 0]) ]
        if store:
            sramread_calls += [call(reg,1)]
            sramread_returns += [ bytearray([0x99]) ]
        else:
            sramwrite_calls += [call(reg, bytearray([0x88]))]
        if predec:
            ixregval -= 1
        if postinc:
            ixregval += 1
        if predec or postinc:
            sramwrite_calls += [call(ixreg, bytearray([ixregval, 0])) ]
        self.bp.dbg.status_register_read.return_value = bytearray([0x88])
        self.bp.dbg.sram_read.side_effect = sramread_returns
        self.assertTrue(self.bp._filter_unsafe_instruction(0x1000, opcode))
        self.bp.dbg.sram_read.assert_has_calls(sramread_calls, any_order=False)
        self.assertEqual(self.bp.dbg.sram_read.call_count,len(sramread_calls))
        self.bp.dbg.sram_write.assert_has_calls(sramwrite_calls, any_order=False)
        self.assertEqual(self.bp.dbg.sram_write.call_count, len(sramwrite_calls))
        if store:
            self.bp.dbg.status_register_write.assert_called_once_with(bytearray([0x99]))
        else:
            self.bp.dbg.status_register_read.assert_called_once_with()

    def test_filter_low_alu(self):
        self.assertFalse(self.bp._filter_unsafe_instruction(0x1000, 0x0000))
        self.assertFalse(self.bp._filter_unsafe_instruction(0x2000, 0x27F7))
        self.assertFalse(self.bp._filter_unsafe_instruction(0x3000, 0x7FFF))

    def test_filter_big_sram(self):
        self.bp._big_sram = True
        with self.assertRaises(FatalError):
            self.bp._filter_unsafe_instruction(0x1000,0x1234)

    def test_filter_lds_positive(self):
        self.bp._read_flash_word.return_value=0x005F
        self.verify_load_or_store(0x90F0, store=False, reg=15) # LDS r15, 0x005F
        self.bp.dbg.program_counter_write.assert_called_once_with(0x1004 >> 1)


    def test_filter_sts_positive(self):
        self.bp._read_flash_word.return_value=0x005F
        self.verify_load_or_store(0x9200, store=True,  reg=0) # STS 0x005F, r0
        self.bp.dbg.program_counter_write.assert_called_once_with(0x1004 >> 1)

    def test_filter_lds_sts_negative(self):
        self.bp._read_flash_word.side_effect = [ 0x0056, 0x005E, 0x0060, 0x1000 ]
        self.assertFalse(self.bp._filter_unsafe_instruction(0x1000, 0x90F0)) # LDS r15, 0x0056
        self.assertFalse(self.bp._filter_unsafe_instruction(0x2000, 0x91F0)) # LDS r31, 0x005E
        self.assertFalse(self.bp._filter_unsafe_instruction(0x3000, 0x9200)) # STS r0, 0x0060
        self.assertFalse(self.bp._filter_unsafe_instruction(0x4000, 0x92a0)) # STS r10, 0x1000

    def test_filter_ld_x_positive(self):
        self.verify_load_or_store(0x909C, store=False,  reg=9, ixreg='X', ixregval=0x5F) # LD r9, X
        self.bp.dbg.program_counter_write.assert_called_once_with(0x1002 >> 1)

    def test_filter_ld_x_predec_positive(self):
        self.verify_load_or_store(0x911E, store=False,  reg=17, ixreg='X', predec=True, ixregval=0x60) # LD r17, -X
        self.bp.dbg.program_counter_write.assert_called_once_with(0x1002 >> 1)

    def test_filter_ld_x_postinc_positive(self):
        self.verify_load_or_store(0x916D, store=False,  reg=22, ixreg='X', postinc=True, ixregval=0x5F) # LD r22, X+
        self.bp.dbg.program_counter_write.assert_called_once_with(0x1002 >> 1)

    def test_filter_ld_y_predec_positive(self):
        self.verify_load_or_store(0x90EA, store=False,  reg=14, ixreg='Y', predec=True, ixregval=0x60) # LD r14, -Y
        self.bp.dbg.program_counter_write.assert_called_once_with(0x1002 >> 1)

    def test_filter_ld_y_postinc_positive(self):
        self.verify_load_or_store(0x91B9, store=False,  reg=27, ixreg='Y', postinc=True, ixregval=0x5F) # LD r27, Y+
        self.bp.dbg.program_counter_write.assert_called_once_with(0x1002 >> 1)

    def test_filter_ld_z_predec_positive(self):
        self.verify_load_or_store(0x91E2, store=False,  reg=30, ixreg='Z', predec=True, ixregval=0x60) # LD r30, -Y
        self.bp.dbg.program_counter_write.assert_called_once_with(0x1002 >> 1)

    def test_filter_ld_z_postinc_positive(self):
        self.verify_load_or_store(0x91F1, store=False,  reg=31, ixreg='Z', postinc=True, ixregval=0x5F) # LD r27, Y+
        self.bp.dbg.program_counter_write.assert_called_once_with(0x1002 >> 1)

    def test_filter_st_x_positive(self):
        self.verify_load_or_store(0x920C, store=True,  reg=0, ixreg='X', ixregval=0x5F) # ST X, r0
        self.bp.dbg.program_counter_write.assert_called_once_with(0x1002 >> 1)

    def test_filter_st_x_predec_positive(self):
        self.verify_load_or_store(0x920E, store=True,  reg=0, ixreg='X', predec=True, ixregval=0x60) # ST -X, r0
        self.bp.dbg.program_counter_write.assert_called_once_with(0x1002 >> 1)

    def test_filter_st_x_postinc_positive(self):
        self.verify_load_or_store(0x929D, store=True,  reg=9, ixreg='X', postinc=True, ixregval=0x5F) # ST X+, r9
        self.bp.dbg.program_counter_write.assert_called_once_with(0x1002 >> 1)

    def test_filter_st_y_predec_positive(self):
        self.verify_load_or_store(0x92AA, store=True,  reg=10, ixreg='Y', predec=True, ixregval=0x60) # ST -Y, r10
        self.bp.dbg.program_counter_write.assert_called_once_with(0x1002 >> 1)

    def test_filter_st_y_postinc_positive(self):
        self.verify_load_or_store(0x9349, store=True,  reg=20, ixreg='Y', postinc=True, ixregval=0x5F) # ST Y+, r20
        self.bp.dbg.program_counter_write.assert_called_once_with(0x1002 >> 1)

    def test_filter_st_z_predec_positive(self):
        self.verify_load_or_store(0x9362, store=True,  reg=22, ixreg='Z', predec=True, ixregval=0x60) # ST -Z, r22
        self.bp.dbg.program_counter_write.assert_called_once_with(0x1002 >> 1)

    def test_filter_st_z_postinc_positive(self):
        self.verify_load_or_store(0x9371, store=True,  reg=23, ixreg='Z', postinc=True, ixregval=0x5F) # ST Z+, r23
        self.bp.dbg.program_counter_write.assert_called_once_with(0x1002 >> 1)

    def test_filter_ld_st_xyz_below_negative(self):
        self.bp.dbg.sram_read.return_value = bytearray([0x5E, 0x00]) # the indirect address from the index register
        self.assertFalse(self.bp._filter_unsafe_instruction(0x1000, 0x901C)) # LD r1, X
        self.assertFalse(self.bp._filter_unsafe_instruction(0x1000, 0x902D)) # LD r2, X+
        self.assertFalse(self.bp._filter_unsafe_instruction(0x1000, 0x903E)) # LD r3, -X
        self.assertFalse(self.bp._filter_unsafe_instruction(0x1000, 0x9049)) # LD r4, Y+
        self.assertFalse(self.bp._filter_unsafe_instruction(0x1000, 0x904A)) # LD r5, -Y
        self.assertFalse(self.bp._filter_unsafe_instruction(0x1000, 0x9059)) # LD r5, Y+
        self.assertFalse(self.bp._filter_unsafe_instruction(0x1000, 0x905A)) # LD r6, -Y

        self.assertFalse(self.bp._filter_unsafe_instruction(0x1000, 0x921C)) # ST X,  r1
        self.assertFalse(self.bp._filter_unsafe_instruction(0x1000, 0x922D)) # ST X+, r2
        self.assertFalse(self.bp._filter_unsafe_instruction(0x1000, 0x923E)) # ST -X, r3
        self.assertFalse(self.bp._filter_unsafe_instruction(0x1000, 0x9249)) # ST Y+, r4
        self.assertFalse(self.bp._filter_unsafe_instruction(0x1000, 0x924A)) # ST -Y, r5
        self.assertFalse(self.bp._filter_unsafe_instruction(0x1000, 0x9259)) # ST Z+, r5
        self.assertFalse(self.bp._filter_unsafe_instruction(0x1000, 0x925A)) # ST -Z, r6

    def test_filter_ld_st_xyz_above_negative(self):
        self.bp.dbg.sram_read.return_value = bytearray([0x61, 0x00]) # the indirect address from the index register
        self.assertFalse(self.bp._filter_unsafe_instruction(0x1000, 0x901C)) # LD r1, X
        self.assertFalse(self.bp._filter_unsafe_instruction(0x1000, 0x902D)) # LD r2, X+
        self.assertFalse(self.bp._filter_unsafe_instruction(0x1000, 0x903E)) # LD r3, -X
        self.assertFalse(self.bp._filter_unsafe_instruction(0x1000, 0x9049)) # LD r4, Y+
        self.assertFalse(self.bp._filter_unsafe_instruction(0x1000, 0x904A)) # LD r5, -Y
        self.assertFalse(self.bp._filter_unsafe_instruction(0x1000, 0x9059)) # LD r5, Y+
        self.assertFalse(self.bp._filter_unsafe_instruction(0x1000, 0x905A)) # LD r6, -Y

        self.assertFalse(self.bp._filter_unsafe_instruction(0x1000, 0x921C)) # ST X,  r1
        self.assertFalse(self.bp._filter_unsafe_instruction(0x1000, 0x922D)) # ST X+, r2
        self.assertFalse(self.bp._filter_unsafe_instruction(0x1000, 0x923E)) # ST -X, r3
        self.assertFalse(self.bp._filter_unsafe_instruction(0x1000, 0x9249)) # ST Y+, r4
        self.assertFalse(self.bp._filter_unsafe_instruction(0x1000, 0x924A)) # ST -Y, r5
        self.assertFalse(self.bp._filter_unsafe_instruction(0x1000, 0x9259)) # ST Z+, r5
        self.assertFalse(self.bp._filter_unsafe_instruction(0x1000, 0x925A)) # ST -Z, r6

    def test_filter_ldd_y_positive(self):
        self.verify_load_or_store(0x80D8, store=False,  reg=13, ixreg='Y', ixregval=0x5F) # LD r13, Y
        self.bp.dbg.program_counter_write.assert_called_once_with(0x1002 >> 1)

    def test_filter_ldd_z_positive(self):
        self.verify_load_or_store(0x8197, store=False,  reg=25, ixreg='Z', ixregval=0x58) # LD r25, Z+7
        self.bp.dbg.program_counter_write.assert_called_once_with(0x1002 >> 1)

    def test_filter_std_y_positive(self):
        self.verify_load_or_store(0x82D8, store=True,  reg=13, ixreg='Y', ixregval=0x5F) # ST Y, r13
        self.bp.dbg.program_counter_write.assert_called_once_with(0x1002 >> 1)

    def test_filter_std_z_positive(self):
        self.verify_load_or_store(0x8397, store=True,  reg=25, ixreg='Z', ixregval=0x58) # STD Z+7, r25
        self.bp.dbg.program_counter_write.assert_called_once_with(0x1002 >> 1)

    def test_filter_ldd_std_above_and_below_negative(self):
        self.bp.dbg.sram_read.return_value = bytearray([0x57, 0x00]) # the indirect address from the index register
        self.assertFalse(self.bp._filter_unsafe_instruction(0x1000, 0x81ff)) # LDD r31, Y+7
        self.assertFalse(self.bp._filter_unsafe_instruction(0x1000, 0x8264)) # LDD r6, Z+4
        self.assertFalse(self.bp._filter_unsafe_instruction(0x1000, 0x8419)) # LDD r1, Y+9
        self.assertFalse(self.bp._filter_unsafe_instruction(0x1000, 0x8411)) # LDD r1, Z+9
        self.assertFalse(self.bp._filter_unsafe_instruction(0x1000, 0x831f)) # STD Y+7, r17
        self.assertFalse(self.bp._filter_unsafe_instruction(0x1000, 0x8202)) # STD Z+2, r0
        self.assertFalse(self.bp._filter_unsafe_instruction(0x1000, 0x8e5b)) # STD Y+27, r5
        self.assertFalse(self.bp._filter_unsafe_instruction(0x1000, 0x8e66)) # STD Z+30, r6

    def test_filter_in_positive(self):
        self.verify_load_or_store(0xB63F, store=False,  reg=3) # IN r3, 0x3F
        self.bp.dbg.program_counter_write.assert_called_once_with(0x1002 >> 1)

    def test_filter_out_positive(self):
        self.verify_load_or_store(0xBF1F, store=True,  reg=17) # OUT r17, 0x3F
        self.bp.dbg.program_counter_write.assert_called_once_with(0x1002 >> 1)

    def test_filter_in_out_below_negative(self):
        self.assertFalse(self.bp._filter_unsafe_instruction(0x1000, 0xBF1E)) # OUT 0x3E, r17
        self.assertFalse(self.bp._filter_unsafe_instruction(0x1000, 0xB63E)) # IN r3, 0x3E

    def test_filter_cli(self):
        self.bp.dbg.status_register_read.return_value = bytearray([0xFF])
        self.assertTrue(self.bp._filter_unsafe_instruction(0x1000, 0x94F8)) # CLI
        self.bp.dbg.status_register_write.assert_called_once_with(bytearray([0x7F]))
        self.bp.dbg.program_counter_write.assert_called_once_with(0x1002 >> 1)

    def test_filter_sei(self):
        self.bp.dbg.status_register_read.return_value = bytearray([0x0F])
        self.assertTrue(self.bp._filter_unsafe_instruction(0x1000, 0x9478)) # SEI
        self.bp.dbg.status_register_write.assert_called_once_with(bytearray([0x8F]))
        self.bp.dbg.program_counter_write.assert_called_once_with(0x1002 >> 1)

    def test_filter_bclr_negative(self):
        self.assertFalse(self.bp._filter_unsafe_instruction(0x1000, 0x9488)) # CLC
        self.assertFalse(self.bp._filter_unsafe_instruction(0x1000, 0x9498)) # CLZ
        self.assertFalse(self.bp._filter_unsafe_instruction(0x1000, 0x94A8)) # CLN
        self.assertFalse(self.bp._filter_unsafe_instruction(0x1000, 0x94B8)) # CLV
        self.assertFalse(self.bp._filter_unsafe_instruction(0x1000, 0x94C8)) # CLS
        self.assertFalse(self.bp._filter_unsafe_instruction(0x1000, 0x94D8)) # CLH
        self.assertFalse(self.bp._filter_unsafe_instruction(0x1000, 0x94E8)) # CLT

    def test_filter_bset_negative(self):
        self.assertFalse(self.bp._filter_unsafe_instruction(0x1000, 0x9408)) # SEC
        self.assertFalse(self.bp._filter_unsafe_instruction(0x1000, 0x9418)) # SEZ
        self.assertFalse(self.bp._filter_unsafe_instruction(0x1000, 0x9428)) # SEN
        self.assertFalse(self.bp._filter_unsafe_instruction(0x1000, 0x9438)) # SEV
        self.assertFalse(self.bp._filter_unsafe_instruction(0x1000, 0x9448)) # SES
        self.assertFalse(self.bp._filter_unsafe_instruction(0x1000, 0x9458)) # SEH
        self.assertFalse(self.bp._filter_unsafe_instruction(0x1000, 0x9468)) # SET

    def test_filter_brie_set(self):
        self.bp.dbg.status_register_read.return_value = bytearray([0x80])
        self.assertTrue(self.bp._filter_unsafe_instruction(0x1000, 0xF08F)) # BRIE .+34
        self.bp.dbg.program_counter_write.assert_called_once_with((0x1000 + 36) >> 1)

    def test_filter_brie_clear(self):
        self.bp.dbg.status_register_read.return_value = bytearray([0x00])
        self.assertTrue(self.bp._filter_unsafe_instruction(0x1000, 0xF08F)) # BRIE .+34
        self.bp.dbg.program_counter_write.assert_called_once_with((0x1000 + 2) >> 1)

    def test_filter_brid_set(self):
        self.bp.dbg.status_register_read.return_value = bytearray([0x80])
        self.assertTrue(self.bp._filter_unsafe_instruction(0x1000, 0xF66F)) # BRID .-102
        self.bp.dbg.program_counter_write.assert_called_once_with((0x1000 + 2) >> 1)

    def test_filter_brid_clear(self):
        self.bp.dbg.status_register_read.return_value = bytearray([0x00])
        self.assertTrue(self.bp._filter_unsafe_instruction(0x1000, 0xF66F)) # BRID .-102
        self.bp.dbg.program_counter_write.assert_called_once_with((0x1000 - 100) >> 1)

    def test_filter_brie_negative(self):
        self.assertFalse(self.bp._filter_unsafe_instruction(0x1000, 0xF590)) # BRCC .+100
        self.assertFalse(self.bp._filter_unsafe_instruction(0x1000, 0xF591)) # BRNE .+100
        self.assertFalse(self.bp._filter_unsafe_instruction(0x1000, 0xF592)) # BRPL .+100
        self.assertFalse(self.bp._filter_unsafe_instruction(0x1000, 0xF593)) # BRVC .+100
        self.assertFalse(self.bp._filter_unsafe_instruction(0x1000, 0xF594)) # BRGE .+100
        self.assertFalse(self.bp._filter_unsafe_instruction(0x1000, 0xF595)) # BRHC .+100
        self.assertFalse(self.bp._filter_unsafe_instruction(0x1000, 0xF596)) # BRTC .+100

    def test_filter_brid_negative(self):
        self.assertFalse(self.bp._filter_unsafe_instruction(0x1000, 0xF2F8)) # BRCS .-66
        self.assertFalse(self.bp._filter_unsafe_instruction(0x1000, 0xF2F9)) # BREQ .-66
        self.assertFalse(self.bp._filter_unsafe_instruction(0x1000, 0xF2FA)) # BRMI .-66
        self.assertFalse(self.bp._filter_unsafe_instruction(0x1000, 0xF2FB)) # BRVS .-66
        self.assertFalse(self.bp._filter_unsafe_instruction(0x1000, 0xF2FC)) # BRLT .-66
        self.assertFalse(self.bp._filter_unsafe_instruction(0x1000, 0xF2FD)) # BRHS .-66
        self.assertFalse(self.bp._filter_unsafe_instruction(0x1000, 0xF2FE)) # BRTS .-66

    def test_filter_xch(self):
        self.bp.dbg.get_architecture.return_value = 'avr8e'
        self.bp.dbg.sram_read.side_effect = [bytearray([0x5F, 0x00]), bytearray([0x18])]
        self.bp.dbg.status_register_read.return_value = bytearray([0x99])
        self.assertTrue(self.bp._filter_unsafe_instruction(0x1000, 0x9354)) # XCH Z, R21
        self.bp.dbg.sram_read.assert_has_calls([call(30, 2), call(21, 1)])
        self.assertEqual(self.bp.dbg.sram_read.call_count,2)
        self.bp.dbg.status_register_read.assert_called_once()
        self.bp.dbg.status_register_write.assert_called_once_with(bytearray([0x18]))
        self.bp.dbg.sram_write.assert_called_once_with(21, bytearray([0x99]))
        self.bp.dbg.program_counter_write.assert_called_once_with(0x1002 >> 1)

    def test_filter_lac(self):
        self.bp.dbg.get_architecture.return_value = 'avr8e'
        self.bp.dbg.sram_read.side_effect = [bytearray([0x5F, 0x00]), bytearray([0x18])]
        self.bp.dbg.status_register_read.return_value = bytearray([0x99])
        self.assertTrue(self.bp._filter_unsafe_instruction(0x1000, 0x9386)) # LAC Z, R24
        self.bp.dbg.sram_read.assert_has_calls([call(30, 2), call(24, 1)])
        self.assertEqual(self.bp.dbg.sram_read.call_count,2)
        self.bp.dbg.status_register_read.assert_called_once()
        self.bp.dbg.status_register_write.assert_called_once_with(bytearray([0x81]))
        self.bp.dbg.sram_write.assert_called_once_with(24, bytearray([0x99]))
        self.bp.dbg.program_counter_write.assert_called_once_with(0x1002 >> 1)

    def test_filter_las(self):
        self.bp.dbg.get_architecture.return_value = 'avr8e'
        self.bp.dbg.sram_read.side_effect = [bytearray([0x5F, 0x00]), bytearray([0x28])]
        self.bp.dbg.status_register_read.return_value = bytearray([0x99])
        self.assertTrue(self.bp._filter_unsafe_instruction(0x1000, 0x93b5)) # LAS Z, R27
        self.bp.dbg.sram_read.assert_has_calls([call(30, 2), call(27, 1)])
        self.assertEqual(self.bp.dbg.sram_read.call_count,2)
        self.bp.dbg.status_register_read.assert_called_once()
        self.bp.dbg.status_register_write.assert_called_once_with(bytearray([0xB9]))
        self.bp.dbg.sram_write.assert_called_once_with(27, bytearray([0x99]))
        self.bp.dbg.program_counter_write.assert_called_once_with(0x1002 >> 1)

    def test_filter_lat(self):
        self.bp.dbg.get_architecture.return_value = 'avr8e'
        self.bp.dbg.sram_read.side_effect = [bytearray([0x5F, 0x00]), bytearray([0x28])]
        self.bp.dbg.status_register_read.return_value = bytearray([0x99])
        self.assertTrue(self.bp._filter_unsafe_instruction(0x1000, 0x9207)) # LAT Z, R0
        self.bp.dbg.sram_read.assert_has_calls([call(30, 2), call(0, 1)])
        self.assertEqual(self.bp.dbg.sram_read.call_count,2)
        self.bp.dbg.status_register_read.assert_called_once()
        self.bp.dbg.status_register_write.assert_called_once_with(bytearray([0xB1]))
        self.bp.dbg.sram_write.assert_called_once_with(0, bytearray([0x99]))
        self.bp.dbg.program_counter_write.assert_called_once_with(0x1002 >> 1)

    def test_filter_xch_lax_wrong_Z_value(self):
        self.bp.dbg.get_architecture.return_value = 'avr8e'
        self.bp.dbg.sram_read.return_value = bytearray([0x5E, 0x00])
        self.assertFalse(self.bp._filter_unsafe_instruction(0x1000, 0x93F4)) # XCH Z, r31
        self.assertFalse(self.bp._filter_unsafe_instruction(0x1000, 0x9276)) # LAC Z, R7
        self.assertFalse(self.bp._filter_unsafe_instruction(0x1000, 0x92D5)) # LAS Z, R13
        self.assertFalse(self.bp._filter_unsafe_instruction(0x1000, 0x9367)) # LAT Z, R2

    def test_filter_xch_lax_wrong_arch(self):
        self.bp.dbg.get_architecture.return_value = 'avr8'
        self.assertFalse(self.bp._filter_unsafe_instruction(0x1000, 0x93F4)) # XCH Z, r31
        self.assertFalse(self.bp._filter_unsafe_instruction(0x1000, 0x9276)) # LAC Z, R7
        self.assertFalse(self.bp._filter_unsafe_instruction(0x1000, 0x92D5)) # LAS Z, R13
        self.assertFalse(self.bp._filter_unsafe_instruction(0x1000, 0x9367)) # LAT Z, R2
















