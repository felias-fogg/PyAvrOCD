"""
Generates SVD files from the ATDF files in a given directory
Uses atdf2svd as its workhorse
"""

import os
import argparse
import textwrap
import subprocess

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
        subprocess.run(['/Users/nebel/.cargo/bin/atdf2svd', '-a', 'add_unsafe_cpu_registers',
                            '-a', 'remove_fuse_and_lockbit',
                            '-o', arguments.filename], check=True)
    else:
        for file in os.listdir(arguments.filename):
            svdfile = os.path.splitext(file)[0].lower() + '.svd'
            print("Generating",svdfile,"...")
            subprocess.run(['atdf2svd', '-a', 'add_unsafe_cpu_registers',
                                '-a', 'remove_fuse_and_lockbit',
                                '-o', arguments.filename + "/" + file, svdfile],
                               stderr=subprocess.STDOUT, check=True)

if __name__ == "__main__":
    main()
