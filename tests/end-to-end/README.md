# Test specification

## Test scripts

Test scripts and MCU/board capabilities are specified using YAML syntax.

Test scripts are stored in the file `scripts.yml`.

```
tests:
  <unique testname>:
    virtual: <bool> # if true, it can only be imported but not used as a test
    requires:
      <capability>    # capability the MCU should provide
      <capability>
    import: <testname> # import all entries from this test
    after: <testname> # has to run directly after this test, see below
    sketch: <sketch path>
    serverargs: <line with serverargs>
    compileargs: <compilerargs>
    steps:
      - import: <testname> # import at this point all the steps of the virtual test
      - stimulus: <gdb command> # we only give the stimulus, but do not check
      - stimulus: <gdb command>
        response: <wildcard expression> # This should be the response
      - stimulus: <gdb command>
        responses:        # different expressions possible
          - <wildcard expression>
          - <wildcard expression>
      - stimulus: <gdb command>
        success: <wildcard expressions> # terminate and count it as success
        fail: <wildcard expressions> # terminate and fail
        interrupt: <number> # interrupt after this number of seconds
      - timeout: <number>
```

Instead or in addition to steps, one can specify `upload`, which will call avrdude with the right -c and -p and -P options.

`after` is for a test that builds on the state another one leaves behind, such as `attach`, which attaches to the program `cblink` has loaded and started, or a test that reconnects in extended-remote mode. The other test is then run directly before it, and added to the run if it was not selected. If two tests are to follow the same test, that test runs before each of them. A test that has already run as a predecessor is not run again. If the predecessor fails, the test is not run and counts as failed; if the predecessor is not feasible for the MCU, the test is skipped.

A \<capability> could be

- ram: \<number> # requested number of kbytes
- flash: \<number> # requested number of kbytes flash
- dw: true # debugging interface
- jtag: true
- updi: true
- arduino: true  # only possible with Arduino support
- cadc: true # needs a classic adc
- autopower: true # requires auto power-cycle (on xminis)
- dirty: true # needs dirty PC

------

## Board specifications

Board specifications are also given in YAML syntax in the file devices.yml. A typical entry could look like as follows:

```
devices:
  <device-id>: # board or mcu id, which is used when starting a test
    virtual: <bool> # when true, then one can only import the description
    import: <deviced-id> # import the description
    mcu: <mcu-name>
    fqbn: <fqbn>
    provides:
      <capability>
    clock: [ <clocklist> ] # 1, 1.2, 4, 8, 9.2, 16, 16i, 20
    core: <core-id> # necessary to figure out the clock id and the value (for make)
    setup: <test-setup String>
```

## Clock Specs
```
clocks:
  <Core name>:
    "<number>":
      code: <code for arduino-cli>
      value: < value in Hz>

  <Core name>:
    import: <Core name>