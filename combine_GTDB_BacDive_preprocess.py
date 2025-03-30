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



# example in gtdb_paths: GCA_000008885.1_genomic.fna.gz database/GCA/000/008/085/
#could maybe just grep the gtdb_id, not sure


