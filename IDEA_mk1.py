import pandas as pd
import numpy as np
import csv
import json
import sys
import urllib.request
import string_call
import data_access
from time import sleep

# read in csv file
# this is somewhat deprecated as data_access includes this feature
df = pd.read_csv(
    '/Users/nmaki/Documents/GitHub/IDEA/DESeq2_genes_wPC_DESeq2out.csv',
    sep=',')
df = df.sort_values(["padj"], ascending=False)
log2FoldChange_sort = df.head()
log2FoldChange_sort.to_csv(
    "/Users/nmaki/Documents/GitHub/IDEA/DESeq2_genes_wPC_DESeq2out_edited.csv",
    index=False)


string_call.request()
data_access.select()
print("This is a divider")
data_access.threshold()