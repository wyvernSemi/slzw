Lzw
---

Lzw is a Python implementation of the LZW lossless data compression
algorithm, which can compress and decompress abitrary files. 

Installation
------------

The python is ready to use straight from the repository. The program
has been tested with v3.9.1  Python.


Usage
-----

Usage: Lzw.py [options] inputFile
    -h, --help            Print this help message
    -d, --decompress      Select decompression (default compression)
    -i, --input   <NAME>  The filename to use for data input (default stdin)
    -o, --output  <NAME>  The filename to use for data output (default stdout)

Note: If decompressing text files with unix like line endings to stdout,
windows may convert to CRLF. This does not happen using the -o option to
specify an output file.