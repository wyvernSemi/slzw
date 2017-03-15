//=======================================================================
//                                                                       
// Codec.java                                            date: 2010/04/01  
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
// $Id: Codec.java,v 1.2 2010-07-31 06:08:48 simon Exp $
// $Source: /home/simon/CVS/src/java/Lzw/codec/Codec.java,v $
//
//=======================================================================

//=======================================================================
// This class implements the LZW algorithm. It has a dictionary space of 
// 4K---See Dict.java.                       
//=======================================================================

package Lzw.codec;

import java.io.*;
import gnu.getopt.Getopt;

public class Codec extends Lz {

    // References to codec objects
    private Dict     dict;
    private Packer   packer;
    private Comp     comp; 
    private Decomp   decomp; 
    private Unpacker unpacker; 

    // The following variables are initialised to the equivalent of
    // a hardware reset. 
    private boolean compress_mode;
    private int previous_codeword;

    // IO configuration 
    private String ip_filename;
    private String op_filename;
    private BufferedOutputStream ofp;
    private BufferedInputStream  ifp;

    private int config_max_str_len;

    //=======================================================================
    // Constructor
    //
    // Only a default constructor, as all the configuration is done from
    // the user command line options in methods set_user_config()
    //=======================================================================

    public Codec() {
        compress_mode = true;
        previous_codeword = NULLCW;
        config_max_str_len = MAXWORDLENGTH;

        ofp = new BufferedOutputStream(System.out);
        ifp = new BufferedInputStream(System.in);

    }

    //=======================================================================
    // Configure and run the codec                                                         
    //=======================================================================
    public int run (String[] argv) {

        int status = NOERROR;
    
        if ((status = set_user_config(argv)) != NOERROR)
            return status;

        // Create a dictionary (inform whether compressing or decompressing---
        // dictionary is used as CAM in compression, SRAM in decompression)
        dict = new Dict(compress_mode);

        // Select compression/decompression routines as specified 
        if (compress_mode) {

            // Create a packer (arguments configure formatter)
            packer = new Packer(compress_mode, ofp);

            // Create a compression encoder
            comp = new Comp(config_max_str_len, ifp);

            // Connect dictionary and packer, and start compressing from input stream
            comp.compress(dict, packer);

        } else {
            // Create an unpacker (arguments configure formatter)
            unpacker = new Unpacker(compress_mode, ifp);

            // Create a decompression decoder
            decomp = new Decomp(config_max_str_len, ofp);

            // Connect dictionary and unpacker, and start decompressing from input stream
            status = decomp.decompress(dict, unpacker);

        }

        return status;
    }

    //=======================================================================
    // Configure the codec from the command line options                     
    //=======================================================================
    
    private int set_user_config(String[] argv) {
        // Program scratch variables---not part of algorithm 
        int option;
        boolean ip_file_specified = false;
        boolean op_file_specified = false;
        String arg;
    
        // Instantiate the Getopt object and define the common command line 
        // option arguments. 
        Getopt g = new Getopt("Lzw", argv, "i:o:dh");
    
    
        // Process the command line options 
        while ((option = g.getopt()) != -1)
            switch(option) {
            // Decompression mode 
            case 'd':
                compress_mode = false;
                break;
            case 'i':
                ip_filename = g.getOptarg();
                ip_file_specified = true;
                break;
   
            case 'o':
                op_filename = g.getOptarg();
                op_file_specified = true;
                break;
    
            // Unknown option specified 
            case 'h':
            case '?':
                // An unrecognised option was specified 
                System.out.format  ("Usage: Lzw [-h] [-d] [-i <filename>] [-o <filename>]\n" +
                                    "\nOptions:\n" +
                                    "   -h Print help message\n" +
                                    "   -d Perform decompression\n" +
                                    "   -i Specify input file (default stdin)\n" +
                                    "   -o Specify output file (default stdout)\n" +
                                    "\n" +
                                    "All debug information sent to standard error\n");
                return USER_ERROR;
            }// end switch 
    
        // Open files if specified, else defaults to standard IO
        if (ip_file_specified) 
            ifp = file_open_read(ip_filename);
    
        if (op_file_specified) 
            ofp = file_open_write(op_filename);
    
        
        return NOERROR;
    }
    
}
