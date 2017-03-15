# SLZW
Simple LZW codec in C, along with a Java version.

A minimalist LZW implementation in C to illustrate the basic lossless compression algorithm. Documentation on the code can be found here:

   http://www.anita-simulators.org.uk/wyvernsemi/compression/comp_pt2.htm

A general article on lossless data compression (which is the 'parent' article to the above), which includes a discussion on LZW, can be found here:

    http://www.anita-simulators.org.uk/wyvernsemi/compression/compress.html
    
The source code is completely self constained, and is compiled as a single step: e.g. 'gcc slzw.c -o slzw'. A Java version is also available in java/, with instructions in that directory for compilation.
