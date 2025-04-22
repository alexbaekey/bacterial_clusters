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

def extract_family(taxonomy_info):
    info = safe_parse(taxonomy_info)
    if info:
        return info.get("family")
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



bacdive_df = pd.DataFrame({
    "species": df["Name and taxonomic classification"].apply(extract_species),
    "family": df["Name and taxonomic classification"].apply(extract_family),
    "description": df["General"].apply(extract_description),
    "gram_stain": df["Morphology"].apply(extract_gram_morphology),
    "cell_shape": df["Morphology"].apply(extract_cell_shape),
    "motility": df["Morphology"].apply(extract_motility),
})


# convert from string to dict if necessary
df['Physiology and metabolism'] = df['Physiology and metabolism'].apply(
    lambda x: ast.literal_eval(x) if isinstance(x, str) else x
)

included_panels = {
    "API zym",
    "API 50CHac",
    "API biotype100",
    "API 20NE",
    "API 20E",
    "API coryne"
}

def extract_selected_api_tests(entry):
    merged_results = defaultdict(list)
    if isinstance(entry, dict):
        for api_key, tests in entry.items():
            if api_key in included_panels and isinstance(tests, dict):
                for test, outcome in tests.items():
                    test_lower = test.lower()
                    if "@ref" in test_lower or \
                    "control" in test_lower or \
                    "value" in test_lower or \
                    "chebi-id" in test_lower:
                        continue  # skip unwanted
                    if outcome not in merged_results[test]:
                        merged_results[test].append(outcome)
    # single-item lists to scalar
    return {k: v[0] if len(v) == 1 else v for k, v in merged_results.items()}

df_api_tests = df['Physiology and metabolism'].apply(extract_selected_api_tests).apply(pd.Series)

rows_with_api = df_api_tests.notna().any(axis=1)
bacdive_df = bacdive_df[rows_with_api].reset_index(drop=True)
df_api_tests = df_api_tests[rows_with_api].reset_index(drop=True)

bacdive_df = pd.concat([bacdive_df, df_api_tests], axis=1)
bacdive_df.to_csv('data/bacdive_typestrains_filtered.csv', index=False)

