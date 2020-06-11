from subprocess import call
import json
from benchling import api_post
import os  # it is for the second method, but the first one allows to pass variables

# This start the external simulation
call(["opentrons_simulate.exe", "v1_station_C.py"])
# os.system("opentrons_simulate.exe v1_station_C.py")  # it's another way
filepath = './outputs/'
with open(filepath + '/payload.json', 'w') as json_write:
    with open(filepath + 'tip_log.json', 'r') as json_read:
        data = json.load(json_read)  # it is a dictionary now
    data["Station"] = "C"
    json.dump(data, json_write)

# now i want to upload on benchling
domain = 'multiplylabstest.benchling.com'
api_key = 'sk_pLytaKiuqk6D6draYkwwK3Yq8KNPe'


def main():
    path = 'custom-entities'  # This is the path where you upload a new custom entity
    folderid = "lib_Ijj1J0fZ"  # it is the folder id associated to the mine
    schemaid = "ts_0m0f82y8"
    with open(filepath + '/payload.json', 'r') as json_read2:
        data2 = json.load(json_read2)
    payload = {
        "aliases": ['Written by Python'],
        "customFields": {
            "Station": {"value": data2["Station"]},
            "tips20": {"value": str(data2["tips20"])},
            "tips300": {"value": str(data2["tips300"])},
            },
        "folderId": folderid,
        "name": "external_execution",
        "schemaId": schemaid}
    # print(data2)
    new_entity = api_post(domain, api_key, path, payload)


if __name__ == "__main__":
    main()
