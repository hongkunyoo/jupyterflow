# Set up on JupyterHub

In this method, you will install JupyterHub, Argo Workflow manually.

## Prerequisite

- Create Kubernetes cluster.
- Install [`kubectl`](https://kubernetes.io/docs/tasks/tools/install-kubectl/#install-kubectl) command.
- Install [`helm`](https://helm.sh/docs/intro/install) command.

Any Kubernetes cluster will work. `Zero to JupyterHub` has a wonderful [guide for setting up Kubernetes.](https://zero-to-jupyterhub.readthedocs.io/en/latest/#setup-kubernetes) 

## Install JupyterHub

Follow the [`Zero to JupyterHub` instruction to set up JupyterHub](https://zero-to-jupyterhub.readthedocs.io/en/latest/#setup-jupyterhub). There are two things you should configure to use `jupyterflow`.

#### 1) Specify serviceAccoutName

 Specify `singleuser.serviceAccoutName` property in `config.yaml`. This service account will be used to create  Argo `Workflow` object on behalf of you.

For example, following configuration uses `default` service account. Later, you should grant this service account a proper role to create `Workflow` object.

```yaml
# config.yaml
singleuser:
  serviceAccountName: default
```

#### 2) Configure Storage

You need a shared storage volume, such as NFS server(`ReadWriteMany` access mode), to make JupyterFlow get the same ML code written in Jupyter notebook. To do this, configure `singleuser.storage` property.
If you're unfamiliar with storage access mode, take a look at [Kubernetes persistent volume access mode](https://kubernetes.io/docs/concepts/storage/persistent-volumes/#access-modes).

The simplest way to have a `ReadWriteMany` type storage is installing nfs-server-provisioner.

```bash
# StorageClass name will be nfs-server
helm install nfs-server stable/nfs-server-provisioner
```

And then use the `nfs-server` StorageClass for `ReadWriteMany` access mode storage in `config.yaml` file.

```yaml
# config.yaml
singleuser:
  storage:
    type: dynamic                           # dynamic or static

    dynamic:
      storageClass: nfs-server              # For example, nfs-server-provisioner
      storageAccessModes: [ReadWriteMany]   # Make sure your volume supports ReadWriteMany.

    static:                                 # Static pvc also works fine. 
      pvcName: my-static-pvc                # Static pvc should support ReadWriteMany mode.
```

The full description of `config.yaml` file will seem like this.

```yaml
# config.yaml
proxy:
  secretToken: "<RANDOM_HEX>"   # openssl rand -hex 32

singleuser:
  serviceAccountName: default
  storage:
    type: dynamic
    dynamic:
      storageClass: nfs-server
      storageAccessModes: [ReadWriteMany]
```

Install JupyterHub using `helm` package manager. Following example installs JupyterHub in `jupyterflow` namespace.

```bash
helm repo add jupyterhub https://jupyterhub.github.io/helm-chart/
helm repo update

RELEASE=jhub
NAMESPACE=jupyterflow

helm install $RELEASE jupyterhub/jupyterhub \
  --namespace $NAMESPACE \
  --create-namespace \
  --values config.yaml
```

## Install Argo Workflow Engine

Install Argo workflow engine with [Argo Workflow quick start page](https://argoproj.github.io/argo-workflows/quick-start). 
You need to install Argo workflow engine in the **same Kubernetes namespace** where JupyterHub is installed.

For example, use `jupyterflow` namespace for installing Argo Workflow engine.

```bash
kubectl apply --namespace jupyterflow -f \
    https://raw.githubusercontent.com/argoproj/argo/stable/manifests/quick-start-postgres.yaml
```

!!! note
    If you want to install Argo workflow engine in different namespace, refer to [Argo installation - cluster install](https://argoproj.github.io/argo-workflows/installation) page.

## Expose Argo Workflow Web UI

You need to expose Argo web UI to see the result of `jupyterflow`. The simplest way is to expose `argo-server` Service as `LoadBalancer` type. For example, if your Argo workflow engine is deployed in `jupyterflow` namespace, run

```bash
# Expose argo-server Service as LoadBalancer type
kubectl patch svc argo-server -p '{"spec": {"type": "LoadBalancer"}}' -n jupyterflow
# service/argo-server patched
```

Browse `<LOAD_BALANCER_IP>:2746` to see Argo Workflow web UI is available. For detail configuration, refer to [https://argoproj.github.io/argo-workflows/argo-server/](https://argoproj.github.io/argo-workflows/argo-server)

## Grant JupyterHub Service Account RBAC

Grant the service account used in JupyterHub a role to create Argo Workflow objects.

#### Options 1)

The simplest way to grant service account is to bind `cluster-admin` role. For example, if you deployed JupyterHub in `jupyterflow` namespace and specify service account as `default`, run

```bash
# binding cluster-admin role to jupyterflow:default
kubectl create clusterrolebinding jupyterflow-admin \
                        --clusterrole=cluster-admin \
                        --serviceaccount=jupyterflow:default
```

#### Options 2)

For more fine-grained Access Control, create Workflow Role in the namespace where JupyterHub is installed.

For example, create Workflow Role in `jupyterflow` namespace with following command.

```bash
cat << EOF | kubectl apply -n jupyterflow -f -
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

Then, bind the Role with your service account. For example, bind `default` service account with workflow role in `jupyterflow` namespace.

```bash
# binding workflow role to jupyterflow:default
kubectl create rolebinding workflow-rb \
                      --role=workflow-role \
                      --serviceaccount=jupyterflow:default \
                      --namespace jupyterflow
```

You might want to look at [https://argoproj.github.io/argo-workflows/service-accounts](https://argoproj.github.io/argo-workflows/service-accounts) for granting permissions.

## Install jupyterflow

Finally, launch a JupyterHub notebook server and install `jupyterflow` using pip.

In jupyter notebook Terminal, run

```bash
pip install jupyterflow
```
