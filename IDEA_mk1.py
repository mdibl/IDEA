import pandas as pd
import csv
import json

# read in csv file
df = pd.read_csv(
    '/Users/nmaki/Documents/GitHub/IDEA/DESeq2_genes_wPC_DESeq2out.csv',
    sep=',')
df = df.sort_values(["padj"], ascending=False)
log2FoldChange_sort = df.head()
log2FoldChange_sort.to_csv(
    "/Users/nmaki/Documents/GitHub/IDEA/DESeq2_genes_wPC_DESeq2out_edited.csv",
    index=False)
