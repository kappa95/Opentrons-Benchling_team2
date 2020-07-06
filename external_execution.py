import paramiko as pk
import scp
import datetime
import subprocess
from scp import SCPClient


key_name = 'ot2_ssh_key'  # Key name
# direct = 'C:/Users/inse9/'  # Folder of the key
direct = '/home/kappa95/'  # Folder of the key in case of linux using
key = direct + key_name
protocol_folder = '/var/lib/jupyter/notebooks/'  # Folder in which is contained the protocol on the machine
protocol_file = 'v1_station_C.py'

remote_log_filepath = '/var/lib/jupyter/outputs/temp_log.json'

def main(w_ip='169.254.128.233'):  # IP used for ssh-ing the robot
    client = pk.SSHClient()  # Create an object SSH client
    client.set_missing_host_key_policy(pk.AutoAddPolicy())  # It is needed to add the device policy
    client.connect(w_ip, username='root', key_filename=key, password='opentrons')  # Connection
    chann = client.invoke_shell()
    chann.send('ls -a \n')
    # chann.send('opentrons_execute {}/{} -n \n'.format(protocol_folder, protocol_file))
    chann.send('exit \n')
    code = chann.recv_exit_status()
    print("I got the code: {}".format(code))

    # SCPCLient takes a paramiko transport as an argument
    scp = SCPClient(client.get_transport())
    local_filepath = "./temperature_log_{}.json".format(datetime.datetime.now().strftime("%m-%d-%Y_%H_%M_%S"))

    scp.get(remote_path=remote_log_filepath, local_path=local_filepath)
    scp.close()


if __name__ == "__main__":
    main()
