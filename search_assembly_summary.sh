column -t -s $'\t' assembly_summary.txt | less -S
grep "type strain" assembly_summary.txt > type_strains.txt #no header
(head -n 2 assembly_summary.txt && grep "type strain" assembly_summary.txt) > type_strains.txt # with header
wc -l NCBI_type_strains.txt
# 618 rows
