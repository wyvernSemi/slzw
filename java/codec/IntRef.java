//=======================================================================
//                                                                        
// IntRef.java                                           date: 2010/04/01 
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
// $Id: IntRef.java,v 1.1 2010-04-04 10:44:26 simon Exp $
// $Source: /home/simon/CVS/src/java/Lzw/codec/IntRef.java,v $
//                                                                      
//=======================================================================

//=======================================================================
// Utility class to allow passing by reference of an integer value
//=======================================================================

package Lzw.codec;
                  
public class IntRef {
    public int value;

    public IntRef() {
        value = 0;
    }

    public IntRef (int initial) {
        value = initial;
    }
}
