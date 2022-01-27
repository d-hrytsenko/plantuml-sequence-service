import os
from pathlib import Path

import yaml


APP_PORT = os.getenv("APP_PORT", 8000)
APP_HOST = "127.0.0.1"
_dir_path = os.path.dirname(os.path.realpath(__file__))
try:
    SERVICE_NAMES = yaml.safe_load(Path(_dir_path, 'service_names.yml').read_text())
except FileNotFoundError:
    print("service_names.yml not found. Create the mapping for better diagram readability")
    SERVICE_NAMES = {}

# UML related settings
REQUEST_STEP_TEMPLATE = '"{client}" -> "{server}": **{message.method} {message.path}** (trace: {message.trace_id})'
RESPONSE_STEP_TEMPLATE = '"{server}" -> "{client}": **{message.status}** (trace: {message.trace_id})'
# Amount of characters to which the body will be limited for displaying in tooltip on a diagram,
BODY_DISPLAY_LIMITER = 200
