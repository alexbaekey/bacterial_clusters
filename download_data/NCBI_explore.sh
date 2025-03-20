wget ftp://ftp.ncbi.nlm.nih.gov/genomes/genbank/bacteria/assembly_summary.txt
grep "type strain" assembly_summary.txt > NCBI_type_strains.txt
cat NCBI_type_strains.txt

