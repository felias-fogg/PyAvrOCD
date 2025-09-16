#!/usr/bin/env python3
"""
Read the file given as an argument and return a dict called instrmap that
maps each opcode to a memonic (if legal). The file contains an assembler listing
with all known opcodes for the AVRe+ architecture. There are a few additional ones in
AVRxm, but they are all non-branching and one word instructions.
"""
#pylint: disable=consider-using-with,consider-using-f-string,too-many-boolean-expressions,missing-function-docstring
import sys
import re


def main():
    try:
        in_file = open(sys.argv[1], "r", encoding='utf8')
    except Exception: #pylint: disable=broad-exception-caught
        sys.exit("ERROR. Did you make a mistake in the spelling of the file name?")

    text = in_file.readlines()
    text = text[text.index("__trampolines_start():\n")+1:]
    print("#pylint: skip-file")
    print("instrmap = {")
    for line in text:
        if line.find(".word") >= 0:
            continue
        elems = re.search(".*:\\s*([0-9a-f][0-9a-f]) ([0-9a-f][0-9a-f])[^a-z]*([a-z]*)", line).\
          groups()
        if elems[2] in ['call', 'jmp', 'lds', 'sts']:
            words = 2
        else:
            words = 1
        instr_type = 'nobranch'
        if (elems[2][0:2] == 'st' or elems[2] == 'xch' or elems[2][0:2] == 'la' or \
            elems[2] == 'sei' or elems[2] == 'cli' or elems[2] == 'out'):
            instr_type = 'store'
        if (elems[2][0:3] == 'sbr' or elems[2] == 'sbic' or elems[2] == 'sbis' or \
            elems[2][0:2] == 'br' or elems[2] == 'cpse') and elems[2] != 'break':
            instr_type = 'cond'
        elif elems[2] in ['jmp', 'ijmp', 'eijmp', 'ret', 'icall', 'reti',
                              'eicall', 'call', 'rjmp', 'rcall']:
            instr_type = 'branch'
        if elems[2] in ['brie', 'brid']:
            instr_type = 'icond'
        print("0x{}{} : ('{}', {}, '{}'),".format(elems[1], elems[0], elems[2], words, instr_type))
    print("}")

if __name__ == "__main__":
    main()
