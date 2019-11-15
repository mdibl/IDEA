#TODO: check for open success, if fail die
import yaml
import logging
import argparse
import pandas as pd

# implement max_query_size(500) for now
# avoid overloading string-db

# argparser for input file
parser = argparse.ArgumentParser()
parser.add_argument('filename')
args = parser.parse_args()
with open(args.filename) as file:
    try:
        #print(yaml.safe_load(file))
        # load in DESeq2 file from yaml
        # TODO: load yaml, create df from csv contents
        # must work with argparse
        #df = pd.io.json.json_normalize(yaml.safe_load(file))
        config = yaml.full_load(file)
        #for item, doc in config.items():
            #print (item, ":", doc)
        input_path = config['DESeq_input']['path']
        #print(input_path)
        df = pd.read_csv(input_path)
        print(df)
        baseMean = config['baseMean']
        print(baseMean)
        log2FoldChange = config['log2FoldChange']
        print(log2FoldChange)
        lfcSE = config['lfcSE']
        print(lfcSE)
        pvalue = config['pvalue']
        print(pvalue)
        padj = config['padj']
        print(padj)
        # now use threshold value to cut down CSV
        thresh_df = df[['genes','baseMean','log2FoldChange','lfcSE','pvalue','padj']]
        #thresh_df.set_index('genes')
        print(thresh_df)
    except yaml.YAMLError as exc:
        print(exc)

# open and read based on secondary threshold
# slice based upon names that pass primary threshhold
# split passing and failing into separate tables
# remove duplicates?

