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



# def wf_run():
#     wf_path = sys.argv[3]
#     rendered = render_wf(wf_path)
#     body = yaml.safe_load(rendered)
#     print(request_object('workflows', body))
    

# def render_wf(wf_path):
#     abs_wf_path = os.path.abspath(wf_path)
#     abs_wf_dir = os.path.dirname(abs_wf_path)

#     with open(abs_wf_path) as f:
#         conf = yaml.safe_load(f)

#     jobs = conf['jobs']
#     d = dict(zip(range(1,len(jobs)+1), jobs))
#     dags = conf.get('dags', [])
#     resolve_tree = {}

#     for k in d.keys():
#         resolve_tree['job-' + str(k)] = []

#     for dag in dags:
#         pre, pro = dag.replace(' ', '').split('>>')
#         resolve_tree['job-' + pro].append('job-' + pre)

#     user_name = os.environ['JUPYTERHUB_USER']
#     escaped_name = get_escaped_user(user_name)
    
#     wf_jobs = []
#     for i, j in enumerate(jobs):
#         job = {}
#         job['name'] = 'job-' + str(i+1)
#         cmds = j.split(' ')
#         job['command'] = cmds
#         try:
#             job['dependencies'] = resolve_tree['job-' + str(i+1)]
#         except:
#             job['dependencies'] = []
#         wf_jobs.append(job)

#     defaults = {
#         "LIMITS_CPU": "8",
#         "LIMITS_MEM": "20Gi"
#     }
#     if os.path.isfile(CONFIG_FILE):
#         with open(CONFIG_FILE) as f:
#             config_file = yaml.safe_load(f)
#             for k, v in config_file.items():
#                 defaults[k] = v

#     cpu = get_value('LIMITS_CPU', defaults)
#     mem = get_value('LIMITS_MEM', defaults)
#     runAsUser = os.getuid() 

#     wf = {}
#     wf['jobs'] = wf_jobs
#     wf['escaped_name'] = escaped_name
#     wf['username'] = user_name
#     wf['workingDir'] = abs_wf_dir
#     wf['PATH'] = os.environ['PATH']
#     wf['runAsUser'] = runAsUser
#     wf['limits'] = {
#       "cpu": cpu,
#       "memory": mem
#     }

#     template = Environment(loader=BaseLoader).from_string(WF_TEMPLATE)
#     return template.render(**wf)
