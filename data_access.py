import pandas as pd

# data selection function
# redundant, remove me
def select():
    deseq_df = pd.read_csv('eDESeq2.csv')

    # select subset of pvalue data using column name
    pvalue_df = deseq_df[['genes', 'pvalue']]
    padj_df = deseq_df[['genes', 'padj']]
    log2fc_df = deseq_df[['genes', 'log2FoldChange']]

    print(pvalue_df)
    print(padj_df)
    print(log2fc_df)

# thresholding function for p-val, padj,l2fc
def threshold():
    df = pd.read_csv('eDESeq2.csv')
    thresh_df = df[['genes', 'pvalue', 'padj', 'log2FoldChange']]
    thresh_val = thresh_df.loc[(thresh_df['pvalue'] < 0.05) & (thresh_df['padj'] < 0.1) & (thresh_df['log2FoldChange'] < 0.5)]
    print(thresh_val)
    print(thresh_val['genes'])