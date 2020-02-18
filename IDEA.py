from __future__ import print_function
#import yaml
import argparse
import pandas as pd
import sys
import random
import requests
import yaml
import urllib.request
import urllib.error
import urllib.parse

parser = argparse.ArgumentParser()
parser.add_argument('filename')
args = parser.parse_args()
with open(args.filename) as file:
    config = yaml.full_load(file)
    input_path = config['DESeq_input']['path']

    # TODO: fix static thresholding, allow for variable

    baseMean = config['baseMean']
    log2FoldChange = config['log2FoldChange']
    lfcSE = config['lfcSE']
    pvalue = config['pvalue']
    padj = config['padj']
    species_id = config['species']
    cs_threshold = config['cs_threshold']
    df = pd.read_csv(input_path)
    # use threshold value to cut down CSV
    # only columns defined in config.yaml file
    df_threshold = df.loc[(df['baseMean'] > baseMean) 
                                    & (df['log2FoldChange'] < log2FoldChange)
                                    & (df['lfcSE'] < lfcSE)
                                    & (df['pvalue'] < pvalue)
                                    & (df['padj'] < padj)]
    my_genes = df_threshold['genes']

    # TODO: Use Dataframe.append to add to gene list

    def mapId():
        string_api_url = "https://string-db.org/api"
        output_format = "tsv"
        method = "get_string_ids"
        # configure parameters
        params = {

            "identifiers": "\r".join(my_genes),
            "species": species_id,
            "limit": 1,
            "echo_query": 1,
            "caller_identity": "mdibl.org"
        }
        request_url = "/".join([string_api_url, output_format, method])
        results = requests.post(request_url, data=params)
        for line in results.text.strip().split("\n"):
            l = line.split("\t")
            input_identifier, string_identifier = l[0], l[2]
            print("Input:", input_identifier, "STRING:",
                    string_identifier, sep="\t")
    mapId()

    # for each protein in a given list, print protein-protein interactions
    # with medium medium or higher confidence exp score
    def networkInteraction():
        string_api_url = "https://string-db.org/api"
        output_format = "tsv-no-header"
        method = "network"
        request_url = "/".join([string_api_url, output_format, method])
        params = {

            "identifiers": "%0d".join(my_genes),  # your protein
            "species": species_id,  # species NCBI identifier
            "caller_identity": "mdibl.org"  # your app name
        }

        # read and parse results
        response = requests.post(request_url, data=params)

        for line in response.text.strip().split("\n"):
            l = line.strip().split("\t")
            p0, p1, p2, p3, p4 = l[0], l[1], l[2], l[3], l[4]
            experimental_score = float(l[10])
            if experimental_score != 0:
                print("\t".join(
                    [p0, p1, p2, p3, p4, "experimentally confirmed (prob. %.3f)" % experimental_score]))
    networkInteraction()

    # for each protein in a given list, print name of best interaction partner(s)
    # dictated by "limit"
    def bestPartners():
        string_api_url = "https://string-db.org/api"
        output_format = "tsv-no-header"
        method = "interaction_partners"

        request_url = "/".join([string_api_url, output_format, method])

        params = {

            "identifiers": "%0d".join(my_genes),  # your protein
            "species": species_id,  # species NCBI identifier
            "limit": 1,
            "caller_identity": "mdibl.org"  # your app name
        }

        response = requests.post(request_url, data=params)

        for line in response.text.strip().split("\n"):

            l = line.strip().split("\t")
            query_ensp = l[0]
            query_name = l[2]
            partner_ensp = l[1]
            partner_name = l[3]
            combined_score = l[5]
            print("\t".join([query_ensp, query_name,
                                partner_ensp, partner_name, combined_score]))
    bestPartners()

'''
if __name__ == "__main__":
    mapId()
    networkInteraction()
    bestPartners()
print("after __name__ guard")
'''

# open and read based on secondary threshold
# slice based upon names that pass primary threshhold
# split passing and failing into separate tables
# remove duplicates?
