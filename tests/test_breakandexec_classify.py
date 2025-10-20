"""
The test suite for classifying opcodes
"""
#pylint: disable=protected-access,missing-function-docstring,invalid-name,line-too-long,missing-class-docstring,too-many-public-methods

from unittest import TestCase
from unittest.mock import Mock, create_autospec
from pyavrocd.breakexec import BreakAndExec
from pyavrocd.xavrdebugger import XAvrDebugger
from .util.instr import instrmap

class TestBreakAndExecClassify(TestCase):

    def setUp(self):
        mock_dbg = create_autospec(XAvrDebugger, spec_set=False, instance=True)
        mock_dbg.memory_info = Mock()
        mock_dbg.memory_info.memory_info_by_name.return_value = {'size' : 100,'address' : 0x60 }
        mock_dbg.get_hwbpnum.return_value = 1
        mock_dbg.get_architecture.return_value = "avr8"
        self.bp = BreakAndExec(Mock(), mock_dbg, Mock())

    def test_extract_io_addr(self):
        for instr in range(0x10000):
            if self.bp._in_or_out_instr(instr):
                ioaddr = self.bp._extract_io_addr(instr)
                realioaddr = int(instrmap[instr][2 - int(self.bp._is_out_instr(instr))],16)
                self.assertEqual(ioaddr, realioaddr,
                                "Failed at 0x%04X, computed: %d, really: %d" % (instr, ioaddr, realioaddr))

    def test_extract_displacement(self):
        for instr in range(0x10000):
            if self.bp._indirect_load_or_store_with_displacement_instr(instr):
                disp = self.bp._extract_displacement(instr)
                realdisp = instrmap[instr][2 - int(self.bp._is_store_instr(instr))][1:]
                realdisp = int(realdisp) if realdisp else 0
                self.assertEqual(disp, realdisp,
                                    "Failed at 0x%04X, computed: %d, really: %d" % (instr, disp, realdisp))

    def test_is_out_instr(self):
        for instr in range(0x10000):
            if self.bp._in_or_out_instr(instr):
                self.assertEqual(self.bp._is_out_instr(instr), instrmap[instr][0] == 'out', "Failed at 0x%04X" % instr)


    def test_is_post_incr(self):
        for instr in range(0x10000):
            if self.bp._indirect_load_or_store_without_displacement_instr(instr):
                self.assertEqual(self.bp._is_post_incr(instr),
                                     instrmap[instr][2 - int(self.bp._is_store_instr(instr))] in ['X+', 'Y+', 'Z+'],
                                     "Failed at 0x%04X" % instr)

    def test_is_pre_decr(self):
        for instr in range(0x10000):
            if self.bp._indirect_load_or_store_without_displacement_instr(instr):
                self.assertEqual(self.bp._is_pre_decr(instr),
                                     instrmap[instr][2 - int(self.bp._is_store_instr(instr))] in ['-X', '-Y', '-Z'],
                                     "Failed at 0x%04X" % instr)

    def test_is_change_ix(self):
        for instr in range(0x10000):
            if self.bp._indirect_load_or_store_without_displacement_instr(instr):
                self.assertEqual(self.bp._is_change_ix(instr),
                                     instrmap[instr][2 - int(self.bp._is_store_instr(instr))] in ['-X', '-Y', '-Z',
                                                                                                  'X+', 'Y+', 'Z+'],
                                     "Failed at 0x%04X" % instr)

    def test_is_x_reg(self):
        for instr in range(0x10000):
            if self.bp._indirect_load_or_store_without_displacement_instr(instr) or \
               self.bp._indirect_load_or_store_with_displacement_instr(instr):
                self.assertEqual(self.bp._is_x_reg(instr),
                                     'X' in instrmap[instr][2 - int(self.bp._is_store_instr(instr))],
                                     "Failed at 0x%04X" % instr)

    def test_is_y_reg(self):
        for instr in range(0x10000):
            if (self.bp._indirect_load_or_store_without_displacement_instr(instr) or \
               self.bp._indirect_load_or_store_with_displacement_instr(instr)) and \
               not self.bp._is_x_reg(instr):
                self.assertEqual(self.bp._is_y_reg(instr),
                   'Y' in instrmap[instr][2 - int(self.bp._is_store_instr(instr))],
                                     "Failed at 0x%04X with Y-reg" % instr)
                self.assertEqual(not self.bp._is_y_reg(instr),
                   'Z' in instrmap[instr][2 - int(self.bp._is_store_instr(instr))],
                                     "Failed at 0x%04X with Z-reg" % instr)

    def test_extract_register(self):
        for instr in range(0x10000):
            if self.bp._long_load_or_store_instr(instr) or \
                self.bp._indirect_load_or_store_without_displacement_instr(instr) or \
                self.bp._indirect_load_or_store_with_displacement_instr(instr) or \
                self.bp._exchange_instr(instr) or \
                self.bp._in_or_out_instr(instr):
                right = True
                if self.bp._in_or_out_instr(instr):
                    right = self.bp._is_out_instr(instr)
                elif not self.bp._exchange_instr(instr):
                    right = self.bp._is_store_instr(instr)
                realreg = instrmap[instr][1 + int(right)]
                reg = 'r' + str(self.bp._extract_register(instr))
                self.assertEqual(reg, realreg,
                                     "Failed at 0x%04X, computed: %s, really: %s" % (instr, reg, realreg))


    def test_is_store_instr(self):
        for instr in range(0x10000):
            if self.bp._long_load_or_store_instr(instr) or \
                self.bp._indirect_load_or_store_without_displacement_instr(instr) or \
                self.bp._indirect_load_or_store_with_displacement_instr(instr):
                self.assertEqual(self.bp._is_store_instr(instr), instrmap[instr][0][:2] == 'st',
                                    "Failed at 0x%04X with store" % instr)
                self.assertEqual(not self.bp._is_store_instr(instr), instrmap[instr][0][:2] == 'ld',
                                    "Failed at 0x%04X with load" % instr)

    def test_low_alu_instr(self):
        for instr in range(0x10000):
            if instr in instrmap:
                self.assertEqual(self.bp._low_alu_instr(instr),
                                 instrmap[instr][0] in ['nop', 'movw', 'muls', 'fmul', 'fmuls',
                                                            'fmulsu', 'mulsu', 'cpc', 'sbc', 'add',
                                                            'adc','and', 'cp', 'sub', 'eor', 'or',
                                                            'mov', 'cpi', 'sbci', 'subi', 'ori',
                                                            'andi'],
                                    "Failed at 0x%04X" % instr)

    def test_lax_instr(self):
        for instr in range(0x10000):
            if instr in instrmap:
                self.assertEqual(self.bp._lax_instr(instr), instrmap[instr][0] in [ 'lac', 'las', 'lat' ],
                                     "Failed at 0x%04X" % instr)

    def test_lac_instr(self):
        for instr in range(0x10000):
            if instr in instrmap:
                self.assertEqual(self.bp._lac_instr(instr), instrmap[instr][0] == 'lac',
                                     "Failed at 0x%04X" % instr)

    def test_las_instr(self):
        for instr in range(0x10000):
            if instr in instrmap:
                self.assertEqual(self.bp._las_instr(instr), instrmap[instr][0] == 'las',
                                     "Failed at 0x%04X" % instr)

    def test_lat_instr(self):
        for instr in range(0x10000):
            if instr in instrmap:
                self.assertEqual(self.bp._lat_instr(instr), instrmap[instr][0] == 'lat',
                                     "Failed at 0x%04X" % instr)

    def test_branch_instr(self):
        for instr in range(0x10000):
            if instr in instrmap:
                self.assertEqual(self.bp._branch_instr(instr),
                                    instrmap[instr][0] in ['ret', 'reti', 'jmp', 'ijmp', 'eijmp', 'rjmp',
                                                               'call', 'icall', 'eicall', 'rcall',
                                                               'brcs', 'breq', 'brmi', 'brvs', 'brlt',
                                                               'brhs', 'brts', 'brie',
                                                               'brcc', 'brne', 'brpl', 'brvc', 'brge',
                                                               'brhc', 'brtc', 'brid',
                                                               'cpse', 'sbic', 'sbis', 'sbrc', 'sbrs'],
                                 "Failed at 0x%04X" % instr)

    def test_pop_instr(self):
        for instr in range(0x10000):
            if instr in instrmap:
                self.assertEqual(self.bp._pop_instr(instr),
                                     instrmap[instr][0] == 'pop',
                                     "Failed at 0x%04X" % instr)

    def test_push_instr(self):
        for instr in range(0x10000):
            if instr in instrmap:
                self.assertEqual(self.bp._push_instr(instr),
                                     instrmap[instr][0] == 'push',
                                     "Failed at 0x%04X" % instr)

    def test_callx_instr(self):
        for instr in range(0x10000):
            if instr in instrmap:
                self.assertEqual(self.bp._callx_instr(instr),
                                     instrmap[instr][0] in [ 'call', 'icall', 'eicall', 'rcall' ],
                                     "Failed at 0x%04X" % instr)

    def test_jmpx_instr(self):
        for instr in range(0x10000):
            if instr in instrmap:
                self.assertEqual(self.bp._jmpx_instr(instr),
                                     instrmap[instr][0] in [ 'jmp', 'ijmp', 'eijmp', 'rjmp' ],
                                     "Failed at 0x%04X" % instr)
    def test_relativ_branch_instr(self):
        for instr in range(0x10000):
            if instr in instrmap:
                self.assertEqual(self.bp._relative_branch_instr(instr),
                                     instrmap[instr][0] in [ 'rcall', 'rjmp' ],
                                     "Failed at 0x%04X" % instr)

    def test_retx_instr(self):
        for instr in range(0x10000):
            if instr in instrmap:
                self.assertEqual(self.bp._retx_instr(instr),
                                     instrmap[instr][0] in [ 'ret', 'reti' ],
                                     "Failed at 0x%04X" % instr)



    def test_relative_branch_instr(self):
        for instr in range(0x10000):
            if instr in instrmap:
                self.assertEqual(self.bp._relative_branch_instr(instr),
                                     instrmap[instr][0] in ['rcall', 'rjmp'])

    def test_compute_destination_of_relative_branch(self):
        self.assertEqual(self.bp._compute_destination_of_relative_branch(0xD100, 0x2000), 0x2202)
        self.assertEqual(self.bp._compute_destination_of_relative_branch(0xCFFF, 0x2000), 0x2000)

    def test_skip_instr(self):
        for instr in range(0x10000):
            if instr in instrmap:
                self.assertEqual(self.bp._skip_instr(instr),
                                    instrmap[instr][0] in ['cpse', 'sbic', 'sbis', 'sbrc', 'sbrs'],
                                    "Failed at 0x%04X" % instr)

    def test_cond_branch_instr(self):
        for instr in range(0x10000):
            if instr in instrmap:
                self.assertEqual(self.bp._cond_branch_instr(instr),
                                    instrmap[instr][0] in [ 'brcs', 'breq', 'brmi', 'brvs', 'brlt',
                                                                'brhs', 'brts', 'brie',
                                                                'brcc', 'brne', 'brpl', 'brvc', 'brge',
                                                                'brhc', 'brtc', 'brid'],
                                    "Failed at 0x%04X" % instr)

    def test_branch_on_ibit_instr(self):
        for instr in range(0x10000):
            if instr in instrmap:
                self.assertEqual(self.bp._branch_on_ibit_instr(instr),
                                    instrmap[instr][0] in ['brie', 'brid'],
                                    "Failed at 0x%04X" % instr)

    def test_compute_possible_destination_of_branch(self):
        for instr in range(0x10000):
            if self.bp._cond_branch_instr(instr):
                realrelative = int(instrmap[instr][1][1:])
                computed = self.bp._compute_possible_destination_of_branch(instr, 0x1000)
                self.assertEqual(computed,
                                     0x1002+realrelative,
                                     "Failed at 0x%04X, computed: %d, really: %d" % (instr, computed, 0x1002+realrelative))

    def test_compute_destination_of_ibranch(self):
        for ibit in [ False, True ]:
            for instr in range(0x10000):
                if self.bp._branch_on_ibit_instr(instr):
                    computed = self.bp._compute_destination_of_ibranch(instr, ibit, 0x1000)
                    if (instrmap[instr][0] == 'brie') ^ ibit:
                        realdest = 0x1002
                    else:
                        realdest = int(instrmap[instr][1][1:]) + 0x1002
                    self.assertEqual(computed,
                                         realdest,
                                        "Failed at 0x%04X, computed: %d, really: %d" % (instr, computed, realdest))

    def test_long_load_or_store_instr(self):
        for instr in range(0x10000):
            if instr in instrmap:
                self.assertEqual(self.bp._long_load_or_store_instr(instr),
                                     instrmap[instr][0] in ['lds', 'sts'],
                                     "Failed at 0x%04X" % instr)

    def test_indirect_load_or_store_without_displacement_instr(self):
        for instr in range(0x10000):
            if instr in instrmap:
                self.assertEqual(self.bp._indirect_load_or_store_without_displacement_instr(instr),
                                     instrmap[instr][0] in ['ld', 'st'] and (instrmap[instr][1] in ['X', '-X', 'X+',
                                                                                                       '-Y', 'Y+',
                                                                                                       '-Z', 'Z+'] or
                                                                            instrmap[instr][2] in ['X', '-X', 'X+',
                                                                                                       '-Y', 'Y+',
                                                                                                       '-Z', 'Z+']),
                                     "Failed at 0x%04X" % instr)

    def test_indirect_load_or_store_with_displacement_instr(self):
        for instr in range(0x10000):
            if instr in instrmap:
                self.assertEqual(self.bp._indirect_load_or_store_with_displacement_instr(instr),
                                     instrmap[instr][0] in ['ldd', 'std'] or \
                                     (instrmap[instr][0] in ['ld', 'st'] and (instrmap[instr][1] in ['Y', 'Z'] or
                                                                              instrmap[instr][2] in ['Y', 'Z'])),
                                    "Failed at 0x%04X" % instr)

    def test_exchange_instr(self):
        for instr in range(0x10000):
            if instr in instrmap:
                self.assertEqual(self.bp._exchange_instr(instr),
                                     instrmap[instr][0] == 'xch',
                                    "Failed at 0x%04X" % instr)

    def test_in_or_out_instr(self):
        for instr in range(0x10000):
            if instr in instrmap:
                self.assertEqual(self.bp._in_or_out_instr(instr),
                                     instrmap[instr][0] in ['in', 'out'],
                                    "Failed at 0x%04X" % instr)

    def test_bit_clear_or_set_in_sreg_instr(self):
        for instr in range(0x10000):
            if instr in instrmap:
                self.assertEqual(self.bp._bit_clear_or_set_in_sreg_instr(instr),
                                     instrmap[instr][0] in ['clc', 'clh', 'cli', 'cln', 'cls', 'clt', 'clv', 'clz',
                                                            'sec', 'seh', 'sei', 'sen', 'ses', 'set', 'sev', 'sez'],
                                    "Failed at 0x%04X" % instr)

    def test_two_word_instr(self):
        for instr in range(0x10000):
            if instr in instrmap:
                self.assertEqual(self.bp._two_word_instr(instr),
                                    instrmap[instr][0] in ['sts', 'lds', 'call', 'jmp'],
                                    "Failed at 0x%04X" % instr)
