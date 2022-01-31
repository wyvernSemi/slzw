#include <stdio.h>
#include <stdlib.h>

#ifdef WIN32
extern int getopt(int, char **, char *);
#endif

#define TRUE                (1==1)
#define FALSE               (1==0)
#define BITSIZE             1
#define BYTESIZE            8
#define BYTEMASK            ((1<<BYTESIZE) - 1)
#define MINCWLEN            9
#ifndef MAXCWLEN
#define MAXCWLEN            12
#endif
#define DICTFULL            (1 << MAXCWLEN)
#define CODEWORDMASK        (DICTFULL - 1)
#define MAXDICTSIZE         DICTFULL
#define NOMATCH             DICTFULL
#define NULLCW              DICTFULL
#define FIRSTCW             0x100
#define NOERRROR            0
#define USERERROR           1
#define DECOMPRESSION_ERROR 2

typedef unsigned int   codeword_type;
typedef unsigned char  byte_type;
typedef unsigned char  boolean;

typedef struct
{
    codeword_type pointer;
    byte_type     byte;
} dictionary_entry_type;

static dictionary_entry_type dictionary [DICTFULL];
static codeword_type         indirection_table [DICTFULL][256];
static codeword_type         next_available_codeword = FIRSTCW;

static codeword_type entry_match(codeword_type pointer, byte_type byte)
{
    codeword_type addr;

    addr = indirection_table[pointer][byte];
    if (addr < FIRSTCW || addr >= next_available_codeword)
        return NOMATCH;

    if ((dictionary[addr].byte == byte) && 
        (dictionary[addr].pointer == pointer))
        return addr;
         
    return NOMATCH; 
}

static unsigned int build_entry(codeword_type codeword, byte_type byte, 
                                boolean compress_mode)
{
    static unsigned int codeword_len = MINCWLEN;

    if (next_available_codeword == DICTFULL) {
        next_available_codeword = FIRSTCW;
        codeword_len = MINCWLEN;
        return codeword_len;
    }

    dictionary[next_available_codeword].pointer = codeword;
    dictionary[next_available_codeword].byte = byte;

    if (compress_mode)
        indirection_table[codeword][byte] = next_available_codeword;

    if (codeword_len < MAXCWLEN) {
        if (next_available_codeword == (1U << codeword_len) - (!compress_mode ? 1U : 0U))
            codeword_len++;
    } else if (!compress_mode && next_available_codeword == (DICTFULL-1))
        codeword_len = MINCWLEN;
     
    ++next_available_codeword;

    return codeword_len;
}

static void pack(codeword_type ip_codeword, unsigned int codelen, 
                 boolean flush, FILE *ofp)
{
    static unsigned long barrel = 0;
    static int residue = 0;

    barrel |= ((ip_codeword & CODEWORDMASK) << residue); 
    residue += codelen;

    while (residue >= (flush ? BITSIZE : BYTESIZE)) {
        putc((barrel & BYTEMASK), ofp);           
        barrel >>= BYTESIZE;                          
        residue -= BYTESIZE;                          
    }
}

static void compress(FILE *ifp, FILE *ofp)
{
    codeword_type previous_codeword = NULLCW;
    unsigned int code_size = MINCWLEN;

    codeword_type match_addr;
    int ipbyte;
    
    while ((ipbyte = getc(ifp)) != EOF) 
        if (previous_codeword == NULLCW)
            previous_codeword = ipbyte;
        else 
            if ((match_addr = entry_match(previous_codeword, ipbyte)) == NOMATCH) {
                pack(previous_codeword, code_size, FALSE, ofp);
                code_size = build_entry(previous_codeword, ipbyte, TRUE);
                previous_codeword = ipbyte;
            } else 
                previous_codeword = match_addr;

    pack(previous_codeword, code_size, TRUE, ofp);
}

static int unpack(codeword_type *codeword, unsigned int codelen, FILE *ifp)
{
    static unsigned int residue = 0, barrel = 0;
    short int ipbyte;

    while (residue < codelen) {
        if ((ipbyte = getc(ifp)) == EOF) 
            return EOF;
        barrel  |= (ipbyte & BYTEMASK) << residue;
        residue += BYTESIZE;
    }

    *codeword = (barrel & ((1 << codelen) - 1));
    residue -= codelen;
    barrel >>= codelen;

    return ipbyte;
}

static void decompress(FILE *ifp, FILE *ofp)
{
    static byte_type stack[MAXDICTSIZE];
    static unsigned int stack_pointer = 0;

    codeword_type ip_codeword, prev_codeword = NULLCW;
    unsigned int code_size = MINCWLEN;
    byte_type byte;
    codeword_type pointer;

    while (unpack(&ip_codeword, code_size, ifp) != EOF) {
        if (ip_codeword <= next_available_codeword) {
            pointer = ip_codeword;
            while (pointer != NULLCW) {
                if (pointer >= FIRSTCW) {
                    if (pointer == next_available_codeword && (prev_codeword != NULLCW)) 
                        pointer = prev_codeword;
                    else {
                        byte    = dictionary[pointer].byte;
                        pointer = dictionary[pointer].pointer;
                    }
                } else { 
                    byte    = pointer;
                    pointer = NULLCW;
                }
                stack[stack_pointer++] = byte;
            } 

            while (stack_pointer != 0)
                putc(stack[--stack_pointer], ofp);

            if (prev_codeword != NULLCW)
                code_size = build_entry(prev_codeword, byte, FALSE);
            prev_codeword = ip_codeword;
        } else {  
            fprintf(stderr, "***decompress: Error --- UNKNOWN CODEWORD (0x%03x)\n", ip_codeword);
            exit(DECOMPRESSION_ERROR);
        }
    } 
}

int main (int argc, char *argv[])
{
    FILE *ifp = stdin, *ofp = stdout;
    boolean compress_mode = TRUE;

    int option;
    extern char *optarg;

    while ((option = getopt(argc, argv, "dhi:o:")) != EOF)
        switch (option) {
        case 'd':
            compress_mode = FALSE;
            break;
        case 'i':
            if ((ifp = fopen(optarg, "rb")) == NULL) {
                fprintf(stderr, "***Error: couldn't open file %s for reading."
                                " Exiting.\n", optarg);
                exit(USERERROR);
            }
            break;
        case 'o':
            if ((ofp = fopen(optarg, "wb")) == NULL) {
                fprintf(stderr, "***Error: couldn't open file %s for writing."
                                " Exiting.\n", optarg);
                exit(USERERROR);
            }
            break;
        case 'h':
        case '?':
            fprintf(stderr, "Usage: %s [-h] [-d] -i <filename>"
                            " -o <filename>\n"
                            "\nOptions:\n"
                            "   -h Print help message\n"
                            "   -d Perform decompression\n"
                            "   -i Input filename\n"
                            "   -o Output filename\n"
                            "\n"
                            "All debug information sent to standard error\n",
                            argv[0]);
            exit(USERERROR);
            break;
    }

    if (compress_mode) 
        compress(ifp, ofp);
    else 
        decompress(ifp, ofp);

    return NOERRROR;
}
