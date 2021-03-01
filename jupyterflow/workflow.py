import yaml

from . import k8s_client
from . import render
from .runtime import runtime


def load_from_command(c):
    jobs = list(map(lambda s: s.strip(), c.split('>>')))
    dags = []
    for i, j in enumerate(jobs):
        if i == len(jobs) -1:
            break
        dags.append(">>".join([str(i+1), str(i+2)]))
    user_workflow = {}
    user_workflow['jobs'] = jobs
    user_workflow['dags'] = dags
    return user_workflow


def load_from_file(f):
    with open(f) as yaml_file:
        return yaml.safe_load(yaml_file)


def build(wf, namespace, runtime, config):
    hostname = runtime['HOSTNAME']
    #########################
    # resolve tree
    #########################

    workflow = {}
    workflow['name'] = wf.get('name', hostname)
    workflow['jobs'] = []

    cmd_mode = wf.get('cmd_mode', 'exec')

    jobs = wf['jobs']
    d = dict(zip(range(1,len(jobs)+1), jobs))
    dags = wf.get('dags', [])
    resolve_tree = {}

    for k in d.keys():
        resolve_tree['job-' + str(k)] = []

    for dag in dags:
        pre, pro = dag.replace(' ', '').split('>>')
        resolve_tree['job-' + pro].append('job-' + pre)

    for i, j in enumerate(jobs):
        job = {}
        job['name'] = 'job-' + str(i+1)
        if cmd_mode == 'exec':
            cmds = j.split(' ')
        else:
            cmds = ["/bin/sh", "-c", j]
        job['command'] = cmds
        if 'job-' + str(i+1) in resolve_tree:
            job['dependencies'] = resolve_tree['job-' + str(i+1)]
        else:
            job['dependencies'] = []
        workflow['jobs'].append(job)
    
    pod = k8s_client.get_notebook_pod(hostname, namespace)
    workflow['spec'] = build_wf_spec_from(pod)
    override_wf(workflow, config)

    ###########################
    # render workflow
    ###########################
    rendered_wf = render.workflow(
            workflow=workflow, \
            runtime=runtime
    )
    workflow_yaml = yaml.safe_load(rendered_wf)

    if 'schedule' in wf:
        rendered_wf = render.cronworkflow(workflow_yaml, wf['schedule'])
        workflow_yaml = yaml.safe_load(rendered_wf)
    return workflow_yaml
        


def run(wf, namespace):
    return k8s_client.create_object(wf, namespace)
    

def build_wf_spec_from(pod):
    spec = {}

    spec['serviceAccountName'] = pod['spec'].get('serviceAccountName', None)
    spec['image'] = pod['spec']['containers'][0].get('image', 'jupyter/datascience-notebook:latest')
    spec['imagePullPolicy'] = pod['spec']['containers'][0].get('imagePullPolicy', 'Always')
    spec['imagePullSecrets'] = pod['spec'].get('imagePullSecrets', None)
    spec['runAsUser'] = runtime['runAsUser']
    spec['runAsGroup'] = runtime['runAsGroup']
    spec['env'] = pod['spec']['containers'][0].get('env', [])
    spec['env_from'] = pod['spec']['containers'][0].get('env_from', None)
    spec['resources'] = pod['spec']['containers'][0].get('resources', None)
    spec['volumeMounts'] = pod['spec']['containers'][0].get('volumeMounts', None)
    spec['volumes'] = pod['spec'].get('volumes', None)
    spec['nodeSelector'] = pod['spec'].get('nodeSelector', None)

    return spec


def override_wf(workflow, config):
    spec = config.get('spec', {})
    wf_spec = workflow['spec']
    
    wf_env = wf_spec['env']
    wf_vol = wf_spec['volumes']
    wf_volMount = wf_spec['volumeMounts']

    del wf_spec['env']
    del wf_spec['volumes']
    del wf_spec['volumeMounts']

    wf_spec.update(spec)

    if 'env' not in wf_spec:
        wf_spec['env'] = []
    wf_spec['env'].extend(wf_env)

    if 'volumes' not in wf_spec:
        wf_spec['volumes'] = []
    wf_spec['volumes'].extend(wf_vol)

    if 'volumeMounts' not in wf_spec:
        wf_spec['volumeMounts'] = []
    wf_spec['volumeMounts'].extend(wf_volMount)


def delete(name, namespace):
    return k8s_client.delete_object(name, 'argoproj.io/v1alpha1', 'workflows', namespace)
