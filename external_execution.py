import paramiko as pk

key_name = 'ot2_ssh_key'
direct = 'C:/Users/inse9/'
key = direct + key_name
protocol_folder = '/var/lib/jupyter/notebooks/'
protocol_file = 'v1_station_C.py'


def main(w_ip='192.168.1.14'):
    client = pk.SSHClient()
    client.set_missing_host_key_policy(pk.AutoAddPolicy())
    client.connect(w_ip, username='root', key_filename=key, password='opentrons')
    # stdin, stdout, stderr = client.exec_command('whoami')
    env_dict = {"OT_SMOOTHIE_ID": "AMA", "RUNNING_ON_PI": "true"}
    (stdin, stdout, stderr) = client.exec_command('opentrons_execute {}/{} -n'.format(protocol_folder, protocol_file),
                                                  environment=env_dict)
    output = stdout.readlines()
    print('\n'.join(output))
    err = stderr.readlines()
    print('\n'.join(err))


if __name__ == "__main__":
    main()
