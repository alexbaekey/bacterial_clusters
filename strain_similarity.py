import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from itertools import combinations

meta = pd.read_csv("data/final_csv.csv")
meta['genome_path'] = meta['genome_path'].astype(str)

phenotype_cols = meta.columns.difference(['species', 'family', 'gtdb_id', 'description', 'genome_path'])
phenotypes = meta.set_index('genome_path')[phenotype_cols]
meta = meta.set_index('genome_path')

strain_order = phenotypes.index.tolist()
family_order = meta.loc[strain_order]['family'].dropna().unique().tolist()

# pheno strains
def simple_similarity(row1, row2):
    return (row1 == row2).sum() / len(row1)

n = len(phenotypes)
pheno_sim_matrix = np.zeros((n, n))

for i in range(n):
    for j in range(n):
        pheno_sim_matrix[i, j] = simple_similarity(phenotypes.iloc[i], phenotypes.iloc[j])

# pheno families
#fam_pheno_sim = pd.DataFrame(index=family_order, columns=family_order, dtype=float)

#for fam1, fam2 in combinations(family_order, 2):
#    rows1 = phenotypes[meta['family'] == fam1]
#    rows2 = phenotypes[meta['family'] == fam2]
#    sims = [simple_similarity(r1, r2) for _, r1 in rows1.iterrows() for _, r2 in rows2.iterrows()]
#    avg_sim = np.mean(sims) if sims else np.nan
#    fam_pheno_sim.loc[fam1, fam2] = fam_pheno_sim.loc[fam2, fam1] = avg_sim

#for fam in family_order:
#    rows = phenotypes[meta['family'] == fam]
#    sims = [simple_similarity(r1, r2) for i, r1 in rows.iterrows() for j, r2 in rows.iterrows() if i != j]
#    fam_pheno_sim.loc[fam, fam] = np.mean(sims) if sims else np.nan

# genome strains
ani_file = "results/many_to_many_ani_output.txt.matrix"
with open(ani_file, 'r') as f:
    lines = [line.strip() for line in f if line.strip()]

num_genomes = int(lines[0])
paths = []
ani_data = []

for i, line in enumerate(lines[1:]):
    parts = line.split('\t')
    path = parts[0]
    paths.append(path)
    row = [float(x) if x != 'NA' else np.nan for x in parts[1:]]
    ani_data.append(row)

#lower triangle to full symmetric matrix
ani_matrix = np.full((num_genomes, num_genomes), np.nan)
for i in range(num_genomes):
    ani_matrix[i, :i] = ani_data[i]
    ani_matrix[:i, i] = ani_data[i]

ani_df = pd.DataFrame(ani_matrix, index=paths, columns=paths)

ani_df = ani_df.loc[strain_order, strain_order]
ani_matrix = ani_df.values

# genome family
#path_to_family = meta['family'].to_dict()
#path_to_family = meta.set_index('genome_path')['family'].to_dict()
#fam_ani_sim = pd.DataFrame(index=family_order, columns=family_order, dtype=float)

#for fam1, fam2 in combinations(family_order, 2):
#    strains1 = [p for p in strain_order if path_to_family.get(p) == fam1]
#    strains2 = [p for p in strain_order if path_to_family.get(p) == fam2]
#    values = [ani_df.loc[p1, p2] for p1 in strains1 for p2 in strains2 if not pd.isna(ani_df.loc[p1, p2])]
#    sim = np.mean(values) if values else np.nan
#    fam_ani_sim.loc[fam1, fam2] = fam_ani_sim.loc[fam2, fam1] = sim

#for fam in family_order:
#    strains = [p for p in strain_order if path_to_family.get(p) == fam]
#    values = [ani_df.loc[p1, p2] for i, p1 in enumerate(strains) for j, p2 in enumerate(strains) if i != j and not pd.isna(ani_df.loc[p1, p2])]
#    fam_ani_sim.loc[fam, fam] = np.mean(values) if values else np.nan

def plot_matrix(matrix, title, xticks=None, yticks=None, cmap='viridis', show_ticks=True, name='default.png'):
    size = matrix.shape[0]
    X, Y = np.meshgrid(np.arange(size + 1), np.arange(size + 1))
    plt.figure(figsize=(10, 8))
    plt.pcolormesh(X, Y, matrix, shading='auto', cmap=cmap)
    plt.colorbar(label='Similarity')
    plt.title(title)
    if show_ticks and xticks is not None:
        plt.xticks(np.arange(size) + 0.5, xticks, rotation=45, ha='right')
    else:
        plt.xticks([])
    if show_ticks and yticks is not None:
        plt.yticks(np.arange(size) + 0.5, yticks)
    else:
        plt.yticks([])
    plt.tight_layout()
    plt.savefig(name)

plot_matrix(pheno_sim_matrix, "Phenotypic Similarity (All vs All)", xticks=strain_order, yticks=strain_order, show_ticks=False, name='results/pheno_strain_sim.png')
plot_matrix(ani_matrix, "ANI Similarity (All vs All)", xticks=strain_order, yticks=strain_order, show_ticks=False, name='results/ani_strain_sim.png')

#plot_matrix(fam_pheno_sim.loc[family_order, family_order].values,
#            "Average Phenotypic Similarity Between Families", xticks=family_order, yticks=family_order, name='results/pheno_fam_sim.png')

#plot_matrix(fam_ani_sim.loc[family_order, family_order].values,
#            "Average ANI Similarity Between Families", xticks=family_order, yticks=family_order, name='results/ani_fam_sim.png')

#fam_pheno_sim.to_csv("results/family_phenotype_similarity.csv")
#fam_ani_sim.to_csv("results/family_ani_similarity.csv")
