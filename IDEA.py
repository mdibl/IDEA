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
        df = pd.io.json.json_normalize(yaml.safe_load(file))
        print(df.head())
        df = pd.read_csv('/Users/nmaki/Documents/GitHub/IDEA/tests/eDESeq2.csv')
    except yaml.YAMLError as exc:
        print(exc)
