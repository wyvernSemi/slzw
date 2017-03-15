//=======================================================================
//                                                                       
// LzConsts.java                                         date: 2010/04/01  
//                                                                       
// Author: Simon Southwell                                               
//                                                                       
// Copyright (c) 2010 Simon Southwell                                                                     
//                                                                       
// This file is part of Lzw.
//
// Lzw is free software: you can redistribute it and/or modify
// it under the terms of the GNU General Public License as published by
// the Free Software Foundation, either version 3 of the License, or
// (at your option) any later version.
//
// Lzw is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// GNU General Public License for more details.
//
// You should have received a copy of the GNU General Public License
// along with Lzw. If not, see <http://www.gnu.org/licenses/>.
//
// $Id: LzConsts.java,v 1.1 2010-04-04 10:44:26 simon Exp $
// $Source: /home/simon/CVS/src/java/Lzw/codec/LzConsts.java,v $
//                                                                      
//=======================================================================

package Lzw.codec;

public interface LzConsts {

    //=======================================================================
    // Common constant definitions common throughout the codec classes
    //=======================================================================

    // Note: all these declarations are 'static final' dy definition in an
    // interface

    boolean SUCCESS             = true;
    boolean FAILURE             = false;

    int NEWLINE                 = 0x0A;

    int BYTESIZE                = 8;
    int BYTEMASK                = 0xff;
    int BITSIZE                 = 1;
    int NUMOF8BITBYTES          = 0x100;
    int DEFAULTSTRSIZE          = 20;

    int DEFAULTRECSIZE          = 0;

    boolean EOR                 = true;
    boolean NO_EOR              = false;

    int RESCWNUM                = 8;
    int FIRSTROOTCW             = 0x000;
    int FIRSTCW                 = 0x100;
    int NULLCW                  = 0xFFFF;
    int EOFFLUSH                = NULLCW;

    int MINCWLEN                = 9;
    int MAXCWLEN                = 12;
    int MAXWORDLENGTH           = (1 << MAXCWLEN);

    int DICTFULL                = (1 << MAXCWLEN);
    int NOMATCH                 = DICTFULL;
    int MAXDICTSIZE             = DICTFULL;

    int CODEWORDMASK            = ((1 << MAXCWLEN) - 1);

    int NOERROR                 = 0;
    int USER_ERROR              = 1;
    int DECOMPRESSION_ERROR     = 2;
    int PACKER_ERROR            = 3;
    int UNPACKER_ERROR          = 4;

}
