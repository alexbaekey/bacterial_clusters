import subprocess
import os
import pandas as pd

final_df = pd.read_csv('final_csv.csv')

#query_genomes = [
#    "genomes/query1.fna",
#    "genomes/query2.fna",
#]
#reference_genomes = [
#    "genomes/ref1.fna",
#    "genomes/ref2.fna",
#]

#query_genomes = list(final_df['genome_path'][0:500])
query_genomes = list(final_df['genome_path'])
#reference_genomes = list(final_df['genome_path'][0:500])
reference_genomes = list(final_df['genome_path'])

with open("query_list.txt", "w") as f:
    for genome in query_genomes:
        f.write(genome + "\n")

with open("ref_list.txt", "w") as f:
    for genome in reference_genomes:
        f.write(genome + "\n")

output_file = "many_to_many_ani_output.txt"
cmd = [
    "fastANI",
    "--ql", "query_list.txt",
    "--rl", "ref_list.txt",
    "--matrix",
#  --fragLen 1500 \
    "--fragLen", "1000",
    "--threads", "8",
    "-o", output_file
]

subprocess.run(cmd, check=True)



