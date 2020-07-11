from flask import request, jsonify, Blueprint, current_app
from queue import Queue
import json

bp_automation = Blueprint('automation', __name__)

# Start polling services
task_queue = Queue()

from services import task_runner
task_runner.start_scheduler()


@bp_automation.route('/automation', methods=['GET'])
def executeAutomation():
    if request.method == 'GET':
        new_run = "start new task"
        task_queue.put(new_run)
        resp = {"task_status": "run scheduled"}
        return jsonify(resp), 201
    return 200


@bp_automation.route('/check', methods=['GET'])
def check_status():
    count = current_app.config["TASK_STATUS"]
    resp = {"current_checks_count": count}
    return jsonify(resp), 201
