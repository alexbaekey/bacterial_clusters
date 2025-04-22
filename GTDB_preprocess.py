import pandas as pd
import numpy as np
import tarfile

### key of identifiers to taxonomies
#datapath = '/home/ab/datasets/BIOINFO_DATA/GTDB/release220/220.0/bac120_taxonomy_r220.tsv'
#bac120tax_df = pd.read_csv(datapath, delimiter='\t')
#print(bac120tax_df.head())

### metadata - bacteria
datapath = '/home/ab/datasets/BIOINFO_DATA/GTDB/release220/220.0/bac120_metadata_r220.tsv.gz'
bac120meta_df = pd.read_csv(datapath, delimiter='\t', compression='gzip')
#print(list(bac120meta_df.columns))
#print(bac120meta_df.info())
#print(bac120meta_df.shape)

### metadata - archaea
datapath = '/home/ab/datasets/BIOINFO_DATA/GTDB/release220/220.0/ar53_metadata_r220.tsv.gz'
ar53meta_df = pd.read_csv(datapath, delimiter='\t', compression='gzip')

### explore representative genomes in genome db
#datapath = '/home/ab/datasets/BIOINFO_DATA/GTDB/release220/220.0/genomic_files_reps/gtdb_genomes_reps_r220.tar.gz'
#with tarfile.open(datapath, 'r:gz') as tar:
#    genome_files = tar.getnames()
#print(genome_files[:10])


# combine bacteria and archaea (if needed)
#combined_meta_df = pd.concat([bac120meta_df, ar53meta_df], ignore_index=True)
#combined_meta_df["gtdb_genome_representative"].value_counts()

rep_df = bac120meta_df.loc[bac120meta_df["gtdb_representative"] == "t"]

type_df = rep_df[rep_df['ncbi_type_material_designation'] != ('na' or '')]
type_df['species'] = type_df['ncbi_taxonomy'].str.extract(r's__([\w\s]+)$')[0] # get species name out of taxa, remove 's__' from entry, add to new column
type_df['gtdb_id'] = type_df['accession'].str[3:]


# only keep relevant columns
final_df = type_df[['species','gtdb_id']]
#final_df = final_df[final_df['species'] != '']
final_df = final_df.dropna()

final_df.to_csv('data/GTDB_typestrains_meta_filtered.csv', index=False)
