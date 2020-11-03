# CLI Reference

`jupyterflow` is the command line interface for JupyterFlow

## jupyterflow run

To run a workflow to Argo Workflow on JupyterHub

### Synopsis

```
jupyterflow run [flags]
```

### Options

```
  -h, --help              help for list
  -c, --command string    Command to run workflow. ex) `jupyterflow run -c "python main.py >> python next.py"`
  -f, --filename string   Path for workflow.yaml file. ex) `jupyterflow run -f workflow.yaml`
  -o, --output string     Output format. (default is `-o jsonpath="metadata.name"`, other possible options are yaml, json, jsonpath.)
      --dry-run           Only prints Argo Workflow object, without accually sending it.
```

---

## jupyterflow config

View or create JupyterFlow configuration file to override Argo `Workflow` object specification.
For detail information, refer to [JupyterFlow Configuration](configuration.md#jupyterflow-configuration)

### Synopsis

```
jupyterflow config [flags]
```

### Options

```
  -h, --help              help for list
      --generate-config   Generates default `$HOME/.jupyterflow.yaml` configuration file.
```
