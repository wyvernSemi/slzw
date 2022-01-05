# =======================================================================
#                                                                        
#  Stack.py                                              date: 2022/01/05
#                                                                        
#  Author: Simon Southwell                                               
# 
#  Copyright (c) 2011 Simon Southwell                                                                     
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
# =======================================================================
 
import sys

# --------------------------------------------------
# Stack
#
# self is a wrapper class for implementing a stack
# that's compatible with the Lzw decompression
# routines.
# --------------------------------------------------

class Stack :
    def __init__(self) :
        self.__stack_pointer = 0
        self.__stack = []

    def reset_stack(self) :
        self.__stack_pointer = 0
        self.__stack = []

    def stack_size(self) :
        return self.__stack_pointer

    def stack_empty(self) :
        return self.__stack_pointer == 0

    def push(self, byte_value) :
        self.__stack.append(byte_value)
        self.__stack_pointer += 1

    def pop(self) :
        self.__stack_pointer -= 1
        return self.__stack.pop()


# --------------------------------------------------
# Mini test program
# --------------------------------------------------

def main(argv) :
    mystack = Stack()

    mystack.push(19)
    mystack.push(64)

    print(mystack.stack_size())
    print(mystack.stack_empty())

    print(mystack.pop())
    print(mystack.pop())

    print(mystack.stack_size())
    print(mystack.stack_empty())

    print("End")


# Only run main if not imported
if __name__ == "__main__" :
    main(sys.argv[1:])
