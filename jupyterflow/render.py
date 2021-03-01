from jinja2 import Environment, BaseLoader, PackageLoader, Template


def workflow(workflow, runtime):

    template = get_template('workflow.yaml')
    return template.render(workflow=workflow, \
                            runtime=runtime
                        )


def cronworkflow(workflow_yaml, schedule):
    template = get_template('cronworkflow.yaml')
    return template.render(name=workflow_yaml['metadata']['generateName'], \
                            workflow=workflow_yaml['spec'], \
                            schedule=schedule)


def get_template(name):
    env = Environment(loader=PackageLoader('jupyterflow', 'templates'), extensions=['jinja2_ansible_filters.AnsibleCoreFiltersExtension'])
    return env.get_template(name)
