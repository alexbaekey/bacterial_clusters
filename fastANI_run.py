import subprocess
import os
import pandas as pd

gtdb_df = pd.read_csv('data/GTDB_typestrains_meta_filtered.csv')
bacdive_df = pd.read_csv('data/bacdive_typestrains_filtered.csv') # warning about mixing types in columns (list/str)
bacdive_df.rename(columns={'Species': 'species'}, inplace=True)
merged_df = pd.merge(gtdb_df, bacdive_df, on='species', how='inner')
gtdb_paths_df = pd.read_csv('~/datasets/BIOINFO_DATA/GTDB/release220/220.0/genomic_files_reps/gtdb_genomes_reps_r220/genome_paths.tsv', sep=r'\s+', names=['gtdb_id','genome_path']) # genome fastas
prefix = '/home/ab/datasets/BIOINFO_DATA/GTDB/release220/220.0/genomic_files_reps/gtdb_genomes_reps_r220/'
gtdb_paths_df['genome_path'] = prefix + gtdb_paths_df['genome_path'] + gtdb_paths_df['gtdb_id']
gtdb_paths_df['gtdb_id'] = gtdb_paths_df['gtdb_id'].str[:15]
final_df = pd.merge(merged_df, gtdb_paths_df, on='gtdb_id', how='inner')


# Paths to genome files (can be .fna or .fa files)
#query_genomes = [
#    "genomes/query1.fna",
#    "genomes/query2.fna",
#]
#reference_genomes = [
#    "genomes/ref1.fna",
#    "genomes/ref2.fna",
#]

query_genomes = list(final_df['genome_path'][0:300])
reference_genomes = list(final_df['genome_path'][0:300])

# Write genome paths to text files (required by FastANI for batch mode)
with open("query_list.txt", "w") as f:
    for genome in query_genomes:
        f.write(genome + "\n")

with open("ref_list.txt", "w") as f:
    for genome in reference_genomes:
        f.write(genome + "\n")

# Output file to store ANI results
output_file = "many_to_many_ani_output.txt"
cmd = [
    "fastANI",
    "--ql", "query_list.txt",
    "--rl", "ref_list.txt",
    "--matrix",
#  --fragLen 1500 \
    "--threads", "8",
    "-o", output_file
]

print("Running FastANI...")
subprocess.run(cmd, check=True)
print(f"Done! Results saved in {output_file}")







