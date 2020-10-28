import yaml
import os


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


