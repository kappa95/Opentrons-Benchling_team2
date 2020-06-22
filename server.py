import requests
import json


def api_get():
    url = "https://ec2-15-161-32-20.eu-south-1.compute.amazonaws.com/api/logfile"
    headers = {
        'Content-Type': 'application/json'
    }
    file_name = "2a290c8f-933f-4ac0-bebf-ef3e9c65b4c5.json"
    response = requests.request("GET", url + '?file=' + file_name, headers=headers, verify=False)
    if response.status_code >= 400:
        raise Exception(
            "Server returned status {}. Response:\n{}".format(
                response.status_code, json.dumps(response.json())
            )
        )
    return response.json()


def api_post(payload={}):
    url = "https://ec2-15-161-32-20.eu-south-1.compute.amazonaws.com/api/logfile"
    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data=payload, verify=False)
    if response.status_code >= 400:
        raise Exception(
            "Server returned status {}. Response:\n{}".format(
                response.status_code, json.dumps(response.json())
            )
        )
    return response.json()
