//=======================================================================
//                                                                       
// Packer.java                                           date: 2010/04/01  
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
// $Id: Packer.java,v 1.1 2010-04-04 10:44:26 simon Exp $
// $Source: /home/simon/CVS/src/java/Lzw/codec/Packer.java,v $
//                                                                      
//=======================================================================

//=======================================================================
// The Packer class takes fixed sized codewords, and 'packs' them into 
// variable length codewords, the size of which is passed in as this is
// determined by the dictionary.
//=======================================================================

package Lzw.codec;
                  
import java.io.*;

public class Packer extends Lz {

    // Stats & config values
    private int ip_codeword = NULLCW;

    private BufferedOutputStream op_file;

    // Barrel shift register used to formulate the output bytes 
    private long barrel = 0;

    // The residue count of unflushed bits left on the barrel shifter 
    private int residue = 0;

    //=======================================================================
    // Constructors
    //=======================================================================

    public Packer() {
        op_file = new BufferedOutputStream(System.out);
    }

    public Packer(boolean compmode, BufferedOutputStream ofp) {
        op_file = ofp;
    }

    //=======================================================================
    // Method name: pack                                                   
    //                                                                       
    // Description:                                                          
    //    This method packs valid LZW codewords into the appropriate        
    //    sized packets (ie. 9 to 12 bits). The codeword length is passed
    //    in as a parameter, as this is managed by the dictionary.
    //=======================================================================

    protected int pack(int ip_codeword, int codeword_length) {

        int byte_count = 0;

        // Append codeword to the bottom of the barrel shifter
        barrel |= ((ip_codeword & CODEWORDMASK) << residue); 

        // If not the last (NULL) codeword, increment the number of bits on the
        // barrel shifter by the current codeword size
        if (ip_codeword != NULLCW)
            residue += codeword_length;

        // While there are sufficient bits, place bytes on the output. 
        // Normally this is whilst there are whole bytes, but the last (NULL)
        // codeword causes a flush of ALL remaining bits 
        while (residue >= ((ip_codeword != NULLCW) ? BYTESIZE : BITSIZE)) {                        
            putc((byte)(barrel & BYTEMASK), op_file);           
            byte_count++;                                  
            barrel >>= BYTESIZE;                          
            residue -= BYTESIZE;                          
        }

        if (ip_codeword == NULLCW) 
            flush(op_file);

        // Return number of bytes output
        return byte_count;
    }
}
