import yaml
import os

# import pkgutil


def load_config():
    # load user config
    return _load_user_config()


def _load_user_config():
    home = os.environ['HOME']
    CONFIG_FILE = os.path.join(home, '.jupyterflow.yaml')
    
    if os.path.isfile(CONFIG_FILE):
        with open(CONFIG_FILE) as f:
            conf = yaml.safe_load(f)
            if conf is None:
                return {}
            return conf
    return {}



# def _load_default_config():
#     data = pkgutil.get_data(__name__, "templates/default_config.yaml")
#     return yaml.safe_load(data)


# def _merge_config(config, default):
#     # default.update(config)
#     return config