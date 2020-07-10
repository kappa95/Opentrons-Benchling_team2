from flask import Flask, request
from flask_cors import CORS
import json
import time
import paramiko as pk
import scp
import datetime
from scp import SCPClient


key_name = 'ot2_ssh_key'  # Key name
direct = 'C:/Users/inse9/'  # Folder of the key
key = direct + key_name
protocol_folder = '/var/lib/jupyter/notebooks'  # Folder in which is contained the protocol on the machine
protocol_file = 'new_protocol.py'

remote_log_filepath = '/var/lib/jupyter/notebooks/outputs/completion_log.json'

app = Flask(__name__)
CORS(app)


@app.route('/barcode', methods=['GET'])
def barcodeReader():
    if request.method == 'GET':
        return json.dumps({'res': "123456"}), 200, {'ContentType': 'application/json'}


@app.route('/automation', methods=['GET'])
def executeAutomation(w_ip='192.168.1.14'):
    if request.method == 'GET':
        client = pk.SSHClient()  # Create an object SSH client
        client.set_missing_host_key_policy(pk.AutoAddPolicy())  # It is needed to add the device policy
        client.connect(w_ip, username='root', key_filename=key, password='opentrons')  # Connection
        chann = client.invoke_shell()
        chann.send('opentrons_execute {}/{} -n \n'.format(protocol_folder, protocol_file))
        chann.send('exit \n')
        code = chann.recv_exit_status()
        print("I got the code: {}".format(code))

        # SCPCLient takes a paramiko transport as an argument
        client = pk.SSHClient()  # Create an object SSH client
        client.set_missing_host_key_policy(pk.AutoAddPolicy())  # It is needed to add the device policy
        client.connect(w_ip, username='root', key_filename=key, password='opentrons')  # Connection
        scp_client = SCPClient(client.get_transport())
        local_filepath = "./log_{}.json".format(datetime.datetime.now().strftime("%m-%d-%Y_%H_%M_%S"))

        scp_client.get(remote_path=remote_log_filepath, local_path=local_filepath)
        scp_client.close()
        with open(local_filepath, 'r') as logjson:
            json_object = json.load(logjson)
        return json.dumps(json_object, indent=4), 200, {'ContentType': 'application/json'}


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5001, threaded=True, use_reloader=False)  # put 'localhost' if you want local
