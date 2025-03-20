### Downloading culture-based phenotype data from BacDive of bacteria typestrains

# online, advanced search for type strain == yes (in gui dropdown)
# 21168 hits

# saved metadata into csv:
# advsearch_bacdive_2025-03-09.csv

import bacdive
import pandas as pd
import time
import csv

USERNAME = <username>
PASSWORD = <password>
client = bacdive.BacdiveClient(USERNAME, PASSWORD)

### get species names from csv
df = pd.read_csv("advsearch_bacdive_2025-03-09.csv", skiprows=2)
midpoint = len(df) // 2
first_half = df.iloc[:midpoint]  # First half
second_half = df.iloc[midpoint:]  # Second half

species_list = second_half["species"].dropna().unique()
#print(species_list)

# search and save results into a list
type_strains = []

for species in species_list:
    print(f"Searching for species: {species}")
    try:
        # format query
        parts = species.split()
        if len(parts) < 2:
            print(f"skipping '{species}' (invalid format)")
            continue
        genus, species_epithet = parts[0], " ".join(parts[1:])
        query = {"taxonomy": (genus, species_epithet)}
        #print(query)
        
        results = client.search(**query)
        #results = client.search(taxonomy=species)  # Search by species name

        if results:
            print(f"Found results for {species}. Retrieving data...")
            # retrieve and filter type strains
            for strain in client.retrieve():
                #print(f'strain: {strain}')
                if strain['Name and taxonomic classification']['type strain'] == 'yes':
                    print("CONDITION MET")
                    type_strains.append(strain)
                else:
                    print("CONDITION NOT MET, REVISE CONDITION")
            time.sleep(0.05)
        else:
            print(f"No results found for {species}.")
    
    except Exception as e:
        print(f"Error searching for {species}: {e}")


#query = {"taxonomy": ("Escherichia", "coli")}
#client.search(**query)  # General search for all bacteria

# Display first few results
#for strain in type_strains[:5]:  # Display first 5 as a sample
#    print(strain)

### save as csv
if type_strains:
    df_results = pd.DataFrame(type_strains)
    df_results.to_csv("bacdive_type_strains_results_second_half.csv", index=False)
    print("saved to bacdive_type_strains_results.csv")


