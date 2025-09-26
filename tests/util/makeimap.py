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
        elems = list(re.search(
         ".*:\\s*([0-9a-f][0-9a-f]) ([0-9a-f][0-9a-f])[^a-z]*([a-z]+)\\s+?([^\\,^\\s]+)?,?\\s*([a-z,A-Z,0-9,+,-]+)?",
            line).groups())
        for ix in range(5):
            if elems[ix] is None:
                elems[ix] = ''
        print("0x{}{} : ('{}', '{}', '{}'),".format(elems[1], elems[0], elems[2], elems[3], elems[4]))
    print("}")

if __name__ == "__main__":
    main()
