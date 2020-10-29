# Configuring workflow file

```yaml
# workflow.yaml
version: 1

name: workflow-name

jobs:
- python job1.py
- python job2.py ARGS

dags:
- 1 >> 2

schedule: '*/2 * * * *'
```

| Property  | Description                                                                | Optional  | Default                           |
|-----------|----------------------------------------------------------------------------|-----------|-----------------------------------|
|`version`  | Version of `workflow.yaml` file format.                                    | Optional  | 1                                 |
|`name`     | Name of the workflow. This name will used for Argo `Workflow` object name. | Optional  | {username} of JupyterHub          |
|`jobs`     | Jobs to run. Any kinds of command will work. (Not just Python)             | Required  |                                   |
|`dags`     | Job dependencies. Index starts at 1. (`$PREVIOUS_JOB` >> `$NEXT_JOB`)      | Optional  | All jobs parallel (No dependency) |
|`schedule` | When to execute this workflow. Follows cron format.                        | Optional  | Run immediately                   |
