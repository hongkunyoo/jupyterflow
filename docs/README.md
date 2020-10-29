# JupyterFlow Documentation

Run your workflow on JupyterHub!

## What is JupyterFlow?

Run [Argo Workflow](https://argoproj.github.io/argo) pipeline on [JupyterHub](https://jupyter.org/hub).

- No Kubernetes knowledge (YAML) needed to run.
- No container build & push or deploy.
- Just simply run your workflow with single command `jupyterflow`.

`jupyterflow` is a command that helps user utilize Argo Workflow engine without making any YAML files or building containers on JupyterHub.

The following `jupyterflow` command will make sequence workflow.

```bash
jupyterflow run -c "python hello.py >> python world.py"
```

![](images/intro.png)

To make parallel workflow, write your own [`workflow.yaml` file](https://hongkunyoo.github.io/jupyterflow/configuration/)

## Problem to solve

- I wanted to train multiple ML models efficiently.
- Using Kubernetes was a good idea, since
    - it is easy to make distributed jobs.
    - it is easy to schedule ML jobs on multiple training server.
    - it has native resource management mechanism.
    - it has good monitoring system.
- But there were some drawbacks.
    - I needed to re-build & re-push image everytime I updated my model. This was painful.
    - People who are not familiar with k8s had a hard time using this method.

`jupyterflow` aims to solve this problem.

## Getting Started

To set up `jupyterflow` and start running your first workflow, follow the [Getting Started](get-started.md) guide.

## How does it work

To learn how it works, go to [How it works](how-it-works.md) guide.

## Examples

For examples how to use, please see [Examples](examples/README.md) page.

## Workflow file Configuration

To find out more configuration, take a look at [Configuration](configuration.md) page.
