import requests

def fetch_id():
    string_api_url = "https://string-db.org/api"
    output_format = "tsv-no-header"
    method = "get_string_ids"

    # configure parameters
    params = {

        "identifiers" : "\r".join(str([my_genes])),
        "species" : species_id,
        "limit" : 1,
        "echo_query" : 1,
        "caller_identity" : "www.awesome_app.org"
        }

    request_url = "/".join([string_api_url, output_format, method])
            
    results = requests.post(request_url, data=params)

    for line in results.text.strip().split("\n"):
        l = line.split("\t")
        input_identifier, string_identifier = l[0], l[2]
        print("Input:", input_identifier, "STRING:", string_identifier, sep="\t")
fetch_id()