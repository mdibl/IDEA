import pandas as pd

def excision():
    deseq_df = pd.read_csv('eDESeq2.csv')

    # select subset of pvalue data using column name
    pvalue_df = deseq_df[['genes', 'pvalue']]
    padj_df = deseq_df[['genes', 'padj']]
    log2fc_df = deseq_df[['genes', 'log2FoldChange']]

    print(pvalue_df)
    print(padj_df)
    print(log2fc_df)