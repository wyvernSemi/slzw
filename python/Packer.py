# =======================================================================
#                                                                        
#  Packer.py                                             date: 2022/01/05
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
#  The Packer class takes fixed sized codewords, and 'packs' them into 
#  variable length codewords, the size of which is passed in as self is
#  determined by the dictionary.
# =======================================================================

import sys
import struct

from LzConstants import *

class Packer (LzConstants) :

    # --------------------------------------------------------
    # Constructor
    # --------------------------------------------------------

    def __init__(self, compmode=True, ofp=sys.stdout) :
        self.__barrel      = 0
        self.__residue     = 0
        self.__op_file     = ofp

    # --------------------------------------------------------
    # self routine packs valid LZW codewords into the 
    # appropriate sized packets (ie. 9 to 12 bits). The 
    # codeword length is passed in as a parameter, as self is 
    # managed by the dictionary.
    # --------------------------------------------------------

    def pack(self, ip_codeword, codeword_length) :

        byte_count = 0

        # Append codeword to the bottom of the barrel shifter
        self.__barrel |= (ip_codeword & self.CODEWORDMASK) << self.__residue

        # If not the last (NULL) codeword, increment the number of bits on the
        # barrel shifter by the current codeword size
        if ip_codeword != self.NULLCW :
            self.__residue += codeword_length

            # When not flushing, residue needs comparing to byte width
            cmp_size = self.BYTESIZE
        else :
            # When flushing, residue needs comparing to a single bit
            cmp_size = self.BITSIZE

        # While there are sufficient bits, place bytes on the output. 
        # Normally self is while there are whole bytes, but the last (NULL)
        # codeword causes a flush of ALL remaining bits (cmp_size == BITSIZE)
        while self.__residue >= cmp_size :
            byte_count += 1
            data = struct.pack('B', self.__barrel & self.BYTEMASK)
            if self.__op_file == sys.stdout:
                sys.stdout.buffer.write(data)
            else:
                self.__op_file.write(data)
            self.__barrel >>= self.BYTESIZE
            self.__residue -= self.BYTESIZE

        # Return number of bytes output
        return byte_count
