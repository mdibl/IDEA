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
        print(yaml.safe_load(file))
    except yaml.YAMLError as exc:
        print(exc)
