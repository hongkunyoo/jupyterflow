# JupyterFlow Documentation

Run your workflow on JupyterHub!

### What is JupyterFlow?

Run [Argo Workflow](https://argoproj.github.io/argo) pipeline on [JupyterHub.](https://jupyter.org/hub)

- No Kubernetes knowledge (YAML) needed to run.
- No container build & push or deploy.
- Just simply run your workflow with single command `jupyterflow`.

`jupyterflow` is a command that helps user utilize Argo Workflow engine without making any YAML files or building containers on JupyterHub.

The following `jupyterflow` command will make sequence workflow.

```bash
jupyterflow run -c "python hello.py >> python world.py"
```

![](images/intro.png)

### Getting Started

To set up `jupyterflow` and start running your first workflow, follow the [Getting Started](get-started.md) guide.

### How does it work

To learn how it works, see [How it works](how-it-works.md) guide.

### Examples

For examples how to use, please see [Examples](/examples/README.md) page.


### `workflow.yaml` Configuration

To find out more detail configuration, look at [Configuration](configuration.md) page.
