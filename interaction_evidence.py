# using a list of proteins, select only interactions
# which have experimental evidence and print scores

import urllib.request
import sys

def request():
    string_api_url = "https://string-db.org/api"
    output_format = "tsv-no-header"
    method = "network"

    my_genes = ["ENSDARG00000003495", "ENSDARG00000007245",
                "ENSDARG00000000779", "ENSDARG00000000690",
                "ENSDARG00000002909", "ENSDARG00000002790"]

   # use taxonomy ID for zebrafish
    species = "7955"
    my_app = "www.awesome_app.org"

    # construct request
    request_url = string_api_url + "/" + output_format + "/" + method + "?"
    request_url += "identifiers=%s" % "%0d".join(my_genes)
    request_url += "&" + "species=" + species
    request_url += "&" + "caller_identity=" + my_app

    try:
        response = urllib.request.urlopen(request_url)
    except urllib.request.HTTPError as err:
        error_message = err.read()
        print (error_message)
        sys.exit()

    # read and parse results
    line = response.readline()

    while line:
        l = line.strip().split("\t")
        p1, p2 = l[2], l[3]
        experimental_score = float(l[10])
        if experimental_score != 0:
            print ("\t".join([p1,p2, "experimentally confirmed (prob. %.3f)" % experimental_score]))
    
        line = response.readline()