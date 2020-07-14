import os

class BaseConfig():
    API_PREFIX = '/api'
    TESTING = False
    DEBUG = False


class DevConfig(BaseConfig):
    FLASK_ENV = 'development'


class ProductionConfig(BaseConfig):
    FLASK_ENV = 'production'


class TestConfig(BaseConfig):
    FLASK_ENV = 'test'
    OT2_SSH_KEY_FILENAME = 'ot2_ssh_key'  # Key name
    OT2_SSH_KEY_PATH = 'C:/Users/inse9/'  # Folder of the key
    OT2_SSH_KEY = os.path.join(OT2_SSH_KEY_PATH, OT2_SSH_KEY_FILENAME)
    OT2_PROTOCOL_PATH = '/var/lib/jupyter/notebooks'  # Target machine folder containing protocol to be run
    OT2_PROTOCOL_FILE = 'new_protocol.py'
    OT2_REMOTE_LOG_FILEPATH = '/var/lib/jupyter/notebooks/outputs/completion_log.json'
    OT2_TARGET_IP_ADDRESS = '192.168.1.14'
    OT2_ROBOT_PASSWORD = 'opentrons'
    TASK_QUEUE_POLLING_INTERVAL = 5