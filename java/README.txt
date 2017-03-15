Lzw
---

Lzw is a JAVA implementation of the LZW lossless data compression algorithm, 
which can compress and decompress abitrary files. The Lzw package uses a public 
Getopt packages which us included in the install under gnu\getopt. If this package 
is already installed, then this directory contents can be removed.

Setup
-----

Once installed, the CLASSPATH environment variable must be updated to include the 
install directory and "java\" sub-directory. E.g., if the package was installed 
in C:\slzw, then CLASSPATH must include
  
	C:\slzw:C:\slzw\java

Alternatively, use the -classpath option of the java program.

Usage
-----

  java Lzw [-h] [-d] [-i <filename>] [-o <filename>]

  Options:
     -h Print help message
     -d Perform decompression
     -i Specify input file (default stdin)
     -o Specify output file (default stdout)

  All debug information sent to standard error

