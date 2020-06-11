import requests
import json


def api_get(domain, api_key, path, params={}):
    url = "https://{}/api/v2/{}".format(domain, path)
    rv = requests.get(url, auth=(api_key, ""), params=params)
    if rv.status_code >= 400:
        raise Exception(
            "Server returned status {}. Response:\n{}".format(
                rv.status_code, json.dumps(rv.json())
            )
        )
    return rv.json()


def api_post(domain, api_key, path, payload={}):
    url = "https://{}/api/v2/{}".format(domain, path)
    rv = requests.post(url, auth=(api_key, ""), json=payload, verify=True)
    if rv.status_code >= 400:
        raise Exception(
            "Server returned status {}. Response:\n{}".format(
                rv.status_code, json.dumps(rv.json())
            )
        )
    return rv.json()


def api_patch(domain, api_key, path, payload={}):
    url = "https://{}/api/v2/{}".format(domain, path)
    rv = requests.patch(url, auth=(api_key, ""), json=payload, verify=True)
    if rv.status_code >= 400:
        raise Exception(
            "Server returned status {}. Response:\n{}".format(
                rv.status_code, json.dumps(rv.json())
            )
        )
    return rv.json()

# def main():
#     api_key = 'sk_l11W7KMVqS2XmuhtqdysHjSok9Xlq'
#     domain = 'multiplylabstest.benchling.com'
#     registry_id = 'src_6Bxs3ci2'
#     path = 'folders'
#     folder = "lib_ClPuAOki"
#     payload = {
#         "aliases": ["created from python"],
#         "customFields": {
#             "Patient_Name": {"value": "Giuseppe"},
#             "Covid_Result": {"value": "TRUE"},
#             "Favorite_Ice_Cream_Flavor": {"value": "Chocolate"}
#         },
#         "folderId": folder,
#         "name": "Testing-Patient-GR",
#         "schemaId": "ts_0m0f82y8"}
#     #data = '{"aliases": ["created from curl"],"custom fields": {"Patient_Name": {"value": "Giuseppe"},"Covid_Result": {"value": "TRUE"},"Favorite_Ice_Cream_Flavor": {"value": "Chocolate"}},"folderId": "null","name": "Testing-Patient-GR","schemaId": "ts_0m0f82y8"}'
#     file = api_get(domain, api_key, path)
#     #file = api_post(domain, api_key, path, payload)
#     string = json.dumps(file, indent=2)
#     print(string)


# if __name__ == "__main__":
#     main()
