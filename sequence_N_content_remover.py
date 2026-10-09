#!/usr/bin/env python3
# This script is supposed to kick out any sequences in your fasta file that have an N content above N proportion (0-1)

import argparse
import sys
import os

def read_fasta(fasta_file):
    #Read a FASTA file and return a dictionary of sequences.
    sequences = {}
    header_details = {}
    current_id = None
    current_seq = []
    
    with open(fasta_file, 'r') as f:
        for line in f:
            line = line.strip()
            if line.startswith('>'):
                if current_id:
                    sequences[current_id] = ''.join(current_seq) 
                current_id = line[1:].split()[0]  # Get ID without '>'
                header_details[current_id] = ' '.join(line[1:].split()[1:])
                current_seq = []
            else:
                current_seq.append(line)
        
        if current_id:
            sequences[current_id] = ''.join(current_seq)
    #print(sequences)
    return sequences, header_details

def file_input_parser(input_file):
    names_to_remove = []
    with open(input_file) as in_file:
        for line in in_file:
            names_to_remove.append(line.rstrip().rstrip(",").lstrip(">"))
            
    return names_to_remove

def list_parser(input_list):
    names_to_remove = input_list.rstrip("] ").lstrip("[").split(",")

    return names_to_remove


def get_it_out(names_to_remove, sequences, header_details, input_file, output=False):
    if output:
        output_name = output + ".fasta"
    else:
        output_name = input_file.split(".fa")[0] + ".curated.fasta"
    
    counter = 0
    with open(f"{output_name}", "w") as output_file:
        for header in sequences:
            if header in names_to_remove:
                continue
            else:
                output_file.write(f'>{header} {header_details[header]}\n{sequences[header]}\n')
                counter += 1
    print(f"You originally had {len(sequences)}, you wanted to remove {len(names_to_remove)} sequences, you now have {counter} sequences left, good for you.")
    


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="Some sequences have lot of Ns? Get rid of 'em! The output is a flat fasta. Get over it.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s -f reference.fasta -r file_of_names_one_per_line.txt -o output_name
  %(prog)s -f reference.fasta -r name1,name2,name3 -o output_name
        """
    )
    parser.add_argument(
        "-f", "--fasta",
        required=True,
        help="Path to input FASTA file"
    )
    parser.add_argument(
        "-r", "--remove",
        required=True,
        help="File or comma separated list of headers to remove (only needs the bit up to first white space)"
    )
    parser.add_argument(
        "-o", "--output",
        help="Output file name (suffix always .fasta)"
    )
    
    args = parser.parse_args()
    
    sequences, header_details = read_fasta(args.fasta)
    if os.path.exists(args.remove):
        names_to_remove = file_input_parser(args.remove)
    else:
        names_to_remove = list_parser(args.remove)
    get_it_out(names_to_remove, sequences, header_details, args.fasta, args.output)