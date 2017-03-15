//=======================================================================
//                                                                       
// Dict.java                                             date: 2010/04/01  
//                                                                       
// Authors: Simon Southwell                                              
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
// $Id: Dict.java,v 1.1 2010-04-04 10:44:26 simon Exp $
// $Source: /home/simon/CVS/src/java/Lzw/codec/Dict.java,v $
//                                                                      
//=======================================================================

//=======================================================================
// Dictionary access class for LZW algorithm                       
//                                                                       
// The dictionary is implemented as a contiguous array of a DICTIONARY   
// structure (dictionary[]) with a 12 bit pointer (for 4K dictionary)    
// space and a 'byte' value. 
//                                                                       
//=======================================================================

package Lzw.codec;

public class Dict extends Lz {

    // Internal data structures
    private int[][]     indirection_table = new int[DICTFULL][256];
    private int         next_available_codeword = FIRSTCW;
    private int         codeword_len = MINCWLEN;
    private boolean     compress_mode;
    private DictEntry[] dictionary = new DictEntry[DICTFULL];


    //=======================================================================
    // Constructors
    //=======================================================================
    public Dict() {
        compress_mode = true;

        for (int idx = 0; idx < DICTFULL; idx++) 
            dictionary[idx] = new DictEntry(); 
    }
    
    public Dict(boolean mode) {
        compress_mode = mode;

        for (int idx = 0; idx < DICTFULL; idx++) 
            dictionary[idx] = new DictEntry(); 
    }
    
    //=======================================================================
    // Method name: reset_dictionary                                       
    //                                                                       
    // Description: 
    //    Resets the dictionary
    //=======================================================================

    public int reset_dictionary() {
        // Reset common state 
        next_available_codeword = FIRSTCW;

        return MINCWLEN;
    }

    //=======================================================================
    // Method name: entry_match                                            
    //                                                                       
    // Description: 
    //    Returns TRUE if the dictionary entry at the specified
    //    address matches the specified byte. Otherwise FALSE.                   
    //=======================================================================

    protected int entry_match(int pointer, byte byte_val) {
        int addr;

        // Get possible dictionary entry value for match. 
        // (This is not part of algorithm, but a method for 
        // speeding up dictionary searches).
        addr = indirection_table[pointer][byte_val];

        // Test to see if we have a match at the address, and is in the
        // valid portion of the dictionary. 
        if (!(addr >= FIRSTCW && addr < next_available_codeword &&
                    (dictionary_entry_byte(addr) == byte_val) &&
                    (dictionary_entry_pointer(addr) == pointer)))
            addr = NOMATCH; // Set addr to indicate no match 
        
        // Return address of match (or no match) 
        return addr;
    }

    //=======================================================================
    // Method name: build_entry                                            
    //                                                                       
    // Description: 
    //    Creates a new dictionary entry at next_free_code, so
    //    long as the dictionary isn't full, in which case the     
    //    build is not performed, and a partial_reset is done      
    //    instead.            
    //=======================================================================

    protected int build_entry(int codeword, byte byte_val) {

        // If the dictionary is full, reset it before doing a build
        if (dictionary_full()) 
            codeword_len = reset_dictionary();

        // Set the entry values for the pointer and bytes 
        set_dictionary_entry_pointer(next_available_codeword, codeword);
        set_dictionary_entry_byte(next_available_codeword, byte_val);

        // Set the pointer table to point into the dictionary. (This is not
        // part of the algorithm, but a mechanism for fast dictionary
        // accesses.)  
        if (compress_mode)
           indirection_table[codeword][byte_val] = next_available_codeword;

        // If we've just built an entry whose codeword value is greater than 
        // the current output codeword size, then increment the current codeword 
        // size. The decompression builds lag behind by one, so this event
        // is anticipated by an entry. 
        if (codeword_len < MAXCWLEN) {
            if (next_available_codeword == (1 << codeword_len) - (!compress_mode ? 1 : 0))
                codeword_len++;

        // If decompressing and we're one short of having a full dictionary,
        // reset the codeword_len. This anticipates a reset next build,
        // in a similar way as for the codeword length increment. 
        } else if (!compress_mode && next_available_codeword == DICTFULL-1)  
            codeword_len = MINCWLEN;

        if (next_available_codeword != DICTFULL)
            ++next_available_codeword;

        return codeword_len;
    }

    //=======================================================================
    // Public test and data hiding methods
    //=======================================================================
    protected boolean codeword_valid (int codeword) { 
        return codeword <= next_available_codeword; 
    }

    protected boolean is_next_free_entry (int address) { 
        return address == next_available_codeword; 
    }

    protected boolean dictionary_full () { 
        return next_available_codeword == DICTFULL; 
    }

    protected byte dictionary_entry_byte (int address) { 
        return dictionary[address].byte_val; 
    }

    protected int dictionary_entry_pointer (int address) { 
        return dictionary[address].pointer; 
    }

    protected boolean root_codeword (int codeword) { 
        return  codeword < FIRSTCW; 
    }

    //=======================================================================
    // Internal update methods
    //=======================================================================
    private void set_dictionary_entry_pointer (int address, int pointer) { 
        dictionary[address].pointer = pointer; 
    }

    private void set_dictionary_entry_byte (int address, byte byte_val) { 
        dictionary[address].byte_val = byte_val; 
    }
}
