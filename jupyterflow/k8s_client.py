
from kubernetes import config
import kubernetes.client
from kubernetes import client, config
from kubernetes.client import Configuration


def create_object(plural, body):
    group, version = body['apiVersion'].split('/')
    namespace = os.environ.get('NAMESPACE', "default")

    config.load_incluster_config()
    api_instance = client.CustomObjectsApi()
    response = api_instance.create_namespaced_custom_object(group, version, namespace, plural, body)

    return response