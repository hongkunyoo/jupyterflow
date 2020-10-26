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
jupyterflow create -c "python main.py >> python train.py"
```

```bash
jupyterflow create -f workflow.yaml
```


```yaml
# workflow.yaml
jobs:
- python input.py 
- python train.py

dags:
- 1 >> 2
```

### Go to Argo Workflow Web

![]()


## How does it work?

그럼 넣기





## Configuration

```yaml
# $HOME/.jupyterflow.yaml
workflow:
  name: jupyterflow
singleuser:
  image:
    name: jupyter/datascience-notebook:latest
    pullPolicy: Always
    secret: "default"
  resources:
    requests:
      cpu: 400m
      memory: 400Mi
    limits:
      cpu: 400m
      memory: 400Mi
  env:
    CUSTOM_ENV: "value"
  runAsUser: 1000
  runAsGroup: 100
  fsGroup: 100
  nodeSelector: {}
  serviceAccountName: default
  storage:
    homePvcName: claim-{username}
    homeMountPath: /home/jovyan
    extraVolumes:
    - name: nas001
      persistentVolumeClaim:
        claimName: nas001
    extraVolumeMounts:
    - name: nas001
      mountPath: /nas001
```


### `workflow`

- `name`: jupyterflow

### `singlueuser`


ethod | HTTP request | Description
------------- | ------------- | -------------
[**create_cluster_custom_object**](CustomObjectsApi.md#create_cluster_custom_object) | **POST** /apis/{group}/{version}/{plural} | 
[**create_namespaced_custom_object**](CustomObjectsApi.md#create_namespaced_custom_object) | **POST** /apis/{group}/{version}/namespaces/{namespace}/{plural} | 
[**delete_cluster_custom_object**](CustomObjectsApi.md#delete_cluster_custom_object) | **DELETE** /apis/{group}/{version}/{plural}/{name} | 
[**delete_collection_cluster_custom_object**](CustomObjectsApi.md#delete_collection_cluster_custom_object) | **DELETE** /apis/{group}/{version}/{plural} | 
[**delete_collection_namespaced_custom_object**](CustomObjectsApi.md#delete_collection_namespaced_custom_object) | **DELETE** /apis/{group}/{version}/namespaces/{namespace}/{plural} | 
[**delete_namespaced_custom_object**](CustomObjectsApi.md#delete_namespaced_custom_object) | **DELETE** /apis/{group}/{version}/namespaces/{namespace}/{plural}/{name} | 
[**get_cluster_custom_object**](CustomObjectsApi.md#get_cluster_custom_object) | **GET** /apis/{group}/{version}/{plural}/{name} | 
[**get_cluster_custom_object_scale**](CustomObjectsApi.md#get_cluster_custom_object_scale) | **GET** /apis/{group}/{version}/{plural}/{name}/scale | 
[**get_cluster_custom_object_status**](CustomObjectsApi.md#get_cluster_custom_object_status) | **GET** /apis/{group}/{version}/{plural}/{name}/status | 



- `image.name`: current JupyterHub Server image
- `image.pullPolicy`: Always
- `image.secret`: default
- `resources.requests`: None
- `resources.limits`: None
- `storage.homePvcName`: `claim-{username}`
- `storage.homeMountPath`: `/home/jovyan`
- `storage.extraVolumes`: 
    - `Pod` Volumes Spec
- `storage.extraVolumeMounts`: 
    - `name`:
    - `mountPath`: 
- `env`: 
    - `name`:
    - `value`:
- `nodeSelector`: {}
- `runAsUser`: 1000
- `runAsGroup`: 100
- `fsGroup`: 100
- `serviceAccountName`: default

