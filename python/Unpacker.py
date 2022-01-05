# =======================================================================
#                                                                        
#  Unpacker.py                                           date: 2022/01/05
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

from ReadByte    import *

class Unpacker (LzConstants) :

    # --------------------------------------------------------
    # CONSTRUCTOR
    # --------------------------------------------------------
    def __init__(self, compmode=True, ifp=sys.stdin, ofp=sys.stdout) :

        self.__currlen           = 0
        self.__barrel            = 0
        self.__ip_file           = ifp
        self.__op_file           = ofp
        self.__io_obj            = ReadByte()

    # --------------------------------------------------------
    # unpack                                                 
    #                                                                       
    # unpack() grabs bytes from input stream, placing then on a barrel
    # shifter until it has enough bits for a codeword of the current 
    # codeword length (codeword_length). 
    # --------------------------------------------------------
    def unpack(self, codeword_length) :

        byte_count = 0

        # Start inputing bytes to form a whole codeword and
        # continue until we have enough bits for a codeword.
        while self.__currlen < codeword_length : 
            ipbyte  = self.__io_obj.read_byte(self.__ip_file)

            # Gracefully fail if no more input bytes---codeword is
            # don't care. 
            if ipbyte == self.INPUTEOF :
                return [byte_count, self.NULLCW]

            # Put the byte on the barrel shifter 
            self.__barrel |= (ipbyte & self.BYTEMASK) << self.__currlen

            # We successfully got a byte so increment the running byte counter
            byte_count     += 1

            # We have another byte's worth of bits on the barrel
            self.__currlen += self.BYTESIZE

        # Codeword is bottom 'codeword_length' bits: I.e. mask=2^codeword_length - 1
        op_codeword      = self.__barrel & ((1 << codeword_length) - 1)
        self.__currlen  -= codeword_length
        self.__barrel  >>= codeword_length

        # Return the current byte count along with the constructed codeword
        return [byte_count, op_codeword]
