import ast
from collections import Counter
import pandas as pd

datapath1 = '/home/ab/GitHub/alexbaekey/bacterial_clusters/data/bacdive_type_strains_results_first_half.csv'
datapath2 = '/home/ab/GitHub/alexbaekey/bacterial_clusters/data/bacdive_type_strains_results_second_half.csv'

df1 = pd.read_csv(datapath1)
df2 = pd.read_csv(datapath2)
df = pd.concat([df1,df2], axis=0, ignore_index=True)

# drop unnecessary columns
# keeping the following: 'General', 'Name and taxonomic classification', 'Morphology', 'Physiology and metabolism'
df.drop(columns=\
    ['Reference', \
     'Sequence information', \
     'Genome-based predictions', \
     'Safety information', \
     'Isolation, sampling and environmental information', \
     'Culture and growth conditions', \
     'External links'], \
     inplace=True)




key_counts = Counter()

def traverse(obj):
    if isinstance(obj, dict):
        for k, v in obj.items():
            key_counts[k] += 1
            traverse(v)
    elif isinstance(obj, list):
        for item in obj:
            traverse(item)

for entry in df["Physiology and metabolism"].dropna():
    try:
        data = ast.literal_eval(entry)
        traverse(data)
    except Exception as e:
        continue

for key, count in key_counts.most_common(50):
    print(f"{key}: {count}")

with open("physio_key_counts.txt", "w") as f:
    for key, count in key_counts.most_common():
        f.write(f"{key}: {count}\n")

