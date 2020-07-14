from scp import SCPClient
from _datetime import datetime, timedelta
import time
import paramiko as pk
from timeloop import Timeloop
from views import task_queue

scheduler = Timeloop()


OT2_SSH_KEY = 'C:/Users/inse9/ot2_ssh_key'
OT2_PROTOCOL_PATH = '/var/lib/jupyter/notebooks'
OT2_PROTOCOL_FILE = 'new_protocol.py'
OT2_REMOTE_LOG_FILEPATH = '/var/lib/jupyter/notebooks/outputs/completion_log.json'
OT2_TARGET_IP_ADDRESS = '192.168.1.14'
OT2_ROBOT_PASSWORD = 'opentrons'
TASK_QUEUE_POLLING_INTERVAL = 5
TASK_RUNNING = False

app = object()


def start_scheduler(f_app):
    global app
    app = f_app
    scheduler.start(block=False)


def create_ssh_client(usr, key_file, pwd):
    client = pk.SSHClient()  # Create an object SSH client
    client.set_missing_host_key_policy(pk.AutoAddPolicy())  # It is needed to add the device policy
    client.connect(OT2_TARGET_IP_ADDRESS, username=usr, key_filename=key_file, password=pwd)
    return client


@scheduler.job(interval=timedelta(seconds=TASK_QUEUE_POLLING_INTERVAL))
def test():
    global TASK_RUNNING
    if not TASK_RUNNING and not task_queue.empty():
        task = task_queue.get()
        app.config['TASK_STATUS'] = "running %s" % str(task)
        TASK_RUNNING = True
        for i in range(0, 10):
            print("doing run ID: %s" % str(task))
            time.sleep(5)
        print("Completed")
        TASK_RUNNING = False
        app.config['TASK_STATUS'] = "completed run ID: %s" % str(task)


# @scheduler.job(interval=timedelta(seconds=QUEUE_POLLING_INTERVAL))
def execute_automation():
    global TASK_RUNNING
    if not TASK_RUNNING and not task_queue.empty():
        TASK_RUNNING = True
        client = create_ssh_client(usr='root', key_file=OT2_SSH_KEY, pwd=OT2_ROBOT_PASSWORD)
        #client = create_ssh_client(usr='root', key_file=key, pwd=target_machine_password)
        channel = client.invoke_shell()
        channel.send('opentrons_execute {}/{} -n \n'.format(OT2_PROTOCOL_PATH, OT2_PROTOCOL_FILE))
        channel.send('exit \n')
        code = channel.recv_exit_status()
        print("I got the code: {}".format(code))
        # SCP Client takes a paramiko transport as an argument
        client = create_ssh_client(usr='root', key_file=OT2_SSH_KEY, pwd=OT2_ROBOT_PASSWORD)
        scp_client = SCPClient(client.get_transport())
        local_filepath = "./log_{}.json".format(datetime.now().strftime("%m-%d-%Y_%H_%M_%S"))
        scp_client.get(remote_path=OT2_REMOTE_LOG_FILEPATH, local_path=local_filepath)
        scp_client.close()
        TASK_RUNNING = False
