import pandas as pd

gtdb_df = pd.read_csv('data/GTDB_typestrains_meta_filtered.csv')
bacdive_df = pd.read_csv('data/bacdive_typestrains_filtered.csv') # warning about mixing types in columns (list/str)

#bacdive_df.rename(columns={'Species': 'species'}, inplace=True)

merged_df = pd.merge(gtdb_df, bacdive_df, on='species', how='inner')

gtdb_paths_df = pd.read_csv('~/datasets/BIOINFO_DATA/GTDB/release220/220.0/genomic_files_reps/gtdb_genomes_reps_r220/genome_paths.tsv', sep=r'\s+', names=['gtdb_id','genome_path']) # genome fastas

prefix = '/home/ab/datasets/BIOINFO_DATA/GTDB/release220/220.0/genomic_files_reps/gtdb_genomes_reps_r220/'
gtdb_paths_df['genome_path'] = prefix + gtdb_paths_df['genome_path'] + gtdb_paths_df['gtdb_id']

gtdb_paths_df['gtdb_id'] = gtdb_paths_df['gtdb_id'].str[:15]

final_df = pd.merge(merged_df, gtdb_paths_df, on='gtdb_id', how='inner')

# additional filtering, #TODO replace the list removal as that is good data, just ran out of time to do so
final_df = final_df[final_df['gram_stain'].notna() & (final_df['gram_stain'] != '') \
    & final_df['cell_shape'].notna() & (final_df['cell_shape'] != '') \
    & final_df['motility'].notna() & (final_df['motility'] != '')
]

import ast
def is_clean_scalar(val):
    # Not a list and not a stringified list
    if isinstance(val, list):
        return False
    if isinstance(val, str):
        try:
            parsed = ast.literal_eval(val)
            if isinstance(parsed, list):
                return False
        except:
            pass
    return True

final_df = final_df[
    final_df['gram_stain'].apply(is_clean_scalar) &
    final_df['cell_shape'].apply(is_clean_scalar) &
    final_df['motility'].apply(is_clean_scalar)
]

top_10_families = [
    'Pseudomonadaceae', 'Rhodobacteraceae', 'Lactobacillaceae', 'Vibrionaceae',
    'Nocardiaceae', 'Microbacteriaceae', 'Burkholderiaceae', 'Flavobacteriaceae',
    'Enterobacteriaceae', 'Streptococcaceae'
]



top_5_families = [
    'Pseudomonadaceae', 'Rhodobacteraceae', 'Lactobacillaceae', 'Vibrionaceae',
    'Nocardiaceae']

smaller_2_families = ['Enterobacteriaceae']

patho_selection = ['Pseudomonadaceae', 'Streptococcaceae', 'Enterobacteriaceae', 'Staphylococcaceae', 'Enterococcaceae', 'Bacillaceae', 'Listeriaceae', 'Mycobacteriaceae', 'Clostridiaceae', 'Helicobacteraceae', 'Neisseriaceae']

#final_df = final_df[final_df['family'].isin(top_5_families)]
final_df = final_df[final_df['family'].isin(patho_selection)]

final_df.to_csv('data/final_csv.csv', index=False)

# example in gtdb_paths: GCA_000008885.1_genomic.fna.gz database/GCA/000/008/085/

