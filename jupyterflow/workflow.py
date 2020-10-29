import yaml

from . import k8s_client
from . import render


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


def build(wf, namespace, runtime):
    escaped_username = runtime['escaped_username']
    #########################
    # resolve tree
    #########################
    workflow = {}
    workflow['name'] = wf.get('name', escaped_username)
    workflow['jobs'] = []

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
        cmds = j.split(' ')
        job['command'] = cmds
        if 'job-' + str(i+1) in resolve_tree:
            job['dependencies'] = resolve_tree['job-' + str(i+1)]
        else:
            job['dependencies'] = []
        workflow['jobs'].append(job)
    
    pod = k8s_client.get_notebook_pod(escaped_username, namespace)

    ###########################
    # render workflow
    ###########################
    rendered_wf = render.workflow(
            workflow=workflow, \
            pod=pod, \
            runtime=runtime, \
            username=escaped_username
    )
    workflow_yaml = yaml.safe_load(rendered_wf)

    if 'schedule' in wf:
        rendered_wf = render.cronworkflow(workflow_yaml, wf['schedule'])
        workflow_yaml = yaml.safe_load(rendered_wf)
    return workflow_yaml
        


def run(wf, namespace):
    response = k8s_client.create_object(wf, namespace)
    return response
    