import pandas as pd

'''
Data access function meant to load in DESEQ2 output
Additionally, thresholds.  Currently hardcoded
Will want to pass in values through yaml file for reusability
'''
# data selection function
# redundant, remove me

#def select():
 #   deseq_df = pd.read_csv('eDESeq2.csv')

  # select subset of pvalue data using column name
#    pvalue_df = deseq_df[['genes', 'pvalue']]
 #   padj_df = deseq_df[['genes', 'padj']]
    #log2fc_df = deseq_df[['genes', 'log2FoldChange']]

    #print(pvalue_df)
    #print(padj_df)
    #print(log2fc_df)

# thresholding function for p-val, padj,l2fc
def threshold():
    df = pd.read_csv('/Users/nmaki/Documents/GitHub/IDEA/tests/eDESeq2.csv')
    df_select = df[['genes', 'pvalue', 'padj', 'log2FoldChange']]
    df_threshold = df_select.loc[(df_select['pvalue'] < 0.05) & (df_select['padj'] < 0.1) & (df_select['log2FoldChange'] < 0.5)]
    print(df_threshold)
threshold()