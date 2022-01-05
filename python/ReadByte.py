# =======================================================================
#                                                                        
#  ReadByte.py                                           date: 2022/01/05
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
 
import sys
import struct

from LzConstants import *

# --------------------------------------------------------
# ReadByte
#
# This class reads raw bytes from an input stream. A
# single byte is read, but is a string. struct's unpack is 
# used # to convert to a number, but returns a single 
# element tuple. The element is extracted and returned.
# --------------------------------------------------------

class ReadByte (LzConstants):

    def read_byte(self, ifp = sys.stdin):
        # Attempt to read a byte of data (returned as a string)
        if ifp != sys.stdin:
            ip     = ifp.read(1)
        else:
            ip     = sys.stdin.buffer.read(1)

        # If the string is not empty, convert to number (returned in a tuple)
        # and return the actual number (first tuple element).
        if ip:
            ipup   = struct.unpack('B', ip)
            return ipup[0]
        # If reading from the input stream returned an empty string, there
        # is no more data, so flag this to the calling routine.
        else:
            return self.INPUTEOF
