import bacdive

# Replace with your BacDive credentials
USERNAME = <username>
PASSWORD = <password>

# Initialize BacDive Client
client = bacdive.BacdiveClient(USERNAME, PASSWORD)

# Search for all type strains (BacDive allows this using a special query)
client.search(type_strain="yes")  # This filters for type strains only

# Retrieve data for all type strains
type_strains = []
for strain in client.retrieve():
    type_strains.append(strain)

# Print the number of retrieved type strains
print(f"Retrieved {len(type_strains)} type strains.")

# Example: Print general information for each type strain
for strain in type_strains[:5]:  # Display first 5 strains as a sample
    print(strain["General"])

import csv

# Define fields to extract
fields = ["full scientific name", "culture collection no.", "BacDive-ID", "General"]

# Save data to CSV
with open("bacdive_type_strains.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(fields)  # Write header
    
    for strain in client.retrieve(fields):  # Filter only selected fields
        writer.writerow([strain.get(field, "N/A") for field in fields])

print("Type strain data saved to bacdive_type_strains.csv")

# Retrieve only taxonomy and culture collection info
#for strain in client.retrieve(["full scientific name", "taxonomy", "culture collection no."]):
#    print(strain)


