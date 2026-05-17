# CLAUDE.md

Guidance for AI assistants working in this repository.

## Project overview

JupyterFlow is a lightweight ML-workflow tool. It turns a shell command into an
[Argo Workflow](https://argoproj.github.io/workflows/) on Kubernetes **without
any containerization step**: it clones the spec of the JupyterHub/Kubeflow
notebook Pod it runs inside (image, env, volumes, resources, security context)
and submits a Workflow that reuses that environment.

```bash
jupyterflow run -c "python job1.py >> python job2.py"   # job1 then job2 (DAG)
jupyterflow run -f workflow.yaml                          # workflow from file
jupyterflow delete <name>
jupyterflow config [--generate-config]
```

Version `0.0.4` (single-sourced in `jupyterflow/__init__.py`). License:
BSD-3-Clause. Python 3, packaged as a pip module — there is no Docker image.

## Architecture / execution path

```
bin/jupyterflow
  → jupyterflow.driver.main()            # Click group: run / delete / config
  → workflow.load_from_command()         # split on ">>" into jobs + dags
    | workflow.load_from_file()           # yaml.safe_load
  → runtime.runtime (Runtime singleton)  # in-cluster env, see constraint below
  → utils.load_config()                  # ~/.jupyterflow.yaml
  → workflow.build()
       k8s_client.get_notebook_pod()     # fetch current Pod via K8s API
       workflow.build_wf_spec_from(pod)  # extract image/env/volumes/resources
       workflow.override_wf(wf, config)  # merge user config onto Pod-derived spec
       render.workflow() / render.cronworkflow()   # Jinja2 + ansible filters
  → workflow.run() → k8s_client.create_object()     # submit Workflow CRD
       (or --dry-run → print rendered manifest as YAML, no submit)
  → printer.format(response, output)     # jsonpath (default) / yaml / text
```

## Module map (`jupyterflow/`)

- `driver.py` — Click CLI: `run`, `delete`, `config` commands.
- `workflow.py` — DAG parsing, Pod-spec extraction, config merge, build/run/delete.
- `runtime.py` — `Runtime` dict singleton; in-cluster environment discovery.
- `k8s_client.py` — Kubernetes API wrappers (create/delete Workflow, read Pod).
- `render.py` — Jinja2 rendering of the templates (with jinja2-ansible-filters).
- `printer.py` — Output formatting: jsonpath / yaml / pretty text.
- `utils.py` — Config file load/generate (`~/.jupyterflow.yaml`).
- `templates/` — `workflow.yaml`, `cronworkflow.yaml`, `jupyterflow.yaml`
  (the rendered Argo manifests and the config-file template).

## Key conventions

- **DAG syntax**: jobs in the `-c` string are separated by `>>`; sequential
  dependencies are auto-generated (`workflow.load_from_command`). File mode
  (`-f`) accepts explicit `jobs` + `dags` (and optional `name`, `schedule`,
  `cmd_mode`).
- **Command mode**: `cmd_mode: exec` (default) splits the job string on spaces;
  any other value wraps it as `/bin/sh -c "<job>"` (`workflow.build`).
- **Template-driven output**: change generated-manifest behavior by editing
  `jupyterflow/templates/*.yaml`, not by hand-assembling dicts in Python.
- **Config**: `~/.jupyterflow.yaml`, overridable via `$JUPYTERFLOW_CONFIG_FILE`
  (`utils._get_config_file_path`). User `spec` is merged onto the Pod-derived
  spec by `workflow.override_wf` — note env/volumes/volumeMounts are *appended*
  to the Pod's, other keys *replace*.
- **Version**: edit `jupyterflow/__init__.py` only; `setup.py` parses it by
  regex. Keep template files listed in `MANIFEST.in` or they won't be packaged.
- **Style**: stdlib-style Python 3, 4-space indent, snake_case functions,
  PascalCase classes, relative imports within the package. No linter/formatter
  config exists — match surrounding style.
- `README.md` is a symlink to `docs/README.md` — edit the target, not the link.

## Runtime constraint (important)

The code **cannot run or be tested outside a Kubernetes Pod**:
`runtime.py` opens `/var/run/secrets/kubernetes.io/serviceaccount/namespace`
and reads `NB_USER`/`HOSTNAME` env vars **at import time** (the `runtime`
singleton is constructed on module import, and `driver` imports it). It also
needs JupyterHub-on-K8s (or Kubeflow) plus the Argo Workflows CRDs installed,
and in-cluster credentials (`k8s_client`). There is no local/dev/docker run
path — importing the package on a normal machine will raise.

## Build / install / test

- Install: `pip install -e .` (deps in `setup.py` / `requirements.txt`).
- Docs site: `mkdocs serve` / `mkdocs build` (config `mkdocs.yml`;
  published to GitHub Pages).
- **Tests: none exist.** No `tests/`, no pytest/tox config; CI
  (`.github/workflows/main.yaml`) is a disabled stub. Because execution
  requires a live cluster, verify changes by careful manual reasoning and by
  inspecting the rendered manifest with `jupyterflow run ... --dry-run`
  (or `-o yaml`). Be conservative — there is no safety net.

## Gotchas

- Don't add a local fallback to make the package importable off-cluster unless
  asked — callers rely on the in-cluster behavior.
- `--dry-run` / `-o yaml` is the safe way to inspect generated manifests
  without touching the cluster.
- No automated tests means regressions are silent; prefer minimal, targeted
  changes and double-check template edits against `render.py`.
