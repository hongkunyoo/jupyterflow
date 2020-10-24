#!/usr/bin/env python
import os, sys
import yaml
import time
import string
import pkg_resources

import escapism
import boto3
from botocore.client import Config

from kubernetes import config
import kubernetes.client
from kubernetes import client, config
from kubernetes.client import Configuration

from jinja2 import BaseLoader
from jinja2 import Environment


__author__ = 'hongkunyoo'
__version__ = '0.0.1'

# try:
#     import importlib.resources as pkg_resources
# except ImportError:
#     # Try backported to PY<37 `importlib_resources`.
#     import importlib_resources as pkg_resources

# from . import templates




# template = pkg_resources.read_text(templates, 'workflow.yaml')
# print(template)

# template = pkg_resources.open_text(templates, 'workflow.yaml')
# print(template)



import pkgutil

data = pkgutil.get_data(__name__, "templates/workflow.yaml")

print(type(data))
print(data)


# CONFIG_FILE = '/home/jovyan/.isctl.yaml'




CRON_WF_TEMPLATE = \
"""
apiVersion: argoproj.io/v1alpha1
kind: CronWorkflow
metadata:
  generateName: cronwf-
  namespace: notebook
spec:
  schedule: "{{ schedule }}"
  concurrencyPolicy: "Replace"
  startingDeadlineSeconds: 0
  workflowSpec:
{{ workflow | indent( width=4, indentfirst=True)}}
"""

DEPLOY_TEMPLATE = \
"""
apiVersion: apps/v1
kind: Deployment
metadata:
  labels:
    lgebigdata.com/username: {{ username }}
    lgebigdata.com/component: user-deploy
  name: deploy-{{ name }}
  namespace: {{ namespace }}
spec:
  replicas: 1
  selector:
    matchLabels:
      lgebigdata.com/username: {{ username }}
      lgebigdata.com/component: user-deploy
  template:
    metadata:
      labels:
        lgebigdata.com/username: {{ username }}
        lgebigdata.com/component: user-deploy
    spec:
      containers:
      - name: web
        image: {{ userimage }}
        command: {{ command }}
        workingDir: {{ workingDir }}
        ports:
        - containerPort: {{ port }}
        volumeMounts:
        - mountPath: /home/jovyan
          name: home-vol
        - mountPath: /nas001
          name: nas001
      volumes:
      - name: home-vol
        persistentVolumeClaim:
          claimName: claim-{{ escaped_name }}
      - name: nas001
        persistentVolumeClaim:
          claimName: nas001
---
apiVersion: v1
kind: Service
metadata:
  labels:
    lgebigdata.com/username: {{ username }}
  name: deploy-{{ name }}
  namespace: {{ namespace }}
spec:
  ports:
  - name: http
    port: 80
    protocol: TCP
    targetPort: {{ port }}
  selector:
    lgebigdata.com/username: {{ username }}
    lgebigdata.com/component: user-deploy
---
apiVersion: extensions/v1beta1
kind: Ingress
metadata:
  annotations:
    cert-manager.io/cluster-issuer: lgebigdata-issuer
    kubernetes.io/ingress.class: nginx
    lgebigdata.com/description: user-deploy
    lgebigdata.com/group: operation
    lgebigdata.com/layer: frontend
  labels:
    lgebigdata.com/username: {{ username }}
  name: deploy-{{ name }}
  namespace: {{ namespace }}
spec:
  rules:
  - host: {{ endpoint }}
    http:
      paths:
      - backend:
          serviceName: deploy-{{ name }}
          servicePort: 80
        path: /
  tls:
  - hosts:
    - {{ endpoint }}
    secretName: {{ username }}-deploy-tls
"""


def get_escaped_user(user):
    safe_chars = set(string.ascii_lowercase + string.digits)
    safe_servername = escapism.escape(user, safe=safe_chars, escape_char='-').lower()
    legacy_escaped_username = ''.join([s if s in safe_chars else '-' for s in user.lower()])
    return escapism.escape(user, safe=safe_chars, escape_char='-').lower()


def get_value(key, defaults):
    return os.environ.get(key, defaults[key])


def request_object(plural, body):
    group = 'argoproj.io'
    version = 'v1alpha1'
    namespace = 'notebook'
    plural = plural

    config.load_incluster_config()
    api_instance = client.CustomObjectsApi()
    response = api_instance.create_namespaced_custom_object(group, version, namespace, plural, body)

    return response['metadata']['selfLink'].split('/')[-1]

def wf_run():
    wf_path = sys.argv[3]
    rendered = render_wf(wf_path)
    body = yaml.safe_load(rendered)
    print(request_object('workflows', body))
    


def render_wf(wf_path):
    abs_wf_path = os.path.abspath(wf_path)
    abs_wf_dir = os.path.dirname(abs_wf_path)

    with open(abs_wf_path) as f:
        conf = yaml.safe_load(f)

    jobs = conf['jobs']
    d = dict(zip(range(1,len(jobs)+1), jobs))
    dags = conf.get('dags', [])
    resolve_tree = {}

    for k in d.keys():
        resolve_tree['job-' + str(k)] = []

    for dag in dags:
        pre, pro = dag.replace(' ', '').split('>>')
        resolve_tree['job-' + pro].append('job-' + pre)

    user_name = os.environ['JUPYTERHUB_USER']
    escaped_name = get_escaped_user(user_name)
    
    wf_jobs = []
    for i, j in enumerate(jobs):
        job = {}
        job['name'] = 'job-' + str(i+1)
        cmds = j.split(' ')
        job['command'] = cmds
        try:
            job['dependencies'] = resolve_tree['job-' + str(i+1)]
        except:
            job['dependencies'] = []
        wf_jobs.append(job)

    defaults = {
        "LIMITS_CPU": "8",
        "LIMITS_MEM": "20Gi"
    }
    if os.path.isfile(CONFIG_FILE):
        with open(CONFIG_FILE) as f:
            config_file = yaml.safe_load(f)
            for k, v in config_file.items():
                defaults[k] = v

    cpu = get_value('LIMITS_CPU', defaults)
    mem = get_value('LIMITS_MEM', defaults)
    runAsUser = os.getuid() 

    wf = {}
    wf['jobs'] = wf_jobs
    wf['escaped_name'] = escaped_name
    wf['username'] = user_name
    wf['workingDir'] = abs_wf_dir
    wf['PATH'] = os.environ['PATH']
    wf['runAsUser'] = runAsUser
    wf['limits'] = {
      "cpu": cpu,
      "memory": mem
    }

    template = Environment(loader=BaseLoader).from_string(WF_TEMPLATE)
    return template.render(**wf)


def config_version():
    print(pkg_resources.get_distribution("isctl").version)

def config_view():
    print("Fetching from %s" % CONFIG_FILE)
    if os.path.isfile(CONFIG_FILE):
        with open(CONFIG_FILE) as f:
            print(f.read())
    else:
        print('No such file in %s' % CONFIG_FILE)


def wf_schedule():
    # wsctl wf schedule workflow.yaml "*/30 * * * *"
    
    wf_path = sys.argv[3]
    sche    = sys.argv[4]

    wf = render_wf(wf_path)
    wf_body = yaml.safe_load(wf)
    wf_spec = yaml.dump(wf_body['spec'], default_flow_style=False)
    template = Environment(loader=BaseLoader).from_string(CRON_WF_TEMPLATE)
    rendered = template.render(workflow=wf_spec, schedule=sche)

    body = yaml.safe_load(rendered)
    print(request_object('cronworkflows', body))
 

def app_deploy():
    wf_path = sys.argv[3]
    abs_wf_path = os.path.abspath(wf_path)
    abs_wf_dir = os.path.dirname(abs_wf_path)
    with open(abs_wf_path) as f:
        conf = yaml.safe_load(f)

    username = os.environ['JUPYTERHUB_USER']
    endpoint = conf.get('endpoint', "%s.app.lgebigdata.com" % username)
    command = conf['command'].split(' ')
    port = conf['port']

    
    escaped_name = get_escaped_user(username)
    name = escaped_name
    namespace = "notebook"
    userimage = "cart.lge.com/lgebigdata/single-user:ssh"

    spec = {}
    spec['username'] = username
    spec['name'] = name
    spec['workingDir'] = abs_wf_dir
    spec['namespace'] = namespace
    spec['endpoint'] = endpoint
    spec['port'] = port
    spec['userimage'] = userimage
    spec['command'] = command
    spec['escaped_name'] = escaped_name

    template = Environment(loader=BaseLoader).from_string(DEPLOY_TEMPLATE)
    deploy, svc, ingress = template.render(**spec).split("---")
    deploy = yaml.safe_load(deploy)
    svc = yaml.safe_load(svc)
    ingress = yaml.safe_load(ingress)

    config.load_incluster_config()

    api_instance = client.AppsV1Api()
    try:
        response = api_instance.create_namespaced_deployment(namespace, deploy)
    except kubernetes.client.rest.ApiException as e:
        if e.reason == "Conflict":
            response = api_instance.replace_namespaced_deployment(deploy['metadata']['name'], namespace, deploy)
    deploy_name = response.metadata.name

    api_instance = client.CoreV1Api()
    try:
        response = api_instance.create_namespaced_service(namespace, svc)
    except kubernetes.client.rest.ApiException as e:
        pass

    api_instance = client.ExtensionsV1beta1Api()
    try:
        response = api_instance.create_namespaced_ingress(namespace, ingress)    
    except kubernetes.client.rest.ApiException as e:
        pass

    print('> Your App Name: ', deploy_name)
    print('> Your Endpoint: ', endpoint)


def app_shutdown():
    config.load_incluster_config()
    username = os.environ['JUPYTERHUB_USER']
    namespace = "notebook"
    escaped_name = get_escaped_user(username)
    name = "deploy-%s" % escaped_name

    api_instance = client.AppsV1Api()
    try:
        response = api_instance.delete_namespaced_deployment(name, namespace)
    except kubernetes.client.rest.ApiException as e:
        pass

    api_instance = client.CoreV1Api()
    try:
        response = api_instance.delete_namespaced_service(name, namespace)
    except kubernetes.client.rest.ApiException as e:
        pass

    api_instance = client.ExtensionsV1beta1Api()
    try:
        response = api_instance.delete_namespaced_ingress(name, namespace)
    except kubernetes.client.rest.ApiException as e:
        pass


def _get_items(label_selector, namespace, api_instance=None):
    if api_instance is None:
        config.load_incluster_config()
        api_instance = client.CoreV1Api()
    api_response = api_instance.list_namespaced_pod(namespace, label_selector=label_selector)
    for item in api_response.items:
        yield item

def app_refresh():
    username = os.environ['JUPYTERHUB_USER']
    namespace = "notebook"
    label_selector = 'lgebigdata.com/username=%s' % username
    config.load_incluster_config()
    api_instance = client.CoreV1Api()

    for item in _get_items(label_selector, namespace):
        api_instance.delete_namespaced_pod(item.metadata.name, namespace)


def app_status():
    username = os.environ['JUPYTERHUB_USER']
    namespace = "notebook"
    label_selector = 'lgebigdata.com/username=%s' % username

    for item in _get_items(label_selector, namespace):
        print(item.metadata.name, item.status.phase)


def app_logs():
    username = os.environ['JUPYTERHUB_USER']
    namespace = "notebook"
    label_selector = 'lgebigdata.com/username=%s' % username

    for item in _get_items(label_selector, namespace):
        if item.status.phase == "Running":
            name =  item.metadata.name
            os.system('kubectl logs -f -nnotebook %s' % name)


def _load_config():
    if os.path.isfile(CONFIG_FILE):
        defaults = {}
        with open(CONFIG_FILE) as f:
            config_file = yaml.safe_load(f)
            for k, v in config_file.items():
                defaults[k] = v

    return defaults


def data_init():
    bucket = os.environ['JUPYTERHUB_USER']
    client = boto3.client(service_name='s3', \
        region_name=region_name, \
        endpoint_url=dm_endpoint, \
        aws_access_key_id=access_key, \
        aws_secret_access_key=secret_key, \
        config=Config(signature_version='s3v4'))
    try:
        client.create_bucket(Bucket=bucket)
    except Exception as e:
        print(e)

def data_upload():
    file_path = sys.argv[3]
    object_name = os.path.basename(file_path)
    if len(sys.argv) > 4:
        object_name = sys.argv[4]
    default_config = _load_config()

    bucket = os.environ['JUPYTERHUB_USER']
    dm_endpoint = default_config.get('datamart_endpoint', "")
    access_key = default_config.get('access_key', "")
    secret_key = default_config.get('secret_key', "")
    region_name = default_config.get('region_name', "")

    client = boto3.client(service_name='s3', \
        region_name=region_name, \
        endpoint_url=dm_endpoint, \
        aws_access_key_id=access_key, \
        aws_secret_access_key=secret_key, \
        config=Config(signature_version='s3v4'))


    if os.path.isfile(file_path):
        try:
            response = client.upload_file(file_path, bucket, object_name)
        except Exception as e:
            print(e)
    elif os.path.isdir(file_path):
        local_directory = file_path
        destination = object_name
        for root, dirs, files in os.walk(local_directory):
            for filename in files:
                local_path = os.path.join(root, filename)
                relative_path = os.path.relpath(local_path, local_directory)
                s3_path = os.path.join(destination, relative_path)
                try:
                    client.upload_file(local_path, bucket, s3_path)
                except Exception as e:
                    print(e)


# if __name__ == "__main__":
#     component = sys.argv[1]
#     func = sys.argv[2]
#     eval("%s_%s" % (component, func))()
