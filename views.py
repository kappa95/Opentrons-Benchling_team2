from flask import request, jsonify, Blueprint, current_app
from queue import Queue
import string
import random
import json
import glob

bp_automation = Blueprint('automation', __name__)

# Start polling services
task_queue = Queue()

from Services import task_runner
task_runner.start_scheduler()


def get_random_string(length):
    letters = string.ascii_letters
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str


@bp_automation.route('/automation', methods=['GET'])
def executeAutomation():
    if request.method == 'GET':
        new_run = {"item": "start new task", "id": get_random_string(6)}
        task_queue.put(new_run)
        resp = {"task_status": "run scheduled"}
        return jsonify(resp), 201
    return 200


@bp_automation.route('/check', methods=['GET'])
def check_status():
    count = current_app.config["TASK_STATUS"]
    resp = {"current_checks_count": count}
    return jsonify(resp), 201


@bp_automation.route('/past_runs', methods=['GET'])
def get_runs():
    all_log_files = glob.glob("log_*.json")
    log_list = {"runs": []}
    for file in all_log_files:
        with open(file) as json_file:
            data = json.load(json_file)
            log_list["runs"].append(data)
    return jsonify(log_list), 200
