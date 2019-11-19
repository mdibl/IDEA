# TODO: check for open success, if fail die
import yaml
import argparse
import pandas as pd
import urllib.request
import sys
from interaction_evidence import request

# TODO: implement max_query_size(500) for now
# avoid overloading string-db

# argparser for input file
parser = argparse.ArgumentParser()
parser.add_argument('filename')
args = parser.parse_args()
with open(args.filename) as file:
    try:
        # print(yaml.safe_load(file))
        # load in DESeq2 file from yaml
        # TODO: load yaml, create df from csv contents
        # must work with argparse
        # df = pd.io.json.json_normalize(yaml.safe_load(file))
        config = yaml.full_load(file)
        # for item, doc in config.items():
        # print (item, ":", doc)
        input_path = config['DESeq_input']['path']
        # print(input_path)
        baseMean = config['baseMean']
        log2FoldChange = config['log2FoldChange']
        lfcSE = config['lfcSE']
        pvalue = config['pvalue']
        padj = config['padj']
        df = pd.read_csv(input_path)
        # print if 0 < than padj for test
        # convert to #, most likely being read as string
        # now use threshold value to cut down CSV
        # only columns defined in config.yaml file
        df_select = df[['genes', 'baseMean', 'log2FoldChange', 'lfcSE', 'pvalue', 'padj']]
        # print(df_select)
        # print(df_select['genes'])
        df_threshold = df_select.loc[#(df_select['baseMean'] < baseMean)
                                           (df_select['log2FoldChange'] < log2FoldChange)
                                         #& (df_select['lfcSE'] < lfcSE)
                                         & (df_select['pvalue'] < pvalue)
                                         & (df_select['padj'] < padj)]
        # df.index = df_select['genes']
        # df.set_index('genes', inplace=True)
        print(df_threshold)
    except yaml.YAMLError as exc:
        print(exc)

# open and read based on secondary threshold
# slice based upon names that pass primary threshhold
# split passing and failing into separate tables
# remove duplicates?
