import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from itertools import combinations

df = pd.read_csv("data/final_csv.csv")

phenotype_cols = df.columns.difference(['species', 'family', 'gtdb_id', 'description', 'genome_path'])
phenotypes = df[phenotype_cols]

def simple_similarity(row1, row2):
    matches = (row1 == row2).sum()
    total = len(row1)
    return matches / total

n = len(phenotypes)
sim_matrix = np.zeros((n, n))

for i in range(n):
    for j in range(n):
        sim_matrix[i, j] = simple_similarity(phenotypes.iloc[i], phenotypes.iloc[j])

print(sim_matrix)

plt.figure(figsize=(10, 8))
X, Y = np.meshgrid(np.arange(n + 1), np.arange(n + 1))
plt.pcolormesh(X, Y, sim_matrix, shading='auto', cmap='viridis')
plt.colorbar(label='Phenotypic Similarity')
plt.title("All-vs-All Strain Similarity")
plt.tight_layout()
plt.savefig('results/pheno_strain_mat.png')
plt.clf()

#df['family'] = df['family'].astype(str)
#families = df['family'].unique()

manual_family_order = [
    "Staphylococcaceae", "Streptococcaceae", "Pseudomonadaceae",
    "Enterococcaceae", "Enterobacteriaceae", "Mycobacterium",
    "Neisseriaceae", "Clostridiaceae", "Bacillaceae", "Listeriaceae", "Helicobacteraceae"
]

families = [f for f in manual_family_order if f in df['family'].values]
family_sim_matrix = pd.DataFrame(index=families, columns=families, dtype=float)

for fam1, fam2 in combinations(families, 2):
    strains1 = phenotypes[df['family'] == fam1]
    strains2 = phenotypes[df['family'] == fam2]
    sims = [simple_similarity(r1, r2) for _, r1 in strains1.iterrows() for _, r2 in strains2.iterrows()]
    avg_sim = np.mean(sims) if sims else np.nan
    family_sim_matrix.loc[fam1, fam2] = avg_sim
    family_sim_matrix.loc[fam2, fam1] = avg_sim

for fam in families:
    strains = phenotypes[df['family'] == fam]
    sims = [simple_similarity(r1, r2) for i, r1 in strains.iterrows() for j, r2 in strains.iterrows() if i != j]
    family_sim_matrix.loc[fam, fam] = np.mean(sims) if sims else np.nan

print(family_sim_matrix)

fam_sim_values = family_sim_matrix.astype(float).values
m = len(families)
X, Y = np.meshgrid(np.arange(m + 1), np.arange(m + 1))

plt.figure(figsize=(12, 10))
plt.pcolormesh(X, Y, fam_sim_values, shading='auto', cmap='viridis')
plt.colorbar(label='Average Similarity')
plt.xticks(ticks=np.arange(m) + 0.5, labels=families, rotation=45, ha='right')
plt.yticks(ticks=np.arange(m) + 0.5, labels=families)
plt.title("Average Phenotype Similarity Between Families")
plt.tight_layout()
plt.savefig('results/pheno_fam_mat.png')



