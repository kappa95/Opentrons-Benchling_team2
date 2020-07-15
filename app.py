from flask import Flask, request
from flask_cors import CORS
from views import bp_automation


def create_app():
    app = Flask(__name__)
    app.secret_key = b'_5#y2L"s8zxec]/'
    app.config.from_object('config')
    app.config['TASK_STATUS'] = 'ready'
    CORS(app)

    # Register all views blueprints
    app.register_blueprint(bp_automation)
    from Services import task_runner
    task_runner.start_scheduler(app)
    return app


if __name__ == "__main__":
    app = create_app()
    app.run(host='localhost', port=5001, debug=False)
