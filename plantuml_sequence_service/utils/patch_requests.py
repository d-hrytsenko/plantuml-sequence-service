import os

import requests

_origin_header = f'http://localhost:{os.environ.get("FLASK_PORT")}'  # set in run.env

# Always add
def _init_with_origin_header(self,
                             method=None, url=None, headers=None, files=None, data=None,
                             params=None, auth=None, cookies=None, hooks=None, json=None):
    # Default empty dicts for dict params.
    data = [] if data is None else data
    files = [] if files is None else files
    # !!!!!!! HACK
    if headers is None:
        headers = {"Origin": _origin_header}
    elif "Origin" not in headers:
        headers.update({"Origin": _origin_header})
    # !!!!!!! END HACK
    params = {} if params is None else params
    hooks = {} if hooks is None else hooks

    self.hooks = requests.models.default_hooks()
    for (k, v) in list(hooks.items()):
        self.register_hook(event=k, hook=v)

    self.method = method
    self.url = url
    self.headers = headers
    self.files = files
    self.data = data
    self.json = json
    self.params = params
    self.auth = auth
    self.cookies = cookies


# dirty patch
requests.models.Request.__init__ = _init_with_origin_header
