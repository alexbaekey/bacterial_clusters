import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("data/final_csv.csv")

unique_families = df['family'].nunique()
print(f"Number of unique families: {unique_families}")

print("Top 10 most common families:")
top10_families = df['family'].value_counts().head(10)
print(top10_families)

top_families = df['family'].value_counts().head(20)
plt.figure(figsize=(10, 6))
top_families.plot(kind='bar')
plt.ylabel("Number of Isolates")
plt.xlabel("Family")
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig('results/a.png')

plt.clf()
df['gram_stain_str'] = df['gram_stain'].astype(str) 
gram_counts = df['gram_stain_str'].value_counts().head(10)
plt.figure(figsize=(8, 5))
gram_counts.plot(kind='bar')
plt.title("Distribution of Gram Stains")
plt.ylabel("Number of Isolates")
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig('results/b.png')

plt.clf()
df['motility_str'] = df['motility'].astype(str)
motility_counts = df['motility_str'].value_counts()
plt.figure(figsize=(6, 4))
motility_counts.plot(kind='bar')
plt.title("Motility Distribution")
plt.ylabel("Number of Isolates")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('results/c.png')

plt.clf()
df['cell_shape_str'] = df['cell_shape'].astype(str)
cell_shape_counts = df['cell_shape_str'].value_counts()
plt.figure(figsize=(6, 4))
cell_shape_counts.plot(kind='bar')
plt.title("Cell Shape Distribution")
plt.ylabel("Count")
plt.xticks(rotation=45)
plt.tight_layout()

plt.savefig('results/d.png')
