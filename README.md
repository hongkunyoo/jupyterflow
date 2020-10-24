# jupyterflow

Run workflow on JupyterHub

## What is jupyterflow

Run [Argo Workflow](https://argoproj.github.io/argo) pipeline on JupyterHub with single command!

#### For Users
- No Kubernetes knowledge (YAML) need.
- No container build & push or deploy.
- Just run pipeline with single command `jupyterflow`!

#### For MLOps Engineer

Although, You need to know Kubernetes to set its up, But it is...

- Easy to deploy ML jobs.
- 



## Get Started

### Prerequisite




### Install jupyterflow



### Run Workflow

```bash
jupyterflow run python train.py
```

```bash
jupyterflow create -c "python main.py >> python train.py"
```

```bash
jupyterflow create -f workflow.yaml
```


```yaml
jobs:
- python input.py 
- python train.py

dags:
- 1 >> 2
```

### Go to Argo Workflow Web

![]()


## How does it work?