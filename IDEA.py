# TODO: check for open success, if fail die
import yaml
import argparse
import pandas as pd
import sys
import urllib.request, urllib.error, urllib.parse
from interaction_evidence import request

# TODO: implement max_query_size(500) for now
# avoid overloading string-db

# argparser for input file
parser = argparse.ArgumentParser()
parser.add_argument('filename')
args = parser.parse_args()
with open(args.filename) as file:
    try:
        # bytes==str
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
                                         & (df_select['lfcSE'] < lfcSE)
                                         & (df_select['pvalue'] < pvalue)
                                         & (df_select['padj'] < padj)]
        # df.index = df_select['genes']
        # df.set_index('genes', inplace=True)
        print(df_threshold)
        # print(df_threshold['genes'])
        # string-api call
        string_api_url = "https://string-db.org/api"
        output_format = "tsv-no-header"
        method = "network"

        my_genes = df_threshold['genes']
        print(my_genes)
        species = "7955"
        my_app = "www.awesome_app.org"
        # build request
        request_url = string_api_url + "/" + output_format + "/" + method + "?"
        request_url += "identifiers=%s" % "%0d".join(my_genes)
        request_url += "&" + "species=" + species
        request_url += "&" + "caller_identity=" + my_app

        try:
            response = urllib.request.urlopen(request_url)
        except urllib.error.HTTPError as err:
            error_message = err.read()
            print(error_message)
            sys.exit()
        
        # read parse results

        line = response.readline()

        while line:
            l = line.strip().split(b"\t".decode('utf-8'))
            p1, p2 = l[2], l[3]
            experimental_score = float(l[10])
            if experimental_score != 0:
                print(b"\t".join([p1,p2, "experimentally confirmed (prob. %.3f)" % experimental_score]).decode('utf-8'))
            
            line = response.readline()
    except yaml.YAMLError as exc:
        print(exc)

# open and read based on secondary threshold
# slice based upon names that pass primary threshhold
# split passing and failing into separate tables
# remove duplicates?
