# JupyterFlow

Run your workflow on JupyterHub!

## What is JupyterFlow?

Run [Argo Workflow](https://argoproj.github.io/argo) on [JupyterHub](https://jupyter.org/hub) with single command.

- No Kubernetes knowledge (YAML) needed to run.
- No container image build & push or deploy.
- Just simply run your workflow with single command `jupyterflow`.

`jupyterflow` is a command that helps user utilize Argo Workflow engine without making any YAML files or building containers on JupyterHub.

> This project only works on [JupyterHub for Kubernetes](https://zero-to-jupyterhub.readthedocs.io/en/latest).

The following `jupyterflow` command will make sequence workflow. That's it!

```bash
jupyterflow run -c "python hello.py >> python world.py"
```

![](https://raw.githubusercontent.com/hongkunyoo/jupyterflow/main/docs/images/intro.png)

To make parallel workflow, write your own [`workflow.yaml`](https://hongkunyoo.github.io/jupyterflow/configuration/) file.

![](https://raw.githubusercontent.com/hongkunyoo/jupyterflow/main/docs/images/dag.png)

## Problem to solve

- I wanted to train multiple ML models efficiently.
- Using Kubernetes was a good idea, since
    - it is easy to make distributed jobs.
    - it is easy to schedule ML jobs on multiple training server.
    - it has native resource management mechanism.
    - it has good monitoring system.
- But there were some drawbacks.
    - I needed to re-build & re-push image everytime I updated my model. This was painful.
    - People who were not familiar with k8s had a hard time using this method.

`jupyterflow` aims to solve this problem. Run your workflow with single command without Kubernetes & container works on JupyterHub.

## Getting Started

To set up `jupyterflow` and start running your first workflow, follow the [Getting Started](https://hongkunyoo.github.io/jupyterflow/get-started) guide.

## How does it work

To learn how it works, go to [How it works](https://hongkunyoo.github.io/jupyterflow/how-it-works) guide.

## Examples

For examples how to use, please see [Examples](https://hongkunyoo.github.io/jupyterflow/examples) page.

## Workflow file Configuration

To find out more configuration, take a look at [Configuration](https://hongkunyoo.github.io/jupyterflow/configuration) page.
