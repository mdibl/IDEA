#!/usr/bin/env python

#################################################################
## For each protein in a given list print the names of the best 5
## interaction partners.
#################################################################

import sys
import urllib.request, urllib.error, urllib.parse

string_api_url = "https://string-db.org/api"
output_format = "tsv-no-header"
method = "interaction_partners"

my_genes = ["9606.ENSP00000000233", "9606.ENSP00000000412",
            "9606.ENSP00000000442", "9606.ENSP00000001008"] 
species = "9606"
limit = 5
my_app = "www.awesome_app.org"

## Construct the request

request_url = string_api_url + "/" + output_format + "/" + method + "?"
request_url += "identifiers=%s" % "%0d".join(my_genes)
request_url += "&" + "species=" + species
request_url += "&" + "limit=" + str(limit)
request_url += "&" + "caller_identity=" + my_app

try:
    response = urllib.request.urlopen(request_url)
except urllib.error.HTTPError as err:
   error_message = err.read()
   print(error_message)
   sys.exit()

## Read and parse the results

line = response.readline()

while line:
    l = line.strip().split("\t")
    query_ensp = l[0]
    query_name = l[2]
    partner_ensp = l[1]
    partner_name = l[3]
    combined_score = l[5]

    print("\t".join([query_ensp, query_name, partner_name, combined_score]))

    line = response.readline()