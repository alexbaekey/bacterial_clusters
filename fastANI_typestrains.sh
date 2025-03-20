#!/bin/bash

# double check dirs
if [[ $# -ne 2 ]]; then
    echo "Usage: $0 <GTDB_directory> <output_directory>"
    exit 1
fi

GTDB_DIR=$1
OUTPUT_DIR=$2

mkdir -p "$OUTPUT_DIR"

QUERY_LIST="$OUTPUT_DIR/query_list.txt"
REFERENCE_LIST="$OUTPUT_DIR/reference_list.txt"

# find all FASTA files in the GTDB directory
find "$GTDB_DIR" -type f \( -name "*.fna" -o -name "*.fa" -o -name "*.fasta" \) > "$QUERY_LIST"

# duplicate query list as reference list (modify if needed)
cp "$QUERY_LIST" "$REFERENCE_LIST"

echo "query list saved to: $QUERY_LIST"
echo "reference list saved to: $REFERENCE_LIST"


# usage: 
# chmod +x generate_fastani_lists.sh
# ./generate_fastani_lists.sh /path/to/GTDB /path/to/output
# ./fastANI --ql /path/to/output/query_list.txt --rl /path/to/output/reference_list.txt -o fastani_output.txt

# or, better, to tsv?
# fastANI supports multithreading, and a script to split up your database, but not a lot of instruction

# ./fastANI_typestrains.sh /home/ab/datasets/BIOINFO_DATA/GTDB/release220/220.0/ /home/ab/GitHub/alexbaekey/bacterial_clusters/GTDB_ANI
