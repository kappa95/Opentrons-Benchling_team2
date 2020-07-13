from flask import Flask, request
from flask_cors import CORS


app = Flask(__name__)
CORS(app)
app.config['TASK_STATUS'] = "ready"

from views import bp_automation
app.register_blueprint(bp_automation)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=False)
