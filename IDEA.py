from __future__ import print_function
# TODO: check for open success, if fail die
import yaml
import argparse
import pandas as pd
import sys
import random
import requests
import urllib.request, urllib.error, urllib.parse

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
        species_id = config['species']
        cs_threshold = config['cs_threshold']
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
        my_genes = df_threshold['genes']
        # df.index = df_select['genes']
        # df.set_index('genes', inplace=True)
        # print(df_threshold)
        # print(df_threshold['genes'])
        # for each protein in a given list, print scores of experimental significance
        def network():
            string_api_url = "https://string-db.org/api"
            output_format = "tsv-no-header"
            method = "network"

            # build request

            request_url = "/".join([string_api_url, output_format, method])

            params = {

                "identifiers" : "%0d".join(my_genes), # your protein
                "species" : species_id, # species NCBI identifier 
                "caller_identity" : "www.awesome_app.org" # your app name
            }
        
            # read and parse results
            response = requests.post(request_url, data=params)

            for line in response.text.strip().split("\n"):
                l = line.strip().split("\t")
                # l = line.strip().split(b"\t".decode('utf-8'))
                #my_str = "\t"
                #my_str_as_bytes = my_str.encode("utf-8")
                # my_decoded_str = my_str_as_bytes.decode("utf-8")
                p0, p1, p2, p3, p4 = l[0], l[1], l[2], l[3], l[4]
                experimental_score = float(l[10])
                if experimental_score != 0:
                    print("\t".join([p0,p1,p2,p3,p4, "experimentally confirmed (prob. %.3f)" % experimental_score]))
                    #s = my_str_as_bytes.join([p0,p1,p2,p3,p4, b"experimentally confirmed (prob. %.3f)" % experimental_score])
                    #x = s.replace(b"\t", b",")
                    # print(x)
        network()

        # for each protein in a given list, print name of best interaction partner
        def partners():
            string_api_url = "https://string-db.org/api"
            output_format = "tsv-no-header"
            method = "interaction_partners"

            request_url = "/".join([string_api_url, output_format, method])

            params = {

                "identifiers" : "%0d".join(my_genes), # your protein
                "species" : species_id, # species NCBI identifier
                "limit" : 1,
                "caller_identity" : "www.awesome_app.org" # your app name
            }

            response = requests.post(request_url, data=params)

            for line in response.text.strip().split("\n"):
    
                l = line.strip().split("\t")
                query_ensp = l[0]
                query_name = l[2]
                partner_ensp = l[1]
                partner_name = l[3]
                combined_score = l[5]
                # attempt to remove trailing \t characters in output string
                # replaces \t with comma

                # s contains extra information related to network query
                # s = my_str_as_bytes.join([query_ensp, query_name, partner_ensp, partner_name, combined_score])

                # s_conserved, only print out ensp related ids (for parsing), first and third column
                print("\t".join([query_ensp, query_name, partner_ensp, partner_name, combined_score]))
        partners()

            # next step is to pull partner_ensp from x, check it against original gene list

    except yaml.YAMLError as exc:
            print(exc)

# open and read based on secondary threshold
# slice based upon names that pass primary threshhold
# split passing and failing into separate tables
# remove duplicates?
