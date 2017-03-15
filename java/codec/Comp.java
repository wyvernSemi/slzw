//=======================================================================
//                                                                       
// Comp.java                                             date: 2010/04/01  
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
// $Id: Comp.java,v 1.1 2010-04-04 10:44:26 simon Exp $
// $Source: /home/simon/CVS/src/java/Lzw/codec/Comp.java,v $
//                                                                      
//=======================================================================

//=======================================================================
// The Comp class implements the LZW compression algorithm. It takes a
// stream of bytes from the input, and sends 12 bit codeword to the
// packer, using the dictionary to store the entries for previously seen
// strings.
//=======================================================================

package Lzw.codec;

import java.io.*;

public class Comp extends Lz {

    private int match_length_so_far;
    private int match_addr;
    private short ipbyte;
    private int code_size;

    private int previous_codeword;
    private int ip_bytecount, op_bytecount;
    private int max_string_length;
    private BufferedInputStream ip_file;

    //=======================================================================
    // Constructors
    //=======================================================================

    // Default constructor
    public Comp() {
        match_length_so_far = 0;
        set_max_string_length(MAXWORDLENGTH);
        ip_file = new BufferedInputStream(System.in);
        ip_bytecount = 0;
        op_bytecount = 0;
    }

    // Constructor with configuration parameters
    public Comp(int maxstrlen, BufferedInputStream ifp) {
        match_length_so_far = 0;
        set_max_string_length(maxstrlen);
        ip_file = ifp;
        ip_bytecount = 0;
        op_bytecount = 0;
    }

    //========================================================================
    // Method name: compress                                                
    //                                                                        
    // Description: 
    //    Performs LZW compression on input stream, outputing codewords 
    //    (via the packer) to an output stream.                                                                 
    //========================================================================

    protected void compress(Dict dict, Packer packer) {

        previous_codeword = NULLCW;
        match_length_so_far = 0;
        code_size = dict.reset_dictionary();

        // Process bytes for the while length of the file.
        while ((ipbyte = getc(ip_file)) != -1) {

            //output_graphics_data_point();

            // Increment the byte counter for each input 
            ip_bytecount++;
            //System.err.println("ip_bytecount="+ip_bytecount+ " ipbyte="+ipbyte);

            // First byte, so we need to go round the loop once more for
            // another byte, and find the root codeword representation for 
            // this byte.  
            if (previous_codeword == NULLCW) {

                previous_codeword = convert_to_rootcw(ipbyte);

                // We have an implied root codeword match i.e. match length = 1 
                match_length_so_far = 1;

            // Otherwise, process the string as normal 
            } else {
             
                // Match found 
                if ((match_addr = dict.entry_match(previous_codeword, (byte)ipbyte)) != NOMATCH) {

                    // A match increases our string length representation by
                    // one. This is used simply to check that we can fit on
                    // the stack at decompression (shouldn't reach this 
                    // limit).
                    match_length_so_far++;

                    // Previous matched codeword becomes codeword value of dictionary 
                    // entry we've just matched 
                    previous_codeword = match_addr;

                // Match not found 
                } else { // entry_match(addr) is TRUE 

                    // Output the last matched codeword 
                    op_bytecount += packer.pack(previous_codeword, code_size);

                    // Build an entry for the new string (if possible) 
                    code_size = dict.build_entry(previous_codeword, (byte)ipbyte);
                
                    // Carry forward the input byte as a 'matched' root codeword 
                    previous_codeword = convert_to_rootcw(ipbyte);

                    // Now we have just a single root codeword match, yet to be processed
                    match_length_so_far = 1;

                }

            } // endelse (previous_codeword == NULLCW) 

        } // end while 

        // If we've terminated and still have a codeword to output, 
        // then we have to output the codeword which represents all the 
        // matched  string so far (and it could be just a root codeword).
        if (previous_codeword != NULLCW) {
            op_bytecount += packer.pack(previous_codeword, code_size);

            // Pipeline flushed, so no previous codeword 
            previous_codeword = NULLCW;
            match_length_so_far = 0;
        }

        // We let the packer know we've finished and thus to flush its pipeline 
        op_bytecount += packer.pack(EOFFLUSH, code_size);

    } // end compress() 

    //=======================================================================
    // Internal access functions
    //=======================================================================
    private int get_max_string_length() { 
        return max_string_length; 
    }

    private void set_max_string_length(int val) { 
        max_string_length = val; 
    }

    private int convert_to_rootcw(short byte_val) { 
        return (int)byte_val; 
    }

}
