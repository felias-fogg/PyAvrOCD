#!/usr/bin/env python3
"""
Generates SVD files from the ATDF files in a given directory
Uses atdf2svd as its workhorse
"""

import os
import argparse
import textwrap
import subprocess
import re

def massage_register_captions(s):
    return re.sub('<register(.*?)caption="(.*?)"(.*?)ocd-rw=""(.*?)>',
                      '<register\\1caption="\\2 (not readable by debugger)"\\3ocd-rw=""\\4>', s)

def extend_with_comments(fname):
    with open(fname, "r") as f:
        atdf = f.read()
    with open(os.path.basename(fname) + ".comments", "w") as f:
        f.write(massage_register_captions(atdf))

def massage_base_addresses(svd):
    return re.sub("<baseAddress>0x000(\\w+)</baseAddress>",
                      "<baseAddress>0x008\\1</baseAddress>", svd)

def main():
    """
    Main function for the SVD generate utility
    """
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=textwrap.dedent('''\
    Harvests device data from a device data file (.atdf) for one device.

    The harvested data can be used to populate a device file in deviceinfo.devices
        '''))

    parser.add_argument("filename",
                        help="name (and path) of atdf file or path to folder with atdf files"
                        )

    arguments = parser.parse_args()

    if arguments.filename.endswith('.atdf'):
        extend_with_comments(arguments.filename)
        result = subprocess.run(['/Users/nebel/.cargo/bin/atdf2svd',
                                    '-a', 'add_unsafe_cpu_registers',
                                    '-a', 'remove_fuse_and_lockbit',
                                     os.path.basename(arguments.filename) + ".comments"],
                                    stdout = subprocess.PIPE,
                                    text = True, check=True)
        os.remove(os.path.basename(arguments.filename) + ".comments")
        print(massage_base_addresses(result.stdout))
    else:
        for file in os.listdir(arguments.filename):
            if os.path.splitext(file)[1].lower() != ".atdf":
                print("Skipping %s" %  file)
                continue
            svdfile = os.path.splitext(file)[0].lower() + '.svd'
            print("Generating",svdfile,"...")
            extend_with_comments(arguments.filename + "/" + file)
            result = subprocess.run(['atdf2svd', '-a', 'add_unsafe_cpu_registers',
                                    '-a', 'remove_fuse_and_lockbit',
                                    file + ".comments"
                                    ],
                                       stdout=subprocess.PIPE,
                                       check=True,
                                       text=True)
            with open(svdfile, 'w') as f:
                f.write(massage_base_addresses(result.stdout))
            os.remove(file + ".comments")

if __name__ == "__main__":
    main()
