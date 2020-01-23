# for each pair of proteins in a list, save PNG image of
# STRING network for defined # of confident interacting partners

import urllib.request
from time import sleep

def request(): 
    string_api_url = "https://string-db.org/api"
    output_format = "image"
    method = "network"

    my_genes = [["ENSDARG00000003495", "ENSDARG00000007245"],
                ["ENSDARG00000000779", "ENSDARG00000000690"],
                ["ENSDARG00000002909", "ENSDARG00000002790"]]

    # use taxonomy ID for zebrafish
    species = "7955"
    my_app = "dev.azure.com/MDIBL"

    # create the request
    request_url = string_api_url + "/" + output_format + "/" + method + "?"
    request_url += "identifiers=%s"
    request_url += "&" + "species=" + species
    request_url += "&" + "add_white_nodes=15"
    request_url += "&" + "caller_identity=" + my_app

    # for each gene, call STRING
    for gene_pair in my_genes:
        # gene1, gene2 = gene_pair
        urllib.request.urlretrieve(request_url % "%0d".join(gene_pair), "%s.png" % "_".join(gene_pair))
        sleep(1)
