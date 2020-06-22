import requests
import urllib3
"""For disabling the insecure warnings"""
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def api_get():
    url = "https://ec2-15-161-32-20.eu-south-1.compute.amazonaws.com/api/logfile"
    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.get(url, headers=headers, verify=False)
    return response


def api_post(payload={}):
    url = "https://ec2-15-161-32-20.eu-south-1.compute.amazonaws.com/api/logfile"
    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.post(url, headers=headers, data=payload, verify=False)
    return response
