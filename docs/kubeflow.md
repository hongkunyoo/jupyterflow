# Set up on Kubeflow

### What is Kubeflow?

[Kubeflow](https://www.kubeflow.org) is a free and open-source machine learning platform designed to enable using machine learning pipelines to orchestrate complicated workflows running on Kubernetes. 

In this method, you will install JupyterFlow on existing Kubeflow platform.

## Install Kubeflow

Refer to [kubeflow getting started page](https://www.kubeflow.org/docs/started/getting-started/) for installation.

## Expose Argo Workflow UI

Expose Web UI for Argo Workflow: [https://argoproj.github.io/argo/argo-server/](https://argoproj.github.io/argo/argo-server/)

You need to expose Argo Web UI to see the result of `jupyterflow`. Unfortunately, JupyterFlow currently does not support Kubeflow Pipelines, so the result of `juypterflow` Workflow does not appear in Kubeflow Pipelines Web pages. You need to manually expose Argo Workflow Web UI to check the result.

## Grant Kubeflow notebook Service Account RBAC

Grant the service account used in Kubeflow notebook a role to create Argo Workflow objects.

### Options 1)

The simplest way to grant service account is to bind `cluster-admin` role. The default service account name in Kubeflow notebook is `default-editor`. Assuming your Kubeflow namespace is `jupyterflow`, run

```bash
# binding cluster-admin role to jupyterflow:default
kubectl create clusterrolebinding jupyterflow-admin \
                        --clusterrole=cluster-admin \
                        --serviceaccount=jupyterflow:default-editor
```

### Options 2)

For more fine-grained RBAC, create Workflow Role in the namespace where Kubeflow is installed.

For example, create Workflow Role in `jupyterflow` namespace with following command.

```bash
cat << EOF | kubectl create -n jupyterflow -f -
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: workflow-role
rules:
# pod get/watch is used to identify the container IDs of the current pod
# pod patch is used to annotate the step's outputs back to controller (e.g. artifact location)
- apiGroups:
  - ""
  resources:
  - pods
  verbs:
  - get
  - watch
  - patch
  - list
# logs get/watch are used to get the pods logs for script outputs, and for log archival
- apiGroups:
  - ""
  resources:
  - pods/log
  verbs:
  - get
  - watch
- apiGroups:
  - "argoproj.io"
  resources:
  - workflows
  verbs:
  - get
  - watch
  - patch
  - list
  - create
EOF
```

Then, bind Role with your service account. For example, bind `default-editor` service account with workflow role in `jupyterflow` namespace.

```bash
# binding workflow role to jupyterflow:default
kubectl create rolebinding workflow-rb \
                      --role=workflow-role \
                      --serviceaccount=jupyterflow:default-editor \
                      --namespace jupyterflow
```

You might want to look at [https://argoproj.github.io/argo/service-accounts](https://argoproj.github.io/argo/service-accounts).

## Install jupyterflow

Finally, launch a JupyterHub notebook server and install `jupyterflow` using pip.

In jupyter notebook Terminal, run

```bash
pip install jupyterflow
```
