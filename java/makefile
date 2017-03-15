#=============================================================
# 
# Copyright (c) 2010 Simon Southwell
# 
# Date: 2nd April 2010
# 
# Makefile for Lzw java code, including codec package
# 
#=============================================================

# N.B. The CLASSPATH environment variable is expected to be
# set to include a path to the directory above this one for
# correct compilation

CODECPKGDIR   = ./codec
CODECPKGTOP   = Codec

CODECPKGFILES = ${CODECPKGDIR}/${CODECPKGTOP}.java 	\
                ${CODECPKGDIR}/Comp.java 		\
		${CODECPKGDIR}/Decomp.java 		\
		${CODECPKGDIR}/Dict.java 		\
                ${CODECPKGDIR}/Packer.java 		\
		${CODECPKGDIR}/Unpacker.java 		\
		${CODECPKGDIR}/Lz.java 			\
		${CODECPKGDIR}/LzConsts.java 		\
	        ${CODECPKGDIR}/DictEntry.java 		\
		${CODECPKGDIR}/IntRef.java 

TOPNAME       = Lzw

all: ${TOPNAME}.class makefile

${TOPNAME}.class: ${TOPNAME}.java ${CODECPKGDIR}/${CODECPKGTOP}.class
	@javac $<

${CODECPKGDIR}/${CODECPKGTOP}.class : ${CODECPKGFILES}
	@cd ${CODECPKGDIR}; javac ${CODECPKGTOP}.java

clean:
	@rm -f *.class ${CODECPKGDIR}/*.class
