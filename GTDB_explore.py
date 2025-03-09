import pandas as pd
import numpy as np
import tarfile

### key of identifiers to taxonomies
#datapath = '/home/ab/datasets/BIOINFO_DATA/GTDB/release220/220.0/bac120_taxonomy_r220.tsv'
#bac120tax_df = pd.read_csv(datapath, delimiter='\t')
#print(bac120tax_df.head())

### metadata
datapath = '/home/ab/datasets/BIOINFO_DATA/GTDB/release220/220.0/bac120_metadata_r220.tsv.gz'
#bac120meta_df = pd.read_csv(datapath, delimiter='\t', compression='gzip')
#print(list(bac120meta_df.columns))
#print(bac120meta_df.info())
#print(bac120meta_df.shape)

### type strains? "Representative genomes"
datapath = '/home/ab/datasets/BIOINFO_DATA/GTDB/release220/220.0/genomic_files_reps/gtdb_genomes_reps_r220.tar.gz'
with tarfile.open(datapath, 'r:gz') as tar:
    genome_files = tar.getnames()
print(genome_files[:10])
