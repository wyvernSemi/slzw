//=======================================================================
//                                                                       
// Unpacker.java                                         date: 2010/04/01  
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
// $Id: Unpacker.java,v 1.1 2010-04-04 10:44:26 simon Exp $
// $Source: /home/simon/CVS/src/java/Lzw/codec/Unpacker.java,v $
//                                                                      
//=======================================================================

//=======================================================================
// The unpack class takes the variable sized codewords from the input
// stream and constructs fixed size codewords suitable for the 
// decompress object, returning them via a passed pointer. The current
// length of the input codewords is also passed in, as this is 
// determined by the dictionary.
//=======================================================================

package Lzw.codec;
                  
import java.io.*;

public class Unpacker extends Lz {

    private short ipbyte;
    private int currlen, barrel;
    private int op_codeword;

    private int delay_op_codeword;
    private boolean delay_enable;

    private short codeword_length;

    private BufferedInputStream ip_file;
    
    //=======================================================================
    // Constructors
    //=======================================================================

    public Unpacker() {
        currlen = 0;
        barrel= 0;
        op_codeword = 0;
        ip_file = new BufferedInputStream(System.in);
    }

    public Unpacker(boolean compmode, BufferedInputStream ifp) {
        currlen = 0;
        barrel= 0;
        op_codeword = 0;
        ip_file = ifp;
    }

    //=======================================================================
    // Method name: unpack                                                 
    //                                                                       
    // Description:                                                          
    //    unpack() grabs bytes from input stream, placing then on a barrel
    //    shifter until it has enough bits for a codeword of the current 
    //    codeword length (codeword_length). 
    //=======================================================================

    protected int unpack(IntRef codeword, int codeword_length) {

        int byte_count = 0;

        // Start inputing bytes to form a whole codeword 
        do {
            // Gracefully fail if no more input bytes---codeword is
            // don't care. 
            if ((ipbyte = getc(ip_file)) == -1) 
                return byte_count;

            // We successfully got a byte so increment the byte counter 
            byte_count++;

            // Put the byte on the barrel shifter 
            barrel |= (ipbyte & BYTEMASK) << currlen;

            // We have another byte's worth of bits 
            currlen += BYTESIZE;

        // Continue until we have enough bits for a codeword.
        } while (currlen < codeword_length);

        // Codeword is bottom 'codeword_length' bits: I.e. mask=2^codeword_length - 1 
        op_codeword = (barrel & ((0x1 << codeword_length) - 1));
        currlen -= codeword_length;
        barrel >>= codeword_length;

        // Return the codeword value in the pointer 
        codeword.value = op_codeword;

        // Mark the operation as successful 
        return byte_count;
    }
}
