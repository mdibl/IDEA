import pandas as pd
import numpy as np
import csv
import json
import sys
import urllib.request
import interaction_visualization
import interaction_evidence
import data_access
import subprocess
from time import sleep

# read in csv file
# this is deprecated as data_access includes this feature
df = pd.read_csv(
    '/Users/nmaki/Documents/GitHub/IDEA/DESeq2_genes_wPC_DESeq2out.csv',
    sep=',')
df = df.sort_values(["padj"], ascending=False)
log2FoldChange_sort = df.head()
log2FoldChange_sort.to_csv(
    "/Users/nmaki/Documents/GitHub/IDEA/DESeq2_genes_wPC_DESeq2out_edited.csv",
    index=False)

data_access.select()
data_access.threshold()

print("STRING interaction database components below:")

interaction_evidence.request()
interaction_visualization.request()


