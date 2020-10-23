# jupytermoon

ML pipeline on JupyterHub

## What is jupytermoon

Run [Argo Workflow](https://argoproj.github.io/argo) pipeline on JupyterHub with single command!

#### For Users
- No Kubernetes knowledge (YAML) need.
- No container build & push or deploy.
- Just run pipeline with single command `jupytermoon`!

#### For MLOps Engineer

Although, You need to know Kubernetes to set its up, But it is...

- Easy to deploy ML jobs.
- 



## Get Started

### Prerequisite




### Install jupytermoon



### Run Pipeline

```bash
jupytermoon run python train.py
```


```yaml
jobs:
- python input.py 
- python train.py

dags:
- 1 >> 2
```


```bash
jupytermoon run -f workflow.yaml
```

### Go to Argo Workflow Web

![]()



## How does it work?