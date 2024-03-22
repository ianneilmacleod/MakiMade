#
# This script copies an input Gcode file to an output. Any lines that end with the pattern will have
# a string appended.  This is intended to add a faster feed rate when the tool is raised, which
# is identified by a "Z" command above the workpiece.
#   Usage example:
#
#      python gcode input_file.nc output_file.nc "Z0.2" "F400"
#
#
import os
import sys
from pathlib import Path

PROCESSED_PREFIX = '_'


def show_usage():
    script = Path(sys.argv[0]).name
    print(f"Usage: python {script} [file or folder] -> file or *.nc files to max speed\
          \n\tProcessed files will have '{PROCESSED_PREFIX}' prefixed to the file name.")


class Gcode:

    def __init__(self, file_name=None, out_file=None, verbose=False):
        file_path = Path(file_name)
        if not file_path.is_file():
            raise FileNotFoundError(file_path)
        self.input = open(file_path, 'r')

        if out_file is None:
            out_file = p.parent / (PROCESSED_PREFIX + p.name)
        self.output = open(out_file, 'w')
        self.verbose = verbose
        if verbose:
            print(f"\nprocessing: {file_name}\n" +
                  f"    output: {out_file}")

        # initialize tracking info
        self.x = self.y = self.z = 0.0
        self.xs = self.ys = self.zs = self.feed = ''
        self.z_up = False
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
                self.z_up = z > self.z
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
                if start:
                    if len(prs) > 1 and prs[1] == 'G0':
                        start = False

                if not start:
                    if self.z_up:
                        self.z_up = False
                        if len(prs) == 3 and prs[1] == "G1" and prs[2][0] == 'Z':
                            # this should be a G0 movement
                            self.fast = True
                            o = f"{prs[0]} G0 {prs[2]}"
                            self.output.write(f"{o}\n")
                            if self.verbose:
                                print(o)
                            continue
                        if len(prs) == 2 and prs[1][0] == 'Z':
                            # this should be a G0 movement
                            self.fast = True
                            o = f"{prs[0]} G0 {prs[1]}"
                            self.output.write(f"{o}\n")
                            if self.verbose:
                                print(o)
                            continue
                    if self.fast:
                        self.fast = False
                        if len(prs) == 3 and prs[1][0] == 'X' and prs[2][0] == 'Y':
                            self.slow = True
                            o = f"{prs[0]} G0 {prs[1]} {prs[2]}"
                            self.output.write(f"{o}\n")
                            if self.verbose:
                                print(o)
                            continue
                    if self.slow:
                        self.slow = False
                        if len(prs) >= 2 and prs[1][0] in "XYZ":
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

    processed = 0
    path = os.getcwd()

    try:

        # make a list of files to process

        if len(sys.argv) >= 2:
            path = sys.argv[1]

        if os.path.isfile(path):
            candidates = [path, ]
        else:
            d = Path(path)
            candidates = [d / f for f in os.listdir(path) if f.endswith('.nc')]

        # create list of files that have not already been processed
        files = []
        for f in candidates:
            p = Path(f)
            n = str(p.name)
            if n[0] != PROCESSED_PREFIX[0]:
                files.append((p, p.parent / (PROCESSED_PREFIX + n)))

        if len(files) == 0:
            print(f"No files found to process in file/path: {path}'\n")
            show_usage()

        for f in files:
            process(f[0], f[1], verbose=True)
            processed += 1

    except IndexError:
        print("No file or folder specified.\n")
        show_usage()

    except OSError:
        print(f"Invalid file or path: {path}")
        show_usage()

    finally:
        if processed:
            print(f"\nSuccessfully processed {processed} files.")
