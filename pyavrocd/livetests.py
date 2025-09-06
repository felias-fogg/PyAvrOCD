"""
Live Tests for dw-gdbserver
"""
#pylint: disable=protected-access

import time
import logging
from logging import getLogger
import binascii

# pylint: disable=too-many-instance-attributes
class LiveTests():
    """
    This class implements a range of integration tests in a live environment.
    Will be activated by the monitor command 'LiveTests'.
    """

    def __init__(self, handler):
        self.logger = getLogger('pyavrocd.livetests')
        self.handler = handler
        self.dbg = handler.dbg
        self.mem = handler.mem
        self.mon = handler.mon
        self.bp = handler.bp
        self.backup_send_packet = None
        self.send_string = ""
        self.success = 0
        self.failure = 0
        self.tests_total = 0
        self.flash_transparent = False
        self.sram_start = self.dbg.memory_info.\
          memory_info_by_name('internal_sram')['address']
        self.test_code = self.setup_test_code(self.sram_start == 0x60)

    def setup_test_code(self, small):
        """
        This sets up the test code in a bytearray. If small is True,
        then the SRAM address is 0x0060 instead of 0x0100.
        bADDR   wADDR
        1aa:	d5:   00 00       	nop
        1ac:	d6:   00 00       	nop
        1ae:	d7:   00 00       	nop
        1b0:	d8:   ff cf       	rjmp .-2      	; 0x1b0 <DL>
        1b2:	d9:   29 e4       	ldi	 r18, 0x49	; 73
        1b4:	da:   20 93 00 01 	sts	0x0100, r18	; 0x800100 <dest>
        1b8:	dc:   00 91 00 01 	lds	r16, 0x0100	; 0x800100 <dest>
        1bc:	de:   00 00       	nop
        1be:	df:   f5 cf       	rjmp .-22     	; 0x1aa <START>
        1c0:	e0:   0e 94 e4 00 	call 0x1c8	    ; 0x1c8 <SUBR>
        1c4:	e2:   0c 94 d9 00 	jmp	0x1b2	    ; 0x1b2 <START2>
        1c8:	e4:   11 e9       	ldi	r17, 0x91	; 145
        1ca:	e5:   08 95       	ret
        1cc:    e6:   98 95         break
        """
        if small:
            msb = 0x00
            lsb = 0x60
        else:
            msb = 0x01
            lsb = 0x00
        return bytearray([0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0xff, 0xcf, 0x29, 0xe4,
                              0x20, 0x93, lsb, msb, 0x00, 0x91, lsb, msb, 0x00, 0x00,
                              0xf5, 0xcf, 0x0e, 0x94, 0xe4, 0x00, 0x0c, 0x94, 0xd9, 0x00,
                              0x11, 0xe9, 0x08, 0x95, 0x98, 0x95])

    def mock_send_packet(self, mes):
        """
        Instead of sending the message mes to GDB, it simply returns the string
        so that it can be checked by the test procedure.
        """
        self.send_string = mes

    # pylint: disable=too-many-statements
    def run_tests(self):
        """
        Running the live tests. All exceptions are caught, counted as failure, and
        the remanibg tests are skipped. In the end, we restore the send_packet method
        and give a short statistic.
        """
        self.backup_send_packet = self.handler.send_packet
        self.mon.set_default_state()
        self.success = 0
        self.failure = 0
        self.tests_total = 26
        if self.dbg.iface == 'jtag' and self.dbg.architecture == 'avr8':
            self.flash_transparent = True # breakpoints are filtered out
        self.mon._cache = False
        try:
            self.handler.send_debug_message("Running live tests ...")
            self.logger.info("Starting live tests (will clobber SRAM and flash)")
            self.handler.send_packet = self.mock_send_packet
            self._live_test_load()
            self._live_test_verify_loaded()
            self._live_test_continue_stop()
            self._live_test_continue_at_break()
            self._live_test_get_register()
            self._live_test_set_register()
            self._live_test_get_memory_sram()
            self._live_test_get_memory_eeprom()
            self._live_test_get_memory_flash()
            self._live_test_set_memory_sram()
            self._live_test_set_memory_eeprom()
            self._live_test_get_one_data_register()
            self._live_test_get_sreg()
            self._live_test_get_sp()
            self._live_test_get_pc()
            self._live_test_set_one_data_register()
            self._live_test_set_sreg()
            self._live_test_set_sp()
            self._live_test_set_pc()
            self._live_test_step()
            self._live_test_vcont_range()
            self._live_test_vcont_step_with_protected_bp()
            self._live_test_vcont_step_with_old_exec()
            self._live_test_vcont_step_hwbp_unprotected()
            self._live_test_v_flash_erase_clean_bps()
            self._live_test_load_clean_bps()
        except Exception as e:
            self.failure += 1
            self.logger.error("... failed")
            if self.logger.getEffectiveLevel() == logging.DEBUG:
                raise
            self.logger.info("Graceful exception: %s", e)
        finally:
            self.logger.info("Live tests completed.")
            self.logger.info("Tests succeeded: %s", self.success)
            self.logger.info("Tests failed:    %s", self.failure)
            self.logger.info("Tests skipped:   %s", self.tests_total -
                                 self.success - self.failure)
            self.handler.send_packet = self.backup_send_packet
            if self.success == self.tests_total:
                self.handler.send_debug_message("... live tests successfully finished.")
            else:
                self.handler.send_debug_message("... live tests finished with some failures.")
            self.logger.info("Loaded binary has been deleted")
            self.mem._flash = bytearray()
            self.mem._flashmem_start_prog = 0
            self.logger.info("All monitor state variables set to default values")
            self.mon.set_default_state()

    def check_result(self, success_condition):
        """
        Check for success, report, and count
        """
        if success_condition:
            self.success += 1
            self.logger.info("... passed")
        else:
            self.failure += 1
            self.logger.error("... failed")

    # pylint: disable=protected-access
    def _live_test_load(self):
        """
        Loads test code and checks that load has been successful (X-packet)
        """
        self.logger.info("Running 'load' test ...")
        verify_save = self.mon._verify
        self.mon._verify = False # because on mEDBG debuggers, first page is not always writeable
        test_code = self.handler.escape(self.test_code)
        header = "0001AA,%0X:" % len(test_code)
        self.send_string = ""
        self.handler.dispatch("X", header.encode("ascii") + test_code)
        self.handler.dispatch(None, None) # signal timeout, so that last record will be written
        self.mon._verify = verify_save
        self.check_result(self.send_string == "OK")

    def _live_test_verify_loaded(self):
        """
        Verify that binary code has been loaded to flash memory.
        """
        self.logger.info("Running 'verify loaded' test ...")
        self.mon._cache = False # disable caching
        codesnippet = self.mem.flash_read(0x1aa, len(self.test_code))
        self.logger.debug("Code flashed: %s", ' '.join('0x{:02x}'.format(x) for x in codesnippet))
        self.mon._cache = True # re-enable caching
        self.check_result(codesnippet == self.test_code)

    # no tests for '!' and '?' packstes because unit tests are enough

    def _live_test_continue_stop(self):
        """
        Test 'continue' and 'stop' function.
        """
        self.logger.info("Running 'continue with signal' and 'stop' test ...")
        self.handler.dispatch("C", b"05;01AA")
        time.sleep(0.01)
        self.dbg.stop()
        self.logger.debug("Sent: %s", self.send_string)
        self.check_result(self.dbg.program_counter_read() == (0x1B0 >> 1))

    def _live_test_continue_at_break(self):
        """
        Test 'continue' at a 'break' location
        """
        self.logger.info("Running 'continue' at a location with a 'break' instruction ...")
        self.handler.dispatch('c', b"01cc")
        self.logger.debug("Sent: %s", self.send_string)
        self.check_result(self.send_string == "S04")
        self.dbg.stop() # stop execution in any case


    # no test for 'D' packet because unit tests are enough

    def _live_test_get_register(self):
        """
        Test 'get register' function.
        """
        self.logger.info("Running 'get register' test ...")
        newdata = bytearray(list(range(32,64))) + \
          bytearray([0x99, 0x77, 0x00, 0x46, 0x34, 0x00, 0x00 ])
        self.dbg.register_file_write(newdata[:32])
        self.dbg.status_register_write(newdata[32:33])
        self.dbg.stack_pointer_write(newdata[33:35])
        self.dbg.program_counter_write(0x000003446 >> 1)
        self.handler.dispatch("g", b"")
        self.logger.debug("Newdata:     %s", (binascii.hexlify(newdata)).decode('ascii'))
        self.logger.debug("Sent string: %s", self.send_string)
        self.check_result(self.send_string == (binascii.hexlify(newdata)).decode('ascii'))

    def _live_test_set_register(self):
        """
        Test 'set register' function.
        """
        self.logger.info("Running 'set register' test ...")
        newdata = binascii.hexlify(bytearray(list(range(64,96))) + \
          bytearray([0x88, 0x66, 0x00, 0x26, 0x16, 0x00, 0x00 ]))
        self.handler.dispatch("G", newdata)
        regs = self.dbg.register_file_read()
        sreg = self.dbg.status_register_read()
        sp = self.dbg.stack_pointer_read()
        # get PC as word address and make a byte address
        pc = self.dbg.program_counter_read() << 1
        reg_string = ""
        for reg in regs:
            reg_string = reg_string + format(reg, '02x')
        sreg_string = ""
        for reg in sreg:
            sreg_string = sreg_string + format(reg, '02x')
        sp_string = ""
        for reg in sp:
            sp_string = sp_string + format(reg, '02x')
        pcstring = binascii.hexlify(pc.to_bytes(4,byteorder='little')).decode('ascii')
        reg_string = reg_string + sreg_string + sp_string + pcstring
        self.logger.debug("Newdata:     %s", newdata.decode("ascii"))
        self.logger.debug("New setting: %s", reg_string)
        self.check_result(reg_string == newdata.decode("ascii") and
                              self.send_string == "OK")

    def _live_test_get_memory_sram(self):
        """
        Tests 'get memory' function on sram
        """
        self.logger.info("Running 'get memory sram' test ...")
        data = bytearray([0x07,0x99,0x12])
        self.dbg.sram_write(self.sram_start+2, data)
        self.handler.dispatch('m', b'80%04X,03' % (self.sram_start+2))
        self.check_result(self.send_string == binascii.hexlify(data).decode('ascii'))

    def _live_test_get_memory_eeprom(self):
        """
        Tests 'get memory' function on eeprom
        """
        self.logger.info("Running 'get memory eeprom' test ...")
        data = bytearray([0x08,0x77,0x51])
        self.dbg.eeprom_write(2, data)
        self.handler.dispatch('m', b'81%04X,03' % 2)
        self.check_result(self.send_string == binascii.hexlify(data).decode('ascii'))

    def _live_test_get_memory_flash(self):
        """
        Tests 'get memory' function on flash memory
        """
        self.logger.info("Running 'get memory flash' test ...")
        data = bytearray([0x95,0x98,0x95]) # is already flashed at 0x1cb
        self.handler.dispatch('m', b'00%04X,03' % 0x1cb)
        self.check_result(self.send_string == binascii.hexlify(data).decode('ascii'))

    def _live_test_set_memory_sram(self):
        """
        Tests 'set memory' function on sram
        """
        self.logger.info("Running 'set memory sram' test ...")
        data = bytearray([0x65,0x99,0x12,0x34,0x56])
        self.handler.dispatch('M', b'80%04X,05:%s' % ((self.sram_start+2),
                                                       binascii.hexlify(data)))
        newdata = self.dbg.sram_read(self.sram_start+2, 5)
        self.check_result(newdata == data and self.send_string == "OK")

    def _live_test_set_memory_eeprom(self):
        """
        Tests 'set memory' function on eeprom
        """
        self.logger.info("Running 'set memory eeprom' test ...")
        data = bytearray([0x75,0x96,0x17,0x84,0x19])
        self.logger.debug("Data to store: %s", ' '.join([format(n, "02X") for n in data]))
        self.handler.dispatch('M', b'81%04X,05:%s' % (2, binascii.hexlify(data)))
        newdata = self.dbg.eeprom_read(2, 5)
        self.logger.debug("Retrieved data: %s", ' '.join([format(n, "02X") for n in newdata]))
        self.check_result(newdata == data and self.send_string == "OK")

    def _live_test_get_one_data_register(self):
        """
        Tests 'get one register' function
        """
        self.logger.info("Running 'get one data register' test ...")
        self.dbg.sram_write(0x16, bytearray([0x71]))
        self.handler.dispatch('p', b'16')
        self.check_result(self.send_string == '71')

    def _live_test_get_sreg(self):
        """
        Tests 'get sreg' function
        """
        self.logger.info("Running 'get status register' test ...")
        self.dbg.status_register_write(bytearray([0xFC]))
        self.logger.debug("sreg: %s", self.dbg.status_register_read())
        self.handler.dispatch('p', b'20')
        self.logger.debug("Result: %s", self.send_string)
        self.check_result(self.send_string == 'FC')

    def _live_test_get_sp(self):
        """
        Tests 'get sp' function
        """
        self.logger.info("Running 'get stack pointer' test ...")
        self.dbg.stack_pointer_write(bytearray([0x61, 0x00]))
        self.logger.debug("sp: %s", self.dbg.stack_pointer_read())
        self.handler.dispatch('p', b'21')
        self.logger.debug("Result: %s", self.send_string)
        self.check_result(self.send_string == '6100')

    def _live_test_get_pc(self):
        """
        Tests 'get pc' function
        """
        self.logger.info("Running 'get program counter' test ...")
        self.dbg.program_counter_write(0x1aa >> 1)
        self.logger.debug("pc: %x", self.dbg.program_counter_read() << 1)
        self.handler.dispatch('p', b'22')
        self.logger.debug("Result: %s", self.send_string)
        self.check_result(self.send_string == 'aa010000')

    def _live_test_set_one_data_register(self):
        """
        Tests 'set one register' function
        """
        self.logger.info("Running 'set one data register' test ...")
        self.handler.dispatch('P', b'03,26')
        result = self.dbg.sram_read(0x03,1)
        self.check_result(self.send_string == 'OK' and result[0] == 0x26)

    def _live_test_set_sreg(self):
        """
        Tests 'set sreg' function
        """
        self.logger.info("Running 'set status register' test ...")
        self.handler.dispatch('P', b'20=87')
        result = self.dbg.status_register_read()
        self.check_result(self.send_string == 'OK' and result[0] == 0x87)

    def _live_test_set_sp(self):
        """
        Tests 'set sp' function
        """
        self.logger.info("Running 'set stack pointer' test ...")
        self.handler.dispatch('P', b'21=3400')
        result = self.dbg.stack_pointer_read()
        self.check_result(self.send_string == 'OK' and result[0] == 0x34 and result[1] == 0)

    def _live_test_set_pc(self):
        """
        Tests 'set pc' function
        """
        self.logger.info("Running 'set program counter' test ...")
        self.handler.dispatch('P', b'22=AA010000')
        result = self.dbg.program_counter_read() << 1
        self.check_result(self.send_string == 'OK' and result == 0x1AA)

    # qAttached, qOffsets, qRcmd, qSupported, qThreadInfo, qsThreadInfo, qXfer:memory-map:read
    # covered by unit tests

    def _live_test_step(self):
        """
        Tests 'step' function
        """
        self.logger.info("Running 'step' test ...")
        self.send_string = ""
        self.dbg.sram_write(self.sram_start, bytearray([0]))
        self.dbg.sram_write(16, bytearray([0,0,0,0]))
        self.logger.debug("PC=%0X", self.dbg.program_counter_read() << 1)
        self.logger.debug("regs=%s", self.dbg.sram_read(16, 3))
        self.logger.debug("mem=%s", self.dbg.sram_read(self.sram_start, 1))
        self.handler.dispatch('S', b'05;01b2')
        time.sleep(0.1)
        self.handler.poll_events()
        send1 = self.send_string
        self.logger.debug("Send1: %s", self.send_string)
        self.send_string = ""
        self.handler.dispatch('s', b'')
        time.sleep(0.1)
        self.handler.poll_events()
        send2 = self.send_string
        self.logger.debug("Send2: %s", self.send_string)
        self.send_string = ""
        self.handler.dispatch('s', b'')
        time.sleep(0.1)
        self.handler.poll_events()
        send3 = self.send_string
        self.logger.debug("Send3: %s", self.send_string)
        self.logger.debug("PC=%0X", self.dbg.program_counter_read() << 1)
        self.logger.debug("regs=%s", self.dbg.sram_read(16, 3))
        self.logger.debug("mem=%s", self.dbg.sram_read(self.sram_start, 1))
        self.check_result(self.dbg.program_counter_read() << 1 == 0x1BC and
                              self.dbg.sram_read(16, 3) == bytearray([73, 0, 73]) and
                              self.dbg.sram_read(self.sram_start, 1) == bytearray([73]) and
                              send1.startswith("T05") and send2.startswith("T05") and
                              send3.startswith("T05"))

    # T-package and vCont;? is covered by unit test
    # vCont;c, vCont;C, vCont;s, vCont;S covered already above

    def _live_test_vcont_range(self):
        """
        Testing the range step command
        """
        self.logger.info("Running vcont range test ...")
        self.dbg.program_counter_write(0x1b2 >> 1)
        self.send_string = ""
        self.handler.dispatch("vCont", b";r1b2,1c0")
        time.sleep(0.1)
        self.handler.poll_events()
        send1 = self.send_string
        self.logger.debug("Result of range-stepping: %s", send1)
        self.dbg.stop() # in order to stop a runaway!
        pc1 = self.dbg.program_counter_read() << 1
        self.send_string = ""
        self.handler.dispatch("vCont", b";r1b2,1c0")
        time.sleep(0.1)
        self.handler.poll_events()
        send2 = self.send_string
        self.dbg.stop() # in order to stop a runaway!
        pc2 = self.dbg.program_counter_read() << 1
        self.logger.debug("Result of range-stepping: %s", send2)
        self.check_result(pc1 == 0x1b4 and pc2 == 0x1aa and
                              send1.startswith("T05") and send2.startswith("T05"))

    def _live_test_vcont_step_with_protected_bp(self):
        """
        Testing the step command when there is a disabled SWBP at the current position.
        This SWBP should not be removed in order to avoid superfluous reprogramming
        """
        self.logger.info("Running 'vcont step' test with protected SWBP...")
        if self.flash_transparent:
            self.logger.info("Cannot be run on JTAG megaAVRs")
            self.check_result(True)
            return
        self.mon._onlyswbps = True
        self.dbg.program_counter_write(0x1c4 >> 1)
        self.dbg.stack_pointer_write(bytearray([0x34, 0x00]))
        self.dbg.status_register_write(bytearray([0x87]))
        self.handler.dispatch("Z", b"1,1b2,2")
        self.handler.dispatch("Z", b"1,1b4,2")
        self.mon._cache = False
        opc1 = self.mem.flash_read_word(0x1b2)
        self.logger.debug("Opcode before 'continue': 0x%X", opc1)
        self.send_string = ""
        self.handler.dispatch("vCont", b";c")
        time.sleep(0.1)
        self.handler.poll_events()
        send1 = self.send_string
        self.dbg.stop() # in order to stop a runaway!
        self.logger.debug("Result of 'continue': %s", send1)
        opc2 = self.mem.flash_read_word(0x1b2)
        self.logger.debug("Opcode after 'continue': 0x%X", opc2)
        self.handler.dispatch("z", b"1,1b2,2")
        self.handler.dispatch("z", b"1,1b4,2")
        opc3 = self.mem.flash_read_word(0x1b2)
        self.logger.debug("Opcode after 'delete BP': 0x%X", opc3)
        self.handler.dispatch("Z", b"1,1b4,2")
        opc4 = self.mem.flash_read_word(0x1b2)
        self.logger.debug("Opcode before 'step': 0x%X", opc4)
        self.send_string = ""
        self.handler.dispatch("vCont", b";s")
        time.sleep(0.1)
        self.handler.poll_events()
        send2 = self.send_string
        self.logger.debug("Result of 'step': %s", send2)
        opc5 = self.mem.flash_read_word(0x1b2)
        self.logger.debug("Opcode after 'step': 0x%X", opc5)
        self.handler.dispatch("Z", b"1,1b2,2")
        opc6 = self.mem.flash_read_word(0x1b2)
        self.logger.debug("Opcode after 'insert BP': 0x%X", opc6)
        self.check_result(self.dbg.program_counter_read() == (0x1b4 >> 1) and
                              send1 == "T0520:87;21:3400;22:b2010000;thread:1;" and
                              send2 == "T0520:87;21:3400;22:b4010000;thread:1;" and
                              opc1 == 0xe429 and opc2 == 0x9598 and
                              opc3 == opc2 and opc4 == opc2 and opc5 == opc2 and
                              opc6 == opc2)
        self.mon._cache = True
        self.bp.cleanup_breakpoints()
        self.mon._onlyswbps = False

    def _live_test_vcont_step_with_old_exec(self):
        """
        This test uses old-style execution in order to demonstrate that
        this leads to reprogramming flash at each breakpoint hit.
        """
        self.logger.info("Running 'vcont step' test using old exec forcing 2xflashing ...")
        if self.flash_transparent:
            self.logger.info("Cannot be run on JTAG megaAVRs")
            self.check_result(True)
            return
        self.mon._onlyswbps = True
        self.mon._old_exec = True
        self.dbg.program_counter_write(0x1aa >> 1)
        self.dbg.stack_pointer_write(bytearray([0x34, 0x00]))
        self.dbg.status_register_write(bytearray([0x87]))
        self.handler.dispatch("Z", b"1,1ac,2")
        self.handler.dispatch("Z", b"1,1ae,2")
        self.mon._cache = False
        opc1 = self.mem.flash_read_word(0x1ac)
        self.logger.debug("Opcode before 'continue' opc1=0x%X", opc1)
        self.send_string = ""
        self.handler.dispatch("vCont", b";c")
        time.sleep(0.1)
        self.handler.poll_events()
        send1 = self.send_string
        self.dbg.stop() # in order to stop a runaway!
        self.logger.debug("Result of 'continue' send1=%s", send1)
        opc2 = self.mem.flash_read_word(0x1ac)
        self.logger.debug("Opcode after 'continue' opc2=0x%X", opc2)
        self.handler.dispatch("z", b"1,1ac,2")
        self.handler.dispatch("z", b"1,1ae,2")
        opc3 = self.mem.flash_read_word(0x1ac)
        self.logger.debug("Opcode after 'delete BP'  opc3=0x%X", opc3)
        self.handler.dispatch("Z", b"1,1ae,2")
        opc4 = self.mem.flash_read_word(0x1ac)
        self.logger.debug("Opcode before 'step'  opc4=0x%X", opc4)
        self.send_string = ""
        self.handler.dispatch("vCont", b";s")
        time.sleep(0.1)
        self.handler.poll_events()
        send2 = self.send_string
        self.logger.debug("Result of 'step' send2=%s", send2)
        opc5 = self.mem.flash_read_word(0x1ac)
        self.logger.debug("Opcode after 'step' opc5=0x%X", opc5)
        self.handler.dispatch("z", b"1,1ae,2")
        self.handler.dispatch("Z", b"1,1ac,2")
        self.handler.dispatch("vCont", b";s")
        time.sleep(0.1)
        self.handler.poll_events()
        send3 = self.send_string
        self.logger.debug("Result of 'step' send3=%s", send3)
        opc6 = self.mem.flash_read_word(0x1ac)
        self.logger.debug("Opcode after 'insert BP' & step: opc6=0x%X", opc6)
        self.check_result(self.dbg.program_counter_read() == (0x1b0 >> 1) and
                              send1 == "T0520:87;21:3400;22:ac010000;thread:1;" and
                              send2 == "T0520:87;21:3400;22:ae010000;thread:1;" and
                              send3 == "T0520:87;21:3400;22:b0010000;thread:1;" and
                              opc1 == 0x0000 and opc2 == 0x9598 and
                              opc3 == 0x9598 and opc4 == 0x9598 and opc5 == 0x0000 and
                              opc6 == 0x9598)
        self.mon._cache = True
        self.mon._old_exec = False
        self.mon._onlyswbps = False
        self.dbg.device.avr.protocol.software_breakpoint_clear_all()

    def _live_test_vcont_step_hwbp_unprotected(self):
        """
        If the breakpoint at the current position is a hardware breakpoint,
        we do not protect it! It will be deleted and (perhaps) later re-asserted
        """
        self.logger.info("Running 'vcont step' test with unprotected HWBP...")
        self.dbg.program_counter_write(0x1c4 >> 1)
        self.dbg.stack_pointer_write(bytearray([0x34, 0x00]))
        self.dbg.status_register_write(bytearray([0x87]))
        self.handler.dispatch("Z", b"1,1b2,2")
        self.handler.dispatch("vCont", b";c")
        time.sleep(0.1)
        self.handler.poll_events()
        self.logger.debug("HWBP after stopping: %s", self.bp._hw[1])
        self.logger.debug("Breakpoint at 0x1b2 after stopping: %s", self.bp._bp.get(0x1b2,None))
        hw1 = self.bp._hw[1]
        self.handler.dispatch("z", b"1,1b2,2")
        self.handler.dispatch("vCont", b";s")
        time.sleep(0.1)
        self.handler.poll_events()
        self.logger.debug("HWBP after single-step: %s", self.bp._hw[1])
        self.logger.debug("Breakpoint at 0x1b2 after step: %s", self.bp._bp.get(0x1b2,None))
        hw2 = self.bp._hw[1]
        self.check_result(hw1 == 0x1b2 and hw2 is None)

    def _live_test_v_flash_erase_clean_bps(self):
        """
        Receives vFalshErase package and checks that all breakpoints are cleared
        """
        self.logger.info("Running test for cleaning BPs after vEraseFlash ...")
        if self.flash_transparent:
            self.logger.info("Cannot be run on JTAG megaAVRs")
            self.check_result(True)
            return
        self.bp.cleanup_breakpoints()
        self.mon._cache = False
        self.mon._onlyswbps = True
        self.handler.dispatch("Z", b"1,1b2,2")
        opc1 = self.mem.flash_read_word(0x1b2)
        self.dbg.program_counter_write(0x1c4 >> 1)
        self.logger.debug("OPC after setting BP: 0x%X", opc1)
        self.handler.dispatch("vCont", b";c")
        time.sleep(0.1)
        self.handler.poll_events()
        self.dbg.stop() # in order to stop a runaway!
        self.handler.dispatch("z", b"1,1b2,2")
        opc2 = self.mem.flash_read_word(0x1b2)
        self.logger.debug("OPC after deleting BP: 0x%X", opc2)
        self.handler.dispatch("vFlashErase", b"")
        opc3 = self.mem.flash_read_word(0x1b2)
        self.logger.debug("OPC after vFlashErase: 0x%X", opc3)
        self.logger.debug("Debug table: %s", self.bp._bp)
        self.mon._cache = True
        self.mon._onlyswbps = False
        self.check_result(opc1 == 0xE429 and opc2 == 0x9598 and opc3 == 0xE429 and
                              self.bp._bp == {})

    def _live_test_load_clean_bps(self):
        """
        Loads test code with X-package and checks that all breakpoints are cleared
        """
        self.logger.info("Running test for cleaning BPs before load ...")
        if self.flash_transparent:
            self.logger.info("Cannot be run on JTAG megaAVRs")
            self.check_result(True)
            return
        self.mon._cache = False
        self.mon._onlyswbps = True
        self.mon._noload = True
        self.handler.dispatch("Z", b"1,1b2,2")
        opc1 = self.mem.flash_read_word(0x1b2)
        self.dbg.program_counter_write(0x1c4 >> 1)
        self.logger.debug("OPC after setting BP: 0x%X", opc1)
        self.handler.dispatch("vCont", b";c")
        time.sleep(0.1)
        self.handler.poll_events()
        self.dbg.stop() # in order to stop a runaway!
        self.handler.dispatch("z", b"1,1b2,2")
        opc2 = self.mem.flash_read_word(0x1b2)
        self.logger.debug("OPC after deleting BP: 0x%X", opc2)
        self.mon._verify = False # because on mEDBG debuggers, first page is not always writeable
        test_code = self.handler.escape(self.test_code)
        header = "0001AA,%0X:" % len(test_code)
        self.handler.dispatch("X", header.encode("ascii") + test_code)
        self.handler.dispatch(None, None) # simulate timeout to flash the last pending record
        opc3 = self.mem.flash_read_word(0x1b2)
        self.logger.debug("OPC after load: 0x%X", opc3)
        self.logger.debug("Debug table: %s", self.bp._bp)
        self.mon._verify = True
        self.mon._cache = True
        self.mon._onlyswbps = False
        self.check_result(opc1 == 0xE429 and opc2 == 0x9598 and opc3 == 0xE429 and
                              self.bp._bp == {})
