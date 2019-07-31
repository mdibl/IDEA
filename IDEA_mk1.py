import pandas as pd
import csv
import json
import sys
import urllib.request
from time import sleep

# read in csv file
df = pd.read_csv(
    '/Users/nmaki/Documents/GitHub/IDEA/DESeq2_genes_wPC_DESeq2out.csv',
    sep=',')
df = df.sort_values(["padj"], ascending=False)
log2FoldChange_sort = df.head()
log2FoldChange_sort.to_csv(
    "/Users/nmaki/Documents/GitHub/IDEA/DESeq2_genes_wPC_DESeq2out_edited.csv",
    index=False)

string_api_url = "https://string-db.org/api"
output_format = "image"
method = "network"

my_genes = [["ENSDARG00000000002", "ENSDARG00000000018"],
            ["ENSDARG00000000472", "ENSDARG00000000690"],
            ["ENSDARG00000000853", "ENSDARG00000001057"]]

# use taxonomy ID for species
species = "7955"
my_app = "dev.azure.com/MDIBL"

# create the request
request_url = string_api_url + "/" + output_format + "/" + method + "?"
request_url += "identifiers=%s"
request_url += "&" + "species=" + species
request_url += "&" + "add_white_nodes=30"
request_url += "&" + "caller_identity=" + my_app

# for each gene, call STRING

for gene_pair in my_genes:
    gene1, gene2 = gene_pair
    urllib.request.urlretrieve(request_url % "%0d".join(gene_pair), "%s.png" % "_".join(gene_pair))
    sleep(1)