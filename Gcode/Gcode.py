#
# Copy an input Fusion 360 Gcode file (.nc) to an output and replace any tool-up movements
# with rapid machine movements.  The output file(s) will have a '_' prefix.


#   Usage example:
#
#      python gcode.py input_file.nc  // creates _input_file.nc
#      python gcode.py // iterates through all .nc files in the current folder
#      python gcode.py "D://my nc programs" // iterates through all .nc programs in this folder
#
# History:
#   See history at https://github.com/ianneilmacleod/MakiMade/commits/main/Gcode

import os
import sys
from pathlib import Path

PROCESSED_PREFIX = '_'
Z_TOLERANCE = 0.199  # Z up movement tolerance


def show_usage():
    script = Path(sys.argv[0]).name
    print(f"\nUsage: python {script} [file or folder] -> file or path with .ncx files to process.\n\n\
       Files are processed to add maximum tool-up speed for .NCX files created using Fusion360\n\
       CAM under the hobby (free) license.  The Fusion360 PostProcessor needs to be modified to\n\
       save nc files with extension .ncx. Processed files are saved as .nc files.")


class Gcode:

    def __init__(self, file_name=None, out_file=None, verbose=False):
        file_path = Path(file_name)
        if not file_path.is_file():
            raise FileNotFoundError(file_path)
        self.input = open(file_path, 'r')

        if out_file is None:
            out_file = file_path.parent / (PROCESSED_PREFIX + file_path.name)
        self.output = open(out_file, 'w')
        self.verbose = verbose
        if verbose:
            print(f"\nprocessing: \"{file_name}\"\n" +
                  f"    output: \"{out_file}\"")

        # initialize tracking info
        self.x = self.y = 0.0
        self.z = None
        self.xs = self.ys = self.zs = self.feed = ''
        self.z_up = False
        self.z_down = False
        self.fast = False
        self.slow = False

    def _track(self, commands):

        for c in commands:
            if c[0] == 'X':
                self.x = float(c[1:])
                self.xs = c
            elif c[0] == 'Y':
                self.y = float(c[1:])
                self.ys = c
            elif c[0] == 'Z':
                z = float(c[1:])
                if not(self.z is None):
                    self.z_up = (z - self.z) >= Z_TOLERANCE
                    self.z_down = z < self.z
                self.z = z
                self.zs = c
            elif c[0] == 'F':
                self.feed = c

    def filter_speed(self):

        # Filters the input to find tool up movements that should be high speed ('G0').
        # When found, replaces instructions with G0 movements in the output file.

        start = True

        for line in self.input:
            oline = line = line.strip()

            if oline and oline[0] != '(':  # skip comments

                prs = line.split()
                self._track(prs[1:])

                # looking for a 'G0' as the second command to start
                if len(prs) > 1 and prs[1] == 'G0':
                    self.fast = True
                    start = False

                if not start:
                    if self.z_up:
                        self.z_up = False
                        if not('X' in oline or 'Y' in oline):

                            if not self.fast:

                                # this Z up starts a G0 (fast) movement
                                self.fast = True
                                o = f"{prs[0]} G0 {self.zs}"
                                self.output.write(f"{o}\n")
                                if self.verbose:
                                    print(o)
                                continue

                    if self.fast:
                        if self.z_down or 'F' in oline:
                            # Feed rates can only apply for G1, so switch to slow.
                            self.slow = True
                            self.fast = False
                            self.z_down = False

                    if self.slow:
                        self.slow = False
                        if prs[1][0] != 'G':
                            o = f"{prs[0]} G1 {self.xs} {self.ys} {self.zs} {self.feed}"
                            self.output.write(f"{o}\n")
                            if self.verbose:
                                print(o)
                            continue

            self.output.write(f"{oline}\n")


def process(gcode_input, gcode_output, verbose=False):
    gc = Gcode(gcode_input, gcode_output, verbose=verbose)
    gc.filter_speed()


if __name__ == "__main__":

    def outname(f):
        return str(Path(f))[:-1]

    processed = 0
    path = ''
    ncxlist = []

    try:

        # make a list of files to process

        if len(sys.argv) <= 1:
            raise ValueError

        path = Path(sys.argv[1].lower())

        # if there is more than one argument, extract the path only from the first argument
        if len(sys.argv) > 2:
            path = str(Path(path).parent)

        # file
        if os.path.isfile(path):
            if str(path)[-4:] != '.ncx':
                print(f"\n\"{path}\" is not a '.ncx' file.")
                raise ValueError
            ncxlist = [Path(path),]

        # path
        else:
            d = Path(path)
            ncxlist = [d / f.lower() for f in os.listdir(path) if f.lower().endswith('.ncx')]

        if len(ncxlist) == 0:
            print(f"\nNo files found to process in file/path: \"{path}\"\n")
            raise ValueError

        for f in ncxlist:
            process(f, outname(f), verbose=True)
            processed += 1

    except ValueError:
        show_usage()

    except OSError:
        print(f"\nInvalid file or folder: {path}")
        show_usage()

    if processed:
        print(f"\nSuccessfully processed {processed} file(s):")
        for f in ncxlist:
            print(f"\t{f} -> {Path(outname(f)).name}")
