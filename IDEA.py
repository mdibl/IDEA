#TODO: check for open success, if fail die
import yaml
import logging
import argparse
import pandas as pd

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
        #print(df.head())
        config = yaml.full_load(file)
        for item, doc in config.items():
            print (item, ":", doc)
    except yaml.YAMLError as exc:
        print(exc)
