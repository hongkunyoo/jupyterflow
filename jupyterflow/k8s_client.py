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


def delete_object(name, apiVersion, plural, namespace):
    group, version = apiVersion.split('/')
    config.load_incluster_config()
    api_instance = client.CustomObjectsApi()
    response = api_instance.delete_namespaced_custom_object(group, version, namespace, plural, name)
        
    return response
    

def get_notebook_pod(hostname, namespace):
    config.load_incluster_config()
    api_instance = client.CoreV1Api()
    response = api_instance.read_namespaced_pod(hostname, namespace, _preload_content=False)
    
    return json.loads(response.data)
