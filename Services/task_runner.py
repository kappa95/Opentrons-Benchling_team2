from scp import SCPClient
from _datetime import datetime, timedelta
import time
import paramiko as pk
from timeloop import Timeloop
from views import task_queue, current_app

scheduler = Timeloop()


ssh_key_filename = 'ot2_ssh_key'  # Key name
directory = 'C:/Users/inse9/'  # Folder of the key
key = directory + ssh_key_filename

# Target machine folder containing protocol to be run
protocol_folder = '/var/lib/jupyter/notebooks'
protocol_file = 'new_protocol.py'
remote_log_filepath = '/var/lib/jupyter/notebooks/outputs/completion_log.json'
target_machine_ip = '192.168.1.14'
target_machine_password = 'opentrons'
QUEUE_POLLING_INTERVAL = 5
OPERATION_RUNNING = False


def start_scheduler():
    scheduler.start(block=False)


def create_ssh_client(usr, key_file, pwd):
    client = pk.SSHClient()  # Create an object SSH client
    client.set_missing_host_key_policy(pk.AutoAddPolicy())  # It is needed to add the device policy
    client.connect(target_machine_ip, username=usr, key_filename=key_file, password=pwd)
    return client


@scheduler.job(interval=timedelta(seconds=QUEUE_POLLING_INTERVAL))
def test():
    print("checking for new runs")
    global OPERATION_RUNNING
    if not OPERATION_RUNNING and not task_queue.empty():
        current_app.config['TASK_STATUS'] = "running"
        task = task_queue.get()
        print(task)
        OPERATION_RUNNING = True
        for i in range(0, 10):
            print("doing long task")
            time.sleep(5)
        OPERATION_RUNNING = False
        current_app.config['TASK_STATUS'] = "ready"


@scheduler.job(interval=timedelta(seconds=QUEUE_POLLING_INTERVAL))
def execute_automation():
    global OPERATION_RUNNING
    if not OPERATION_RUNNING and not task_queue.empty():
        OPERATION_RUNNING = True
        run_item = task_queue.get()
        client = create_ssh_client(usr='root', key_file=key, pwd=target_machine_password)
        channel = client.invoke_shell()
        channel.send('opentrons_execute {}/{} -n \n'.format(protocol_folder, protocol_file))
        channel.send('exit \n')
        code = channel.recv_exit_status()
        print("I got the code: {}".format(code))
        # SCP Client takes a paramiko transport as an argument
        client = create_ssh_client(usr='root', key_file=key, pwd=target_machine_password)
        scp_client = SCPClient(client.get_transport())
        local_filepath = "./log_{}.json".format(run_item["id"])
        scp_client.get(remote_path=remote_log_filepath, local_path=local_filepath)
        scp_client.close()
        OPERATION_RUNNING = False
