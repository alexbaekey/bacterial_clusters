import pandas as pd
import ast

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


#TODO write full docstrings

# Filter, can test, like in ipython, with the following
# ast.literal_eval(df['General'][1]) 
# parses string entries in dataframe and automatically organizes into dict
# Then check for columns of interest and add to extract function

#TODO Some entries are lists, which ast cannot deal with directly

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










# untested
phys_keys = ["oxygen tolerance", "temperature range", "salinity"]
phys_data = extract_fields_from_column(df["Physiology and metabolism"], phys_keys)

bacdive_df = pd.concat([
    bacdive_df,
    phys_data
], axis=1)



#print(bacdive_df.head)
#bacdive_df.to_csv('data/bacdive_typestrains_filtered.csv', index=False)
'''
def extract_info(row):
    try:
        result = {}
        # convert string to dictionary (if needed)
        taxonomy_info = ast.literal_eval(row["Name and taxonomic classification"]) if isinstance(row["Name and taxonomic classification"], str) else row["Name and taxonomic classification"]
        morphology_info = ast.literal_eval(row["Morphology"]) if isinstance(row["Morphology"], str) else row["Morphology"]
        physiology_info = ast.literal_eval(row["Physiology and metabolism"]) if isinstance(row["Physiology and metabolism"], str) else row["Physiology and metabolism"]

        #species
        result["Species"] = taxonomy_info.get("species", None)

        #morphology and gram stain
        cell_morphology = morphology_info.get("cell morphology", {})
        result["Morphology"] = cell_morphology.get("cell shape", None)
        result["Gram Stain"] = cell_morphology.get("gram stain", None)

        #metabolite tests
        metabolite_tests = physiology_info.get("metabolite tests", [])
        for test in metabolite_tests:
            test_name = test.get("metabolite", "Unknown")
            result[f"Metabolite: {test_name}"] = test.get("utilization activity", None)

        #enzyme tests
        enzyme_tests = physiology_info.get("enzymes", [])
        for enzyme in enzyme_tests:
            enzyme_name = enzyme.get("value", "Unknown")
            result[f"Enzyme: {enzyme_name}"] = enzyme.get("activity", None)

        #API tests
        api_tests = physiology_info.get("API zym", {})
        for api_test, result_value in api_tests.items():
            if api_test != "@ref":  # skip reference keys
                result[f"API Test: {api_test}"] = result_value
        return result
    except Exception as e:
        return {"Species": None, "Error": str(e)}


extracted_df = df.apply(extract_info, axis=1).apply(pd.Series)
extracted_df.dropna(how='all', inplace=True)
extracted_df.dropna(axis=1, how='all', inplace=True)
extracted_df.to_csv('data/bacdive_typestrains_extracted.csv', index=False)


#import ace_tools as tools
#tools.display_dataframe_to_user(name="Extracted BacDive Data", dataframe=extracted_df)
# ?
'''
