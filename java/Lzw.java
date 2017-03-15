//=======================================================================
//                                                                       
// Lzw.java                                              date: 2010/04/01 
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
// $Id: Lzw.java,v 1.1 2010-04-04 10:44:08 simon Exp $
// $Source: /home/simon/CVS/src/java/Lzw/Lzw.java,v $
//
//=======================================================================

//=======================================================================
// This is the top level execution class for the LZW Java implementation.
// As the main() method must be a static, it cannot call non-static 
// methods within the same class, so a Codec object is created, and
// its top level method called.
//=======================================================================

import Lzw.codec.*;

public class Lzw {
    public static void main(String[] argv) {
        Codec codec = new Codec();

        codec.run(argv);
    }
}
