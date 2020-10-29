# Configuring workflow

`workflow.yaml` is a description about how to run your jobs. You can asign a dependencies between jobs.

## Minimum description

Each job will run in parallel.

```yaml
# workflow.yaml

jobs:
- echo hello
- echo world
- echo again
```

## Full description

Job dependencies will be resolved based on `dags` information.

```yaml
# workflow.yaml
version: 1

name: workflow-name

jobs:
- echo hello
- echo world
- echo again

dags:
- 1 >> 2
- 1 >> 3

schedule: '*/2 * * * *'
```

| Property  | Description                                                           | Optional  | Default                           |
|-----------|-----------------------------------------------------------------------|-----------|-----------------------------------|
|`version`  | Version of `workflow.yaml` file format.                               | Optional  | 1                                 |
|`name`     | Name of the workflow. This name is used for Argo `Workflow` name.     | Optional  | {username} of JupyterHub          |
|`jobs`     | Jobs to run. Any kinds of command works.                              | Required  |                                   |
|`dags`     | Job dependencies. Index starts at 1. (`$PREVIOUS_JOB` >> `$NEXT_JOB`) | Optional  | All jobs parallel (No dependency) |
|`schedule` | When to execute this workflow. Follows cron format.                   | Optional  | Run immediately                   |
