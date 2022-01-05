# =======================================================================
#                                                                        
#  LzConstants.py                                        date: 2022/01/05
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
#  $Source$
#  $Id$
#                                                                       
# =======================================================================
 

# --------------------------------------------------------
# LzConstants
#
# There are no constant values, or macros in Python, so
# this class is used instead to be inherited by all
# the classes that need these common values.
#
# --------------------------------------------------------

class LzConstants :

    FIRSTROOTCW         = 0x000
    FIRSTCW             = 0x100
    NULLCW              = 0xffff
    MINCWLEN            = 9
    MAXCWLEN            = 12
    MAXWORDSIZE         = (1 << MAXCWLEN)
    DICTFULL            = MAXWORDSIZE
    NOMATCH             = MAXWORDSIZE
    EOFFLUSH            = NULLCW
    CODEWORDMASK        = ((1 << MAXCWLEN) - 1)
    BYTESIZE            = 8
    BYTEMASK            = 0xff
    BITSIZE             = 1
    MAXWORDLENGTH       = (1 << MAXCWLEN)
    INPUTEOF            = NULLCW
    NULL                = 0

    NOERROR             = 0
    USERERROR           = 1
    DECOMPRESSION_ERROR = 2
    PACKER_ERROR        = 3
    UNPACKER_ERROR      = 4
