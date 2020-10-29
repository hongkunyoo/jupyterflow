# How it works

![](images/architecture.png)

`jupyterflow` has a strict constraint that it only works on [JupyterHub for Kubernetes](https://zero-to-jupyterhub.readthedocs.io/en/latest).
Because of this constraint, `jupyterflow` can easily collect current environment information (meta data).
With this information, `jupyterflow` constructs Argo `Workflow` object on behalf of you.

`jupyterflow` uses following metadata from jupyter notebook `Pod`.

- Container image
- Environment variables
- Home directory (home `PersistentVolumeClaim`)
- Extra volume mount points
- Resource management (`requests`, `limits`)
- UID, GUID

Following pseudo code helps you understand how `jupyterflow` works.

```python
# collect meta data of current environment.
pod_spec = get_current_pod_spec_from_k8s(pod_name, service_account)

# build Workflow based on meta data and user workflow information
workflow_spec = build_workflow(pod_spec, user_workflow_file)

# create new workflow
response = request_for_new_workflow_to_k8s(workflow_spec, service_account)
```
