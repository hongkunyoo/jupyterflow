import os

import yaml
import escapism
import string
import pkgutil


# def get_escaped_user(user):
#     safe_chars = set(string.ascii_lowercase + string.digits)
#     safe_servername = escapism.escape(user, safe=safe_chars, escape_char='-').lower()
#     legacy_escaped_username = ''.join([s if s in safe_chars else '-' for s in user.lower()])
#     return escapism.escape(user, safe=safe_chars, escape_char='-').lower()


def create_config():
    data = pkgutil.get_data(__name__, "templates/jupyterflow.yaml")

    home = os.environ['HOME']
    CONFIG_FILE = os.path.join(home, '.jupyterflow.yaml')
    with open(CONFIG_FILE, 'wt') as f:
        f.write(data.decode('utf-8'))


def load_config():
    home = os.environ['HOME']
    CONFIG_FILE = os.path.join(home, '.jupyterflow.yaml')
    
    if os.path.isfile(CONFIG_FILE):
        with open(CONFIG_FILE) as f:
            conf = yaml.safe_load(f)
            if conf is None:
                return {}
            return conf
    return {}



def hanle_exception():
    pass



# import pkgutil
# data = pkgutil.get_data(__name__, "templates/workflow.yaml")