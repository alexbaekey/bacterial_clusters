#TODO write full docstrings

# Filter, can test, like in ipython, with the following
# ast.literal_eval(df['General'][1]) 
# parses string entries in dataframe and automatically organizes into dict
# Then check for columns of interest and add to extract function

#TODO Some entries are lists, which ast cannot deal with directly


import pandas as pd
import ast
from collections import defaultdict

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



def safe_parse(entry):
    """Safely parse a string to dict using ast.literal_eval."""
    try:
        if isinstance(entry, str):
            return ast.literal_eval(entry)
        return entry
    except Exception as e:
        print(f"Parse error: {entry}\nError: {e}")
        return {}

def extract_species(taxonomy_info):
    info = safe_parse(taxonomy_info)
    if info:
        return info.get("species")
    else:
        return None

def extract_description(general_info):
    info = safe_parse(general_info)
    if info:
        return info.get("description")
    else:
        return None

def extract_gram_morphology(morphology_info):
    info = safe_parse(morphology_info)
    cell_info = info.get("cell morphology")
    print(cell_info)
    if cell_info:
        if type(cell_info)==list:
            return [item.get("gram stain") for item in cell_info if isinstance(item, dict)]
        if type(cell_info)==dict:
            return cell_info.get("gram stain")
    else:
        return None

def extract_cell_shape(morphology_info):
    info = safe_parse(morphology_info)
    cell_info = info.get("cell morphology")
    if cell_info:
        if type(cell_info)==list:
            return [item.get("cell_shape") for item in cell_info if isinstance(item, dict)]
        elif type(cell_info)==dict:
            return cell_info.get("cell shape")
    else:
        return None

def extract_motility(morphology_info):
    info = safe_parse(morphology_info)
    cell_info = info.get("cell morphology")
    if cell_info:
        if type(cell_info)==list:
            return [item.get("motility") for item in cell_info if isinstance(item, dict)]
        elif type(cell_info)==dict:
            return cell_info.get("motility")
    else:
        return None

def extract_fields_from_column(column_data, top_level_keys):
    """
        parses a stringified dict and extract multiple keys.

        returns a dataframe
    """
    def extract(entry):
        try:
            parsed = ast.literal_eval(entry) if isinstance(entry, str) else entry
            return {key: parsed.get(key, None) for key in top_level_keys}
        except Exception as e:
            print(f"Failed to parse: {entry}, Error: {e}")
            return {key: None for key in top_level_keys} 
    return column_data.apply(extract)


bacdive_df = pd.DataFrame({
    "species": df["Name and taxonomic classification"].apply(extract_species),
    "description": df["General"].apply(extract_description),
    "gram_stain": df["Morphology"].apply(extract_gram_morphology),
    "cell_shape": df["Morphology"].apply(extract_cell_shape),
    "motility": df["Morphology"].apply(extract_motility),
})





flattened_rows = []

# extract from nested dicts
def extract_kv_pairs(obj, collector):
    if isinstance(obj, dict):
        for k, v in obj.items():
            if isinstance(v, (dict, list)):
                extract_kv_pairs(v, collector)
            else:
                collector[k].append(v)
    elif isinstance(obj, list):
        for item in obj:
            extract_kv_pairs(item, collector)

for entry in df["Physiology and metabolism"]:
    try:
        data = ast.literal_eval(entry) if pd.notna(entry) else {}
        collector = defaultdict(list)
        extract_kv_pairs(data, collector)
        flat = {k: v if len(v) > 1 else v[0] for k, v in collector.items()}
        flattened_rows.append(flat)
    except Exception as e:
        flattened_rows.append({})

physio_df = pd.DataFrame(flattened_rows)
combined_df = pd.concat([bacdive_df.reset_index(drop=True), physio_df.reset_index(drop=True)], axis=1)



print(combined_df.head)
combined_df.to_csv('data/bacdive_typestrains_filtered.csv', index=False)

