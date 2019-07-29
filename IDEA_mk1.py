import pandas as pd
import csv
import json
import sys
import urllib.request

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
output_format = "tsv-no-header"
method = "network"

my_genes = ["DPP", "W", "UBX", "N", "BRCA2"]

species = "7227"
my_app = "awesome_app.org"

# construct request

request_url = string_api_url + "/" + output_format + "/" + method + "?"
request_url += "identifiers=%s" % "%0d".join(my_genes)
request_url += "&" + "species=" + species
request_url += "&" + "caller_identity=" + my_app

try:
    response = urllib.request.urlopen(request_url)
except urllib.request.HTTPError as err:
    error_message = err.read()
    print (error_message)
    sys.exit()

# read and parse results

line = response.readline()

while line:
    l = line.strip().split("\t")
    p1, p2 = l[2], l[3]
    experimental_score = float(l[10])
    if experimental_score != 0:
        print ("\t".join([p1,p2, "experimentally confirmed (prob. %.3f)" % experimental_score]))
    
    line = response.readline()