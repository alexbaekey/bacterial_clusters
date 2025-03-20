import pandas as pd
import ast

datapath1 = '/home/ab/GitHub/alexbaekey/bacterial_clusters/data/bacdive_type_strains_results_first_half.csv'
datapath2 = '/home/ab/GitHub/alexbaekey/bacterial_clusters/data/bacdive_type_strains_results_second_half.csv'

df1 = pd.read_csv(datapath1)
df2 = pd.read_csv(datapath2)

#print(df1.head)
#print(df2.head)

df = pd.concat([df1,df2], axis=0, ignore_index=True)
#print(df.head)

def extract_species(taxonomy_info):
    try:
        #convert string to dictionary
        if isinstance(taxonomy_info, str):
            taxonomy_info = ast.literal_eval(taxonomy_info)
        return taxonomy_info.get("species", None)
    except Exception as e:
        print(f"error parsing: {taxonomy_info}, Error: {e}")
        return None

#bacdive_df = pd.DataFrame({"Species": df["Name and taxonomic classification"].apply(extract_species)})
#print(bacdive_df.head)
#bacdive_df.to_csv('data/bacdive_typestrains_filtered.csv', index=False)

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
