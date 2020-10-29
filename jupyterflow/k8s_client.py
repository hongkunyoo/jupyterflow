import json
import yaml

from kubernetes import config
from kubernetes import client


def create_object(body, namespace):
    group, version = body['apiVersion'].split('/')
    plural = body['kind'].lower() + 's'

    config.load_incluster_config()
    api_instance = client.CustomObjectsApi()
    response = api_instance.create_namespaced_custom_object(group, version, namespace, plural, body)
    
    return response


def get_notebook_pod(escaped_username, namespace):
    config.load_incluster_config()
    api_instance = client.CoreV1Api()
    label_selector = 'jupyterflow/username=%s' % escaped_username
    response = api_instance.list_namespaced_pod(namespace, label_selector=label_selector, _preload_content=False)
    
    return json.loads(response.data)['items'][0]
