# How it works

![](images/architecture.png)

JupyterFlow has a strict constraint that it only works on Kubernetes(`JupyterHub for Kubernetes` or `Kubeflow`).
This is because JupyterFlow collects user's execution environment information from `Pod` metadata and the source code from Kubernetes storage volume. JupyterFlow uses these information to construct a new Kubernetes manifest(Argo `Workflow`) for ML job without any containerization on behalf of you.

`jupyterflow` collects following metadata from jupyter notebook `Pod`.

- Container image
- Environment variables
- Home directory volume (home `PersistentVolumeClaim`)
- Extra volume mount points
- Resource management (`requests`, `limits`)
- `NodeSelector` label
- UID, GUID
- Etc.

Following pseudo code might help you understand how `jupyterflow` works.

- JupyterFlow main logic

```python
jupyterflow run -c "python hello.py >> python world.py"
# ...
# inside jupyterflow
# ...

# get user workflow(DAG) information.
user_workflow_data = get_user_workflow(user_input)

# collect metadata of current environment(jupyter notebook Pod).
nb_pod_spec = get_current_pod_spec_from_k8s(jupyter_notebook_pod_name, service_account)

# build Workflow manifest based on meta data and user workflow information.
argo_workflow_spec = build_workflow(nb_pod_spec, user_workflow_data)

# request new Argo workflow.
response = request_for_new_workflow_to_k8s(K8S_MASTER, argo_workflow_spec, service_account)
```

For more details, please [read this article.](https://coffeewhale.com/kubernetes/mlops/2021/03/02/mlops-jupyterflow-en)
