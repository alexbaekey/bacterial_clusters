# untested chatgpt rec



import pandas as pd

# Load the FastANI matrix file
df = pd.read_csv("fastani_matrix_output.txt", sep="\t", index_col=0)

# Convert 'NA' to np.nan and all values to float
df.replace("NA", pd.NA, inplace=True)
df = df.astype(float)

# Optional: clean index/column names to show just genome IDs
df.index = df.index.str.extract(r'(GCF_\d+\.\d+)', expand=False)
df.columns = df.columns.str.extract(r'(GCF_\d+\.\d+)', expand=False)

print(df.head())





import seaborn as sns
import matplotlib.pyplot as plt

plt.figure(figsize=(10, 8))
sns.heatmap(df, annot=True, fmt=".2f", cmap="viridis", mask=df.isna(), square=True, cbar_kws={'label': 'ANI (%)'})
plt.title("FastANI Similarity Matrix")
plt.xticks(rotation=90)
plt.yticks(rotation=0)
plt.tight_layout()
plt.show()






# OR





import numpy as np
import matplotlib.pyplot as plt

# Convert DataFrame to NumPy array
ani_array = df.to_numpy()

# Plot
plt.figure(figsize=(10, 8))
im = plt.imshow(ani_array, cmap='viridis')
plt.colorbar(im, label='ANI (%)')

# Axis labels
plt.xticks(ticks=np.arange(len(df.columns)), labels=df.columns, rotation=90)
plt.yticks(ticks=np.arange(len(df.index)), labels=df.index)
plt.title("FastANI Heatmap")
plt.tight_layout()
plt.show()





# OR







sns.clustermap(df, cmap="viridis", figsize=(10, 10), cbar_kws={'label': 'ANI (%)'})
plt.title("Clustered FastANI Heatmap")
plt.show()






