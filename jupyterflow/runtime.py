import os
import pwd

from . import utils

class Runtime(dict):
    def __init__(self, *args, **kwargs):
        self.update(*args, **kwargs)

        with open('/var/run/secrets/kubernetes.io/serviceaccount/namespace') as f:
            dict.__setitem__(self, 'namespace', f.read())
        
        NB_USER = os.environ['NB_USER']
        nb_user_pwd = pwd.getpwnam(NB_USER)
        dict.__setitem__(self, 'image', os.environ['JUPYTER_IMAGE_SPEC'])
        dict.__setitem__(self, 'workingDir', None)
        dict.__setitem__(self, 'PATH', os.environ['PATH'])
        dict.__setitem__(self, 'HOME', os.environ['HOME'])
        dict.__setitem__(self, 'NB_USER', NB_USER)
        dict.__setitem__(self, 'runAsUser', nb_user_pwd.pw_uid)
        dict.__setitem__(self, 'runAsGroup', nb_user_pwd.pw_gid)
        dict.__setitem__(self, 'escaped_username', utils.get_escaped_user(os.environ['JUPYTERHUB_USER']))


runtime = Runtime()


