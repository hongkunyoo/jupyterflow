# JupyterFlow

Run your workflow on JupyterHub!

## What is JupyterFlow?

![](https://raw.githubusercontent.com/hongkunyoo/jupyterflow/main/docs/images/architecture.png)

Run [Argo Workflow](https://argoproj.github.io/argo) on [JupyterHub](https://jupyter.org/hub) with single command.

- **No Kubernetes knowledge (YAML) needed to run.**
- **No container image build & push or deploy.**
- Just simply run your workflow with single command `jupyterflow`.

`jupyterflow` is a single command that helps user utilize Argo workflow engine without making any YAML files or building containers on JupyterHub. The following `jupyterflow` command will make sequence workflow for you. That's it!

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

JupyterFlow aims to solve this problem. Run your workflow  on JupyterHub with single command without Kubernetes & container troublesome task.

## Limitation

JupyterFlow only works on JupyterHub deployed on Kubernetes.

- [JupyterHub for Kubernetes](https://zero-to-jupyterhub.readthedocs.io/en/latest)
- [Kubeflow](https://www.kubeflow.org)

Therefore, although using JupyterFlow does not require Kubernetes knowledge, setting up JupyterFlow requires Kubernetes understandings(YAML, `helm`, `Service`). If you're familiar with Kubernetes, it will not be too hard.

## Getting Started

To set up `jupyterflow` and start running your first workflow, follow the [Getting Started](https://hongkunyoo.github.io/jupyterflow/get-started) guide.

## How does it work

To learn how it works, go to [How it works](https://hongkunyoo.github.io/jupyterflow/how-it-works) guide.

## Examples

For examples how to use, please see [Examples](https://hongkunyoo.github.io/jupyterflow/examples) page.

## Configuration

To find out more configuration, take a look at [Configuration](https://hongkunyoo.github.io/jupyterflow/configuration) page.

## CLI Reference

For more detail usage of `jupyterflow` command line interface, find out more at [CLI Reference](https://hongkunyoo.github.io/jupyterflow/cli-ref) page.
