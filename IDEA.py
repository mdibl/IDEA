#TODO: check for open success, if fail die
import yaml
import logging
import pandas as pd

# update to be dynamic
with open("/Users/nmaki/Documents/GitHub/IDEA/tests/config.yaml", 'r') as stream:
    try:
        print(yaml.safe_load(stream))
    except yaml.YAMLError as exc:
        print(exc)
# argparser for yaml input file
def parser():
    parser.add_argument("--file", type=FileType('r'))