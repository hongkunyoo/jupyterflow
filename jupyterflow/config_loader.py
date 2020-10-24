import yaml
import os

CONFIG_FILE = '$HOME/.jupyterflow.yaml'

def load_config():
    if os.path.isfile(CONFIG_FILE):
        with open(CONFIG_FILE) as f:
            return yaml.safe_load(f)
    return {}
