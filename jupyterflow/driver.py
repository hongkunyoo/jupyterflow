import os
import click
import yaml
import jinja2
from . import config_loader

@click.group()
def main():
    pass

@main.command()
@click.argument('command', nargs=-1)
def run(command):
    print(command)
    

@main.command()
@click.option('-f', help='workflow.yaml', default=None)
@click.option('-c', help='python train.py', default=None)
def create(f, c):
    if f is None and c is None:
        raise Exception()

    if not os.path.isfile(f):
        raise Exception("No such file %s" % f)

    with open(f) as f:
        user_workflow = yaml.safe_load(f)

    default_config = config_loader.load_config()
    wf = build_workflow(user_workflow, default_config)
    _run_workflow(wf)



def build_workflow(wf, config):
    jobs = wf['jobs']
    d = dict(zip(range(1,len(jobs)+1), jobs))
    dags = wf.get('dags', [])
    resolve_tree = {}

    for k in d.keys():
        resolve_tree['job-' + str(k)] = []

    for dag in dags:
        pre, pro = dag.replace(' ', '').split('>>')
        resolve_tree['job-' + pro].append('job-' + pre)

    username = os.environ['JUPYTERHUB_USER']
    import utils
    escaped_username = utils.get_escaped_user(username)
    
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

    runAsUser = os.getuid()

    wf = {}
    wf['jobs'] = wf_jobs
    wf['name'] = 'plz'

    singleuser = config['singleuser']
    username = 'hongkun.yoo'
    workingDir = 'MYWORKDIR'
    PATH = os.environ['PATH']
    
    templateLoader = jinja2.FileSystemLoader(searchpath="templates")
    templateEnv = jinja2.Environment(loader=templateLoader)
    TEMPLATE_FILE = "workflow.yaml"
    template = templateEnv.get_template(TEMPLATE_FILE)
    # template = Environment(loader=BaseLoader).from_string(WF_TEMPLATE)
    print(template.render(**wf))




def _run_workflow(workflow):
    wf = config_loader.load_config(workflow)
    rendered = render.render(wf)
    yaml_body = yaml.safe_load(rendered)
    response = k8s_client.create_object('workflows', yaml_body)
    print(response)