# Get Started

Although using JupyterFlow does not require Kubernetes knowledge, setting up JupyterFlow requires Kubernetes understandings(YAML, `helm`, `Service`). If you're familiar with Kubernetes, it will not be too hard. 

> This project only works on JupyterHub deployed on Kubernetes.

## Options for setting up JupyterFlow

There are two ways to set up `jupyterflow`

- [Set up JupyterFlow from scratch.](scratch.md)
- [Set up JupyterFlow on Kubeflow](kubeflow.md)

---

After the setup, you can run your workflow with `jupyterflow` on JupyterHub. Launch your jupyter notebook and follow the example.

## Run my first workflow

Refer to [examples/get-started](https://github.com/hongkunyoo/jupyterflow/tree/main/examples/get-started) to get the example scripts.

### by command

Write your own code in notebook server.

```python
# job1.py
print('hello')
```

```python
# job2.py
import sys
print('world %s!' % sys.argv[1])
```

Run following command for sequence workflow.

```bash
jupyterflow run -c "python job1.py >> python job2.py foo"
```

Go to Argo Web UI and check out the output of launched workflow.

![](images/intro.png)


### by `workflow.yaml` file

If you want to run more sophisticated workflow, such as DAG (Directed Acyclic Graph), write your own workflow file (for example, `workflow.yaml`, the name doesn't matter)

For more information, check out [Configuring workflow](configuration.md)

```yaml
# workflow.yaml
jobs:
- python job1.py 
- python job2.py foo
- python job2.py bar
- python job3.py

# Job index starts at 1.
dags:
- 1 >> 2
- 1 >> 3
- 2 >> 4
- 3 >> 4
```

```python
# job3.py
print('again!')
```

Run `jupyteflow` with `-f` option.

```bash
jupyterflow run -f workflow.yaml
```

Check out the result.

![](images/dag.png)
