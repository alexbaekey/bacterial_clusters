# pip install biodive

import bacdive
client = bacdive.BacdiveClient('username', 'password')

# two methods, search and retrieve

    # Search with BacDive IDs, taxon names, etc...
#client.search(id="5621;138170")
    # or
#client.search(taxonomy="Myroides") # Myroides is a genus
client.search(taxonomy="Myroides odoratus") # is a species

# search method will return the number of strains that match the query
# To actually get data, use retrieve()

# retrieval of data for the strains previously searched
for strain in client.retrieve():
    print(strain["General"])

'''
# Filters for retrieve
# add a parameter to retrieve() to filter like in
for strain in client.retrieve(["culture collection no."]):
    print(strain)

# Or can go back to filter search and filter retrieve
client.search(culturecolno="DSM 100861")
# then
for strain in client.retrieve(["family"]):
    print(strain)

# culture info
for strain in client.retrieve(["full scientific name", "culture medium"]):
    print(strain)

# For a number of DSM strains
for i in range(1,21):
    DSM_num="DSM "+str(i)
    print(DSM_num, end="\t")
    result=client.search(culturecolno=DSM_num)
    if result:
        for strain in client.retrieve(["BacDive-ID"]):
            print(list(strain)[0])

'''
