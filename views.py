from flask import request, jsonify, Blueprint, current_app, render_template
from queue import Queue
from uuid import uuid4

bp_automation = Blueprint('automation', __name__)

# # Start polling services
task_queue = Queue()
#
# from services import task_runner
# task_runner.start_scheduler()


@bp_automation.route('/automation', methods=['GET', 'POST'])
def execute_automation():
    message = ""
    if request.method == 'POST':
        run_id = uuid4()
        task_queue.put(run_id)
        message = "A new run has been scheduled for protocol. Run ID: %s" % run_id
        return render_template('index.html', title="station A", msg=message), 201
    if request.method == 'GET':
        return render_template('index.html', title="station A", msg=message), 200
    return 404


@bp_automation.route('/check', methods=['GET'])
def check_status():
    status = current_app.config["TASK_STATUS"]
    return render_template('status.html', msg=status)
