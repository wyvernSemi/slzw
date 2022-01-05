# =======================================================================
#                                                                        
#  Compress.py                                           date: 2022/01/05
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
 
# =======================================================================
#  The Compress class implements the LZW compression algorithm. It takes 
#  a stream of bytes from the input, and sends 12 bit codeword to the
#  packer, using the dictionary to store the entries for previously seen
#  strings.
# =======================================================================

from Dictionary  import *
from Packer      import *
from ReadByte    import *


# noinspection PyUnusedLocal
class Compress (LzConstants) :

    # --------------------------------------------------------
    # Contructor
    # --------------------------------------------------------

    def __init__(self, ifp = sys.stdin, ofp = sys.stdout, grph = False, maxstrlen = 0) :
        self.__ip_file             = ifp
        self.__io_obj              = ReadByte()

        # If maxstrlen arg is the default value, set __max_string_length to maximum
        if maxstrlen == 0 :
            self.__max_string_length = self.MAXWORDLENGTH
        # Otherwise use user defined value
        else :
            self.__max_string_length = maxstrlen

    # --------------------------------------------------------
    # compress
    #
    # Public compression function. Performs LZW compression on 
    # input stream, outputing codewords (via the packer) to 
    # the defined output stream.
    # --------------------------------------------------------

    def compress(self, DictObj, PackerObj) :

        # Define and initialise some local variables
        previous_codeword   = self.NULLCW
        match_length_so_far = 0
        op_bytecount        = 0
        code_size           = DictObj.reset_dictionary()

        # Get the first byte from the input stream
        ipbyte              = self.__io_obj.read_byte(self.__ip_file)

        # Process bytes for the whole length of the file.
        while ipbyte != self.INPUTEOF :

            # First byte, so we need to go round the loop once more for
            # another byte, and find the root codeword representation for 
            # this byte.  
            if previous_codeword == self.NULLCW :

                previous_codeword = self.__convert_to_rootcw(ipbyte)

                # We have an implied root codeword match i.e. match length = 1 
                match_length_so_far = 1

            # Otherwise, process the string as normal 
            else :
                __match_addr = DictObj.entry_match(previous_codeword, ipbyte)

                # Match found 
                if __match_addr != self.NOMATCH :

                    # A match increases our string length representation by
                    # one. This is used simply to check that we can fit on
                    # the stack at decompression (shouldn't reach this 
                    # limit).
                    match_length_so_far += 1
                    
                    # Previous matched codeword becomes codeword value of dictionary
                    # entry we've just matched 
                    previous_codeword    = __match_addr

                # Match not found 
                else :
                    # Output the last matched codeword 
                    op_bytecount += PackerObj.pack(previous_codeword, code_size)

                    # Build an entry for the new string (if possible) 
                    code_size = DictObj.build_entry(previous_codeword, ipbyte)

                    # Carry forward the input byte as a 'matched' root codeword 
                    previous_codeword = self.__convert_to_rootcw(ipbyte)

                    # Now we have just a single root codeword match, yet to be processed
                    match_length_so_far = 1

            # Fetch next byte from input stream
            ipbyte = self.__io_obj.read_byte(self.__ip_file)

        # If we've terminated and still have a codeword to output, 
        # then we have to output the codeword which represents all the 
        # matched  string so far (and it could be just a root codeword).
        if previous_codeword != self.NULLCW :
            op_bytecount += PackerObj.pack(previous_codeword, code_size)

            # Pipeline flushed, so no previous codeword 
            previous_codeword = self.NULLCW
            match_length_so_far = 0

        # We let the packer know we've finished and thus to flush its pipeline 
        op_bytecount += PackerObj.pack(self.EOFFLUSH, code_size)

    # --------------------------------------------------------
    # Private assist functions
    # --------------------------------------------------------

    # Convert a byte value to a root codword
    def __convert_to_rootcw(self, byte) :
        return byte + self.FIRSTROOTCW


def main(argv) :
    mydict = Dictionary()
    mypack = Packer()
    mycomp = Compress()
    mycomp.compress(mydict, mypack)


# Only run main if not imported
if __name__ == "__main__" :
    main(sys.argv[1:])
