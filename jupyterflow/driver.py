import os
import click
import yaml
import jinja2

from click import ClickException

import pwd
import pkgutil

from . import config_loader
from . import utils
from . import render
from . import k8s_client


@click.group()
def main():
    pass


@main.command()
@click.option('--generate-config/--no', help='Generate config', default=False)
def config(generate_config):
    data = pkgutil.get_data(__name__, "templates/jupyterflow.yaml")
    home = os.environ['HOME']
    path = os.path.join(home, '.jupyterflow.yaml')
    with open(path, 'wt') as f:
        f.write(data.decode('utf-8'))



@main.command()
@click.option('-f', help='Path for workflow.yaml file', default=None)
@click.option('-c', help="Command to run workflow ex) jupyterflow create -c 'python main.py >> python next.py'", default=None)
@click.option('--dry-run/--', help='Only print Argo Workflow object, without accually sending it', default=False)
def run(f, c, dry_run):
    if f is None and c is None:
        raise ClickException("Provide either `-f` or `-c` option")

    if c is not None:
        jobs = list(map(lambda s: s.strip(), c.split('>>')))
        dags = []
        for i, j in enumerate(jobs):
            if i == len(jobs) -1:
                break
            dags.append(">>".join([str(i+1), str(i+2)]))
        user_workflow = {}
        user_workflow['jobs'] = jobs
        user_workflow['dags'] = dags
        workingDir = os.getcwd()
    else:
        if not os.path.isfile(f):
            raise ClickException("No such file %s" % f)

        with open(f) as ff:
            user_workflow = yaml.safe_load(ff)
        workingDir = os.path.dirname(os.path.abspath(f))
    
    # load config
    config = config_loader.load_config()

    wf = build_workflow(user_workflow, config, workingDir)
    # os.system("cat << EOF | kubectl create -f -\n%s\nEOF" % wf)
    if dry_run:
        print(wf)
    else:  
        response = _run_workflow(wf)
        print(response['metadata']['name'])



def build_workflow(wf, config, workingDir):
    jobs = wf['jobs']
    d = dict(zip(range(1,len(jobs)+1), jobs))
    dags = wf.get('dags', [])
    resolve_tree = {}

    for k in d.keys():
        resolve_tree['job-' + str(k)] = []

    for dag in dags:
        pre, pro = dag.replace(' ', '').split('>>')
        resolve_tree['job-' + pro].append('job-' + pre)

    wf_jobs = []
    for i, j in enumerate(jobs):
        job = {}
        job['name'] = 'job-' + str(i+1)
        cmds = j.split(' ')
        job['command'] = cmds
        if 'job-' + str(i+1) in resolve_tree:
            job['dependencies'] = resolve_tree['job-' + str(i+1)]
        else:
            job['dependencies'] = []
        wf_jobs.append(job)


    runtime = get_runtime_informations()
    runtime['workingDir'] = workingDir


    workflow = {}
    workflow['jobs'] = wf_jobs
    # workflow['name'] = 'plz-'

    singleuser = config.get('singleuser', {})
    
    escaped_username = utils.get_escaped_user(os.environ['JUPYTERHUB_USER'])
    NB_USER = os.environ['NB_USER']


    # override runtime by configs
    if 'name' in wf:
        workflow['name'] = wf['name']
    
    if 'image' in singleuser:
        if 'name' in singleuser['image']:
            runtime['image'] = singleuser['image']['name']
    if 'runAsUser' in singleuser:
        runtime['runAsUser'] = singleuser['runAsUser']
    if 'runAsGroup' in singleuser:
        runtime['runAsGroup'] = singleuser['runAsGroup']
    if 'workingDir' in singleuser:
        runtime['workingDir'] = singleuser['workingDir']

    template = render.get_template('workflow.yaml')
    rendered = template.render(workflow=workflow, \
                                singleuser=singleuser, \
                                runtime=runtime, \
                            ).format(username=escaped_username, nb_user=NB_USER)
    return rendered


def get_runtime_informations():
    NB_USER = os.environ['NB_USER']
    JUPYTERHUB_USER = os.environ['JUPYTERHUB_USER']
    PATH = os.environ['PATH']
    JUPYTER_IMAGE_SPEC = os.environ['JUPYTER_IMAGE_SPEC']
    HOME = os.environ['HOME']
    
    nb_user_pwd = pwd.getpwnam(NB_USER)
    runAsUser = nb_user_pwd.pw_uid
    runAsGroup = nb_user_pwd.pw_gid

    runtime = {}
    runtime['env'] = {}
    runtime['env']['JUPYTERHUB_USER'] = JUPYTERHUB_USER
    runtime['env']['PATH'] = PATH
    runtime['env']['NB_USER'] = NB_USER
    runtime['env']['HOME'] = HOME

    runtime['image'] = JUPYTER_IMAGE_SPEC
    runtime['runAsUser'] = runAsUser
    runtime['runAsGroup'] = runAsGroup

    return runtime


def _run_workflow(workflow):
    with open('/var/run/secrets/kubernetes.io/serviceaccount/namespace') as f:
        ns = f.read()
    
    yaml_body = yaml.safe_load(workflow)
    return k8s_client.create_object('workflows', yaml_body, ns)