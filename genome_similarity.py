import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from itertools import combinations

meta = pd.read_csv("data/final_csv.csv")
meta['genome_path'] = meta['genome_path'].astype(str)
ani_file = "results/many_to_many_ani_output.txt.matrix"

with open(ani_file, 'r') as f:
    lines = [line.strip() for line in f if line.strip()]

n = int(lines[0])
paths = []
ani_data = []

for i, line in enumerate(lines[1:]):
    parts = line.split('\t')
    path = parts[0]
    paths.append(path)
    row = [float(x) if x != 'NA' else np.nan for x in parts[1:]]
    ani_data.append(row)

ani_matrix = np.full((n, n), np.nan)
for i in range(n):
    ani_matrix[i, :i] = ani_data[i]
    ani_matrix[:i, i] = ani_data[i]

ani_df = pd.DataFrame(ani_matrix, index=paths, columns=paths)
print(ani_df)

#ani_df.to_csv('ANI_matrix.csv')

plt.figure(figsize=(10, 8))
plt.pcolormesh(ani_matrix, shading='auto', cmap='viridis')
plt.colorbar(label='ANI (%)')
plt.title("All-vs-All ANI Similarity")
plt.xlabel("Genome Index")
plt.ylabel("Genome Index")
plt.tight_layout()
plt.savefig('results/ani_strain_mat.png')


path_to_family = meta.set_index('genome_path')['family'].to_dict()
#families = sorted(set(path_to_family.get(p) for p in paths if path_to_family.get(p)))

manual_family_order = [
    "Staphylococcaceae", "Streptococcaceae", "Pseudomonadaceae",
    "Enterococcaceae", "Enterobacteriaceae", "Mycobacterium",
    "Neisseriaceae", "Clostridiaceae", "Bacillaceae", "Listeriaceae", "Helicobacteraceae"
]
families = [f for f in manual_family_order if f in path_to_family.values()]


fam_sim = pd.DataFrame(index=families, columns=families, dtype=float)

for fam1, fam2 in combinations(families, 2):
    strains1 = [p for p in paths if path_to_family.get(p) == fam1]
    strains2 = [p for p in paths if path_to_family.get(p) == fam2]
    
    values = [ani_df.loc[p1, p2] for p1 in strains1 for p2 in strains2 if not pd.isna(ani_df.loc[p1, p2])]
    sim = np.mean(values) if values else np.nan
    fam_sim.loc[fam1, fam2] = fam_sim.loc[fam2, fam1] = sim

for fam in families:
    strains = [p for p in paths if path_to_family.get(p) == fam]
    values = [ani_df.loc[p1, p2] for i, p1 in enumerate(strains) for j, p2 in enumerate(strains) if i != j and not pd.isna(ani_df.loc[p1, p2])]
    fam_sim.loc[fam, fam] = np.mean(values) if values else np.nan

print(fam_sim)
#fam_sim.to_csv('testgenfam.csv')

fam_values = fam_sim.astype(float).values
m = len(families)
X, Y = np.meshgrid(np.arange(m + 1), np.arange(m + 1))

plt.figure(figsize=(12, 10))
plt.pcolormesh(X, Y, fam_values, shading='auto', cmap='viridis')
plt.colorbar(label='Avg ANI (%)')
plt.xticks(ticks=np.arange(m) + 0.5, labels=families, rotation=45, ha='right')
plt.yticks(ticks=np.arange(m) + 0.5, labels=families)
plt.title("Average ANI Similarity Between Families")
plt.tight_layout()
plt.savefig('results/ani_fam_mat.png')

