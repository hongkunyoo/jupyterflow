# JupyterFlow

Run your workflow on JupyterHub!

## What is JupyterFlow?

![](https://raw.githubusercontent.com/hongkunyoo/jupyterflow/main/docs/images/side.png)

Run your ML job right away on Kubernetes with `jupyterflow`.

- **No container image build & push**
- **No Kubernetes manifest (YAML)**
- Just simply run your ML code with single command `jupyterflow`.

`jupyterflow` is a ML tool for Data Scientist to help run ML code on Kubernetes without any **containerization process**.

1. Launch your jupyter notebook
2. Write your ML code
3. Run your ML model on Kubernetes through `jupyterflow`

```bash
# Write your code.
echo "print('hello')" > hello.py
echo "print('world')" > world.py

# Install jupyterflow.
pip install jupyterflow

# in jupyterflow `>>` directive expresses container dependencies similar to Airflow.
jupyterflow run -c "python hello.py >> python world.py"
```

![](https://raw.githubusercontent.com/hongkunyoo/jupyterflow/main/docs/images/intro.png)

<!-- To make parallel workflow, write your own [`workflow.yaml`](https://hongkunyoo.github.io/jupyterflow/configuration/) file.

![](https://raw.githubusercontent.com/hongkunyoo/jupyterflow/main/docs/images/dag.png) -->

## Motivation

- I wanted to run ML models across multiple training server efficiently.
- Using Kubernetes was a good idea, since
    - it is easy to run jobs distributedly.
    - it is easy to schedule jobs on multiple training server.
    - it has native resource management mechanism.
    - it has good monitoring system.
- But there were some drawbacks.
    - I needed to re-build & re-push image everytime I updated my model. This was painful.
    - People who were not familiar with k8s had a hard time writing K8s manifest file.

JupyterFlow aims to solve this problem. Run your workflow on JupyterHub with single command without containerization & k8s troublesome task. For more details, [read this article.](https://coffeewhale.com/kubernetes/mlops/2021/03/02/mlops-jupyterflow-en)

## Limitation

JupyterFlow only works on following platforms:

- [JupyterHub for Kubernetes](https://zero-to-jupyterhub.readthedocs.io/en/latest)
- [Kubeflow](https://www.kubeflow.org)

Therefore, although using JupyterFlow does not require Kubernetes manifest, setting up JupyterFlow requires Kubernetes understandings(YAML, `helm`, `Service`). If you're familiar with Kubernetes, it will not be too hard.

If you want to know why there is such limitation, refer to [How it works](https://hongkunyoo.github.io/jupyterflow/how-it-works) guide.

## Getting Started

To set up `jupyterflow` and start running your first workflow, follow the [Getting Started](https://hongkunyoo.github.io/jupyterflow/get-started) guide.

## How it works

To learn how it works, go to [How it works](https://hongkunyoo.github.io/jupyterflow/how-it-works) guide.

## Examples

For examples how to use, please see [Examples](https://hongkunyoo.github.io/jupyterflow/examples) page.

## Configuration

To find out more configuration, take a look at [Configuration](https://hongkunyoo.github.io/jupyterflow/configuration) page.

## CLI Reference

For more detail usage of `jupyterflow` command line interface, find out more at [CLI Reference](https://hongkunyoo.github.io/jupyterflow/cli-ref) page.
