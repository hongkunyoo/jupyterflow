import os

import click
from click import ClickException

from . import workflow
from . import printer
from . import utils
from .runtime import runtime


@click.group()
def main():
    pass


@main.command()
@click.option('-f', '--filename', help='Path for workflow.yaml file. ex) \'jupyterflow run -f workflow.yaml\'', default=None)
@click.option('-c', '--command', help="Command to run workflow. ex) \'jupyterflow run -c \"python main.py >> python next.py\"\'", default=None)
@click.option('-o', '--output', help='Output format. default is \'-o jsonpath="metadata.name"\'', default='jsonpath="metadata.name"')
@click.option('--dry-run', help='Only prints Argo Workflow object, without accually sending it', default=False, is_flag=True)
def run(filename, command, output, dry_run):

    if command is not None:
        user_workflow = workflow.load_from_command(command)
        workingDir = os.getcwd()
    elif filename is not None:
        if not os.path.isfile(filename):
            raise ClickException("No such file %s" % filename)
        user_workflow = workflow.load_from_file(filename)
        workingDir = os.path.dirname(os.path.abspath(filename))
    else:
        raise ClickException("Provide either `-f` or `-c` option")

    runtime['workingDir'] = workingDir
    namespace = runtime['namespace']
    conf = utils.load_config()
    wf = workflow.build(user_workflow, namespace, runtime, conf)
    
    if dry_run:
        response = wf
        output = 'yaml'
    else:
        response = workflow.run(wf)

    printer.format(response, output)


@main.command()
@click.argument('name')
@click.option('-n', '--namespace', help='namespace', default=None)
def delete(name, namespace):
    if namespace is None:
        namespace = runtime['namespace']
    response = workflow.delete(name, namespace)
    printer.format(response, 'text')


@main.command()
@click.option('--generate-config', help='Generate config file', default=False, is_flag=True)
def config(generate_config):
    if generate_config:
        utils.create_config()
        printer.format('jupyterflow config file created', 'text')
    else:
        conf = utils.load_config()
        printer.format(conf, 'yaml')
