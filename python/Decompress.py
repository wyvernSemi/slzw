# =======================================================================
#                                                                        
#  Decompress.py                                         date: 2022/01/05
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
# The Decompress class takes a stream of valid LZW codewords (through  
# calls to the unpacker) and formulates a dictionary as it goes. The  
# output is a byte sequence constructed from following a linked list  
# of entries, starting with the entry for the input codeword, until  
# reaching a root codeword (pointing to NULL). The bytes are pushed  
# onto a stack as the list is followed, and then flushed upon list  
# termination. An exception condition  exists (called the K omega K  
# case, as originally  described by Welch) where a codeword is input  
# that has a yet to be constructed entry in the linked list it points
# to. The code will reconstruct the entry before proceeding down the
# rest of the list.
# =======================================================================

from Stack       import *
from Dictionary  import *
from Unpacker    import *

class Decompress (LzConstants, Stack) :

    # --------------------------------------------------------
    # Private member variables
    # --------------------------------------------------------

    __max_string_length = 0
    __op_file           = sys.stdout
    __errmsg            = ""

    # --------------------------------------------------------
    # CONSTRUCTOR
    # --------------------------------------------------------

    def __init__(self, ofp = sys.stdout, maxstr = 0) :
        if maxstr == 0 :
            self.__max_string_length  = self.MAXWORDLENGTH
        else :
            self.__max_string_length  = maxstr
        self.__op_file                = ofp

        self.reset_stack()

    # --------------------------------------------------------
    # decompress
    #
    # Public decompression function. Performs LZW decompression 
    # of codewords from the input streama via the unpacker, 
    # outputing decompressed data to the output stream.
    # --------------------------------------------------------

    def decompress(self, DictObj, UnpackObj) :
        status    = self.NOERROR
        code_size = self.MINCWLEN

        string_terminator_byte = 0
        previous_codeword      = self.NULLCW

        # Fetch first codeword and the number of bytes read
        [byte_count, ip_codeword] = UnpackObj.unpack(code_size)

        # Keep going until thare are no more codewords 
        while byte_count != 0 :
            # If the codeowrd is valid (root, or in the dictionary), process it
            if DictObj.codeword_valid(ip_codeword) :

                # Traverse down the dictionary's linked list placing bytes onto 
                # the stack. Empty the stack when reached a NULLCW pointer and remember 
                # the last flushed byte.
                [string_terminator_byte, status] = self.__output_linked_list(DictObj,
                                                                             UnpackObj,
                                                                             ip_codeword,
                                                                             string_terminator_byte,
                                                                             previous_codeword)

                # If returned status was no good, flag the error to the calling routine
                if status != self.NOERROR :
                    return [status, self.__errmsg]

                # We must build a dictionary entry using the last codeword fully 
                # processed and the first flushed byte of the present codeword (if we 
                # aren't flushed)
                if previous_codeword != self.NULLCW :
                    code_size = DictObj.build_entry(previous_codeword, string_terminator_byte)

            # Input codeword was bad
            else :
                # Unknown codeword error
                errstr = "***decompress: Error --- UNKNOWN CODEWORD "
                self.__errmsg = "%s (%03x)" % (errstr, ip_codeword)
                return [self.DECOMPRESSION_ERROR, self.__errmsg]

            previous_codeword = ip_codeword

            # Fetch next codeword from unpacker, along with the number of bytes read
            [byte_count, ip_codeword] = UnpackObj.unpack(code_size)

        return [self.NOERROR, ""]

    # --------------------------------------------------------
    # __output_linked_list 
    #
    # Private assist function for decompress().
    # Follows a linked list of dictionary entries and outputs
    # the bytes in reverse order.                  
    # --------------------------------------------------------

    def __output_linked_list(self, DictObj, UnpackObj, ip_codeword, string_terminator_byte, previous_codeword) :
        self.__errflag = False

        pointer        = ip_codeword

        # While not at the end of the list, follow the linked list, placing
        # byte values on a stack 
        while pointer != self.NULLCW :

            # If not a root codeword ... 
            if not DictObj.root_codeword(pointer) :

                # If an entry in the linked list is the next free codeword,
                # then it must need building as a KwK case. 
                if DictObj.is_next_free_entry(pointer) and previous_codeword != self.NULLCW :

                    # The pointer and byte values are as for the KwK build;
                    # i.e. the last codeword that was input and its first
                    # character 
                    byte    = string_terminator_byte
                    pointer = previous_codeword
                else :
                    # Get the byte and pointer values from the dictionary entry. 
                    byte    = DictObj.dictionary_entry_byte(pointer)
                    pointer = DictObj.dictionary_entry_pointer(pointer)
            # We have to generate the entry for root codewords 
            else :
                byte    = pointer
                pointer = self.NULLCW

            # It is an error to have a codeword which overflows the stack 
            if self.stack_size() == self.__max_string_length :
                self.__errmsg = "***decompress: Error --- BAD WORD LENGTH"
                self.__errflag = self.DECOMPRESSION_ERROR
                return [self.NULL, self.__errflag]

            self.push(byte)

        # Now flush the stack to the output stream 
        while not self.stack_empty() :
            data = struct.pack('B', self.pop() & self.BYTEMASK)
            if self.__op_file == sys.stdout:
                sys.stdout.buffer.write(data)
            else:
                self.__op_file.write(data)

        # Return the last flushed byte, for use in building dictionary entries, along
        # with a good error status
        return [byte, self.NOERROR]


# Mini test program
def main(argv) :
    mydict   = Dictionary(False)
    myunpack = Unpacker()
    mydecomp = Decompress()
    mydecomp.decompress(mydict, myunpack)


# Only run main if not imported
if __name__ == "__main__" :
    main(sys.argv[1:])
