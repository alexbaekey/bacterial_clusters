wget ftp://ftp.ncbi.nlm.nih.gov/genomes/genbank/bacteria/assembly_summary.txt
grep "type strain" assembly_summary.txt > type_strains.txt
cat type_strains.txt

