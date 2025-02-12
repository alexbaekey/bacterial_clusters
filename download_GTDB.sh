wget -r -np -nH --cut-dirs=3 -R "index.html*" <url>
# -R "index.html" ignore files named index.html*

wget -r -np -nH -R "index.html*" https://data.ace.uq.edu.au/public/gtdb/data/releases/release220/
