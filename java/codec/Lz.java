//=======================================================================
//                                                                       
// Lz.java                                               date: 2010/04/01  
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
// $Id: Lz.java,v 1.1 2010-04-04 10:44:26 simon Exp $
// $Source: /home/simon/CVS/src/java/Lzw/codec/Lz.java,v $
//                                                                      
//=======================================================================

package Lzw.codec;
                  
import java.io.*;

public class Lz implements LzConsts {

    //=======================================================================
    // Helper IO methods to hide the try/catch awkwardness
    //=======================================================================

    // Open a file for writing and attached to a buffer
    public BufferedOutputStream file_open_write(String op_filename) {

        try {
            FileOutputStream fos = new FileOutputStream(new File(op_filename));
            return new BufferedOutputStream(fos);
        } catch (IOException e) {
            e.printStackTrace(System.err);
            System.exit(1);
        }

        return null;
    }

    // Open a file for reading and attached to a buffer
    public BufferedInputStream file_open_read(String ip_filename) {

        try {
            FileInputStream fis = new FileInputStream(new File(ip_filename));
            return new BufferedInputStream(fis);
        } catch (IOException e) {
            e.printStackTrace(System.err);
            System.exit(1);
        }

        return null;
    }

    // Get a byte from a buffered input
    public short getc(BufferedInputStream ip) {
        int rbyte;

        try {
            rbyte = ip.read();
            return (short)rbyte;
        } catch (IOException e) {
            e.printStackTrace(System.err);
            System.exit(1);
        }

        return 0;
    }

    // Write a byte to a buffered input
    public void putc(byte val, BufferedOutputStream op) {
        try {
            op.write(val);
        } catch (IOException e) {
            e.printStackTrace(System.err);
            System.exit(1);
        }
    }

    public void flush(BufferedOutputStream op) {
        try {
            op.flush();
        } catch (IOException e) {
            e.printStackTrace(System.err);
            System.exit(1);
        }
    }
}
