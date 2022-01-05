#!/usr/local/bin/python
# =======================================================================
#                                                                        
#  Lzw.py                                                date: 2022/01/05
#                                                                        
#  Author: Simon Southwell                                               
# 
#  Copyright (c) 2022 Simon Southwell
#                                                                        
#  This file is part of Lzw.
# 
#  Lzw is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
# 
#  Lzw is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
# 
#  You should have received a copy of the GNU General Public License
#  along with Lzw. If not, see <http://www.gnu.org/licenses/>.
#                                                                       
# =======================================================================

import getopt

from Decompress import *
from Compress   import *

# --------------------------------------------------------

def usage():

    print("Usage: Lzw.py [options] inputFile", file=sys.stderr)
    print("    -h, --help            Print this help message", file=sys.stderr)
    print("    -d, --decompress      Select decompression (default compression)", file=sys.stderr)
    print("    -i, --input   <NAME>  The filename to use for data input (default stdin)", file=sys.stderr)
    print("    -o, --output  <NAME>  The filename to use for data output (default stdout)", file=sys.stderr)
    print("", file=sys.stderr)

# --------------------------------------------------------

# noinspection SpellCheckingInspection
def main(argv):

    outstream       = sys.stdout
    outfile_default = True
    instream        = sys.stdin
    infile_default  = True
    output_file     = sys.stdout
    input_file      = sys.stdin

    compress_mode   = True

    # Parse the command line arguments with getopt
    try:
        # noinspection PyUnusedLocal
        [opts, args] = getopt.getopt(argv, "hi:o:d", ["help", "input=", "output=", "decompress"])
    except getopt.GetoptError as er:
        print("Error:", er)
        usage()
        sys.exit(2)
    
    for opt, arg in opts:
        if opt in ["-h", "--help"]:
            usage()
            sys.exit()
        elif opt in ["-i", "--input"]:
            input_file = arg
            infile_default = False
        elif opt in ["-o", "--output"]:
            output_file = arg
            outfile_default = False
        elif opt in ["-d", "--decompress"]:
            compress_mode = False
    
    # Attempt to create the output file
    if not outfile_default:
        try:
            outstream = open(output_file, 'wb')
        except Exception as ex:
            print("Error:", ex)
            sys.exit(3)
 
    if not infile_default:
        try:
            instream = open(input_file, 'rb')
        except Exception as ex:
            print("Error:", ex)
            sys.exit(3)

    # Create a dictionary
    DictObj = Dictionary(compress_mode)

    if compress_mode:
        PackObj = Packer(compress_mode, outstream)
        CompObj = Compress(instream, outstream)
        CompObj.compress(DictObj, PackObj)
    else:
        UnpackObj = Unpacker(compress_mode, instream, outstream)
        DecompObj = Decompress(outstream)
        status, errmsg = DecompObj.decompress(DictObj, UnpackObj)

        if status != 0:
            print(errmsg, file=sys.stderr)


# Simple main function to get things started
if __name__ == "__main__":
    main(sys.argv[1:])
