# =======================================================================
#                                                                        
#  Dictionary.py                                         date: 2022/01/05
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
# Dictionary access utilities for LZW algorithm                       
#                                                                        
# The dictionary is implemented as a Python dictionary. In compression
# mode, the key is a tuple of byte and pointer, storing an address. In
# decompression, the key is an address storing a byte pointer tuple
# (a more traditional memory).
#
# =======================================================================

import sys
from LzConstants import *

# =======================================================================
# Main dictionary class

class Dictionary (LzConstants) :

    # Private  members
    __dictionary              = {}
    __next_available_codeword = 0
    __codeword_len            = 0
    __compress_mode           = True

    # Public methods

    # --------------------------------------------------------
    # CONSTRUCTOR
    # --------------------------------------------------------
    def __init__(self, comp_mode=True):

        self.__compress_mode           = comp_mode
        self.__next_available_codeword = self.FIRSTCW
        self.__codeword_len            = self.MINCWLEN

    # --------------------------------------------------------
    # reset_dictionary
    #
    # Resets the dictionary and internal state to empty status
    # --------------------------------------------------------
    def reset_dictionary(self):

        self.__next_available_codeword = self.FIRSTCW
        self.__dictionary              = {}
        return self.MINCWLEN

    # --------------------------------------------------------
    # build_entry                                            
    #                                                                       
    # Creates a new dictionary entry at __next_available_codeword, 
    # so long as the dictionary isn't full, in which case the     
    # build is not performed, and a reset is done instead.            
    # --------------------------------------------------------
    def build_entry(self, codeword, byte):

        # If the dictionary is full, reset it before doing a build
        if self.dictionary_full():
            self.__codeword_len = self.reset_dictionary()

        # Set the entry values for the pointer and bytes 
        self.__set_dictionary_entry(self.__next_available_codeword, codeword, byte)

        # If we've just built an entry whose codeword value is greater than 
        # the current output codeword size, then increment the current codeword 
        # size. The decompression builds lag behind by one, so self event
        # is anticipated by an entry. 
        if self.__codeword_len < self.MAXCWLEN:
            if not self.__compress_mode:
                offset = 1
            else :
                offset = 0

            if self.__next_available_codeword == ((1 << self.__codeword_len) - offset):
                self.__codeword_len += 1
        # No change in codeword size...
        else :
            # If decompressing and we're one short of having a full dictionary,
            # reset the codeword_len. self anticipates a reset next build,
            # in a similar way as for the codeword length increment. 
            if not self.__compress_mode and self.__next_available_codeword == (self.DICTFULL - 1):
                self.__codeword_len = self.MINCWLEN

        # If the dictionary isn't full, increment the __next_available_codeword, pointing
        # to the next free dictionary space.
        if self.__next_available_codeword != self.DICTFULL:
            self.__next_available_codeword += 1

        # Return the current codeword length to inform the caller if it has changed.
        return self.__codeword_len

# --------------------------------------------------------
    # entry_match                                            
    #                                                                       
    # Returns matching address if the pointer and byte 
    # combination is in the dictionary.
    # --------------------------------------------------------
    def entry_match(self, pointer, byte):
        if (byte, pointer) in self.__dictionary:
            return self.__dictionary[(byte, pointer)]
        else :
            return self.NOMATCH

    # --------------------------------------------------------
    # codeword_valid
    #
    # Return TRUE if the codeword is in the dictionary
    # --------------------------------------------------------
    def codeword_valid(self, codeword):
        return codeword <= self.__next_available_codeword

    # --------------------------------------------------------
    # is_next_free_entry
    #
    # Return TRUE if the address is the next free dictionary 
    # entry
    # --------------------------------------------------------
    def is_next_free_entry(self, address):
        return address == self.__next_available_codeword

    # --------------------------------------------------------
    # dictionary_full
    #
    # Return TRUE if the dictionary is full
    # --------------------------------------------------------
    def dictionary_full(self):
        return self.__next_available_codeword == self.DICTFULL

    # --------------------------------------------------------
    # dictionary_entry_byte
    #
    # Return the byte values stored at 'address' in the
    # dictionary
    # --------------------------------------------------------
    def dictionary_entry_byte(self, address):
        lbyte, lptr = self.__dictionary[address]
        return lbyte

    # --------------------------------------------------------
    # dictionary_entry_pointer
    #
    # Return the pointer value stored at 'address' in the
    # dictionary
    # --------------------------------------------------------
    def dictionary_entry_pointer(self, address):
        lbyte, lptr = self.__dictionary[address]
        return lptr

    # --------------------------------------------------------
    # root_codeword
    #
    # Return TRUE if the codeword is a root codeword
    # --------------------------------------------------------
    def root_codeword(self, codeword):
        return codeword < self.FIRSTCW

    # --------------------------------------------------------
    # dump_dict
    #
    # utility meothod to dump the dictionary contents to
    # stderr.
    # --------------------------------------------------------
    def dump_dict(self):
        print(self.__dictionary, file=sys.stderr)

    # Private methods

    # --------------------------------------------------------
    # __set_dictionary_entry
    #
    # When compressing, uses __dictionary as a true dictionary,
    # and stores the address value with a key of a tuple
    # created from the byte and pointer. When decompressing,
    # uses __dictionary as a straight ram, and stores a tuple
    # constructed from the byte and pointer at address.
    #
    # --------------------------------------------------------
    def __set_dictionary_entry(self, address, pointer, byte):
        if self.__compress_mode:
            self.__dictionary[(byte, pointer)] = address
        else :
            self.__dictionary[address] = (byte, pointer)


# Mini test program
def main(argv) :
    mydict = Dictionary()

    mydict.build_entry(0x000, 0x22)
    mydict.build_entry(0x001, 0x33)
    mydict.build_entry(0x100, 0x44)

    print(mydict.entry_match(0x001, 0x33))
    print(mydict.entry_match(0x001, 0x32))
    print(mydict.entry_match(0x100, 0x44))


# Only run main if not imported
if __name__ == "__main__" :
    main(sys.argv[1:])
