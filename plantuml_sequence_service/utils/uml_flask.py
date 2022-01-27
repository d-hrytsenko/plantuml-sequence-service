import json
import os
import uuid
from datetime import datetime

import requests
from flask import request, g, Flask

UML_APP_HOST = os.getenv("UML_APP_HOST", "127.0.0.1")
UML_APP_PORT = os.getenv("UML_APP_PORT", 8000)


def init(app: Flask):
    """
    Add two callbacks for Flask application:
    1) Before request - send the incoming request to plantuml sequence service
    2) After request - send the response to plantuml sequence service
    """
    @app.before_request
    def before_request_callback():
        g.trace_id = str(uuid.uuid4())
        r_data = {
            "timestamp": datetime.now().timestamp(),
            "trace_id": g.trace_id,
            "path": request.path,
            "method": request.method,
            "host": request.host,
            "headers": {k: v for k, v in request.headers.items()},
            "body": request.get_json() if request.data else None,
            "remote_addr": f"{request.remote_addr}:" + str(request.environ.get("REMOTE_PORT"))
        }
        requests.post(
            f"http://{UML_APP_HOST}:{UML_APP_PORT}/requests/",
            json.dumps(r_data)
        )

    @app.after_request
    def after_request_callback(response):
        response.direct_passthrough = False
        # ^^^ Workaround for:
        # RuntimeError: Attempted implicit sequence conversion but the response object is in direct passthrough mode.
        r_data = {
            "timestamp": datetime.now().timestamp(),
            "trace_id": g.trace_id,
            "headers": {k: v for k, v in response.headers.items()},
            "body": response.get_json() if response.data else None,
            "status": str(response.status)
        }
        requests.post(
            f"http://{UML_APP_HOST}:{UML_APP_PORT}/responses/",
            json.dumps(r_data)
        )
        return response
