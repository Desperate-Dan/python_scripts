#!/usr/bin/env python3
# This script is supposed to kick out any sequences in your fasta file that have an N content above N proportion (0-1)

import argparse
import sys

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

def n_prop(sequences, prop, inverse=False):
    keepers = []
    #print(sequences)
    for header, seq in sequences.items():
        #print(seq)
        seq = seq.upper()
        seq_len = len(seq[0])
        N_count = seq[0].count("N")
        N_prop = N_count/seq_len
        #print(N_prop)
        prop = float(prop)
        if inverse:
            if N_prop > prop:
                keepers.append(header)
        else: 
            if N_prop < prop:
                keepers.append(header)

    #print(keepers)
    return keepers

def get_it_out(keepers, sequences_to_write, input_file, output=False):
    if output:
        output_name = output + ".fasta"
    else:
        output_name = input_file.split(".fa")[0] + ".clean.fasta"
    print(f"You have kept {len(keepers)} sequences out of {len(sequences_to_write)}, good for you.")
    with open(f"{output_name}", "w") as output_file:
        for header in keepers:
            output_file.write(f'>{header}\n{sequences_to_write[header]}\n')



if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="Some sequences have lot of Ns? Get rid of 'em! The output is a flat fasta. Get over it.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s -f reference.fasta -p 0.1 -o output_name
        """
    )
    parser.add_argument(
        "-f", "--fasta",
        required=True,
        help="Path to input FASTA file"
    )
    parser.add_argument(
        "-p", "--prop",
        required=True,
        help="Proportion of N bases. Higher than this and the sequence is chucked out!"
    )
    parser.add_argument(
        "-o", "--output",
        help="Output file name (suffix always .fasta)"
    )
    parser.add_argument(
        "--inverse",
        action='store_true',
        help="Use this if you want to KEEP the sequences with at least X proportion of N bases. You mad man!"
    )
    
    args = parser.parse_args()
    
    sequences, header_details = read_fasta(args.fasta)
    keepers = n_prop(sequences, args.prop, args.inverse)
    get_it_out(keepers, sequences, args.fasta, args.output)