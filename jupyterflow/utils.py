import pkgutil
import escapism
import string

# data = pkgutil.get_data(__name__, "templates/workflow.yaml")

def get_escaped_user(user):
    safe_chars = set(string.ascii_lowercase + string.digits)
    safe_servername = escapism.escape(user, safe=safe_chars, escape_char='-').lower()
    legacy_escaped_username = ''.join([s if s in safe_chars else '-' for s in user.lower()])
    return escapism.escape(user, safe=safe_chars, escape_char='-').lower()


def get_value(key, defaults):
    return os.environ.get(key, defaults[key])


