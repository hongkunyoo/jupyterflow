# Configuration

## `workflow.yaml` Configuration

`workflow.yaml` is a description about how to run your jobs. You can asign a dependencies between jobs. The name and the path does not matter as long as you pass to `run -f` option argument.

### Minimum description

Each job will run in parallel.

```yaml
# workflow.yaml
jobs:
- echo hello
- echo world
- echo again
```

```bash
jupyterflow run -f workflow.yaml
```

### Full description

Job dependencies will be resolved based on `dags` information.

```yaml
# workflow.yaml
version: 1

name: workflow-name

jobs:
- echo hello
- echo world
- echo again

cmd_mode: exec   # shell

dags:
- 1 >> 2
- 1 >> 3

schedule: '*/2 * * * *'
```

| Property  | Description                                                           | Optional  | Default                           |
|-----------|-----------------------------------------------------------------------|-----------|-----------------------------------|
|`version`  | Version of `workflow.yaml` file format.                               | Optional  | 1                                 |
|`name`     | Name of the workflow. This name is used for Argo `Workflow` name.     | Optional  | `{username}` of JupyterHub        |
|`jobs`     | Jobs to run. Any kinds of command works.                              | Required  |                                   |
|`cmd_mode` | Choose to run image in `exec` or `shell` form.                        | Optional  | `exec`                            |
|`dags`     | Job dependencies. Index starts at 1. (`$PREVIOUS_JOB` >> `$NEXT_JOB`) | Optional  | All jobs parallel (No dependency) |
|`schedule` | When to execute this workflow. Follows cron format.                   | Optional  | Run immediately                   |


##### `exec` vs `shell`

- In `exec` mode, your command will be executed as `["echo", "hello", "world"]`.
- In `shell` mode, your command will be executed as `["/bin/sh", "-c", "echo hello world"]`.

In exec mode, the command is more straightforward since there is no shell process involved and it is being called directly. In shell mode, you can fully utilize the power of shell, such as shell script commands. (`>>`, `&&` and so on.)


## Jupyterflow Configuration

You can override Argo `Workflow` spec by configuring `$HOME/.jupyterflow.yaml` file. This file has to be specifically named `.jupyterflow.yaml` in `$HOME` directory.

The following command will create `.jupyterflow.yaml` on `$HOME` directory.

```bash
jupyterflow config --generate-config
# jupyterflow config file created.

cat $HOME/.jupyterflow.yaml
# spec:
#   image: jupyter/datascience-notebook:latest
#   imagePullPolicy: Always
#   imagePullSecrets:
#   -  name: "default"
#   env:
#   - name: "CUSTOM_KEY"
#     value: "CUSTOM_VAL"
#   resources:
#     requests:
#       cpu: 500m
#       memory: 500Mi
#     limits:
#       cpu: 500m
#       memory: 500Mi
#   nodeSelector: {}
#   runAsUser: 1000
#   runAsGroup: 100
#   serviceAccountName: default
#   volumes:
#   - name: nas001
#     persistentVolumeClaim:
#       claimName: nas001
#   volumeMounts:
#   - name: nas001
#     mountPath: /nas001
```

Umcomment the property you want to override. For example, if you want your workflow jobs to run on GPU nodes, configure `spec.resources` or `spec.nodeSelector` property.

```bash
spec:
#   image: jupyter/datascience-notebook:latest
#   imagePullPolicy: Always
#   imagePullSecrets:
#   -  name: "default"
#   env:
#   - name: "CUSTOM_KEY"
#     value: "CUSTOM_VAL"
  resources:
    requests:
      cpu: 500m
      memory: 500Mi
      nvidia.com/gpu: 1
    limits:
      cpu: 500m
      memory: 500Mi
      nvidia.com/gpu: 1
  nodeSelector:
    accelerator: nvidia-node
#   runAsUser: 1000
#   runAsGroup: 100
#   serviceAccountName: default
#   volumes:
#   - name: nas001
#     persistentVolumeClaim:
#       claimName: nas001
#   volumeMounts:
#   - name: nas001
#     mountPath: /nas001
```

Run `jupyterflow` and check out the result whether your workflow has run on GPU nodes.

```bash
jupyterflow run -f workflow.yaml
```
